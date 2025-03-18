from transformers import AutoTokenizer
import torch
from utils.preprocessing import clean_text
from utils.brand_detection import analyze_review_from_epson_perspective
from utils.config import SCRIPTED_MODEL_PATH

# Model & tokenizer hanya dimuat jika dibutuhkan
model = None
tokenizer = None

def load_model():
    global model, tokenizer
    if model is None or tokenizer is None:
        model_name = "indobenchmark/indobert-base-p1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = torch.jit.load(SCRIPTED_MODEL_PATH)
    return model, tokenizer

def predict_sentiment(text):
    model, tokenizer = load_model()
    text = clean_text(text)
    
    # Cek apakah ada perbandingan dengan kompetitor
    competitor_analysis = analyze_review_from_epson_perspective(text)
    if "Sentimen" in competitor_analysis:
        return competitor_analysis
    
    # Prediksi sentimen
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    
    prediction = torch.argmax(outputs.logits, dim=1).item()
    labels = ["Negatif", "Netral", "Positif"]
    
    return labels[prediction]

# Contoh penggunaan
if __name__ == "__main__":
    test_review = "Hasil cetak Canon lebih bagus dari Epson."
    sentiment = predict_sentiment(test_review)
    print(f"Sentimen: {sentiment}")
