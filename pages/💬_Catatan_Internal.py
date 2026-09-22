import streamlit as st
import json
import os
from datetime import datetime

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Catatan Internal | BPS Dairi", page_icon="💬", layout="wide")

# 2. Injeksi CSS Premium (Glassmorphism & Dark UI)
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
    
    /* Revisi Header agar sidebar tidak hilang */
    .stAppDeployButton {display: none;}
    header {background-color: transparent !important;}
    
    /* Header Modul */
    .module-header { padding: 1.5rem 0 2rem 0; animation: fadeIn 0.8s ease-out; }
    .module-tag { font-size: 0.85rem; color: #10b981; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; font-family: monospace;}
    .module-title { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #ffffff 0%, #a1a1a6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2; margin-bottom: 0.5rem; }
    .module-desc { color: #86868b; font-size: 0.95rem; font-weight: 300; max-width: 800px; line-height: 1.5; }
    
    /* Custom Chat/Note Card bergaya Palantir/Enterprise */
    .note-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #10b981; /* Garis aksen hijau */
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.5s ease-out;
    }
    .note-meta {
        font-family: monospace;
        color: #86868b;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
    }
    .note-msg {
        font-size: 1rem;
        color: #e5e5ea;
        line-height: 1.5;
    }
    
    @keyframes fadeIn { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:translateY(0);} }
</style>
""", unsafe_allow_html=True)

# 3. Header Modul
st.markdown("""
<div class="module-header">
    <div class="module-tag">MODUL KOMUNIKASI &middot; 04</div>
    <div class="module-title">Sistem Catatan Internal.</div>
    <div class="module-desc">Papan transmisi pesan lintas sesi. Gunakan modul ini untuk meninggalkan instruksi, pengingat, atau catatan operasional secara anonim kepada staf analitik lainnya.</div>
</div>
""", unsafe_allow_html=True)

# 4. Sistem Penyimpanan File JSON (Database Lokal)
DB_FILE = "catatan_internal.json"

def load_notes():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_note(pesan):
    notes = load_notes()
    waktu_sekarang = datetime.now().strftime("%d %b %Y - %H:%M WIB")
    # Menyimpan format data baru
    new_entry = {
        "timestamp": waktu_sekarang,
        "pesan": pesan
    }
    notes.insert(0, new_entry) # Memasukkan pesan baru di urutan paling atas
    with open(DB_FILE, "w") as file:
        json.dump(notes, file)

# 5. Desain Layout (Kiri: Form Input, Kanan: Daftar Pesan)
col_input, col_feed = st.columns([1, 2], gap="large")

with col_input:
    st.markdown("#### 📝 Transmisi Pesan Baru")
    st.caption("Pesan akan dienkripsi sebagai anonim.")
    
    # Form untuk mengirim pesan
    with st.form("form_catatan", clear_on_submit=True):
        pesan_baru = st.text_area("Tulis instruksi atau pengingat...", height=150, placeholder="Contoh: Tolong perbarui matriks Sensus Pertanian sebelum rapat hari Jumat...")
        kirim = st.form_submit_button("Kirim ke Jaringan")
        
        if kirim:
            if pesan_baru.strip() == "":
                st.warning("Transmisi gagal: Pesan tidak boleh kosong.")
            else:
                save_note(pesan_baru)
                st.success("Transmisi berhasil disimpan.")
                st.rerun() # Merefresh halaman agar pesan langsung muncul

with col_feed:
    st.markdown("#### 📡 Log Catatan Operasional")
    
    # Memuat dan menampilkan pesan dari file JSON
    catatan = load_notes()
    
    if len(catatan) == 0:
        st.info("Log komunikasi masih kosong. Belum ada aktivitas transmisi.")
    else:
        # Menampilkan pesan dalam bentuk "Glass Card"
        for note in catatan:
            st.markdown(f"""
            <div class="note-card">
                <div class="note-meta">
                    <span>ID: ANONIM</span>
                    <span>{note['timestamp']}</span>
                </div>
                <div class="note-msg">{note['pesan']}</div>
            </div>
            """, unsafe_allow_html=True)