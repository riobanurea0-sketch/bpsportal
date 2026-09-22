import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. KONFIGURASI HALAMAN DASAR
# ==========================================
st.set_page_config(page_title="Perjalanan Dinas | BPS Dairi", page_icon="🚗", layout="wide")

# ==========================================
# 2. INJEKSI CSS PREMIUM (TEMA GELAP - AKSEN HIJAU EMERALD)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        color: #f5f5f7; 
    }
    
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 0% 0%, hsla(150,100%,10%,0.4) 0px, transparent 50%),
            radial-gradient(at 100% 0%, hsla(210,100%,12%,0.4) 0px, transparent 50%);
        background-attachment: fixed;
    }
    
    .stAppDeployButton {display: none;}
    header {background-color: transparent !important;}
    
    .module-header { 
        padding: 1.5rem 0 2rem 0; 
        animation: fadeIn 0.8s ease-out; 
    }
    
    .module-tag { 
        font-size: 0.85rem; 
        color: #10b981; 
        font-weight: 500; 
        letter-spacing: 0.1em; 
        text-transform: uppercase; 
        margin-bottom: 0.5rem; 
        font-family: monospace;
    }
    
    .module-title { 
        font-size: 2.2rem; 
        font-weight: 700; 
        background: linear-gradient(135deg, #ffffff 0%, #6ee7b7 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        line-height: 1.2; 
        margin-bottom: 0.5rem; 
    }
    
    .module-desc { 
        color: #86868b; 
        font-size: 0.95rem; 
        font-weight: 300; 
        max-width: 800px; 
        line-height: 1.5; 
    }
    
    @keyframes fadeIn { 
        from {opacity:0; transform:translateY(10px);} 
        to {opacity:1; transform:translateY(0);} 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER MODUL 7
# ==========================================
st.markdown("""
<div class="module-header">
    <div class="module-tag">MODUL OPERASIONAL LAPANGAN &middot; 07</div>
    <div class="module-title">Kendali Perjalanan Dinas & SPPD.</div>
    <div class="module-desc">Pusat kontrol logistik penugasan pegawai, penyuntingan data langsung (Editable), serta manajemen dokumen perjalanan dinas.</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# 4. LOGIKA UPLOAD & INISIASI FILE FISIK
# ==========================================
st.markdown("### 📥 Manajemen Database & Impor Berkas")

FILE_DINAS_PERMANEN = "database_dinas_aktif.xlsx"

# Jika file belum ada sama sekali, buatkan template data awal secara otomatis agar tabel langsung muncul
if not os.path.exists(FILE_DINAS_PERMANEN):
    template_awal = pd.DataFrame({
        "Nama Pegawai": ["Budi Santoso, SST", "Siti Rahma, M.Si"],
        "Tujuan": ["Kec. Sidikalang", "Kec. Sumbul"],
        "Keperluan": ["Pendataan Sensus Ekonomi", "Verifikasi Lapangan UMK"],
        "Tanggal Berangkat": ["2026-04-01", "2026-04-03"],
        "Status": ["Dijadwalkan", "Berlangsung"]
    })
    template_awal.to_excel(FILE_DINAS_PERMANEN, index=False)

# Opsi unggah file baru untuk menimpa database
file_unggahan_dinas = st.file_uploader("Unggah database SPPD baru (.xlsx) jika ingin mengganti total data:", type=["xlsx"], key="uploader_dinas")

if file_unggahan_dinas is not None:
    df_baru = pd.read_excel(file_unggahan_dinas)
    df_baru.to_excel(FILE_DINAS_PERMANEN, index=False)
    st.success("✅ Database berhasil diganti dengan file baru yang diunggah!")
    st.rerun()

# ==========================================
# 5. FITUR EDITOR DATA INTERAKTIF
# ==========================================
if os.path.exists(FILE_DINAS_PERMANEN):
    try:
        df_dinas = pd.read_excel(FILE_DINAS_PERMANEN)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ✏️ Lembar Kerja & Editor Data Langsung")
        st.info("💡 **Tips:** Anda bisa langsung mengklik sel di tabel bawah untuk **mengedit teks**, menambah baris baru (ikon `+`), atau menghapus baris. Jangan lupa klik tombol **Simpan Perubahan** di bawah setelah selesai.")

        # Komponen Tabel Interaktif yang bisa diedit (Editable Table)
        df_hasil_edit = st.data_editor(
            df_dinas, 
            num_rows="dynamic", 
            use_container_width=True, 
            key="editor_tabel_dinas"
        )

        # Tombol untuk menyimpan perubahan hasil edit ke file fisik permanen
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Simpan Perubahan Data ke Sistem", type="primary"):
            df_hasil_edit.to_excel(FILE_DINAS_PERMANEN, index=False)
            st.success("🎉 Perubahan data berhasil disimpan secara permanen dan aman dari refresh!")
            st.rerun()

        # Tombol Unduh Laporan
        st.markdown("<hr>", unsafe_allow_html=True)
        csv_data = df_hasil_edit.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Data SPPD Terbaru (CSV)",
            data=csv_data,
            file_name="rekap_perjalanan_dinas_terbaru.csv",
            mime="text/csv",
        )
        
    except Exception as e:
        st.error(f"Gagal memproses sistem editor dinas: {e}")

# ==========================================
# 6. FOOTER
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #86868b; font-size: 0.9rem; font-weight: 300;">
    <strong>🚗 MODUL OPERASIONAL: Kendali Perjalanan Dinas Terpadu</strong><br>
    Sistem manajemen khusus penugasan lapangan dengan dukungan editor data interaktif.
</div>
""", unsafe_allow_html=True)