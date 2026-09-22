import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. KONFIGURASI HALAMAN DASAR
# ==========================================
st.set_page_config(page_title="Dashboard PSS | BPS Dairi", page_icon="📊", layout="wide")

# ==========================================
# 2. INJEKSI CSS PREMIUM (TEMA GELAP)
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
            radial-gradient(at 0% 0%, hsla(210,100%,12%,0.5) 0px, transparent 50%),
            radial-gradient(at 100% 0%, hsla(30,100%,10%,0.3) 0px, transparent 50%);
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
        color: #3b82f6; 
        font-weight: 500; 
        letter-spacing: 0.1em; 
        text-transform: uppercase; 
        margin-bottom: 0.5rem; 
        font-family: monospace;
    }
    
    .module-title { 
        font-size: 2.2rem; 
        font-weight: 700; 
        background: linear-gradient(135deg, #ffffff 0%, #93c5fd 100%); 
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
# 3. HEADER MODUL 6
# ==========================================
st.markdown("""
<div class="module-header">
    <div class="module-tag">MODUL SEKTORAL &middot; 06</div>
    <div class="module-title">Dashboard PSS 2026.</div>
    <div class="module-desc">Pusat evaluasi dan pemantauan target indikator Pemantauan Statistik Sektoral (PSS) untuk instansi daerah secara real-time.</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# 4. LOGIKA UPLOAD & PENYIMPANAN FISIK PERMANEN
# ==========================================
st.markdown("### 📥 Inisiasi Data Sektoral")

# Menentukan nama file yang akan disimpan di folder Anda
FILE_PERMANEN = "database_pss_aktif.xlsx"

file_unggahan = st.file_uploader("Unggah arsip indikator (Format: .xlsx)", type=["xlsx"])

# Menyimpan file ke sistem komputer (kebal refresh)
if file_unggahan is not None:
    with open(FILE_PERMANEN, "wb") as f:
        f.write(file_unggahan.getbuffer())
    st.success("✅ Modul berhasil diinisiasi. Data tersimpan permanen di sistem lokal!")

# ==========================================
# 5. TAMPILAN DASHBOARD (BACA DARI FILE FISIK)
# ==========================================
if os.path.exists(FILE_PERMANEN):
    try:
        df = pd.read_excel(FILE_PERMANEN)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Ringkasan Indikator Sektoral")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Baris Data", value=f"{len(df)} Entri")
        with col2:
            st.metric(label="Total Atribut/Kolom", value=f"{len(df.columns)} Atribut")
        with col3:
            if len(df.columns) > 0:
                st.metric(label="Parameter Utama", value=str(df.columns[0]))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("**Tinjauan Matriks Data (Preview 15 Baris Pertama):**")
        st.dataframe(df.head(15), use_container_width=True)
        
    except Exception as e:
        st.error(f"Gagal membaca file sistem: {e}")
else:
    st.info("⚠️ Menunggu unggahan dokumen. Silakan unggah file Excel Anda pada panel di atas untuk merender dashboard.")

# ==========================================
# 6. FOOTER: OVERVIEW SISTEM
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #86868b; font-size: 0.9rem; font-weight: 300;">
    <strong>🌐 OVERVIEW SISTEM: Statistik Lintas Sektoral</strong><br>
    Modul ini terintegrasi langsung dengan arsitektur data instansi. Pastikan kerahasiaan dan integritas data operasional terjaga dengan baik.
</div>
""", unsafe_allow_html=True)