from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Gunakan IndoBERT Base (bukan Sentiment)
# MODEL_NAME = "indobenchmark/indobert-base-p1"
MODEL_NAME = "crypter70/IndoBERT-Sentiment-Analysis"
MODEL_PATH = "models/sentiment_model"

def download_model():
    """Unduh dan simpan model IndoBERT Base ke folder lokal."""
    print("📥 Mengunduh model IndoBERT Base...")
    
    # Load tokenizer dan model dari Hugging Face
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)

    # Simpan model ke folder lokal
    model.save_pretrained(MODEL_PATH)
    tokenizer.save_pretrained(MODEL_PATH)

    print(f"✅ Model berhasil diunduh dan disimpan di '{MODEL_PATH}'")

if __name__ == "__main__":
    download_model()
