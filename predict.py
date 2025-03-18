from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from utils.preprocessing import clean_text
from utils.brand_detection import analyze_review_from_epson_perspective
from utils.config import MODEL_PATH

# Cek apakah GPU tersedia, jika tidak gunakan CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model IndoBERT yang sudah ditraining
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)  # Pindahkan model ke GPU jika tersedia

def predict_sentiment(text):
    """Memprediksi sentimen ulasan dengan model IndoBERT dari perspektif Epson."""
    text = clean_text(text)

    # Cek perbandingan kompetitor terlebih dahulu
    competitor_analysis = analyze_review_from_epson_perspective(text)
    if "Sentimen" in competitor_analysis:
        return competitor_analysis

    # Tokenisasi dan pindahkan ke perangkat yang sesuai
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # Pastikan input berada di perangkat yang sama dengan model

    # Prediksi sentimen dengan model IndoBERT
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)  # Ambil probabilitas setiap kelas
    prediction = torch.argmax(probs, dim=1).item()
    labels = ["Negatif", "Netral", "Positif"]

    return f"{labels[prediction]} (Confidence: {probs[0][prediction]:.2f})"

# Contoh penggunaan
if __name__ == "__main__":
    print(predict_sentiment("Printer ini sangat cepat dan hasil cetaknya tajam. Saya sangat puas!"))
