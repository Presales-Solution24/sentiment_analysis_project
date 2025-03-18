import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Hapus URL
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Hapus karakter spesial
    text = re.sub(r"\s+", " ", text).strip()  # Hapus spasi berlebih
    return text
