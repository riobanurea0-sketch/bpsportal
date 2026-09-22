import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ==========================================
# 1. KONFIGURASI HALAMAN DASAR
# ==========================================
st.set_page_config(page_title="Monitoring PSS | BPS Dairi", page_icon="📈", layout="wide")

# CSS Premium (Dark Mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #f5f5f7; }
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(at 0% 0%, hsla(210,100%,12%,0.5) 0px, transparent 50%),
                          radial-gradient(at 100% 0%, hsla(30,100%,10%,0.3) 0px, transparent 50%);
        background-attachment: fixed;
    }
    header {background-color: transparent !important;}
    .module-header { padding: 1.5rem 0 2rem 0; }
    .module-tag { font-size: 0.85rem; color: #3b82f6; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem;}
    .module-title { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #ffffff 0%, #93c5fd 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="module-header">
    <div class="module-tag">PORTAL MONITORING &middot; 06</div>
    <div class="module-title">Dashboard Pemantauan PSS.</div>
    <div class="module-desc">Tinjau update progress indikator berdasarkan kelompok data dan status target secara real-time.</div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ==========================================
# 2. BACA DATA DARI UNTITLED_2.XLSX
# ==========================================
FILE_PROGRESS = "Untitled_2.xlsx"

if not os.path.exists(FILE_PROGRESS):
    st.warning(f"⚠️ File referensi '{FILE_PROGRESS}' belum ditemukan di folder sistem. Harap upload file tersebut ke GitHub Anda.")
else:
    try:
        df_progress = pd.read_excel(FILE_PROGRESS)
        
        # ==========================================
        # 3. FITUR FILTER DROPDOWN: KELOMPOK DATA
        # ==========================================
        st.markdown("### 🔍 Filter Indikator")
        
        # Deteksi kolom Kelompok Data atau Status Target secara otomatis
        # Jika nama kolomnya berbeda, Anda bisa mengganti teks di dalam tanda kutip bawah ini
        kolom_kelompok = next((col for col in df_progress.columns if 'kelompok data' in col.lower() or 'status target' in col.lower() or 'target' in col.lower()), df_progress.columns[0])
        
        df_tampil = df_progress
        
        if kolom_kelompok:
            # Mengambil nilai unik dari kolom tersebut untuk dijadikan opsi Dropdown
            daftar_kelompok = ["Semua Kelompok Data"] + sorted(df_progress[kolom_kelompok].dropna().astype(str).unique().tolist())
            
            # Membuat Dropdown
            pilihan_kelompok = st.selectbox(
                f"Pilih {kolom_kelompok} untuk memfilter nama indikator:", 
                options=daftar_kelompok
            )
            
            # Melakukan penyaringan (filter) data berdasarkan pilihan Dropdown
            if pilihan_kelompok != "Semua Kelompok Data":
                df_tampil = df_progress[df_progress[kolom_kelompok].astype(str) == pilihan_kelompok]

        # ==========================================
        # 4. HIGHLIGHT METRICS (RINGKASAN)
        # ==========================================
        st.markdown("<br>### 📊 Ringkasan Indikator", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Indikator (Tampil)", f"{len(df_tampil)} Baris")
        with col2:
            st.metric("Kelompok Aktif", pilihan_kelompok if pilihan_kelompok != "Semua Kelompok Data" else "Semua")
        with col3:
            # Menghitung jumlah entitas unik jika ada kolom nama indikator
            kolom_indikator = next((col for col in df_tampil.columns if 'indikator' in col.lower()), None)
            if kolom_indikator:
                jumlah_unik = df_tampil[kolom_indikator].nunique()
                st.metric("Total Indikator Unik", f"{jumlah_unik} Jenis")
            else:
                st.metric("Status Data", "Tersinkronisasi")

        # ==========================================
        # 5. TABEL UPDATE & VISUALISASI
        # ==========================================
        st.markdown("<br>### 📋 Daftar Nama Indikator & Progress", unsafe_allow_html=True)
        
        # Menampilkan tabel yang sudah tersaring
        st.dataframe(df_tampil, use_container_width=True)
        
        # Opsional: Jika Anda ingin menambahkan grafik, ia akan menyesuaikan dengan filter
        kolom_numerik = df_tampil.select_dtypes(include='number').columns.tolist()
        if kolom_indikator and kolom_numerik:
            st.markdown("<br>### 📈 Visualisasi Data", unsafe_allow_html=True)
            # Menggunakan kolom numerik pertama yang tersedia untuk sumbu Y
            fig = px.bar(df_tampil, x=kolom_indikator, y=kolom_numerik[0], 
                         title=f"Grafik Berdasarkan {pilihan_kelompok}",
                         template="plotly_dark", color_discrete_sequence=['#3b82f6'])
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Gagal memuat portal monitoring: {e}")

# ==========================================
# 6. FOOTER
# ==========================================
st.markdown("<br><br><br>---", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #86868b; font-size: 0.9rem; font-weight: 300;">
    <strong>🌐 PORTAL MONITORING TERPADU</strong><br>
    Data difilter secara dinamis berdasarkan Kelompok Data dan Target Status.
</div>
""", unsafe_allow_html=True)
