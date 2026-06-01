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

# [CSS Styles tetap sama agar UI tetap cantik]
custom_css = """
<style>
    .stApp { background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 50%, #f5f7fa 100%) !important; }
    .clean-box { background: rgba(255, 255, 255, 0.85) !important; backdrop-filter: blur(12px); border-radius: 20px !important; padding: 26px !important; margin-bottom: 22px !important; box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.08) !important; border-left: 6px solid #0d9488 !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'antrean_kasir' not in st.session_state: st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state: st.session_state.is_logged_in = False
if 'database_produk' not in st.session_state:
    st.session_state.database_produk = {
        "Minyak Goreng 2L": 36000, "Susu UHT 1L": 18500, "Mie Instan Goreng": 3500,
        "Beras Premium 5kg": 75000, "Gula Pasir 1kg": 17000, "Teh Celup Isi 25": 6000
    }

# --- LOGIN ---
if not st.session_state.is_logged_in:
    # ... (Kode login tetap sama) ...
    pass 
else:
    menu = st.sidebar.radio("PILIH MODUL:", ["1. Antrean", "2. Katalog", "3. Monitor", "4. Input", "5. Pembayaran", "6. Cetak"])

    # --- MODUL 2: KATALOG DINAMIS (UPGRADED) ---
    if menu == "2. Katalog":
        st.markdown('<h1>📋 Manajemen Katalog & Inventaris</h1>', unsafe_allow_html=True)
        
        # 1. Search Logic
        search_query = st.text_input("🔍 Cari produk berdasarkan nama...", placeholder="Masukkan nama barang...")
        
        # 2. Performance & Data Handling (Filter Dinamis)
        filtered_products = {
            k: v for k, v in st.session_state.database_produk.items() 
            if search_query.lower() in k.lower()
        }
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        if not filtered_products:
            st.warning("⚠️ Produk tidak ditemukan dalam database.")
        else:
            st.write(f"Menampilkan {len(filtered_products)} produk.")
            for k, v in filtered_products.items():
                # 3. Validasi & Integrasi (Simulasi status stok)
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #e2e8f0;'>
                    <span style='font-weight:600;'>📦 {k}</span>
                    <span style='color:#0d9488; font-weight:700;'>Rp {v:,}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ... (Modul lainnya) ...
