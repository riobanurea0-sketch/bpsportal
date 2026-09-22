import streamlit as st
import os
from datetime import datetime

# 1. Konfigurasi Halaman & Inisiasi Folder Penyimpanan
st.set_page_config(page_title="Repositori Survei | BPS Dairi", page_icon="📋", layout="wide")

# Membuat folder 'arsip_survei' sebagai brankas penyimpanan file fisik
DIR_ARSIP = "arsip_survei"
os.makedirs(DIR_ARSIP, exist_ok=True)

# 2. Injeksi CSS Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #f5f5f7; }
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 0% 0%, hsla(210,100%,12%,0.5) 0px, transparent 50%),
            radial-gradient(at 100% 0%, hsla(30,100%,10%,0.3) 0px, transparent 50%);
        background-attachment: fixed;
    }
    .stAppDeployButton {display: none;}
    header {background-color: transparent !important;}
    
    .module-header { padding: 1.5rem 0 2rem 0; animation: fadeIn 0.8s ease-out; }
    .module-tag { font-size: 0.85rem; color: #a855f7; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; font-family: monospace;}
    .module-title { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #ffffff 0%, #a1a1a6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; margin-bottom: 0.5rem; }
    .module-desc { color: #86868b; font-size: 0.95rem; font-weight: 300; max-width: 800px; line-height: 1.5; }
    
    @keyframes fadeIn { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:translateY(0);} }
</style>
""", unsafe_allow_html=True)

# 3. Header Modul
st.markdown("""
<div class="module-header">
    <div class="module-tag">MODUL OPERASIONAL &middot; 05</div>
    <div class="module-title">Repositori Data Bersama.</div>
    <div class="module-desc">Pusat distribusi dan pengarsipan file internal. Unggah berkas hasil survei lapangan, dokumen metodologi, atau laporan sektoral agar dapat diakses, ditinjau, dan diunduh oleh seluruh staf dalam jaringan.</div>
</div>
""", unsafe_allow_html=True)

def format_ukuran(ukuran_bytes):
    if ukuran_bytes < 1024:
        return f"{ukuran_bytes} B"
    elif ukuran_bytes < 1024 * 1024:
        return f"{ukuran_bytes / 1024:.1f} KB"
    else:
        return f"{ukuran_bytes / (1024 * 1024):.2f} MB"

# 4. Mekanisme Upload File
st.markdown("#### 📤 Transmisi Berkas Baru")
file_unggah = st.file_uploader("Pilih satu atau beberapa berkas (CSV, Excel, PDF, ZIP, dll) untuk diunggah ke repositori.", accept_multiple_files=True)

if file_unggah:
    with st.spinner("Mengenkripsi dan memindahkan berkas ke repositori server..."):
        berhasil = 0
        for f in file_unggah:
            file_path = os.path.join(DIR_ARSIP, f.name)
            with open(file_path, "wb") as out_file:
                out_file.write(f.read())
            berhasil += 1
        
        st.success(f"Transmisi Selesai: {berhasil} berkas berhasil diamankan di repositori.")
        st.rerun()

st.markdown("---")

# 5. Explorer: Daftar File, Unduh, dan Hapus
st.markdown("#### 🗄️ Indeks Berkas Tersimpan")

daftar_file = os.listdir(DIR_ARSIP)

if len(daftar_file) == 0:
    st.info("Repositori saat ini kosong. Menunggu transmisi berkas dari staf.")
else:
    # Membagi header menjadi 5 kolom untuk memberi ruang pada tombol hapus
    col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns([3, 2, 1, 1, 1])
    col_h1.caption("NAMA BERKAS")
    col_h2.caption("WAKTU UNGGAH")
    col_h3.caption("UKURAN")
    col_h4.caption("TINDAKAN")
    col_h5.caption("KONTROL")
    
    st.markdown("<hr style='margin-top: 0; margin-bottom: 1rem; opacity: 0.2'>", unsafe_allow_html=True)
    
    for nama_file in sorted(daftar_file):
        file_path = os.path.join(DIR_ARSIP, nama_file)
        
        ukuran_file = os.path.getsize(file_path)
        waktu_modifikasi = os.path.getmtime(file_path)
        waktu_format = datetime.fromtimestamp(waktu_modifikasi).strftime('%d %b %Y, %H:%M')
        
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**📄 {nama_file}**")
        with col2:
            st.markdown(f"<span style='color: #86868b; font-family: monospace;'>{waktu_format}</span>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<span style='color: #86868b;'>{format_ukuran(ukuran_file)}</span>", unsafe_allow_html=True)
        with col4:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Unduh",
                    data=f,
                    file_name=nama_file,
                    key=f"dl_{nama_file}",
                    use_container_width=True
                )
        with col5:
            # Tombol hapus yang akan memicu penghapusan file di server
            if st.button("❌ Hapus", key=f"del_repo_{nama_file}", use_container_width=True):
                try:
                    os.remove(file_path)
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menghapus: {e}")
        
        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)