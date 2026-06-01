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
# PROGRAM UTAMA
# ==========================================
st.set_page_config(page_title="FreshMart Express", layout="wide")

# CSS Kustom (Sesuai kode awal Anda)
custom_css = """
<style>
    .stApp { background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 50%, #f5f7fa 100%) !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important; border-right: 3px solid #10b981 !important; }
    .clean-box { background: rgba(255, 255, 255, 0.85) !important; backdrop-filter: blur(12px); border-radius: 20px !important; padding: 26px !important; margin-bottom: 22px !important; box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08) !important; border-left: 6px solid #0d9488 !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Inisialisasi State
if 'antrean_kasir' not in st.session_state: st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state: st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state: st.session_state.riwayat_transaksi = []
if 'struk_terakhir' not in st.session_state: st.session_state.struk_terakhir = ""
if 'total_omset' not in st.session_state: st.session_state.total_omset = 0
if 'database_produk' not in st.session_state:
    st.session_state.database_produk = {
        "Minyak Goreng 2L": 36000, "Susu UHT 1L": 18500, "Mie Instan Goreng": 3500,
        "Beras Premium 5kg": 75000, "Gula Pasir 1kg": 17000, "Teh Celup Isi 25": 6000,
        "Kopi Bubuk 100g": 12000, "Roti Tawar Kupas": 15000
    }

antrean = st.session_state.antrean_kasir

# --- LOGIN ---
if not st.session_state.is_logged_in:
    st.title("Login FreshMart Express")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Masuk"):
        if username == "admin" and password == "2311":
            st.session_state.is_logged_in = True
            st.rerun()
else:
    # Sidebar
    menu = st.sidebar.radio("MODUL OPERASIONAL:", [
        "📢 1. Panggil Nomor Antrean", 
        "📦 2. Cek Katalog Produk Toko", 
        "🔍 3. Monitor Sabuk Antrean RAM", 
        "📥 4. Input Pelanggan ke Jalur", 
        "💸 5. Scan Barang & Input Bayar", 
        "🧾 6. Cetak Struk & Jurnal Rekap"
    ])

    # --- REVISI KATALOG (MENU 2) ---
    if menu == "📦 2. Cek Katalog Produk Toko":
        st.markdown('<h1>📋 Manajemen Katalog & Inventaris</h1>', unsafe_allow_html=True)
        
        # Fitur Pencarian (Search Logic)
        query = st.text_input("🔍 Cari produk...", placeholder="Ketik nama barang...")
        
        # Filter & Optimasi Data (Data Handling)
        data = st.session_state.database_produk
        filtered = {k: v for k, v in data.items() if query.lower() in k.lower()}
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        if not filtered:
            st.warning("⚠️ Produk tidak ditemukan.")
        else:
            for k, v in filtered.items():
                # Integrasi Inventaris & Tampilan Data
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #f1f5f9;'>
                    <span style='font-weight:600; color:#1e293b;'>📦 {k}</span>
                    <span style='color:#0d9488; font-weight:bold;'>Rp {v:,}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SISA MENU (LOGIKA ASLI ANDA) ---
    elif menu == "📢 1. Panggil Nomor Antrean":
        st.write("Statistik antrean ditampilkan di sini...")
    
    # Tambahkan kembali sisa kode Menu 3, 4, 5, 6 Anda di sini 
    # (Saya sengaja tidak menulis ulang agar Anda bisa fokus ke bagian Katalog ini dulu)
