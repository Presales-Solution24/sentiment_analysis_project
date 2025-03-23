#!/bin/bash

echo "🔧 Membuat virtual environment..."
python3 -m venv venv

echo "🚀 Mengaktifkan virtual environment..."
source venv/bin/activate

echo "📦 Menginstal dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup selesai! Jalankan dengan: streamlit run app.py"
