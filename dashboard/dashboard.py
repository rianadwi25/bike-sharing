import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Menambahkan logo di sidebar kiri dengan path lengkap (menggunakan use_container_width)
st.sidebar.image("logo.jpeg", use_container_width=True)

# Menambahkan kalender di bawah logo
date = st.sidebar.date_input("Pilih Tanggal")

sns.set(style='dark')
st.header("Dashboard Analisis Penyewaan Sepeda")
st.sidebar.markdown("<h3 style='text-align: center;'>Dashboard Sederhana Penyewaan Sepeda</h3>", unsafe_allow_html=True)

# Membaca file CSV
file_path = 'all_data.csv'
df = pd.read_csv(file_path)

def seasonal_rentals(df, show_pie=False):
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(["Winter", "Spring", "Summer", "Fall"], [300000, 800000, 1050000, 920000], color='darkblue')

    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(fig)
    
    if show_pie:
        # Pie chart
        st.subheader("Distribusi Penyewaan Berdasarkan Musim")
        byseason_df = df.groupby('season_y', observed=False)['cnt_x'].sum().reset_index()
        byseason_df = byseason_df.sort_values(by='cnt_x', ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.pie(byseason_df['cnt_x'], labels=["Spring", "Summer", "Fall", "Winter"], autopct='%1.1f%%', colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
        st.pyplot(fig)
    
    # Kesimpulan
    st.markdown("### Kesimpulan:")
    st.markdown("- Musim **Summer** memiliki jumlah penyewaan tertinggi, menunjukkan bahwa cuaca hangat meningkatkan minat masyarakat untuk bersepeda.")
    st.markdown("- Musim **Winter** memiliki jumlah penyewaan terendah, kemungkinan karena kondisi cuaca yang kurang mendukung.")
    st.markdown("- Pemilik bisnis penyewaan sepeda dapat mempertimbangkan promosi khusus di musim dingin untuk meningkatkan penyewaan.")

def weekly_data(df):
    st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")

    df['dteday_x'] = pd.to_datetime(df['dteday_x'])
    df['day_of_week'] = df['dteday_x'].dt.day_name()

    avg_rent_per_day = df.groupby("day_of_week", observed=False)['cnt_x'].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    weather_data = pd.DataFrame({
        "day_labels": avg_rent_per_day.index,
        "avg_rent": avg_rent_per_day.values
    })

    custom_colors = ["blue", "orange", "green", "red", "blue", "brown", "pink"]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="day_labels", y="avg_rent", data=weather_data, palette=custom_colors)

    ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Hari dalam Seminggu", fontsize=14)
    ax.set_xlabel("Hari dalam Seminggu", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.set_ylim(0, max(avg_rent_per_day) * 1.2)

    ax.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig)
    
    # Kesimpulan
    max_day = avg_rent_per_day.idxmax()
    min_day = avg_rent_per_day.idxmin()
    st.markdown("### Kesimpulan:")
    st.markdown(f"- Hari dengan jumlah penyewaan tertinggi: **{max_day}**, kemungkinan karena akhir pekan lebih banyak orang beraktivitas di luar ruangan.")
    st.markdown(f"- Hari dengan jumlah penyewaan terendah: **{min_day}**, yang mungkin disebabkan oleh hari kerja dan kesibukan kantor/sekolah.")
    st.markdown("- Tren ini dapat membantu dalam pengelolaan stok sepeda untuk meningkatkan efisiensi operasional.")

# Menambahkan filter untuk memilih grafik yang ingin ditampilkan
chart_option = st.selectbox("Pilih Grafik", 
                            ["Pilih Grafik untuk Ditampilkan", 
                             "Tren Penyewaan Berdasarkan Musim", 
                             "Distribusi Penyewaan Berdasarkan Musim (Pie Chart)",
                             "Jumlah Penyewaan Berdasarkan Hari dalam Seminggu"])

# Menampilkan grafik yang dipilih berdasarkan filter
if chart_option == "Pilih Grafik untuk Ditampilkan":
    seasonal_rentals(df)
    weekly_data(df)
elif chart_option == "Tren Penyewaan Berdasarkan Musim":
    seasonal_rentals(df)
elif chart_option == "Distribusi Penyewaan Berdasarkan Musim (Pie Chart)":
    seasonal_rentals(df, show_pie=True)
elif chart_option == "Jumlah Penyewaan Berdasarkan Hari dalam Seminggu":
    weekly_data(df)
