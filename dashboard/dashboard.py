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
    
    => dashboard ini dirancang untuk memberikan gambaran mendalam mengenai tren dan pola penggunaan sepeda berdasarkan dataset "Bike Sharing". Melalui analisis yang telah dilakukan, dashboard ini juga menjawab dua pertanyaan penting yang menjadi fokus eksplorasi data. Semoga informasi yang disajikan dapat memberikan wawasan yang bermanfaat bagi Anda.
    """
)

#Load Data
bike_url = "https://raw.githubusercontent.com/aynarifdah/Bigdata/refs/heads/main/Bigdata.csv"
bike_df = pd.read_csv(bike_url)

st.write(bike_df.info())
st.write(bike_df.head())

def season(df):
    season_df = df.groupby('season').agg({
        "cnt": "sum",        
        "windspeed": "mean"  
    }).reset_index()

    season_df.rename(columns={
        "cnt": "total_sewa",
        "windspeed": "average_windspeed"
    }, inplace=True)

    return season_df


# sidebar 
st.sidebar.header("Pengaturan Dashboard")

season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

selected_season = st.sidebar.selectbox(
    "choose season",
    options=[1, 2, 3, 4],  
    format_func=lambda x: season_map[x]
)

filtered_df = bike_df[bike_df['season'] == selected_season]

st.subheader(f"Perbandingan Jumlah Penyewa di {season_map[selected_season]} (2011 vs 2012)")
season_year_df = filtered_df.groupby('yr')['cnt'].sum().reset_index()

season_year_df['yr'] = season_year_df['yr'].map({0: 2011, 1: 2012})

fig, ax = plt.subplots()
sns.barplot(x="yr", y="cnt", data=season_year_df, palette=["blue", "yellow"], ax=ax)

ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Penyewa")
ax.set_xticklabels(["2011", "2012"])
ax.set_title(f"Jumlah Penyewa di Musim {season_map[selected_season]}")
st.pyplot(fig)

#ending sidebar


#pertanyaan 1
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])
data_2011 = bike_df[bike_df['dteday'].dt.year == 2011]

st.subheader("Sejauh mana hubungan kecepatan angin mempengaruhi jumlah penyewaan sepeda pada tahun 2011?")

#visualisasi untuk melihat pengaruh kecepatan angin
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x="windspeed", y="cnt", data=data_2011, color="royalblue", alpha=0.6, ax=ax)
ax.set_title("Hubungan Kecepatan Angin dengan Jumlah Penyewaan Sepeda (2011)")
ax.set_xlabel("Kecepatan Angin", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=13)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ Dari grafik ini, kita bisa melihat apakah ada pola tertentu antara kecepatan angin dan jumlah penyewaan sepeda. 
            pada visualisasinya, menunjukan bahwa tidak ada kenaikan ataupun penurunan penyewaan sepeda yang kuat jadi, kecepatan angin tidak terlalu berpengaruh terhadap jumlah penyewaan sepeda.
        """
    )


#pertanyaan 2
musim = {1: "Musim Dingin", 2: "Musim Semi", 3: "Musim Panas", 4: "Musim Gugur"}
bike_df['season'] = bike_df['season'].map(musim)

#untuk melihat Korelasi Musim dengan Penyewaan Sepeda
st.subheader("Berdasarkan pengaruh kecepatan angin, apakah yang menjadi faktor terbesar dalam jumlah penyewaan?")
bike_df['seasons'] = bike_df['season'].astype('category').cat.codes

corr_season = bike_df[['seasons', 'cnt']].corr()
fig, ax = plt.subplots(figsize=(6,5))
sns.heatmap(corr_season, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Korelasi Musim dengan Jumlah Penyewaan Sepeda")
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ heatmap ini menunjukkan jumlah penyewaan sepeda di setiap musim. 
            Dalam heatmap season menunjukan korelasi positif yang artinya, musim berpengaruh besar terhadap jumlah penyewaan sepeda. Setiap perubahan musim, makan akan berubah juga jumlah penyewaannya
        """
    )


#Addition

# Menghitung rata-rata penyewa casual dan registered untuk tiap tahun
casual_2011 = bike_df[bike_df['yr'] == 0]['casual'].mean()
regist_2011 = bike_df[bike_df['yr'] == 0]['registered'].mean()
casual_2012 = bike_df[bike_df['yr'] == 1]['casual'].mean()
regist_2012 = bike_df[bike_df['yr'] == 1]['registered'].mean()

year = ['2011', '2012']
casual = [casual_2011, casual_2012]
registered = [regist_2011, regist_2012]

# visualisas untuk Casual & Registered Users
st.subheader("Rata-rata Penyewa Casual dan Registered (2011 - 2012)")

fig, ax = plt.subplots(figsize=(8,5))

ax.plot(year, casual, marker='o', linestyle='-', color='blue', label='Casual')
ax.plot(year, registered, marker='o', linestyle='-', color='skyblue', label='Registered')

ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Rata-rata Penyewa", fontsize=12)
ax.set_title("Tren Rata-rata Penyewa Casual dan Registered (2011 - 2012)", fontsize=14)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

ax.set_ylim(0, max(max(casual), max(registered)) * 1.1)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """
            pada visualisasi rata - rata penyewa berdasarkan status (casual or registered ) menunjukkan bahwa pada tahun 2011 dan 2012 kebanyakan adalah pengguna yang sudah terdaftar (registered). Dan rata - rata terendah adalah penyewa yang belum terdaftar (casual).
        """
    )


st.caption('Ayna Dwi Rifdah (Februari 2025)')

