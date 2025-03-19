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
    """Menganalisis ulasan dari perspektif Epson dengan deteksi yang lebih akurat."""
    review_lower = review.lower()
    detected_brands = detect_competitor(review)

    # Jika tidak ada kompetitor terdeteksi, langsung keluar
    if not detected_brands:
        return "Tidak ada perbandingan dengan kompetitor"

    sentiment_results = []

    for competitor in detected_brands:
        # Mendeteksi pola kompetitor lebih baik
        better_pattern = re.search(rf"{competitor}.*({'|'.join(better_keywords)})", review_lower)
        worse_pattern = re.search(rf"{competitor}.*({'|'.join(worse_keywords)})", review_lower)
        epson_better_pattern = re.search(rf"epson.*({'|'.join(better_keywords)})", review_lower)
        epson_worse_pattern = re.search(rf"epson.*({'|'.join(worse_keywords)})", review_lower)

        if better_pattern:
            sentiment_results.append(f"Sentimen Negatif (Kompetitor {competitor} lebih baik)")
        elif worse_pattern:
            sentiment_results.append(f"Sentimen Positif (Kompetitor {competitor} lebih buruk)")
        elif epson_better_pattern:
            sentiment_results.append(f"Sentimen Positif (Epson lebih baik dari {competitor})")
        elif epson_worse_pattern:
            sentiment_results.append(f"Sentimen Negatif (Epson lebih buruk dari {competitor})")

    # Jika ada lebih dari satu hasil sentimen dalam satu review, gabungkan
    if sentiment_results:
        return " | ".join(sentiment_results)

    # **Jika Epson tidak disebut tetapi kompetitor dibandingkan, asumsikan Epson sebagai referensi**
    for competitor in detected_brands:
        for word in better_keywords:
            if re.search(rf"{word}.*{competitor}", review_lower):
                return f"Sentimen Negatif (Kompetitor {competitor} lebih baik)"

        for word in worse_keywords:
            if re.search(rf"{word}.*{competitor}", review_lower):
                return f"Sentimen Positif (Kompetitor {competitor} lebih buruk)"

    return "Tidak ada perbandingan dengan kompetitor"
