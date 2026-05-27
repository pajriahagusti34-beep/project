import streamlit as st
import random

# ==========================================
# KELAS NODE PELANGGAN & ANTRIAN (QUEUE)
# ==========================================
class PelangganNode:
    def __init__(self, nama, list_belanjaan, total_harga):
        self.nama = nama
        self.list_belanjaan = list_belanjaan  
        self.total_harga = total_harga        
        self.next = None

class QueueSupermarket:
    def __init__(self):
        self.head = None
        self.tail = None
        self.total_pelanggan_dilayani = 0

    def is_empty(self):
        return self.head is None

    def tambah_pelanggan(self, nama, list_belanjaan, total_harga):
        baru = PelangganNode(nama, list_belanjaan, total_harga)
        if self.is_empty():
            self.head = baru
            self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru

    def layani_pelanggan(self):
        if self.is_empty():
            return None
        pelanggan_dilayani = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.total_pelanggan_dilayani += 1
        return pelanggan_dilayani

    def dapatkan_antrean_string(self):
        if self.is_empty():
            return "Antrean Kosong"
        hasil = ""
        sekarang = self.head
        nomor = 1
        while sekarang:
            jumlah_item = len(sekarang.list_belanjaan)
            hasil += f"[{nomor}] {sekarang.nama} ({jumlah_item} Item Barang)\n"
            sekarang = sekarang.next
            nomor += 1
        return hasil

# ==========================================
# PROGRAM UTAMA (STREAMLIT UI LUXURY THEME)
# ==========================================
st.set_page_config(page_title="FreshMart Express", layout="wide")

# --- ULTRA PREMIUM UI CUSTOM CSS WITH ADVANCED SIDEBAR NAVIGATION ---
custom_css = """
<style>
    /* 1. Latar Belakang Utama dengan Gradasi Mewah (Soft Mint to Sky Blue) */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 50%, #f5f7fa 100%) !important;
    }
    
    /* 2. Sidebar Bergaya Dark Premium (Deep Navy) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 3px solid #10b981 !important;
    }
    
    /* Teks dan Label di dalam Sidebar */
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
    }

    /* 3. DESAIN KUSTOM TOMBOL MENU SIDEBAR */
    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 2px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        width: 100% !important;
    }

    /* Efek Hover: Saat Menu Disorot Kursor */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        transform: translateX(4px);
    }

    /* Efek Aktif: Saat Menu Dipilih/Diklik */
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(13, 148, 136, 0.25) 0%, rgba(16, 185, 129, 0.15) 100%) !important;
        border-left: 5px solid #10b981 !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    /* Sembunyikan lingkaran radio asli agar terlihat seperti tombol navigasi kustom */
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p::before {
        content: "";
    }
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetRadioDot"] {
        display: none !important;
    }
    
    /* 4. Desain Kustom Judul Utama */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        background: linear-gradient(45deg, #0f172a, #0d9488);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    /* 5. Kotak Kontainer Bergaya Glassmorphism */
    .clean-box {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-left: 6px solid #0d9488 !important;
        border-radius: 20px !important;
        padding: 26px !important;
        margin-bottom: 22px !important;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08) !important;
    }

    /* Kotak Kosong Khusus Kuburan Biar Ramai */
    .empty-graveyard-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        border: 2px dashed #cbd5e1 !important;
        border-radius: 20px !important;
        padding: 40px 20px !important;
        text-align: center;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    
    /* 6. Mengubah Tampilan Card Statistik */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(13, 148, 136, 0.1) !important;
        border: 1px solid rgba(13, 148, 136, 0.15) !important;
        border-top: 4px solid #0d9488 !important;
    }
    [data-testid="stMetricValue"] {
        color: #0d9488 !important;
        font-size: 40px !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-size: 12px !important;
    }
    
    /* 7. Desain Tombol Interaktif Premium */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0d9488 0%, #115e59 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 20px rgba(13, 148, 136, 0.4) !important;
    }

    /* Tombol Keluar Sistem */
    button[kind="secondary"] {
        background: rgba(239, 68, 68, 0.1) !important;
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        background: #ef4444 !important;
        color: white !important;
    }
    
    textarea, input {
        color: #0f172a !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# CSS KHUSUS UNTUK STRUK KASIR (DIMASUKKAN DALAM IFRAME)
html_struk_style = """
<style>
    .struk-container {
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        padding: 25px 20px;
        border-radius: 12px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        max-width: 330px;
        margin: 10px auto;
        border-top: 6px dashed #cbd5e1;
        border-bottom: 6px dashed #cbd5e1;
    }
    .struk-header { text-align: center; margin-bottom: 15px; }
    .struk-title { font-size: 18px !important; font-weight: bold !important; margin: 0 !important; color: #0f172a !important; }
    .struk-subtitle { font-size: 11px !important; color: #64748b !important; margin: 0 !important; }
    .struk-meta { font-size: 13px !important; margin-bottom: 12px; }
    .struk-divider { border-top: 1px dashed #94a3b8; margin: 8px 0; }
    .struk-item-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
    .struk-item-name { flex: 1; text-align: left; }
    .struk-item-price { text-align: right; font-weight: bold; }
    .struk-footer { text-align: center; margin-top: 25px; font-size: 12px !important; color: #64748b !important; }
</style>
"""

# --- INITIALIZATION TRANSAKSI ---
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []
if 'struk_terakhir' not in st.session_state:
    st.
