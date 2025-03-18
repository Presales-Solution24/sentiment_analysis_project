from transformers import TrainingArguments, Trainer, AutoModelForSequenceClassification, AutoTokenizer
from datasets import Dataset
import pandas as pd
import torch
from utils.config import MODEL_PATH, DATASET_PATH

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Hapus baris dengan nilai kosong pada kolom "review" atau "sentiment"
# df.dropna(subset=["review", "sentiment"], inplace=True)

# Pastikan dataset memiliki kolom 'labels'
df.rename(columns={"sentiment": "labels"}, inplace=True)

# Mapping label sentimen
label_mapping = {"Negatif": 0, "Netral": 1, "Positif": 2}
df["labels"] = df["labels"].map(label_mapping)

# Hapus kolom yang tidak diperlukan
df.drop(columns=["id"], inplace=True, errors="ignore")

# Periksa apakah masih ada nilai kosong
if df.isnull().values.any():
    raise ValueError("❌ Dataset masih memiliki nilai kosong setelah pembersihan!")

# Konversi dataset ke format Hugging Face
dataset = Dataset.from_pandas(df)

# Load tokenizer IndoBERT Base
# model_name = "indobenchmark/indobert-base-p1"
model_name = "crypter70/IndoBERT-Sentiment-Analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenisasi dataset
def tokenize_data(examples):
    return tokenizer(examples["review"], truncation=True, padding="max_length", max_length=128)

dataset = dataset.map(tokenize_data, batched=True)

# Split dataset untuk training & testing
train_test_split = dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split["train"]
test_dataset = train_test_split["test"]

# Load model IndoBERT Base untuk klasifikasi sentimen
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Konfigurasi training

## Base Configuration
# training_args = TrainingArguments(
#     output_dir=MODEL_PATH,
#     eval_strategy="epoch",  # Evaluasi dilakukan setiap epoch
#     save_strategy="epoch",  # Simpan model setiap epoch agar cocok dengan eval_strategy
#     per_device_train_batch_size=8,
#     per_device_eval_batch_size=8,
#     num_train_epochs=3,
#     save_total_limit=2,
#     logging_dir="logs",
#     logging_steps=100,
#     learning_rate=2e-5,
#     warmup_steps=500,
#     weight_decay=0.01,
#     load_best_model_at_end=True,
# )

# Gunakan GPU jika tersedia
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Konfigurasi training (DISESUAIKAN UNTUK RTX 4060 - 8GB VRAM)
training_args = TrainingArguments(
    output_dir=MODEL_PATH,
    eval_strategy="epoch",  # Evaluasi dilakukan setiap epoch
    save_strategy="epoch",  # Simpan model setiap epoch agar cocok dengan eval_strategy
    per_device_train_batch_size=16,  # Meningkatkan batch size (GPU 8GB cukup untuk 16)
    per_device_eval_batch_size=16,
    num_train_epochs=5,  # Naikkan jumlah epoch untuk hasil lebih stabil
    save_total_limit=2,
    logging_dir="logs",
    logging_steps=100,
    learning_rate=2e-5,
    warmup_steps=500,
    weight_decay=0.01,
    load_best_model_at_end=True,
    fp16=True,  # Mixed Precision Training untuk mempercepat proses
    gradient_accumulation_steps=1,  # Tidak perlu akumulasi karena VRAM cukup besar
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset.remove_columns(["review"]),  # Hapus kolom yang tidak diperlukan
    eval_dataset=test_dataset.remove_columns(["review"]),
)

# Jalankan training
trainer.train()

# Simpan model yang sudah dilatih
model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)

print("✅ Model IndoBERT berhasil di-fine-tune dan disimpan di 'models/sentiment_model'!")
