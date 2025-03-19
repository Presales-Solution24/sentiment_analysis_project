# Epson-Minded Sentiment Analysis

## 📌 Deskripsi Proyek
Proyek ini bertujuan untuk membangun **model analisis sentimen berbasis IndoBERT** yang dapat mengenali sentimen dalam ulasan pelanggan, khususnya dari perspektif **Epson**. Model ini akan **menganalisis dan membandingkan Epson dengan kompetitor** seperti **Canon, HP, Brother, Ricoh, dan Xerox** untuk menentukan apakah ulasan bersifat **positif, netral, atau negatif**.

## 📂 Struktur Direktori
```
│── app.py                      # Aplikasi Streamlit untuk UI
│── train.py                    # Skrip untuk fine-tuning model IndoBERT
│── predict.py                   # Skrip untuk memprediksi sentimen ulasan
│── requirements.txt             # Daftar dependensi Python
│── dataset/
│   ├── dataset.csv              # Dataset utama (asli)
│   ├── dataset_extended.csv     # Dataset yang telah diperluas dengan data tambahan
│── models/
│   ├── sentiment_model/         # Model IndoBERT yang telah dilatih
│── utils/
│   ├── preprocessing.py         # Preprocessing teks (pembersihan data)
│   ├── config.py                # Konfigurasi model & path dataset
│   ├── brand_detection.py       # Deteksi merek kompetitor dalam ulasan
```

## 🚀 Cara Instalasi & Menjalankan Proyek

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/username/repository_name.git
cd repository_name
```

### 2️⃣ **Buat Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
venv\Scripts\activate  # Untuk Windows
```

### 3️⃣ **Instal Dependensi**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Jalankan Training Model (Opsional jika ingin fine-tuning ulang)**
```bash
python train.py
```

### 5️⃣ **Jalankan Aplikasi Streamlit**
```bash
streamlit run app.py
```

### 6️⃣ **Jalankan Aplikasi Streamlit Tanpa Watcher**
```bash
streamlit run app.py --server.fileWatcherType=none
```

## 🔍 Fitur Utama
✅ **Fine-Tuned IndoBERT Model** → Model telah dilatih ulang agar lebih "Epson-Minded"
✅ **Deteksi Kompetitor** → Model dapat mengenali apakah Epson dibandingkan dengan merek lain
✅ **Prediksi Sentimen** → Klasifikasi ulasan menjadi **Positif, Netral, atau Negatif**
✅ **Input Manual & File Upload** → Analisis ulasan secara langsung atau melalui file **Excel**
✅ **Export Hasil Analisis** → Simpan hasil dalam format **CSV**
✅ **Visualisasi Data** → Pie Chart, Bar Chart, dan Word Cloud untuk analisis kata
✅ **Dukungan GPU** → Memanfaatkan akselerasi CUDA jika tersedia

## 🏗 Teknologi yang Digunakan
- **Python 3.8+**
- **Hugging Face Transformers (IndoBERT)**
- **PyTorch**
- **Pandas**
- **Streamlit**
- **Matplotlib & Seaborn** untuk visualisasi
- **WordCloud** untuk analisis kata yang sering muncul

## 📦 Dependensi yang Digunakan
```plaintext
torch
transformers
datasets
pandas
scikit-learn
streamlit
accelerate
openpyxl
matplotlib
seaborn
xlsxwriter
plotly
wordcloud
```

🚀 **Selamat Mengembangkan Model Sentimen Epson-Minded!** 🚀
# 🚀 DWTD 🚀 # 

