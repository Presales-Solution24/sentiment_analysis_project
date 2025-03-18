import streamlit as st
import pandas as pd
from predict import predict_sentiment

st.title("Sentiment Analysis Epson Printer")

# Opsi input: Manual atau Upload File
option = st.radio("Pilih metode input:", ("Input Manual", "Upload File Excel"))

if option == "Input Manual":
    # Input manual: pengguna mengetik review
    user_input = st.text_area("Masukkan ulasan printer:")
    
    if st.button("Analisis Sentimen"):
        if user_input.strip():
            sentiment = predict_sentiment(user_input)
            st.write(f"**Sentimen dari perspektif Epson:** {sentiment}")
        else:
            st.warning("⚠️ Harap masukkan teks sebelum menganalisis.")

elif option == "Upload File Excel":
    # Upload file
    uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        # Baca file Excel
        df = pd.read_excel(uploaded_file)

        # Periksa apakah kolom "review" ada dalam dataset
        if "review" not in df.columns:
            st.error("❌ File yang diunggah harus memiliki kolom 'review'.")
        else:
            # Analisis sentimen untuk setiap review
            st.write("📊 **Analisis Sentimen**")
            df["sentiment"] = df["review"].apply(predict_sentiment)

            # Tampilkan hasil analisis dalam tabel
            st.dataframe(df)

            # Tambahkan tombol untuk mengunduh hasil analisis
            st.download_button(
                label="📥 Download Hasil Analisis",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="sentiment_analysis_results.csv",
                mime="text/csv",
            )
