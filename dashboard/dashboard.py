import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import sys

# Cek apakah matplotlib tersedia
try:
    import matplotlib.pyplot as plt
    print("Matplotlib berhasil diimpor!")
except ModuleNotFoundError:
    print("Matplotlib tidak ditemukan! Menginstall ulang...")
    subprocess.run([sys.executable, "-m", "pip", "install", "matplotlib"])

# Load dataset
file_path = "all_data.csv"
df = pd.read_csv("all_data.csv")

# Convert date column to datetime format
df['dteday_x'] = pd.to_datetime(df['dteday_x'])

# Streamlit App
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.image("logo.jpeg", use_container_width=True)

# Date filter
date_range = st.sidebar.date_input("Pilih Rentang Waktu", 
                                  [df['dteday_x'].min(), df['dteday_x'].max()], 
                                  min_value=df['dteday_x'].min(), 
                                  max_value=df['dteday_x'].max())

# Filter data berdasarkan rentang waktu
filtered_df = df[(df['dteday_x'] >= pd.to_datetime(date_range[0])) & (df['dteday_x'] <= pd.to_datetime(date_range[1]))]

# Main content
st.title("Dashboard Visualisasi Data")

# Visualisasi distribusi penyewaan berdasarkan musim
st.subheader("Distribusi Penyewaan Berdasarkan Musim")
byseason_df = pd.DataFrame({
    'season': [1, 2, 3, 4],
    'cnt_day': [179, 182, 188, 176]
})

# Buat mapping angka ke nama musim
season_mapping = {
    1: 'Spring (Semi)',
    2: 'Summer (Panas)',
    3: 'Fall (Gugur)',
    4: 'Winter (Dingin)'
}

byseason_df['season'] = byseason_df['season'].map(season_mapping)

# Sidebar untuk filter musim
selected_season = st.sidebar.multiselect("Pilih Musim", options=byseason_df['season'].unique(), default=byseason_df['season'].unique())

# Filter data berdasarkan musim
display_df = byseason_df[byseason_df['season'].isin(selected_season)]

# Visualisasi setelah filter
display_df = display_df.sort_values(by='cnt_day', ascending=False)

fig, ax = plt.subplots()
ax.bar(display_df['season'], display_df['cnt_day'], color='blue')
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Visualisasi tren penyewaan sepeda dari waktu ke waktu
st.subheader("Tren Penyewaan Sepeda dari Waktu ke Waktu")
fig, ax = plt.subplots()
ax.plot(filtered_df['dteday_x'], filtered_df['cnt_x'], color='blue', marker='o', linestyle='-')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)