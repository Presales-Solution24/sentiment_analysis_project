# utils/category_zero_shot.py

import streamlit as st
from transformers import pipeline

# ✅ Label deskriptif untuk zero-shot classification
DESCRIPTIVE_LABELS = [
    "Harga dan nilai produk, seperti murah, mahal, sebanding atau tidak dengan harga",
    "Layanan dan dukungan pelanggan, termasuk servis, teknisi, dan garansi",
    "Kualitas produk secara umum, termasuk daya tahan, bahan, dan keandalan",
    "Performa seperti kecepatan cetak, efisiensi tinta, dan kinerja printer saat digunakan",
    "Fitur dan teknologi seperti Wi-Fi, auto duplex, scanner, dan konektivitas modern",
    "Kemudahan penggunaan seperti instalasi mudah, antarmuka ramah pengguna, dan penggunaan sehari-hari"
]

# 🔄 Mapping ke kategori final
LABEL_MAPPING = {
    DESCRIPTIVE_LABELS[0]: "Harga & Nilai",
    DESCRIPTIVE_LABELS[1]: "Layanan & Dukungan",
    DESCRIPTIVE_LABELS[2]: "Kualitas",
    DESCRIPTIVE_LABELS[3]: "Performa",
    DESCRIPTIVE_LABELS[4]: "Fitur & Teknologi",
    DESCRIPTIVE_LABELS[5]: "Kemudahan Penggunaan"
}

# ✅ Cache pipeline zero-shot classification agar lebih cepat
@st.cache_resource(show_spinner="🔄 Memuat model zero-shot classification...")
def load_zero_shot_classifier():
    return pipeline(
        task="zero-shot-classification",
        model="joeddav/xlm-roberta-large-xnli"
    )

# Inisialisasi pipeline
classifier = load_zero_shot_classifier()

def classify_category_zero_shot(text: str) -> str:
    """
    Mengklasifikasikan ulasan ke dalam 6 kategori utama menggunakan zero-shot classification.
    Selalu menghasilkan salah satu kategori dari LABEL_MAPPING.
    """
    if not text.strip():
        return "Kemudahan Penggunaan"  # fallback default jika kosong

    # Lakukan klasifikasi
    result = classifier(
        text,
        candidate_labels=DESCRIPTIVE_LABELS,
        hypothesis_template="Topik utama dari review ini adalah {}."
    )

    best_label = result["labels"][0]
    return LABEL_MAPPING.get(best_label, "Kemudahan Penggunaan")  # fallback aman
