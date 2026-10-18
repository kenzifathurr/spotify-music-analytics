import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px

# 1. KUNCI AKSES SPOTIFY KAMU
CLIENT_ID = "MASUKKAN_CLIENT_ID_KAMU_DI_SINI"
CLIENT_SECRET = "MASUKKAN_CLIENT_SECRET_KAMU_DI_SINI"

# Koneksi Otomatis ke Server Spotify
try:
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
except Exception as e:
    st.error("Gagal koneksi ke Spotify API. Pastikan Client ID dan Secret sudah diisi dengan benar.")

st.set_page_config(page_title="Automated Music Analytics", page_icon="🚀", layout="wide")
st.title("🚀 Real-Time Spotify Audio Features Tracker")
st.markdown("Aplikasi ini menembak API Spotify secara otomatis untuk menganalisis karakteristik lagu secara real-time.")

# 2. Fitur Input Otomatis: Ketik Nama Artis Sesukamu!
artis_input = st.text_input("Ketik Nama Artis (Contoh: Bruno Mars, NewJeans, Eminem):", "BABYMONSTER")

if artis_input and CLIENT_ID:
    try:
        # Komputer mencari lagu artis tersebut di server Spotify secara otomatis
        results = sp.search(q=f"artist:{artis_input}", type="track", limit=10)
        tracks = results['tracks']['items']
        
        list_data = []
        for track in tracks:
            track_id = track['id']
            track_name = track['name']
            
            # Komputer mengambil metrik Energy, Danceability, dll langsung dari AI Spotify
            audio_features = sp.audio_features(track_id)
            
            if audio_features and audio_features[0]:
                features = audio_features[0]
                list_data.append({
                    "Lagu": track_name,
                    "Energy": features['energy'],
                    "Danceability": features['danceability'],
                    "Loudness": features['loudness']
                })
        
        if list_data:
            # Mengubah data mentah dari Spotify menjadi tabel otomatis
            df = pd.DataFrame(list_data)
            
            # 3. Menampilkan Hasil ke Website
            kolom1, kolom2 = st.columns(2)
            with kolom1:
                st.subheader(f"📊 Data Lagu Otomatis dari {artis_input}")
                st.dataframe(df, use_container_width=True)
                
            with kolom2:
                st.subheader("🔥 Karakteristik Hasil Tembak API")
                fig = px.scatter(df, x="Danceability", y="Energy", hover_name="Lagu", 
                                 size="Danceability", title=f"Peta Logika Musik: {artis_input}")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Lagu tidak ditemukan. Coba ketik nama artis lain.")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengambil data: {e}")
else:
    st.info("Silakan masukkan Client ID dan Client Secret Spotify Anda di dalam kode terlebih dahulu untuk mengaktifkan fitur otomatisasi.")
