# utils/epson_products.py

epson_products = {
    "l-series": ["epson l120", "epson l310", "epson l3150", "epson l5190"],
    "ecotank": ["epson ecotank l3210", "epson ecotank l3250", "epson ecotank l5290"],
    "workforce": ["epson workforce wf-c579r", "epson workforce pro wf-c878r", "epson workforce pro wf-c5890"],
    "surecolor": ["epson surecolor p600", "epson surecolor p800", "epson surecolor f570"],
    "dot matrix": ["epson lx-310", "epson lq-310", "epson fx-2190"],
    "scanner": ["epson perfection v600", "epson ds-530", "epson fastfoto ff-680w"],
}

# Fungsi untuk mendeteksi tipe produk Epson dalam teks
def detect_epson_product(text):
    text = text.lower()
    for category, models in epson_products.items():
        for model in models:
            if model in text:
                return model
    return None  # Tidak ada produk yang terdeteksi
