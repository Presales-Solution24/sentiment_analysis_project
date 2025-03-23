@echo off
echo Membuat virtual environment...
python -m venv venv

echo Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

echo Menginstal dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup selesai! Jalankan: streamlit run app.py
pause
