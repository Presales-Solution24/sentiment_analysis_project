import re

competitor_brands = ["canon", "hp", "brother", "ricoh", "xerox"]

# Kata-kata yang menunjukkan perbandingan kompetitor lebih baik
better_keywords = [
    "lebih baik", "lebih unggul", "lebih cepat", "lebih hemat", "lebih murah",
    "hasil lebih tajam", "lebih awet", "lebih efisien", "kualitas lebih bagus"
]

# Kata-kata yang menunjukkan perbandingan kompetitor lebih buruk
worse_keywords = [
    "lebih buruk", "lebih lambat", "lebih boros", "lebih mahal",
    "lebih jelek", "lebih rendah", "sering rusak", "cepat macet", "tidak tahan lama"
]

def detect_competitor(text):
    """Mendeteksi merek kompetitor dalam review (bisa lebih dari satu)."""
    detected_brands = []
    for brand in competitor_brands:
        if brand in text.lower():
            detected_brands.append(brand)
    return detected_brands  # Mengembalikan daftar merek yang terdeteksi

def analyze_review_from_epson_perspective(review):
    """Menganalisis ulasan dari perspektif Epson dengan hasil hanya berupa Positif, Negatif, atau Netral."""
    review_lower = review.lower()
    detected_brands = detect_competitor(review)

    # Jika tidak ada kompetitor terdeteksi, anggap Netral
    if not detected_brands:
        return "Netral"

    sentiment = "Netral"  # Default jika tidak ada kata kunci yang cocok

    for competitor in detected_brands:
        # Mendeteksi pola kompetitor lebih baik atau lebih buruk
        better_pattern = re.search(rf"{competitor}.*({'|'.join(better_keywords)})", review_lower)
        worse_pattern = re.search(rf"{competitor}.*({'|'.join(worse_keywords)})", review_lower)
        epson_better_pattern = re.search(rf"epson.*({'|'.join(better_keywords)})", review_lower)
        epson_worse_pattern = re.search(rf"epson.*({'|'.join(worse_keywords)})", review_lower)

        if better_pattern or epson_worse_pattern:
            sentiment = "Negatif"  # Kompetitor lebih baik → Epson kalah → Negatif
        elif worse_pattern or epson_better_pattern:
            sentiment = "Positif"  # Kompetitor lebih buruk → Epson menang → Positif

    return sentiment
