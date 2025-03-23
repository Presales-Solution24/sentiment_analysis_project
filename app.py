import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import time  # ⏱️ Tambahkan ini
from predict import predict_sentiment
from utils.category_zero_shot import classify_category_zero_shot

st.title("📊 Customer Review Analysis Tools")

# Opsi input: Manual atau Upload File
option = st.radio("Pilih metode input:", ("Input Manual", "Upload File Excel"))

if option == "Input Manual":
    user_input = st.text_area("Masukkan ulasan printer:")
    
    if st.button("Analisis Sentimen"):
        if user_input.strip():
            start_time = time.time()
            sentiment = predict_sentiment(user_input)
            category = classify_category_zero_shot(user_input)
            end_time = time.time()

            st.write(f"**📝 Sentimen dari perspektif Epson:** {sentiment}")
            st.write(f"**📂 Kategori:** {category}")
            st.write(f"⏱️ Waktu analisis: {end_time - start_time:.2f} detik")
        else:
            st.warning("⚠️ Harap masukkan teks sebelum menganalisis.")

elif option == "Upload File Excel":
    uploaded_file = st.file_uploader("📤 Upload file Excel (.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        if "review" not in df.columns:
            st.error("❌ File yang diunggah harus memiliki kolom 'review'.")
        else:
            start_time = time.time()
            df["sentiment"] = df["review"].apply(predict_sentiment)
            df["kategori"] = df["review"].apply(classify_category_zero_shot)
            duration = time.time() - start_time

            st.write(f"⏱️ Total waktu analisis: {duration:.2f} detik")
            st.write("📊 **Analisis Sentimen**")
            st.dataframe(df)

            # Visualisasi Pie Chart
            st.write("### 📊 Distribusi Sentimen")
            sentiment_counts = df["sentiment"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90,
                    colors=["red", "blue", "green"])
            ax1.axis("equal")
            st.pyplot(fig1)

            # Visualisasi Bar Chart Sentimen
            st.write("### 📊 Bar Chart Sentimen")
            fig2, ax2 = plt.subplots()
            sns.countplot(data=df, x="sentiment", hue="sentiment",
                          palette={"Negatif": "red", "Netral": "blue", "Positif": "green"}, legend=False)
            plt.xlabel("Sentimen")
            plt.ylabel("Jumlah Ulasan")
            st.pyplot(fig2)

            # Visualisasi Kategori
            st.write("### 🧩 Bar Chart Kategori Ulasan")
            fig3, ax3 = plt.subplots()
            sns.countplot(data=df, x="kategori", order=df["kategori"].value_counts().index, palette="pastel")
            plt.xlabel("Kategori")
            plt.ylabel("Jumlah Ulasan")
            plt.xticks(rotation=15)
            st.pyplot(fig3)

            # Unduhan hasil
            download_format = st.radio("Pilih format file untuk diunduh:", ("Excel (.xlsx)", "CSV (.csv)"))

            if download_format == "Excel (.xlsx)":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Sentiment Analysis")
                    workbook = writer.book
                    worksheet = workbook.add_worksheet("Visualisasi")
                    writer.sheets["Visualisasi"] = worksheet

                    for i, fig in enumerate([fig1, fig2, fig3], start=1):
                        imgdata = io.BytesIO()
                        fig.savefig(imgdata, format="png")
                        imgdata.seek(0)
                        worksheet.insert_image(f"B{2 + (i - 1) * 18}", f"Chart_{i}.png", {"image_data": imgdata})

                output.seek(0)
                st.download_button(
                    label="📥 Download Hasil Analisis (Excel)",
                    data=output,
                    file_name="sentiment_analysis_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            elif download_format == "CSV (.csv)":
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Hasil Analisis (CSV)",
                    data=csv_data,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv",
                )
