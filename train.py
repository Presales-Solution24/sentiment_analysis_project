from transformers import TrainingArguments, Trainer, AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset
import pandas as pd
from utils.config import DATASET_PATH, MODEL_PATH, SCRIPTED_MODEL_PATH

# Load dataset dari CSV
df = pd.read_csv(DATASET_PATH)
dataset = {"train": df.sample(frac=0.8), "test": df.drop(df.sample(frac=0.8).index)}

# Load tokenizer IndoBERT
model_name = "indobenchmark/indobert-base-p1"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenisasi dataset
def tokenize_data(examples):
    return tokenizer(examples["review"], truncation=True, padding="max_length", max_length=128)

train_dataset = dataset["train"].apply(tokenize_data, axis=1)
test_dataset = dataset["test"].apply(tokenize_data, axis=1)

# Load model untuk training
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Konfigurasi training
training_args = TrainingArguments(
    output_dir=MODEL_PATH,
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    save_steps=500,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Jalankan training
trainer.train()

# Simpan model dalam format TorchScript untuk startup lebih cepat
scripted_model = torch.jit.script(model)
scripted_model.save(SCRIPTED_MODEL_PATH)
