def classify_category(review):
    review = review.lower()

    if any(word in review for word in ["mahal", "murah", "harga", "terjangkau", "biaya"]):
        return "Harga"
    elif any(word in review for word in ["layanan", "servis", "pelayanan", "garansi", "cs", "service center"]):
        return "Layanan"
    elif any(word in review for word in ["kualitas", "ketahanan", "hasil cetak", "tajam", "warna", "awet", "rusak", "cacat"]):
        return "Kualitas Produk"
    elif any(word in review for word in ["fitur", "wifi", "scanner", "auto duplex", "spesifikasi", "fungsi", "multi fungsi", "auto", "smart", "print via"]):
        return "Fitur Produk"
    else:
        return "Lainnya"
