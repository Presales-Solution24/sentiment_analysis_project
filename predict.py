from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from utils.preprocessing import clean_text
from utils.brand_detection import analyze_review_from_epson_perspective
from utils.epson_product import detect_epson_product  # Fungsi untuk mendeteksi tipe Epson
from utils.config import MODEL_PATH

# Cek apakah GPU tersedia, jika tidak gunakan CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model IndoBERT yang sudah ditraining
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)  # Pindahkan model ke GPU jika tersedia

def predict_sentiment(text, debug=False):
    """Memprediksi sentimen ulasan dengan model IndoBERT dari perspektif Epson."""
    text = clean_text(text)

    # Deteksi apakah ada tipe produk Epson dalam review
    detected_product = detect_epson_product(text)

    # Deteksi apakah ada perbandingan dengan kompetitor
    competitor_analysis = analyze_review_from_epson_perspective(text)

    # Jika ada kompetitor dan tipe produk Epson disebut, gabungkan hasilnya
    if "Sentimen" in competitor_analysis and detected_product:
        return f"{competitor_analysis} | Produk Epson: {detected_product}"

    # Jika hanya ada kompetitor tanpa tipe produk Epson
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

    # Opsi Debug: Tampilkan probabilitas hanya jika debug=True
    if debug:
        print(f"📊 Probabilitas Sentimen:")
        print(f"   ➡ Negatif: {probs[0][0]:.2f}")
        print(f"   ➡ Netral : {probs[0][1]:.2f}")
        print(f"   ➡ Positif: {probs[0][2]:.2f}")

    # Format hasil dengan deteksi produk jika ditemukan
    # sentiment_result = f"{labels[prediction]} (Confidence: {probs[0][prediction]:.2f})"
    sentiment_result = f"{labels[prediction]}"
    
    # if detected_product:
    #     sentiment_result += f" | Produk Epson: {detected_product}"

    return sentiment_result

# Contoh penggunaan
if __name__ == "__main__":
    sample_reviews = [
        "Epson L3150 lebih boros tinta dibanding Canon, tidak cocok untuk bisnis.",
        "Saya lebih suka Epson SureColor P800 daripada HP karena hasil warnanya lebih akurat.",
        "Canon lebih murah dibanding Epson Ecotank L3250, tapi kualitasnya beda jauh!",
        "Epson WorkForce WF-4820 sangat cocok untuk bisnis kecil, saya puas!",
    ]
    
    for review in sample_reviews:
        print(f"📝 Ulasan: {review}")
        print(f"🔍 Prediksi: {predict_sentiment(review, debug=True)}\n")  # Debug aktif untuk melihat probabilitas
