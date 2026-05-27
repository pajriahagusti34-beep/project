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

# --- CUSTOM CSS: TEMA GRADIENT & DESAIN STRUK PREMIUM ---
custom_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #e0f2fe 50%, #f8fafc 100%) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 2px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    h1, h2, h3, h4, h5, h6, .stText {
        color: #0f172a !important;
        font-family: 'Segoe UI', Roboto, sans-serif !important;
        font-weight: 700 !important;
    }
    .clean-box {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-left: 6px solid #10b981 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05) !important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    /* DESAIN STRUK KASIR THERMAL */
    .struk-container {
        background-color: #ffffff !important;
        color: #1e293b !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        padding: 25px 20px;
        border-radius: 4px;
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.15);
        max-width: 360px;
        margin: 10px auto;
        border-top: 5px dashed #cbd5e1;
        border-bottom: 5px dashed #cbd5e1;
    }
    .struk-header { text-align: center; margin-bottom: 15px; }
    .struk-title { font-size: 18px !important; font-weight: bold !important; margin: 0 !important; color: #0f172a !important; }
    .struk-subtitle { font-size: 11px !important; color: #64748b !important; margin: 0 !important; }
    .struk-meta { font-size: 13px !important; margin-bottom: 12px; }
    .struk-divider { border-top: 1px dashed #94a3b8; margin: 8px 0; }
    .struk-item-row { display: flex; justify-content: space-between; margin-bottom: 5px; }
    .struk-item-name { flex: 1; text-align: left; }
    .struk-item-price { text-align: right; font-weight: bold; }
    .struk-footer { text-align: center; margin-top: 20px; font-size: 12px !important; color: #64748b !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'antrean_kasir' not in st.session_state:
    st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []
if 'struk_terakhir' not in st.session_state:
    st.session_state.struk_terakhir = ""

# DATABASE PRODUK
if 'database_produk' not in st.session_state:
    st.session_state.database_produk = {
        "Minyak Goreng 2L": 36000, "Susu UHT 1L": 18500, "Mie Instan Goreng": 3500,
        "Beras Premium 5kg": 75000, "Gula Pasir 1kg": 17000, "Teh Celup Isi 25": 6000,
        "Kopi Bubuk 100g": 12000, "Roti Tawar Kupas": 15000, "Mentega Serbaguna": 8500,
        "Sabun Mandi Cair": 22000, "Shampoo Anti Dandruff": 28000, "Pasta Gigi": 12500,
        "Air Mineral 600ml": 3500, "Keripik Kentang": 11000, "Tisu Wajah 200s": 9000
    }

antrean = st.session_state.antrean_kasir

if not st.session_state.is_logged_in:
    _, col_m, _ = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:60px;"><h2>FreshMart Express</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        if st.button("Masuk", type="primary", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Salah!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown("### FreshMart Express")
    menu = st.sidebar.radio("Menu Navigasi:", ["Beranda Utama", "Daftar Produk Toko", "Monitor Antrean", "Tambah Pelanggan Baru", "Proses Pembayaran (Checkout)", "Riwayat Jurnal Transaksi"])
    
    if st.sidebar.button("Keluar"):
        st.session_state.is_logged_in = False
        st.rerun()

    if menu == "Beranda Utama":
        st.markdown('<h2>Statistik Kasir</h2>', unsafe_allow_html=True)
        st.metric(label="Pelanggan Sukses Dilayani", value=f"{antrean.total_pelanggan_dilayani} Orang")

    elif menu == "Daftar Produk Toko":
        st.markdown('<h2>Katalog Toko</h2>', unsafe_allow_html=True)
        for k, v in st.session_state.database_produk.items():
            st.write(f"- {k} : Rp {v:,}")

    elif menu == "Monitor Antrean":
        st.markdown('<h2>Urutan Antrean</h2>', unsafe_allow_html=True)
        st.text_area("Status Memori Queue:", value=antrean.dapatkan_antrean_string(), height=200, disabled=True)

    elif menu == "Tambah Pelanggan Baru":
        st.markdown('<h2>Registrasi Pelanggan</h2>', unsafe_allow_html=True)
        with st.form("form_tambah"):
            nama_input = st.text_input("Nama Pelanggan:")
            pilihan_barang = st.multiselect("Pilih Barang:", options=list(st.session_state.database_produk.keys()))
            if st.form_submit_button("Masukkan Ke Antrean"):
                if nama_input and pilihan_barang:
                    total = sum(st.session_state.database_produk[i] for i in pilihan_barang)
                    antrean.tambah_pelanggan(nama_input, pilihan_barang, total)
                    st.success("Berhasil masuk antrean!")
                    st.rerun()

    # ==========================================
    # MENU 5: PROSES CHECKOUT (PERBAIKAN TOTAL)
    # ==========================================
    elif menu == "Proses Pembayaran (Checkout)":
        st.markdown('<h2>Meja Transaksi Utama</h2>', unsafe_allow_html=True)
        col_kiri, col_kanan = st.columns([1.2, 1])
        
        with col_kiri:
            if antrean.is_empty():
                st.info("Tidak ada antrean pelanggan saat ini.")
            else:
                pelanggan_depan = antrean.head
                st.write(f"Pelanggan Terdepan: **{pelanggan_depan.nama}**")
                
                st.markdown('<div class="clean-box">', unsafe_allow_html=True)
                for b in pelanggan_depan.list_belanjaan:
                    st.write(f"• {b} (Rp {st.session_state.database_produk[b]:,})")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.write(f"### Total Tagihan: **Rp {pelanggan_depan.total_harga:,}**")
                uang_bayar = st.number_input("Masukkan Uang Tunai (Rp):", min_value=0, step=1000)
                
                # Gunakan key dinamis bawaan form agar nilainya langsung diproses tanpa ke-reset rerun
                if st.button("Selesaikan Pembayaran & Cetak Nota", type="primary", use_container_width=True):
                    if uang_bayar < pelanggan_depan.total_harga:
                        st.error("Uang tunai kurang!")
                    else:
                        kembalian = uang_bayar - pelanggan_depan.total_harga
                        no_transaksi = f"TRX-{random.randint(10000, 99999)}"
                        
                        html_items = ""
                        for b in pelanggan_depan.list_belanjaan:
                            html_items += f"""
                            <div class="struk-item-row">
                                <span class="struk-item-name">{b}</span>
                                <span class="struk-item-price">Rp {st.session_state.database_produk[b]:,}</span>
                            </div>"""
                        
                        # Set nilai HTML murni langsung ke session_state sebelum dibaca col_kanan
                        st.session_state.struk_terakhir = f"""
                        <div class="struk-container">
                            <div class="struk-header">
                                <h3 class="struk-title">FRESHMART EXPRESS</h3>
                                <p class="struk-subtitle">Sistem Antrean Kasir FIFO</p>
                            </div>
                            <div class="struk-meta">
                                <div><b>No. Trans</b> : {no_transaksi}</div>
                                <div><b>Pelanggan</b>: {pelanggan_depan.nama}</div>
                                <div><b>Kasir</b>     : Admin Aktif</div>
                            </div>
                            <div class="struk-divider"></div>
                            {html_items}
                            <div class="struk-divider"></div>
                            <div class="struk-item-row" style="font-weight:bold;">
                                <span>TOTAL</span><span>Rp {pelanggan_depan.total_harga:,}</span>
                            </div>
                            <div class="struk-item-row">
                                <span>TUNAI</span><span>Rp {uang_bayar:,}</span>
                            </div>
                            <div class="struk-item-row" style="color:#059669; font-weight:bold;">
                                <span>KEMBALIAN</span><span>Rp {kembalian:,}</span>
                            </div>
                            <div class="struk-divider"></div>
                            <div class="struk-footer">~ Terima Kasih Atas Kunjungan Anda ~</div>
                        </div>"""
                        
                        # Lakukan operasi Dequeue
                        dilayani = antrean.layani_pelanggan()
                        if dilayani:
                            st.session_state.riwayat_transaksi.append(f"Sukses: {dilayani.nama} - Rp {dilayani.total_harga:,}")
                        st.rerun()

        with col_kanan:
            st.markdown("### 📄 Nota Transaksi")
            if st.session_state.struk_terakhir:
                # BAGIAN UTAMA: Merender paksa String HTML menjadi grafik web utuh
                st.components.v1.html(st.session_state.struk_terakhir, height=500, scrolling=True)
            else:
                st.caption("Belum ada transaksi.")

    elif menu == "Riwayat Jurnal Transaksi":
        st.markdown('<h2>Jurnal Rekap</h2>', unsafe_allow_html=True)
        for r in st.session_state.riwayat_transaksi:
            st.write(r)
