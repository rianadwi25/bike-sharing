import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load dataset
file_path = "all_data.csv"
df = pd.read_csv(file_path)

# Convert date column to datetime format
df['dteday_x'] = pd.to_datetime(df['dteday_x'])

# Pastikan kolom tanggal dalam format datetime
df['dteday_x'] = pd.to_datetime(df['dteday_x'])
print(df.columns)

rfm_df = df.groupby('dteday_x', as_index=False).agg({
    'cnt_x': ['max', 'nunique', 'sum']
})
rfm_df.columns = ['dteday_x', 'frequency', 'monetary', 'recency']
rfm_df['dteday_x'] = rfm_df['dteday_x'].dt.date
recent_date = df['dteday_x'].dt.date.max()
rfm_df['recency'] = rfm_df['dteday_x'].apply(lambda x: (recent_date - x).days)
rfm_df.head()

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
byseason_df = byseason_df.sort_values(by='cnt_day', ascending=False)

fig, ax = plt.subplots()
ax.bar(byseason_df['season'], byseason_df['cnt_day'], color='blue')
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Visualisasi tren penyewaan sepeda dari waktu ke waktu
st.subheader("Tren Penyewaan Sepeda dari Waktu ke Waktu")
start_date = pd.to_datetime("2011-01-01")
end_date = pd.to_datetime("2012-12-31")

df_filtered = df[(df['dteday_x'] >= start_date) & (df['dteday_x'] <= end_date)]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_filtered['dteday_x'], df_filtered['cnt_x'], label='Total Rentals (Daily)', color='b')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda dari Waktu ke Waktu")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# RFM Analysis: Sort by Recency
st.subheader("Top 5 Pelanggan Berdasarkan Recency")
rfm_top5 = rfm_df.sort_values(by="recency", ascending=True).head(5)
st.write(rfm_top5)
