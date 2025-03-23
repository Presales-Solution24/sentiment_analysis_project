from transformers import pipeline

MODEL_NAME = "joeddav/xlm-roberta-large-xnli"
MODEL_PATH = "models/category_model/xlm-roberta-xnli"

def download_zero_shot_model():
    print("📥 Mengunduh model zero-shot classification...")
    
    classifier = pipeline("zero-shot-classification", model=MODEL_NAME)
    
    # Simpan model dan tokenizer
    classifier.model.save_pretrained(MODEL_PATH)
    classifier.tokenizer.save_pretrained(MODEL_PATH)
    
    print(f"✅ Model zero-shot berhasil disimpan di '{MODEL_PATH}'")

if __name__ == "__main__":
    download_zero_shot_model()
