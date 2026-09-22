import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & CSS Premium
st.set_page_config(page_title="Sensus Pertanian | BPS Dairi", page_icon="🌾", layout="wide")

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
    .module-tag { font-size: 0.85rem; color: #10b981; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; font-family: monospace;}
    .module-title { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #ffffff 0%, #a1a1a6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; margin-bottom: 0.5rem; }
    .module-desc { color: #86868b; font-size: 0.95rem; font-weight: 300; max-width: 800px; line-height: 1.5; }
    @keyframes fadeIn { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:translateY(0);} }
</style>
""", unsafe_allow_html=True)

# 2. Header Modul
st.markdown("""
<div class="module-header">
    <div class="module-tag">MODUL ANALITIK &middot; 03</div>
    <div class="module-title">Sensus Pertanian & Pangan.</div>
    <div class="module-desc">Pusat analisis data komoditas, luas panen, dan perikanan. Tumpuk beberapa dataset untuk analisis tren komprehensif.</div>
</div>
""", unsafe_allow_html=True)

# 3. Inisialisasi Memori (Sektor Pertanian)
if 'history_pertanian' not in st.session_state:
    st.session_state['history_pertanian'] = {}

# 4. Engine Pemroses Data & Manajemen Histori File
col_upload, col_analisis = st.columns([1, 2], gap="large")

with col_upload:
    st.markdown("#### 📥 Injeksi Dataset")
    file_sensus = st.file_uploader("Unggah berkas Pertanian (CSV/XLSX)", type=["csv", "xlsx", "xls"], accept_multiple_files=True, key="upload_pertanian")
    
    if file_sensus:
        with st.spinner('Menyuntikkan matriks data...'):
            for f in file_sensus:
                if f.name not in st.session_state['history_pertanian']:
                    try:
                        if f.name.endswith('.csv'):
                            df_temp = pd.read_csv(f)
                        else:
                            df_temp = pd.read_excel(f)
                        st.session_state['history_pertanian'][f.name] = df_temp
                    except Exception as e:
                        st.error(f"Gagal membaca {f.name}: {e}")

    st.markdown("---")
    st.markdown("#### 📂 Histori Berkas Aktif")
    st.caption("Berkas di bawah ini sedang ditumpuk (digabungkan).")
    
    if len(st.session_state['history_pertanian']) == 0:
        st.info("Belum ada berkas di memori.")
    else:
        for nama_file in list(st.session_state['history_pertanian'].keys()):
            col_nama, col_hapus = st.columns([4, 1])
            col_nama.write(f"📄 `{nama_file}`")
            if col_hapus.button("❌", key=f"del_tani_{nama_file}"):
                del st.session_state['history_pertanian'][nama_file]
                st.rerun()

with col_analisis:
    if len(st.session_state['history_pertanian']) > 0:
        df = pd.concat(st.session_state['history_pertanian'].values(), ignore_index=True)
        st.session_state['data_pertanian'] = df # Simpan untuk dibaca panel Global
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Baris Gabungan", f"{df.shape[0]:,}")
        col_m2.metric("Total File Tersimpan", f"{len(st.session_state['history_pertanian'])}")
        status_integritas = "Optimal" if df.isnull().sum().sum() == 0 else f"{df.isnull().sum().sum()} Blank"
        col_m3.metric("Integritas Matriks", status_integritas)
        
        tab1, tab2 = st.tabs(["📊 Panel Visualisasi", "📑 Inspeksi Data Gabungan"])
        with tab1:
            col_cfg, col_chart = st.columns([1, 2])
            kolom_angka = df.select_dtypes(include=['number']).columns.tolist()
            kolom_kategori = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            with col_cfg:
                if len(kolom_kategori) > 0 and len(kolom_angka) > 0:
                    sumbu_x = st.selectbox("X Axis (Kategori)", kolom_kategori, key="x_pertanian")
                    sumbu_y = st.selectbox("Y Axis (Angka)", kolom_angka, key="y_pertanian")
                    jenis_grafik = st.radio("Tipe Render", ["Bar Chart", "Line Chart", "Area Chart"], key="chart_pertanian")
                else:
                    st.warning("Struktur tidak mendukung grafik.")
                    sumbu_x, sumbu_y = None, None
            
            with col_chart:
                if sumbu_x and sumbu_y:
                    df_grouped = df.groupby(sumbu_x)[sumbu_y].sum().reset_index()
                    if jenis_grafik == "Bar Chart":
                        st.bar_chart(data=df_grouped, x=sumbu_x, y=sumbu_y, use_container_width=True)
                    elif jenis_grafik == "Line Chart":
                        st.line_chart(data=df_grouped, x=sumbu_x, y=sumbu_y, use_container_width=True)
                    else:
                        st.area_chart(data=df_grouped, x=sumbu_x, y=sumbu_y, use_container_width=True)

        with tab2:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.session_state['data_pertanian'] = None
        st.info("Sistem dalam mode siaga. Silakan injeksi matriks data dari panel kiri.")

# ==========================================
# FITUR OVERVIEW GLOBAL LINTAS SEKTORAL
# ==========================================
st.markdown("<br><hr style='opacity: 0.2'>", unsafe_allow_html=True)
with st.expander("🌐 OVERVIEW SISTEM: Statistik Lintas Sektoral"):
    st.markdown("#### Agregasi Data Aktif di Memori Sistem")
    
    total_baris = 0
    total_kolom = 0
    dataset_aktif = {}
    
    if 'data_ekonomi' in st.session_state and st.session_state['data_ekonomi'] is not None:
        dataset_aktif['Sektor Ekonomi'] = st.session_state['data_ekonomi']
    if 'data_penduduk' in st.session_state and st.session_state['data_penduduk'] is not None:
        dataset_aktif['Sektor Penduduk'] = st.session_state['data_penduduk']
    if 'data_pertanian' in st.session_state and st.session_state['data_pertanian'] is not None:
        dataset_aktif['Sektor Pertanian'] = st.session_state['data_pertanian']
        
    if len(dataset_aktif) == 0:
        st.info("Sistem belum mendeteksi matriks data apa pun.")
    else:
        for nama_modul, df_modul in dataset_aktif.items():
            total_baris += df_modul.shape[0]
            total_kolom += df_modul.shape[1]
            
        col_g1, col_g2, col_g3 = st.columns(3)
        col_g1.metric("Modul Aktif", f"{len(dataset_aktif)} / 3 Sektor", delta="Online")
        col_g2.metric("Total Volume Gabungan (Baris)", f"{total_baris:,}")
        col_g3.metric("Total Dimensi Gabungan (Kolom)", f"{total_kolom:,}")
        
        st.markdown("---")
        tabs_global = st.tabs(list(dataset_aktif.keys()))
        for index_tab, (nama_modul, df_modul) in enumerate(dataset_aktif.items()):
            with tabs_global[index_tab]:
                st.markdown(f"**Status:** `{df_modul.shape[0]:,} Baris` x `{df_modul.shape[1]:,} Kolom`")
                st.dataframe(df_modul.head(3), use_container_width=True)
                kolom_numerik = df_modul.select_dtypes(include=['number']).columns.tolist()
                if len(kolom_numerik) > 0:
                    st.caption(f"📊 Rata-rata (Mean) pada {nama_modul}:")
                    st.dataframe(df_modul[kolom_numerik].mean().to_frame(name='Mean').T, use_container_width=True, hide_index=True)