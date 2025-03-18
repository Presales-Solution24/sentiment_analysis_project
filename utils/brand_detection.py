import re

competitor_brands = ["canon", "hp", "brother", "ricoh", "xerox"]

def detect_competitor(text):
    """Mendeteksi apakah ulasan menyebut merek kompetitor."""
    for brand in competitor_brands:
        if brand in text.lower():
            return brand
    return None

def analyze_review_from_epson_perspective(review):
    """Menganalisis ulasan dari perspektif Epson dengan logika yang lebih cerdas."""
    competitor = detect_competitor(review)

    if competitor:
        review_lower = review.lower()

        # Pola perbandingan kompetitor
        better_pattern = re.search(rf"{competitor}.*(lebih baik|lebih bagus|unggul|paling bagus)", review_lower)
        worse_pattern = re.search(rf"{competitor}.*(lebih jelek|lebih buruk|tidak bagus)", review_lower)
        epson_better_pattern = re.search(rf"epson.*(lebih baik|lebih bagus|unggul|paling bagus)", review_lower)
        epson_worse_pattern = re.search(rf"epson.*(lebih jelek|lebih buruk|tidak bagus)", review_lower)

        if better_pattern:
            return f"Sentimen Negatif (Kompetitor {competitor} lebih baik)"
        elif worse_pattern:
            return f"Sentimen Positif (Kompetitor {competitor} lebih buruk)"
        elif epson_better_pattern:
            return f"Sentimen Positif (Epson lebih baik dari {competitor})"
        elif epson_worse_pattern:
            return f"Sentimen Negatif (Epson lebih buruk dari {competitor})"

    return "Tidak ada perbandingan dengan kompetitor"
