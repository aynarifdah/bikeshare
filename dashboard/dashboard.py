import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from babel.numbers import format_currency

#Header
st.title(
    """
    BIKE SHARING DASHBOARD 
    """
)

st.markdown (
    """
    Helow 🙌
    
    Welcome to Bike Sharing Dasboard !!!
    
    Dashboard ini dirancang untuk memberikan gambaran mendalam mengenai tren dan pola penggunaan sepeda berdasarkan dataset "Bike Sharing". Melalui analisis yang telah dilakukan, dashboard ini juga menjawab dua pertanyaan penting yang menjadi fokus eksplorasi data. 
    1. Bagaimana Pengaruh Musim terhadap Jumlah penyewaan?
    2. Pada jam berapakah penyewaan sepeda mengalami peningkatan?

    Semoga informasi yang disajikan dapat memberikan wawasan yang bermanfaat yaaaaaa 💡.
    """
)

#Load Data
bike_url = "https://raw.githubusercontent.com/aynarifdah/bigdata/refs/heads/main/datacleaned.csv"
bike_df = pd.read_csv(bike_url)

# sidebar 
st.sidebar.header("Pengaturan Dashboard")

season_map = {1: "Springer", 2: "Summer", 3: "fall", 4: "Winter"}
bike_df['season_x'] = bike_df['season_x'].map(season_map)

selected_season = st.sidebar.selectbox("Pilih Musim:", ["all season"] + list(season_map.values()))

if selected_season != "all season":
    filtered_df = bike_df[bike_df['season_x'] == selected_season]
else:
    filtered_df = bike_df

seasons = filtered_df.groupby('season_x', as_index=False)['cnt_x'].sum()
#ending sidebar


#pertanyaan 1
# Mapping angka ke nama musim
st.subheader("Bagaimana Pengaruh Musim terhadap Jumlah Penyewaan Sepeda?")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='season_x', y='cnt_x', data=seasons, palette='Blues', ax=ax)

ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")

ax.ticklabel_format(style='plain', axis='y')

# untuk Menampilkan plot 
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """visualisasi pertama, menunjukkan bahwa jumlah penyewa meningkat pada saat musim gugur dan terjadi penurunan pada saat musim dingin. Itu artinya terjadi fluktuasi jumlah penyewa.
        pada musim gugur, penyewaan sepeda maningkat yang mencapai 1.061.129 penyewa yang kemudian mengalami penurunan pada musim panas dan mengalami penurunan juga pada musim dingin. Penyewaan terendah terdapat pada musim semi. Dapat disimpulkan bahwa musim berpengaruh besar terhadap jumlah penyewa sepeda.
        """
    )




#pertanyaan 2
# Pastikan kolom datetime sudah dalam format datetime
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

hourly_data = bike_df.groupby("hr")["cnt_x"].mean().reset_index()

st.subheader("Pada Jam Berapakah Penyewaan Sepeda Mengalami Peningkatan?")


fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hourly_data["hr"], y=hourly_data["cnt_x"], marker="o", linestyle="-", color="b", ax=ax)

ax.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle="--", alpha=0.7)

st.pyplot(fig)

with st.expander("Lihat Penjelasan"):
    st.write(
        """ Grafik ini menunjukkan pola penyewaan sepeda berdasarkan jam dalam sehari.
            Tren menunjukkan bahwa jumlah penyewaan meningkat pada jam-jam tertentu.
            Berdasarkan hasil analisis, puncak penyewaan sepeda terjadi pada jam 5 sore atau jam-jam sibuk, 
            seperti jam pulang kerja atau aktivitas luar ruangan."""
    )
