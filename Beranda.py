import streamlit as st

# Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="Internal | BPS Dairi", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INJEKSI CSS MODERN (ENTERPRISE / GLASSMORPHISM STYLE)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #f5f5f7;
    }

/* Menyembunyikan tombol 'Deploy' di kanan atas, tapi membiarkan tombol Sidebar tetap ada */
    .stAppDeployButton {display: none;}
    header {background-color: transparent !important;}
    footer {visibility: hidden;}

    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 0% 0%, hsla(210,100%,12%,0.5) 0px, transparent 50%),
            radial-gradient(at 100% 0%, hsla(30,100%,10%,0.3) 0px, transparent 50%),
            radial-gradient(at 100% 100%, hsla(210,100%,8%,0.6) 0px, transparent 50%);
        background-attachment: fixed;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-wrapper {
        text-align: center;
        padding: 5rem 1rem 2rem 1rem;
        animation: fadeIn 1s ease-out;
    }
    
    .hero-tag {
        font-size: 0.85rem;
        font-weight: 500;
        color: #f39200;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #a1a1a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        color: #86868b;
        letter-spacing: 0em;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .glass-container {
        display: flex;
        gap: 1.5rem;
        margin-top: 4rem;
        justify-content: center;
        flex-wrap: wrap;
        animation: fadeIn 1.2s ease-out;
    }
    
    .glass-card {
        flex: 1;
        min-width: 280px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: background 0.2s ease;
        text-align: left;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .card-icon {
        font-size: 2rem;
        margin-bottom: 1.2rem;
        opacity: 0.9;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 0.6rem;
    }

    .card-desc {
        font-size: 0.9rem;
        color: #a1a1a6;
        line-height: 1.5;
        font-weight: 300;
    }

    .cta-container {
        text-align: center;
        margin-top: 5rem;
        margin-bottom: 3rem;
        animation: fadeIn 1.5s ease-out;
    }
    
    .cta-badge {
        display: inline-block;
        padding: 10px 24px;
        background: rgba(255,255,255,0.04);
        border-radius: 6px;
        font-size: 0.85rem;
        color: #86868b;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08);
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# KONTEN HTML (STRUKTUR HALAMAN)
# ==========================================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-tag">Internal Dashboard &middot; BPS Kab. Dairi (1211)</div>
    <div class="hero-title">Sistem Analisis Sektoral.</div>
    <div class="hero-subtitle">
        Pusat pengolahan dan visualisasi data statistik terintegrasi untuk kebutuhan pemantauan internal dan evaluasi lintas sektor.
    </div>
</div>

<div class="glass-container">
    <div class="glass-card">
        <div class="card-icon">🌾</div>
        <div class="card-title">Sektor Pertanian</div>
        <div class="card-desc">Pemantauan indikator strategis, fluktuasi komoditas unggulan daerah, dan agregat Nilai Tukar Petani.</div>
    </div>
    <div class="glass-card">
        <div class="card-icon">👥</div>
        <div class="card-title">Sektor Demografi</div>
        <div class="card-desc">Analisis dinamika kependudukan, struktur ketenagakerjaan, dan metrik Indeks Pembangunan Manusia.</div>
    </div>
    <div class="glass-card">
        <div class="card-icon">🏢</div>
        <div class="card-title">Sektor Ekonomi</div>
        <div class="card-desc">Evaluasi pertumbuhan PDRB, tingkat inflasi, serta agregat pergerakan unit usaha lokal.</div>
    </div>
</div>

<div class="cta-container">
        > Navigasi melalui menu sidebar untuk inisiasi modul analitik
    </div>
</div>
""", unsafe_allow_html=True)