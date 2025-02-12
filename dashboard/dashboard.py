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
musim = {1: "Musim Dingin", 2: "Musim Semi", 3: "Musim Panas", 4: "Musim Gugur"}
bike_df['season'] = bike_df['season'].map(musim)

#untuk melihat Korelasi Musim dengan Penyewaan Sepeda
st.subheader("Bagaimana Pengaruh Musim terhadap Jumlah penyewaan?")
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

#pertanyaan 2
# Pastikan kolom datetime sudah dalam format datetime
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

hourly_data = bike_df.groupby("hr")["cnt"].mean().reset_index()

st.subheader("Pada Jam Berapakah Penyewaan Sepeda Mengalami Peningkatan?")


fig, ax = plt.subplots(figsize=(10,6))
sns.lineplot(x="hr", y="cnt", data=hourly_data, marker="o", color="royalblue", ax=ax)
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ Grafik ini menunjukkan pola penyewaan sepeda berdasarkan jam dalam sehari.
            peningkatan penyewaan terjadi pada jam - jam tertentu. berdasarkan hasil analisa menunjukkan bahwa jumlah penyewaan sepeda tertinggi terjadi pada jam 6 sore yang mana pada jam tersebut merupakan jam pulang kantor sehingga menyebabkan peningkatan penyewa

        """
    )


#Addition
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

hourly_data = bike_df.groupby("hr")[["cnt", "temp", "hum", "windspeed"]].mean().reset_index()

st.subheader("Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.scatterplot(ax=axes[0], x=hourly_data["temp"], y=hourly_data["cnt"], alpha=0.5, color="tomato")
axes[0].set_title("Pengaruh Suhu terhadap Penyewaan Sepeda")
axes[0].set_xlabel("Suhu")
axes[0].set_ylabel("Jumlah Penyewaan")

sns.scatterplot(ax=axes[1], x=hourly_data["hum"], y=hourly_data["cnt"], alpha=0.5, color="royalblue")
axes[1].set_title("Pengaruh Kelembaban terhadap Penyewaan Sepeda")
axes[1].set_xlabel("Kelembaban")
axes[1].set_ylabel("Jumlah Penyewaan")

sns.scatterplot(ax=axes[2], x=hourly_data["windspeed"], y=hourly_data["cnt"], alpha=0.5, color="seagreen")
axes[2].set_title("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
axes[2].set_xlabel("Kecepatan Angin")
axes[2].set_ylabel("Jumlah Penyewaan")

plt.tight_layout()
st.pyplot(fig)


st.subheader("Korelasi antara Cuaca dan Penyewaan Sepeda")
plt.figure(figsize=(8,6))
corr_matrix = hourly_data[["temp", "hum", "windspeed", "cnt"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Heatmap Korelasi")
st.pyplot(plt)

with st.expander("See explanation"):
    st.write(
        """ Dari visualisasi ini, kita bisa melihat bagaimana faktor cuaca seperti suhu, kelembaban, dan kecepatan angin 
            mempengaruhi jumlah penyewaan sepeda. Biasanya, suhu yang lebih tinggi meningkatkan penyewaan, sedangkan 
            kelembaban dan kecepatan angin tidak terlalu berpengaruh signifikan.
        """
    )

st.caption('Ayna Dwi Rifdah (Februari 2025)')

