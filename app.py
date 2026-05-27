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
# PROGRAM UTAMA (STREAMLIT UI)
# ==========================================
st.set_page_config(page_title="FreshMart Express", layout="wide")

# --- CUSTOM CSS: TEMA LUXURY FRESH GRADIENT (SANGAT INTERAKTIF) ---
custom_css = """
<style>
    /* 1. Latar Belakang Utama dengan Gradasi Estetik */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 50%, #f8fafc 100%) !important;
    }
    
    /* 2. Sidebar Dibuat Kontras Tinggi & Profesional */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important; /* Biru Gelap/Midnight Navy */
        border-right: 2px solid #e2e8f0 !important;
    }
    
    /* Teks di Dalam Sidebar Jadi Putih Cerah */
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    
    /* Radio Button Menu di Sidebar saat Aktif */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.05);
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 5px;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(16, 185, 129, 0.2) !important; /* Efek Hijau saat Disorot */
    }
    
    /* 3. Pewarnaan Teks Halaman Utama */
    h1, h2, h3, h4, h5, h6, .stText {
        color: #0f172a !important;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif !important;
        font-weight: 700 !important;
    }
    p, span, div {
        color: #334155 !important;
    }
    
    /* 4. Mempercantik Kotak Kontainer (Clean Box) dengan Glassmorphism Tipis */
    .clean-box {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-left: 6px solid #10b981 !important; /* Aksen Hijau Segar */
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* 5. Mengubah Tampilan Angka Statistik (Metric Widget) agar Mencolok */
    [data-testid="stMetricValue"] {
        color: #047857 !important; /* Hijau Tua Mewah */
        font-size: 36px !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* 6. Tombol Utama (Primary Button) Jadi Lebih Keren */
    button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* 7. Input Form & Text Area */
    textarea, input {
        color: #0f172a !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    
    /* 8. Desain Nota / Struk Kasir Estetik */
    .struk-container {
        background-color: #fffdf0 !important; /* Warna kertas kasir premium */
        color: #111111 !important;
        font-family: 'Courier New', Courier, monospace !important;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 15px auto;
        border: 2px dashed #a7f3d0;
    }
    .struk-container pre {
        background-color: transparent !important;
        color: #111111 !important
