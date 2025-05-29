import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cek Tiang", layout="wide")

st.title("📍 Cek Posisi Tiang")

st.markdown("""
Selamat datang di aplikasi **Cek Tiang**!  
Gunakan aplikasi ini untuk melihat dan mengecek posisi tiang berdasarkan data koordinat.
""")

# Upload file data tiang (contoh: Excel/CSV dengan kolom latitude, longitude, dan nama)
uploaded_file = st.file_uploader("Unggah file data tiang (CSV atau Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File berhasil dibaca!")
        st.dataframe(df)

        # Pastikan kolom lokasi ada
        if all(col in df.columns for col in ['latitude', 'longitude']):
            st.subheader("🗺️ Peta Lokasi Tiang")

            # Buat peta awal
            map_center = [df['latitude'].mean(), df['longitude'].mean()]
            m = folium.Map(location=map_center, zoom_start=15)

            # Tambahkan marker tiap tiang
            for idx, row in df.iterrows():
                folium.Marker(
                    [row['latitude'], row['longitude']],
                    popup=row.get('nama', f"Tiang {idx+1}")
                ).add_to(m)

            st_data = st_folium(m, width=700, height=500)
        else:
            st.warning("File harus memiliki kolom 'latitude' dan 'longitude'.")

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
else:
    st.info("Silakan unggah file untuk mulai.")