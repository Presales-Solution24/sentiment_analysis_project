import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io  # Untuk menyimpan file sementara di memori
from predict import predict_sentiment

st.title("📊 Sentiment Analysis Epson Printer")

# Opsi input: Manual atau Upload File
option = st.radio("Pilih metode input:", ("Input Manual", "Upload File Excel"))

if option == "Input Manual":
    user_input = st.text_area("Masukkan ulasan printer:")
    
    if st.button("Analisis Sentimen"):
        if user_input.strip():
            sentiment = predict_sentiment(user_input)
            st.write(f"**📝 Sentimen dari perspektif Epson:** {sentiment}")
        else:
            st.warning("⚠️ Harap masukkan teks sebelum menganalisis.")

elif option == "Upload File Excel":
    uploaded_file = st.file_uploader("📤 Upload file Excel (.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        if "review" not in df.columns:
            st.error("❌ File yang diunggah harus memiliki kolom 'review'.")
        else:
            df["sentiment"] = df["review"].apply(predict_sentiment)
            st.write("📊 **Analisis Sentimen**")
            st.dataframe(df)

            # **VISUALISASI: Pie Chart Distribusi Sentimen**
            st.write("### 📊 Distribusi Sentimen")
            sentiment_counts = df["sentiment"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=["red", "blue", "green"])
            ax1.axis("equal")  # Agar pie chart berbentuk lingkaran
            st.pyplot(fig1)

            # **VISUALISASI: Bar Chart Distribusi Sentimen**
            st.write("### 📊 Bar Chart Sentimen")
            fig2, ax2 = plt.subplots()
            sns.countplot(data=df, x="sentiment", hue="sentiment", palette={"Negatif": "red", "Netral": "blue", "Positif": "green"}, legend=False)
            plt.xlabel("Sentimen")
            plt.ylabel("Jumlah Ulasan")
            st.pyplot(fig2)

            # **🔹 Opsi Pilih Format Unduhan**
            download_format = st.radio("Pilih format file untuk diunduh:", ("Excel (.xlsx)", "CSV (.csv)"))

            if download_format == "Excel (.xlsx)":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Sentiment Analysis")

                    # **Tambahkan visualisasi ke dalam Excel**
                    workbook = writer.book
                    worksheet = workbook.add_worksheet("Visualisasi")
                    writer.sheets["Visualisasi"] = worksheet

                    # Simpan Pie Chart
                    imgdata1 = io.BytesIO()
                    fig1.savefig(imgdata1, format="png")
                    imgdata1.seek(0)
                    worksheet.insert_image("B2", "Pie_Chart.png", {"image_data": imgdata1})

                    # Simpan Bar Chart
                    imgdata2 = io.BytesIO()
                    fig2.savefig(imgdata2, format="png")
                    imgdata2.seek(0)
                    worksheet.insert_image("B20", "Bar_Chart.png", {"image_data": imgdata2})

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
