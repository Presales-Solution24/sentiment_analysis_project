def analyze_review_from_epson_perspective(review):
    from utils.preprocessing import detect_competitor
    
    competitor = detect_competitor(review)
    
    if competitor:
        if "lebih baik" in review or "bagus" in review:
            return f"Sentimen Negatif (Kompetitor {competitor} lebih baik)"
        elif "lebih jelek" in review or "buruk" in review:
            return f"Sentimen Positif (Kompetitor {competitor} lebih buruk)"
    
    return "Tidak ada perbandingan dengan kompetitor"
