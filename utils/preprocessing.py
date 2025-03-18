import re

# Daftar kompetitor yang ingin dideteksi
competitor_brands = ["canon", "hp", "brother", "ricoh", "xerox"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Hapus URL
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Hapus karakter spesial
    text = re.sub(r"\s+", " ", text).strip()  # Hapus spasi berlebih
    return text

def detect_competitor(text):
    for brand in competitor_brands:
        if brand in text:
            return brand
    return None
