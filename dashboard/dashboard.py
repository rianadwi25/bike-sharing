import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Menambahkan logo di sidebar kiri dengan path lengkap (menggunakan use_container_width)
logo_path = 'D:/dwi/kuliah/submission/dashboard/logo.jpeg'  # Path lengkap ke file logo
st.sidebar.image(logo_path, use_container_width=True)  # Gantilah ke use_container_width

sns.set(style='dark')
st.header("Dashboard Analisis Penyewaan Sepeda")
st.sidebar.markdown("<h3 style='text-align: center;'>Dashboard Sederhana Penyewaan Sepeda</h3>", unsafe_allow_html=True)

# Membaca file CSV
file_path = 'D:/dwi/kuliah/submission/dashboard/all_data.csv'
df = pd.read_csv(file_path)

def season(df):
    st.subheader("Distribusi Penyewaan Berdasarkan Musim")

    byseason_df = pd.DataFrame({
        'season': [1, 2, 3, 4],
        'cnt_day': [179, 182, 188, 176]
    })
    byseason_df = byseason_df.sort_values(by='cnt_day', ascending=False)

    fig, ax = plt.subplots()
    sns.barplot(y='cnt_day', x='season', data=byseason_df, color='blue')
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
    plt.xticks(ticks=[0, 1, 2, 3], labels=["Spring", "Summer", "Fall", "Winter"])
    st.pyplot(fig)

def seasonal_rentals(df):
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(["Winter", "Spring", "Summer", "Fall"], [300000, 800000, 1050000, 920000], color='darkblue')

    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan Sepeda")
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(fig)

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

# Menambahkan filter untuk memilih grafik yang ingin ditampilkan
chart_option = st.selectbox("Pilih Grafik", 
                            ["Pilih Grafik untuk Ditampilkan", 
                             "Distribusi Penyewaan Berdasarkan Musim", 
                             "Tren Penyewaan Berdasarkan Musim", 
                             "Jumlah Penyewaan Berdasarkan Hari dalam Seminggu"])

# Menampilkan grafik yang dipilih berdasarkan filter
if chart_option == "Pilih Grafik untuk Ditampilkan":
    # Menampilkan semua grafik jika tidak ada pilihan
    season(df)
    seasonal_rentals(df)
    weekly_data(df)
elif chart_option == "Distribusi Penyewaan Berdasarkan Musim":
    season(df)
elif chart_option == "Tren Penyewaan Berdasarkan Musim":
    seasonal_rentals(df)
elif chart_option == "Jumlah Penyewaan Berdasarkan Hari dalam Seminggu":
    weekly_data(df)