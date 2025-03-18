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
git clone https://github.com/username/epson-sentiment-analysis.git
cd epson-sentiment-analysis
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

## 🔍 Fitur Utama
✅ **Fine-Tuned IndoBERT Model** → Model telah dilatih ulang agar lebih "Epson-Minded"
✅ **Deteksi Kompetitor** → Model dapat mengenali apakah Epson dibandingkan dengan merek lain
✅ **Prediksi Sentimen** → Klasifikasi ulasan menjadi **Positif, Netral, atau Negatif**
✅ **Input Manual & File Upload** → Analisis ulasan secara langsung atau melalui file **Excel**
✅ **Export Hasil Analisis** → Simpan hasil dalam format **CSV**

## 🏗 Teknologi yang Digunakan
- **Python 3.8+**
- **Hugging Face Transformers (IndoBERT)**
- **PyTorch**
- **Pandas**
- **Streamlit**

## 📄 Lisensi
Proyek ini berada di bawah lisensi **MIT**. Silakan gunakan, modifikasi, dan distribusikan dengan bebas!

## 🤝 Kontribusi
Jika ingin berkontribusi:
1. **Fork repository ini**
2. **Buat branch baru (`git checkout -b feature-nama`)**
3. **Commit perubahan (`git commit -m 'Menambahkan fitur X'`)**
4. **Push ke GitHub (`git push origin feature-nama`)**
5. **Buat Pull Request**

🚀 **Selamat Mengembangkan Model Sentimen Epson-Minded!** 🚀