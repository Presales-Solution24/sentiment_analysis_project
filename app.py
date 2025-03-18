import streamlit as st
from predict import predict_sentiment, load_model

# Cache model agar tidak reload setiap kali ada input baru
@st.cache_resource
def get_model():
    return load_model()

st.title("Sentiment Analysis Epson Printer")

user_input = st.text_area("Masukkan ulasan printer:")

if st.button("Analisis Sentimen"):
    get_model()  # Pastikan model sudah dimuat
    sentiment = predict_sentiment(user_input)
    st.write(f"Sentimen dari perspektif Epson: {sentiment}")
