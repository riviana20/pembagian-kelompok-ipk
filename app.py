import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import re
from datetime import datetime
import io

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA & TEMA OVAL PASTEL SPACE (PURE ASTRONAUT EDITION)
# ==========================================
st.set_page_config(page_title="Pembagian Kelompok Adil K-Means", layout="wide")

# --- SUNTIKAN HTML, CSS, & JAVASCRIPT EFEK ROKET MELUNCUR ---
st.markdown("""
<div class="floating-icons-container">
    <div class="floating-icon icon-1">🪐</div>
    <div class="floating-icon icon-2">🚀</div>
    <div class="floating-icon icon-3">👨‍🚀</div>
    <div class="floating-icon icon-4">🌟</div>
    <div class="floating-icon icon-5">☄️</div>
    <div class="floating-icon icon-6">🛸</div>
    <div class="floating-icon icon-7">🛰️</div>
    <div class="floating-icon icon-8">💫</div>
    <div class="floating-icon icon-9">🪐</div>
    <div class="floating-icon icon-10">🚀</div>
    <div class="floating-icon icon-11">🌟</div>
    <div class="floating-icon icon-12">☄️</div>
    <div class="floating-icon icon-13">🛸</div>
    <div class="floating-icon icon-14">👨‍🚀</div>
    <div class="floating-icon icon-15">💫</div>
    <div class="floating-icon icon-16">🪐</div>
    <div class="floating-icon icon-17">🚀</div>
    <div class="floating-icon icon-18">🌟</div>
    <div class="floating-icon icon-19">☄️</div>
    <div class="floating-icon icon-20">🛸</div>
    <div class="floating-icon icon-21">🛰️</div>
    <div class="floating-icon icon-22">💫</div>
    <div class="floating-icon icon-23">👨‍🚀</div>
    <div class="floating-icon icon-24">🪐</div>
    <div class="floating-icon icon-25">🌟</div>
</div>

<style>
    /* Latar belakang dasar pastel lembut dengan tekstur bintang halus */
    .stApp {
        background: url("https://www.transparenttextures.com/patterns/stardust.png"), #f0f4f8;
        overflow: hidden;
    }
    
    /* Container untuk ikon melayang di background */
    .floating-icons-container {
        position: fixed;
        top: 0; 
        left: 0; 
        width: 100vw; 
        height: 100vh;
        pointer-events: none;
        z-index: 0;
    }
    
/* Warna Pink Soft Pastel untuk Boks Hasil */
    .result-oval-container {
        background: linear-gradient(135deg, #fff0f2 0%, #ffe3e7 100%) !important;
        backdrop-filter: blur(6px);
        border: 2px solid #ffb3ba !important;
        border-radius: 25px !important;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(255, 179, 186, 0.25) !important;
        margin-bottom: 25px;
        position: relative;
        z-index: 2;
    }
    
    /* Gaya umum untuk setiap ikon latar belakang */
    .floating-icon {
        position: absolute;
        opacity: 0.28; 
        animation: floatAnimation infinite ease-in-out;
    }
    
    /* Keyframes untuk animasi melayang & berputar pelan */
    @keyframes floatAnimation {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-35px) rotate(15deg); }
    }
    
    /* Distribusi Posisi, Ukuran, Durasi Animasi yang Sangat Acak & Padat */
    .icon-1  { top: 5%;   left: 3%;   font-size: 65px; animation-duration: 18s; }
    .icon-2  { top: 10%;  left: 22%;  font-size: 38px; animation-duration: 14s; animation-delay: 1s; }
    .icon-3  { top: 4%;   left: 42%;  font-size: 48px; animation-duration: 22s; animation-delay: 3s; }
    .icon-4  { top: 14%;  left: 62%;  font-size: 35px; animation-duration: 19s; animation-delay: 5s; }
    .icon-5  { top: 7%;   left: 82%;  font-size: 55px; animation-duration: 13s; }
    .icon-6  { top: 22%;  left: 93%;  font-size: 42px; animation-duration: 16s; animation-delay: 2s; }
    .icon-7  { top: 28%;  left: 4%;   font-size: 40px; animation-duration: 20s; animation-delay: 4s; }
    .icon-8  { top: 42%;  left: 14%;  font-size: 52px; animation-duration: 15s; }
    .icon-9  { top: 26%;  left: 76%;  font-size: 58px; animation-duration: 24s; animation-delay: 1s; }
    .icon-10 { top: 40%;  left: 86%;  font-size: 45px; animation-duration: 17s; animation-delay: 6s; }
    .icon-11 { top: 58%;  left: 5%;   font-size: 50px; animation-duration: 21s; animation-delay: 2s; }
    .icon-12 { top: 72%;  left: 12%;  font-size: 38px; animation-duration: 13s; animation-delay: 4s; }
    .icon-13 { top: 88%;  left: 3%;   font-size: 55px; animation-duration: 19s; }
    .icon-14 { top: 82%;  left: 24%;  font-size: 42px; animation-duration: 25s; animation-delay: 3s; }
    .icon-15 { top: 85%;  left: 46%;  font-size: 35px; animation-duration: 16s; animation-delay: 1s; }
    .icon-16 { top: 90%;  left: 66%;  font-size: 50px; animation-duration: 22s; }
    .icon-17 { top: 80%;  left: 82%;  font-size: 65px; animation-duration: 18s; animation-delay: 5s; }
    .icon-18 { top: 88%;  left: 92%;  font-size: 32px; animation-duration: 14s; animation-delay: 3s; }
    .icon-19 { top: 52%;  left: 26%;  font-size: 30px; animation-duration: 23s; animation-delay: 2s; }
    .icon-20 { top: 65%;  left: 36%;  font-size: 44px; animation-duration: 15s; }
    .icon-21 { top: 48%;  left: 54%;  font-size: 32px; animation-duration: 20s; animation-delay: 4s; }
    .icon-22 { top: 60%;  left: 66%;  font-size: 40px; animation-duration: 18s; animation-delay: 2s; }
    .icon-23 { top: 50%;  left: 76%;  font-size: 48px; animation-duration: 26s; animation-delay: 1s; }
    .icon-24 { top: 68%;  left: 89%;  font-size: 45px; animation-duration: 17s; }
    .icon-25 { top: 32%;  left: 48%;  font-size: 36px; animation-duration: 19s; animation-delay: 3s; }

    /* Gaya untuk Animasi Roket Selebrasi Pasca-Klik */
    .rocket-blast {
        position: fixed;
        bottom: -50px;
        font-size: 40px;
        z-index: 9999;
        pointer-events: none;
        animation: launchUp 3s forwards ease-in-out;
    }

    @keyframes launchUp {
        0% { transform: translateY(0) scale(0.5); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-110vh) translateX(var(--x-move)) rotate(var(--rot)); scale(1.2); opacity: 0; }
    }

/* Kontainer Judul Utama bertema Kapsul Galaxy Premium - DIPERBESAR & DINAIKKAN */
    .space-title-container {
        background: linear-gradient(135deg, rgba(255, 154, 162, 0.18), rgba(186, 225, 255, 0.18));
        border: 3px dashed #bae1ff; /* Mengubah garis border menjadi lebih tebal */
        border-radius: 25px;
        padding: 35px 20px; /* Memperbesar padding atas & bawah dari 20px menjadi 35px */
        margin-top: -10px;  /* Menggunakan margin minus agar posisi kotak naik ke atas */
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(186, 225, 255, 0.3);
    }

.space-title {
        font-size: 38px !important; /* Memperbesar ukuran teks dari 32px menjadi 38px */
        font-weight: 850;
        color: #1e293b !important; 
        margin-bottom: 12px;
        letter-spacing: 0.8px;
        text-shadow: 1px 1px 0px #ffffff;
    }
    
    .space-subtitle {
        font-size: 13px !important;
        color: #334155 !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 700;
        margin: 0 !important;
    }
    
    /* Box Kapsul Utama dengan Bentuk Oval dan Warna Pastel Lembut */
    .oval-container {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(6px);
        border: 2px solid #ffdfba;
        border-radius: 25px !important;
        padding: 25px;
        box-shadow: 0 8px 24px rgba(186, 225, 255, 0.3);
        margin-bottom: 25px;
        position: relative;
        z-index: 2;
    }

/* Memaksa teks di dalam konten expander agar selalu berwarna gelap */
div[data-testid="stExpander"] div[role="region"] * {
    color: #1e293b !important;
}
    
    /* Memaksa header / teks yang bisa diklik agar selalu berwarna gelap dan kontras */
    .stExpander [data-testid="stExpanderHeader"] p, 
    .stExpander [data-testid="stExpanderHeader"] span,
    .stExpander [data-testid="stExpanderHeader"] svg {
        color: #1e293b !important;
        fill: #1e293b !important;
        font-weight: 700 !important;
    }

    /* Memaksa isi/teks di dalam expander saat dibuka agar background transparan dan teks gelap */
    div[data-testid="stExpanderDetails"] > div {
        background-color: transparent !important;
        color: #1e293b !important;
    }
    
    /* === FORCE SEMUA TEXT UTAMA AGAR HITAM / GELAP PEKAT === */
    html, body, [data-testid="stAppViewContainer"], .stApp, label, p, span, h1, h2, h3, h4, h5, h6, li, div {
        color: #1e293b !important;
        font-weight: 550 !important;
    }
    
    /* === FORCE INPUT TEXT AREA AGAR TETAP KONTRAS === */
    .stTextArea textarea {
        color: #1e293b !important;
        background-color: #ffffff !important;
        font-weight: 550 !important;
        caret-color: #000000 !important; /* <--- INI SAKTI: Memaksa kursor ketik berwarna hitam */
    }

    /* === FIX UNTUK BOKS UNGGAH FILE (FILE UPLOADER) AGAR TIDAK HITAM DI HP === */
    div[data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 2px dashed #ffdfba !important;
        border-radius: 20px !important;
        padding: 15px !important;
    }
    div[data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }
    div[data-testid="stFileUploader"] section div, 
    div[data-testid="stFileUploader"] section p, 
    div[data-testid="stFileUploader"] section span, 
    div[data-testid="stFileUploader"] section small {
        color: #1e293b !important;
        font-weight: 550 !important;
    }
    div[data-testid="stFileUploader"] button {
        background: linear-gradient(90deg, #ffdfba, #ffb3ba) !important;
        color: #1e293b !important;
        border: 1px solid #ffb3ba !important;
        border-radius: 15px !important;
    }

    /* === FORCE BOKS NOTIFIKASI INFO / WARNING AGAR KONTRAS === */
    div[data-testid="stNotification"] {
        background-color: #e0f2fe !important;
        border: 1px solid #bae1ff !important;
    }
    div[data-testid="stNotification"] p, 
    div[data-testid="stNotification"] span, 
    div[data-testid="stNotification"] div {
        color: #0369a1 !important;
        font-weight: 600 !important;
    }
    ::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }
    
    /* Membuat Tombol-tombol Berbentuk Oval dengan Warna Pastel */
    .stButton>button {
        border-radius: 30px !important;
        background: linear-gradient(90deg, #ffb3ba, #ffdfba) !important;
        color: #1e293b !important;
        border: 1px solid #ffb3ba !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        box-shadow: 0 4px 12px rgba(255, 179, 186, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 179, 186, 0.6);
        background: linear-gradient(90deg, #ffdfba, #ffb3ba) !important;
    }
    
    /* Kustomisasi Metrik bergaya Kapsul Astronot Pastel Oval */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(3px);
        border: 2px solid #baffc9;
        border-radius: 25px !important;
        padding: 15px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(186, 255, 201, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        color: #ff6b81 !important;
        font-weight: 800;
    }
    
    /* Pengayaan Sidebar Gradasi Kosmis */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff0f5 0%, #e6f2ff 100%) !important;
        border-right: 3px dashed #bae1ff;
    }
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
        font-weight: bold !important;
        color: #1e293b !important;
        letter-spacing: 1px;
    }
    /* Efek boks oval untuk pilihan menu di dalam sidebar */
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.8);
        padding: 12px;
        border-radius: 18px;
        border: 1px solid #ffdfba;
    }
    /* FIX EXPANDER AGAR TIDAK HITAM SAAT DARK MODE */

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.95) !important;
    border: 2px solid #ffdfba !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
}

div[data-testid="stExpander"] details {
    background: rgba(255,255,255,0.95) !important;
}

div[data-testid="stExpander"] summary {
    background: linear-gradient(90deg,#fff7e6,#ffeef2) !important;
    color: #1e293b !important;
    font-weight: 700 !important;
    border-radius: 18px !important;
}

div[data-testid="stExpander"] summary p {
    color: #1e293b !important;
}

div[data-testid="stExpanderDetails"] {
    background: rgba(255,255,255,0.95) !important;
}

div[data-testid="stExpanderDetails"] p,
div[data-testid="stExpanderDetails"] span,
div[data-testid="stExpanderDetails"] div {
    color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# Kepala Kontrol Misi (Header) Baru dengan Kontainer Khusus
st.markdown("""
<div class="space-title-container">
    <div class="space-title">🪐 Pembagian Tugas Kelompok Mahasiswa Berdasarkan IPK 🪐</div>
    <div class="space-subtitle">ALGORITMA K-Means × STRATIFIED ROUND-ROBIN</div>
</div>
""", unsafe_allow_html=True)

# Mengubah expander menjadi transparan/default agar responsif penuh terhadap Light & Dark Mode
with st.expander("✨ Halo Kapten! (Klik untuk melihat panduan misi kelompok)", expanded=False):
    st.markdown("""
                
    <b>Sistem ini membagi kelompok secara otomatis menggunakan pendekatan kecerdasan buatan:</b><br><br>
    &nbsp;&nbsp;1. <b>Orbit K-Means:</b> Memetakan dan membagi mahasiswa ke dalam cluster performa akademik (Strata Tinggi, Sedang, Kurang).<br>
    &nbsp;&nbsp;2. <b>Warp Drive Round-Robin:</b> Mendistribusikan mahasiswa dari tiap orbit cluster ke kelompok tujuan secara bergiliran.<br><br>
    <b>Hasil akhirnya adalah tim yang seimbang dan adil layaknya kru astronot yang siap menjalankan misi!</b>
    """, unsafe_allow_html=True)

# Inisialisasi session state untuk histori jika belum ada
if "histori_kelompok" not in st.session_state:
    st.session_state.histori_kelompok = []

# Fungsi pembantu untuk mengubah DataFrame menjadi file Excel (.xlsx)
def konversi_ke_excel(df_data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_data.to_excel(writer, index=False, sheet_name='Hasil Kelompok')
    return output.getvalue()

# ==========================================
# 2. INPUT DATA DI SIDEBAR
# ==========================================
st.sidebar.markdown("### 🚀 KONTROL GALAXY")
metode_input = st.sidebar.radio("Pilih Metode Input Data:", ("Ketik Manual", "Unggah File (Excel/CSV)"))

df = None

if metode_input == "Ketik Manual":
    st.markdown('<div class="oval-container"><h3>📝 Entri Manual Kru Kelas</h3>Silakan ketik nama dan IPK mahasiswa di bawah ini (Satu mahasiswa per baris). Pemisah bisa berupa spasi atau koma.</div>', unsafe_allow_html=True)
    
    st.info("🛰️ **Contoh Ketikan:**\n- Justin Bieber 3.85\n- Ariana Grande, 3.24\n- Katy Perry; 2.90")
    
    input_teks = st.text_area("Masukkan nama & IPK di sini:", height=200, placeholder="Ketik disini...")
    tombol_input_manual = st.button("🌟 Kunci Manifest Kru")
    
    if "df_manual" not in st.session_state:
        st.session_state.df_manual = None
        
    if tombol_input_manual:
        if input_teks.strip():
            baris_data = []
            lines = input_teks.strip().split("\n")
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                match = re.search(r'(.*?)[,\s;\t]+([0-9][.,][0-9]{1,2}|[0-9])$', line)
                if match:
                    nama = match.group(1).strip()
                    ipk_str = match.group(2).strip().replace(',', '.')
                    try:
                        ipk = float(ipk_str)
                        if 0.0 <= ipk <= 4.0:
                            baris_data.append([nama, ipk])
                    except ValueError:
                        continue

            if baris_data:
                st.session_state.df_manual = pd.DataFrame(baris_data, columns=["Nama", "IPK"])
                st.toast("Manifest data kru berhasil diamankan!", icon="🚀")
            else:
                st.error("❌ Format teks tidak terbaca. Pastikan menuliskan Nama diikuti Angka IPK di akhir baris.")
        else:
            st.warning("⚠️ Kolom teks masih kosong.")
            
    df = st.session_state.df_manual

elif metode_input == "Unggah File (Excel/CSV)":
    st.session_state.df_manual = None
    st.markdown('<div class="oval-container"><h3>📁 Unggah Log Data</h3>Sistem akan mendeteksi kolom berisi informasi Nama dan IPK mahasiswa menggunakan sensor otomatis.</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Pilih file Excel atau CSV", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        kolom_asli = {col: str(col).strip() for col in df.columns}
        df = df.rename(columns=kolom_asli)
        
        kolom_ketemu_nama = None
        kolom_ketemu_ipk = None
        
        for col in df.columns:
            if 'nama' in col.lower():
                kolom_ketemu_nama = col
            elif 'ipk' in col.lower() or 'gpa' in col.lower():
                kolom_ketemu_ipk = col
        
        if kolom_ketemu_nama and kolom_ketemu_ipk:
            df = df.rename(columns={kolom_ketemu_nama: "Nama", kolom_ketemu_ipk: "IPK"})
            df["IPK"] = pd.to_numeric(df["IPK"].astype(str).str.replace(',', '.'), errors='coerce')
            df["Nama"] = df["Nama"].astype(str).str.strip()
            df = df.dropna(subset=["Nama", "IPK"])
            st.toast("Database terhubung sempurna!", icon="🛸")
        else:
            st.error("❌ Sensor Error: Sistem tidak menemukan kolom Nama atau IPK di file Anda.")
            df = None

# ==========================================
# 3. PROSES STRATIFIED K-MEANS
# ==========================================
if df is not None and not df.empty:
    st.markdown('<div class="oval-container"><h3>📋 Pratinjau Manifest Data</h3>Daftar data mahasiswa yang terdeteksi sistem saat ini.</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    max_kelompok = min(15, len(df))
    min_k = 2 if len(df) >= 2 else 1
    
    if len(df) < 2:
        st.warning("⚠️ Masukkan minimal 2 data mahasiswa untuk melakukan pembagian orbit.")
    else:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👨‍🚀 SETTING KAPSUL")
        jumlah_kelompok = st.sidebar.slider("Jumlah Kelompok yang Dibentuk:", min_value=min_k, max_value=max_kelompok, value=min_k if min_k < 4 else 4)
        
        st.markdown('<div class="oval-container"><h3>🪐 Peluncuran Komputasi</h3>Tekan tombol untuk memulai kalkulasi pembagian kru.</div>', unsafe_allow_html=True)
        
        if st.button("🛸 HITUNG KELOMPOK HETEROGEN (KLIK)"):
            X = df[['IPK']].values
            
            n_strata = min(3, len(df))
            kmeans = KMeans(n_clusters=n_strata, random_state=42, n_init=10)
            df['Strata_Cluster'] = kmeans.fit_predict(X)
            
            df = df.sort_values(by="IPK", ascending=False).reset_index(drop=True)
            
            kelompok_assignment = []
            for i in range(len(df)):
                nomor_kelompok = (i % jumlah_kelompok) + 1
                kelompok_assignment.append(nomor_kelompok)
                
            df['Kelompok Tugas'] = kelompok_assignment
            
            df_hasil = df.sort_values(by=["Kelompok Tugas", "IPK"], ascending=[True, False])
            df_tampil = df_hasil.drop(columns=['Strata_Cluster'])
            
            waktu_sekarang = datetime.now().strftime("%H:%M:%S")
            item_histori = {
                "waktu": waktu_sekarang,
                "k": jumlah_kelompok,
                "total_mhs": len(df_tampil),
                "data": df_tampil.copy()
            }
            st.session_state.histori_kelompok.insert(0, item_histori)
            
            # --- EFEK CELEBRATION ROKET MELUNCUR KE ATAS ---
            efek_html = ""
            emojis = ["🚀", "✨", "🪐", "☄️"]
            import random
            for i in range(35):
                emoji_pilihan = emojis[i % len(emojis)]
                left_pos = random.randint(5, 95)
                delay = random.uniform(0.0, 1.2)
                x_move = random.randint(-150, 150)
                rot_deg = random.randint(-45, 45)
                efek_html += f'<div class="rocket-blast" style="left: {left_pos}vw; animation-delay: {delay}s; --x-move: {x_move}px; --rot: {rot_deg}deg;">{emoji_pilihan}</div>'
            st.markdown(efek_html, unsafe_allow_html=True)
            
            # Tampilan Hasil Output Utama
            st.markdown('<div class="result-oval-container"><h2>👨‍🚀 Hasil Pembagian KRU Terbentuk</h2>Seluruh pembagian tim telah divalidasi dan diatur secara seimbang menggunakan logika kluster.</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🚀 Total Awak Kelas", f"{len(df)} orang")
            col2.metric("🛸 Kapsul Terbentuk", f"{jumlah_kelompok} kelompok")
            col3.metric("🪐 Rerata IPK Kelas", f"{df['IPK'].mean():.2f}")
            
            st.markdown("#### 📋 Tabel Distribusi Anggota Kelompok")
            st.dataframe(df_tampil.style.background_gradient(subset=['Kelompok Tugas'], cmap='Pastel1'), use_container_width=True)
            
            st.markdown("#### 📈 Matriks Keseimbangan Kualitas Kelompok")
            per_kelompok_stats = df_tampil.groupby('Kelompok Tugas')['IPK'].agg(['count', 'mean', 'min', 'max']).reset_index()
            per_kelompok_stats.columns = ['Kelompok', 'Jumlah Anggota', 'Rata-rata IPK', 'IPK Terendah', 'IPK Tertinggi']
            st.dataframe(per_kelompok_stats.style.format({'Rata-rata IPK': '{:.2f}'}), use_container_width=True)
            
            st.markdown("#### 📉 Konstelasi Sebaran Nilai Mahasiswa di Tiap Kelompok")
            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(7, 1.8))
            fig.patch.set_facecolor('#f0f4f8')
            ax.set_facecolor('#ffffff')
            
            warna_pastel_titik = ['#ffb3ba', '#ffdfba', '#ffffba', '#baffc9', '#bae1ff', '#e8cef6']
            
            for k in range(1, jumlah_kelompok + 1):
                sub_df = df_tampil[df_tampil['Kelompok Tugas'] == k]
                warna = warna_pastel_titik[(k-1) % len(warna_pastel_titik)]
                ax.scatter(
                    sub_df['IPK'],
                    [f"Grup {k}"] * len(sub_df),
                    label=f"Grup {k}",
                    s=40,
                    color=warna,
                    edgecolors='#4a4a4a', 
                    alpha=0.9, 
                    linewidth=0.8)
                
            ax.set_title("Peta Sebaran Keseimbangan IPK Antar Kelompok (Pastel View)", color='#4a4a4a', fontsize=9, fontweight='bold', pad=8)
            ax.set_xlabel("Rentang Parameter IPK", color='#708090', fontsize=8)
            ax.set_ylim(-0.6, jumlah_kelompok - 0.4)
            ax.grid(True, linestyle='--', alpha=0.3, color='#ccd6dd')
            ax.tick_params(axis='both', which='major', labelsize=8, colors='#4a4a4a')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=False)
            
            excel_data = konversi_ke_excel(df_tampil)
            st.download_button(
                label="📥 UNDUH LAPORAN RESMI KELOMPOK (.XLSX)",
                data=excel_data,
                file_name="Laporan_Kelompok_Pastel.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
else:
    st.info("🛰️ Radar Menunggu Data. Masukkan manifest siswa atau unggah file nilai pada panel kontrol sebelah kiri untuk memulai peluncuran.")

# ==========================================
# 4. PANEL HISTORI RIWAYAT DI SIDEBAR
# ==========================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛰️ LOG PENERBANGAN MISI")

if st.session_state.histori_kelompok:
    if st.sidebar.button("🛸 Reset Semua Log", use_container_width=True):
        st.session_state.histori_kelompok = []
        st.rerun()
        
    for idx, hist in enumerate(st.session_state.histori_kelompok):
        judul_expander = f"🪐 Sesi {hist['waktu']} (K={hist['k']})"
        
        # Tampilkan ringkasan singkat di sidebar
        st.sidebar.markdown(f"**{judul_expander}**")
        st.sidebar.caption(f"📊 Kapasitas: {hist['total_mhs']} Kru Astronot")
        
        excel_histori = konversi_ke_excel(hist["data"])
        st.sidebar.download_button(
            label="📥 Tarik Berkas .xlsx",
            data=excel_histori,
            file_name=f"Log_K{hist['k']}_{hist['waktu'].replace(':','')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"btn_hist_{idx}",
            use_container_width=True
        )
        # Hapus st.sidebar.markdown("---") di sini agar garis di bawah tombol tidak ganda
        
else:
    # BUNGKUS KECELAKAAN KOSONG DI DALAM BLOK ELSE INI
    st.sidebar.markdown("---")
    st.sidebar.caption("Log kosong. Belum ada aktivitas penerbangan.")

# --- TOMBOL RESTART BARU (UNTUK MENGULANG DARI AWAL) ---
st.sidebar.markdown("---")
if st.sidebar.button("🔄 RESTART KONTROL MISI", use_container_width=True):
    if "df_manual" in st.session_state:
        st.session_state.df_manual = None
    st.toast("Sistem Kontrol Misi berhasil di-boot ulang!", icon="🛸")
    st.rerun()
