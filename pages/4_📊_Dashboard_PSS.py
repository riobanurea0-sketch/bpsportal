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
    <div class="module-desc">Tinjau update progress lapangan harian dan evaluasi target berdasarkan riwayat perjalanan dinas.</div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ==========================================
# 2. BACA DATA DARI UNTITLED_2.XLSX
# ==========================================
FILE_PROGRESS = "Untitled_2.xlsx"

# Simulasi template jika file belum ada (agar error tidak muncul saat diuji coba pertama kali)
if not os.path.exists(FILE_PROGRESS):
    st.warning(f"⚠️ File referensi '{FILE_PROGRESS}' belum ditemukan di sistem. Harap pastikan karyawan telah melakukan submit data awal.")
else:
    try:
        # Membaca data submission dari karyawan
        df_progress = pd.read_excel(FILE_PROGRESS)
        
        # ==========================================
        # 3. FITUR FILTER: PERJALANAN DINAS
        # ==========================================
        st.markdown("### 🔍 Filter Pantauan")
        
        # Asumsi ada kolom bernama 'Perjalanan Dinas' atau mirip dengan itu di dalam Untitled_2.xlsx
        kolom_dinas = next((col for col in df_progress.columns if 'dinas' in col.lower() or 'perjalanan' in col.lower()), None)
        
        df_tampil = df_progress
        
        if kolom_dinas:
            daftar_dinas = ["Semua Perjalanan Dinas"] + sorted(df_progress[kolom_dinas].dropna().astype(str).unique().tolist())
            pilihan_dinas = st.selectbox("Tinjau progress berdasarkan Perjalanan Dinas:", options=daftar_dinas)
            
            if pilihan_dinas != "Semua Perjalanan Dinas":
                df_tampil = df_progress[df_progress[kolom_dinas].astype(str) == pilihan_dinas]
        else:
            st.info("ℹ️ Kolom 'Perjalanan Dinas' tidak terdeteksi di dalam file. Menampilkan semua data.")

        # ==========================================
        # 4. HIGHLIGHT METRICS (RINGKASAN PROGRESS)
        # ==========================================
        st.markdown("<br>### 📊 Ringkasan Eksekutif", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Agenda Terpantau", f"{len(df_tampil)} Kegiatan")
        with col2:
            # Mencari kolom yang berisi persentase progress (jika ada)
            kolom_persentase = next((col for col in df_tampil.columns if 'progress' in col.lower() or 'capaian' in col.lower()), None)
            if kolom_persentase and pd.api.types.is_numeric_dtype(df_tampil[kolom_persentase]):
                rata_rata = df_tampil[kolom_persentase].mean()
                st.metric("Rata-rata Progress", f"{rata_rata:.1f}%")
            else:
                st.metric("Status Pemantauan", "Aktif")
        with col3:
            st.metric("Update Terakhir", "Real-time dari Lapangan")

        # ==========================================
        # 5. TABEL UPDATE LAPANGAN & VISUALISASI
        # ==========================================
        st.markdown("<br>### 📋 Log Update Progress Lapangan", unsafe_allow_html=True)
        st.dataframe(df_tampil, use_container_width=True)
        
        # Opsional: Jika ada kolom numerik, kita bisa tampilkan grafik batang sederhana
        if kolom_persentase and pd.api.types.is_numeric_dtype(df_tampil[kolom_persentase]):
            st.markdown("<br>### 📈 Visualisasi Capaian", unsafe_allow_html=True)
            kolom_label = df_tampil.columns[0] # Ambil kolom pertama sebagai label (misal: Nama Instansi)
            
            # Membuat grafik bar chart menggunakan Plotly Express
            fig = px.bar(df_tampil, x=kolom_label, y=kolom_persentase, 
                         title="Grafik Capaian Progress per Entitas",
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
    Sistem ini memantau perubahan data secara langsung dari titik input operasional.
</div>
""", unsafe_allow_html=True)
