import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import time
from predict import predict_sentiment
from utils.category_zero_shot import classify_category_zero_shot

# Konfigurasi halaman
st.title("📊 Customer Review Analysis Tools")

option = st.radio("Pilih metode input:", ("Input Manual", "Upload File Excel"))

# 🔹 INPUT MANUAL
if option == "Input Manual":
    user_input = st.text_area("Masukkan ulasan printer:")

    if st.button("Analisis Sentimen"):
        if user_input.strip():
            start_time = time.time()
            sentiment = predict_sentiment(user_input)
            category = classify_category_zero_shot(user_input)
            duration = time.time() - start_time

            st.write(f"**📝 Sentimen dari perspektif Epson:** {sentiment}")
            st.write(f"**📂 Kategori:** {category}")
            st.write(f"⏱️ Waktu analisis: {duration:.2f} detik")
        else:
            st.warning("⚠️ Harap masukkan teks sebelum menganalisis.")

# 🔹 UPLOAD EXCEL
elif option == "Upload File Excel":
    uploaded_file = st.file_uploader("📤 Upload file Excel (.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        if "review" not in df.columns:
            st.error("❌ File yang diunggah harus memiliki kolom 'review'.")
        else:
            if "analyzed_df" not in st.session_state:
                start_time = time.time()
                df["sentiment"] = df["review"].apply(predict_sentiment)
                df["kategori"] = df["review"].apply(classify_category_zero_shot)
                duration = time.time() - start_time
                st.session_state.analyzed_df = df
                st.session_state.analysis_duration = duration
            else:
                df = st.session_state.analyzed_df
                duration = st.session_state.analysis_duration

            st.success(f"⏱️ Total waktu analisis: {duration:.2f} detik")
            st.write("📊 **Hasil Analisis Ulasan**")
            st.dataframe(df)

            # 📊 Pie Chart Sentimen
            st.subheader("📊 Distribusi Sentimen")
            sentiment_counts = df["sentiment"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90,
                    colors=["red", "blue", "green"])
            ax1.axis("equal")
            st.pyplot(fig1)

            # 📊 Bar Chart Sentimen
            st.subheader("📊 Bar Chart Sentimen")
            fig2, ax2 = plt.subplots()
            sns.countplot(data=df, x="sentiment", hue="sentiment",
                          palette={"Negatif": "red", "Netral": "blue", "Positif": "green"}, legend=False)
            plt.xlabel("Sentimen")
            plt.ylabel("Jumlah Ulasan")
            st.pyplot(fig2)

            # 📊 Bar Chart Kategori
            st.subheader("🧩 Bar Chart Kategori Ulasan")
            fig3, ax3 = plt.subplots()
            sns.countplot(data=df, x="kategori", order=df["kategori"].value_counts().index, palette="pastel")
            plt.xlabel("Kategori")
            plt.ylabel("Jumlah Ulasan")
            plt.xticks(rotation=15)
            st.pyplot(fig3)

            # 📋 Tabel Persentase & Jumlah Kategori per Sentimen
            st.subheader("📋 Distribusi Kategori per Sentimen (%) dan Jumlah")
            table = df.groupby(["kategori", "sentiment"]).size().unstack(fill_value=0)
            table_percent = table.div(table.sum(axis=1), axis=0) * 100
            st.write("📌 **Persentase**")
            st.dataframe(table_percent.style.format("{:.1f}%"))
            st.write("📌 **Jumlah**")
            st.dataframe(table)

            # 📊 Stacked Bar Chart
            st.subheader("📊 Distribusi Kategori per Sentimen (Stacked Bar)")
            fig4, ax4 = plt.subplots()
            table.plot(kind="bar", stacked=True, colormap="Set2", ax=ax4)
            plt.xlabel("Kategori")
            plt.ylabel("Jumlah Ulasan")
            plt.xticks(rotation=15)
            st.pyplot(fig4)

            # 🔽 DOWNLOAD
            download_format = st.radio("Pilih format file untuk diunduh:", ("Excel (.xlsx)", "CSV (.csv)"))

            if download_format == "Excel (.xlsx)":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Sentiment Analysis")
                    table.to_excel(writer, sheet_name="Jumlah Kategori")
                    table_percent.to_excel(writer, sheet_name="Persentase Kategori")

                    workbook = writer.book
                    worksheet = workbook.add_worksheet("Visualisasi")
                    writer.sheets["Visualisasi"] = worksheet

                    for i, fig in enumerate([fig1, fig2, fig3, fig4], start=1):
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
