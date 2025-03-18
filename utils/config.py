import os

# Path model IndoBERT yang sudah dilatih
MODEL_PATH = os.path.join("models", "sentiment_model")

# Path dataset (jika ingin fine-tuning)
DATASET_PATH = os.path.join("dataset", "dataset.csv")

# Path model yang sudah dikompilasi (TorchScript)
SCRIPTED_MODEL_PATH = os.path.join("models", "scripted_model.pt")
