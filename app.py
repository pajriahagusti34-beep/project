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
            sekarang = Clinical_node = sekarang.next
            nomor += 1
        return hasil

# ==========================================
# PROGRAM UTAMA (STREAMLIT UI LUXURY THEME)
# ==========================================
st.set_page_config(page_title="FreshMart Express", layout="wide")

# --- ULTRA PREMIUM UI CUSTOM CSS WITH ADVANCED SIDEBAR NAVIGATION ---
custom_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 50%, #f5f7fa 100%) !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 3px solid #10b981 !important;
    }
    
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
    }

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

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        transform: translateX(4px);
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(13, 148, 136, 0.25) 0%, rgba(16, 185, 129, 0.15) 100%) !important;
        border-left: 5px solid #10b981 !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p::before {
        content: "";
    }
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetRadioDot"] {
        display: none !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        background: linear-gradient(45deg, #0f172a, #0d9488);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
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

    .empty-graveyard-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        border: 2px dashed #cbd5e1 !important;
        border-radius: 20px !important;
        padding: 40px 20px !important;
        text-align: center;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    
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
    st.session_state.struk_terakhir = ""
if 'total_omset' not in st.session_state:
    st.session_state.total_omset = 0

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

# ==========================================
# HALAMAN 1: LOGIN PAGE
# ==========================================
if not st.session_state.is_logged_in:
    _, col_m, _ = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:80px; margin-bottom: 10px;"><h1>✨ FreshMart Express</h1><p style="color:#475569; font-size:14px; font-weight:500;">Kasir Berbasis Antrean Dinamis (FIFO)</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin-top:0; margin-bottom:15px; font-size:16px; color:#0f172a;">Otorisasi Akses Pegawai</h4>', unsafe_allow_html=True)
        username = st.text_input("Username Kasir:")
        password = st.text_input("Password Pengaman:", type="password")
        st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
        if st.button("Buka Akses Sistem", type="primary", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Kredensial salah! Gunakan admin / 123.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: OPERASIONAL UTAMA
# ==========================================
else:
    st.sidebar.markdown("<h2 style='background:linear-gradient(45deg, #10b981, #38bdf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:22px; font-weight:800; margin-bottom:5px; margin-top:15px;'>FreshMart UI v2.5</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#94a3b8; font-size:12px; margin-top:0; font-weight:500;'>🟢 Sistem Siap Melayani</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='margin:10px 0; border-color:#334155;'>", unsafe_allow_html=True)
    
    menu = st.sidebar.radio(
        "PILIH MODUL OPERASIONAL:", 
        [
            "📢 1. Panggil Nomor Antrean", 
            "📦 2. Cek Katalog Produk Toko", 
            "🔍 3. Monitor Sabuk Antrean RAM", 
            "📥 4. Input Pelanggan ke Jalur", 
            "💸 5. Scan Barang & Input Bayar", 
            "🧾 6. Cetak Struk & Jurnal Rekap"
        ]
    )
    
    st.sidebar.markdown("<hr style='margin:15px 0; border-color:#334155;'>", unsafe_allow_html=True)
    if st.sidebar.button("🔒 Tutup Shift (Keluar)", type="secondary", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()

    # --- JALUR MENU 1 ---
    if menu == "📢 1. Panggil Nomor Antrean":
        st.markdown('<h1>📊 Statistik & Dasbor Utama</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#475569; margin-top:-10px; font-weight:500;">Ringkasan aktivitas transaksi supermarket Anda hari ini</p>', unsafe_allow_html=True)
        
        panjang_antrean = 0
        curr = antrean.head
        while curr:
            panjang_antrean += 1
            curr = curr.next
            
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Pelanggan Menunggu Antrean", value=f"{panjang_antrean} Jiwa")
        with col_m2:
            st.metric(label="Total Sukses Dilayani", value=f"{antrean.total_pelanggan_dilayani} Orang")
            
        st.markdown('<div style="margin-top:25px;"></div>', unsafe_allow_html=True)
        st.markdown('<h3>📢 Pelanggan di Garis Depan Kasir</h3>', unsafe_allow_html=True)
        if antrean.is_empty():
            st.info("Kondisi Jalur Kasir Aman. Tidak ada antrean standby.")
        else:
            p_depan = antrean.head
            st.markdown(f"""
            <div class="clean-box">
                <p style="margin:0; font-size:12px; color:#0d9488; font-weight:bold; text-transform:uppercase;">Sedang Melakukan Scan Barang</p>
                <h3 style="margin:5px 0 10px 0; font-size:24px; background:none; -webkit-text-fill-color:initial; color:#0f172a !important;">{p_depan.nama}</h3>
                <p style="margin:0; font-size:14px; color:#475569;">Membawa total belanjaan sebanyak <b>{len(p_depan.list_belanjaan)} jenis barang</b> dengan estimasi tagihan <b>Rp {p_depan.total_harga:,}</b>.</p>
            </div>
            """, unsafe_allow_html=True)

    # --- JALUR MENU 2 ---
    elif menu == "📦 2. Cek Katalog Produk Toko":
        st.markdown('<h1>📋 Katalog Produk Terdaftar</h1>', unsafe_allow_html=True)
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        for k, v in st.session_state.database_produk.items():
            st.markdown(f"<div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f1f5f9;'><span style='font-weight:600; color:#1e293b;'>📦 {k}</span><span style='font-weight:700; color:#0d9488;'>Rp {v:,}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- JALUR MENU 3 ---
    elif menu == "🔍 3. Monitor Sabuk Antrean RAM":
        st.markdown('<h1>🔍 Visualisasi Memori Node (Queue)</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#475569; margin-top:-10px; font-weight:500;">Status urutan objek antrean FIFO murni di dalam RAM komputer</p>', unsafe_allow_html=True)
        clean_antrean = antrean.dapatkan_antrean_string()
        st.text_area("Urutan Barisan Pelanggan (Head -> Tail):", value=clean_antrean, height=250, disabled=True)

    # --- JALUR MENU 4 ---
    elif menu == "📥 4. Input Pelanggan ke Jalur":
        st.markdown('<h1>📥 Registrasi Masuk Antrean</h1>', unsafe_allow_html=True)
        with st.form("form_tambah_baru"):
            st.markdown('<div style="padding:5px;"></div>', unsafe_allow_html=True)
            nama_input = st.text_input("Input Nama Pelanggan Baru:")
            pilihan_barang = st.multiselect("Pilih Item Belanjaan yang Dibawa:", options=list(st.session_state.database_produk.keys()))
            st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
            if st.form_submit_button("Dorong Masuk Barisan Antrean"):
                if nama_input.strip() and pilihan_barang:
                    total = sum(st.session_state.database_produk[i] for i in pilihan_barang)
                    antrean.tambah_pelanggan(nama_input, pilihan_barang, total)
                    st.success(f"Sukses! Node '{nama_input}' dimasukkan di urutan paling belakang (Tail).")
                    st.rerun()
                else:
                    st.error("Gagal! Nama dan barang tidak boleh kosong.")

    # --- JALUR MENU 5 ---
    elif menu == "💸 5. Scan Barang & Input Bayar":
        st.markdown('<h1>💸 Meja Penyelesaian Pembayaran</h1>', unsafe_allow_html=True)
        
        if antrean.is_empty():
            st.info("Meja kasir siap. Tidak ada antrean pelanggan yang menunggu.")
        else:
            pelanggan_depan = antrean.head
            st.markdown(f"### Pembayaran Atas Nama: `{pelanggan_depan.nama}`")
            
            st.markdown('<div class="clean-box">', unsafe_allow_html=True)
            st.markdown('<p style="margin-top:0; font-weight:700; color:#334155;">Daftar Item Keranjang:</p>', unsafe_allow_html=True)
            for b in pelanggan_depan.list_belanjaan:
                st.markdown(f"<div style='font-size:14px; margin-bottom:4px; color:#475569;'>• {b} (<span style='font-weight:600;'>Rp {st.session_state.database_produk[b]:,}</span>)</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"<h2 style='background:none; -webkit-text-fill-color:initial; color:#0f172a;'>Total Tagihan: <span style='color:#0d9488;'>Rp {pelanggan_depan.total_harga:,}</span></h2>", unsafe_allow_html=True)
            uang_bayar = st.number_input("Masukkan Jumlah Nominal Uang Tunai (Rp):", min_value=0, step=1000)
            
            st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)
            if st.button("Finalisasi Pembayaran & Cetak Nota", type="primary", use_container_width=True):
                if uang_bayar < pelanggan_depan.total_harga:
                    st.error("Transaksi Ditolak! Nominal uang tunai yang diberikan kurang.")
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
                    
                    st.session_state.struk_terakhir = f"""
                    {html_struk_style}
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
                        <div class="struk-item-row" style="font-weight:bold; font-size:15px;">
                            <span>TOTAL AGREGAT</span><span>Rp {pelanggan_depan.total_harga:,}</span>
                        </div>
                        <div class="struk-item-row">
                            <span>CASH TUNAI</span><span>Rp {uang_bayar:,}</span>
                        </div>
                        <div class="struk-item-row" style="color:#0d9488; font-weight:bold;">
                            <span>KEMBALIAN</span><span>Rp {kembalian:,}</span>
                        </div>
                        <div class="struk-divider"></div>
                        <div class="struk-footer">~ Terima Kasih Atas Kunjungan Anda ~<br>Sistem Berjalan Lancar</div>
                    </div>"""
                    
                    st.session_state.total_omset += pelanggan_depan.total_harga
                    dilayani = antrean.layani_pelanggan()
                    if dilayani:
                        st.session_state.riwayat_transaksi.append(f"Sukses: {dilayani.nama} - Total Belanja: Rp {dilayani.total_harga:,} (Lunas)")
                    
                    st.balloons()
                    st.success("Pembayaran Berhasil! Silakan cek Menu 6 untuk melihat Struk Terbuka.")

    # --- JALUR MENU 6 ---
    elif menu == "🧾 6. Cetak Struk & Jurnal Rekap":
        st.markdown('<h1>🧾 Dokumen Struk & Jurnal Rekapitulasi</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#475569; margin-top:-10px; font-weight:500;">Monitor arus kas masuk dan validasi nota digital kasir</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #0f172a 0%, #0d9488 100%); padding: 18px 25px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 10px 25px -5px rgba(13,148,136,0.25);">
            <div style="font-size: 11px; font-weight: 700; color: #ccfbf1; text-transform: uppercase; letter-spacing: 1px;">LIVE FINANCIAL TRACKER (SHIFT AKTIF)</div>
            <div style="font-size: 28px; font-weight: 800; color: #ffffff; margin-top: 2px;">Total Arus Pendapatan: <span style="color: #2dd4bf;">Rp {st.session_state.total_omset:,}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        col_struk, col_jurnal = st.columns([1, 1.2])
        
        with col_struk:
            st.markdown("### 📄 Struk Pembayaran Terakhir")
            if st.session_state.struk_terakhir:
                st.components.v1.html(st.session_state.struk_terakhir, height=520, scrolling=True)
            else:
                st.markdown("""
                <div class="empty-graveyard-box">
                    <div style="font-size: 50px; margin-bottom: 10px;">📭</div>
                    <h4 style="margin: 0; font-size: 16px; color: #475569; background:none; -webkit-text-fill-color:initial;">Printer Nota Standby</h4>
                    <p style="margin: 5px 0 0 0; font-size: 13px; color: #94a3b8; line-height:1.4;">Belum ada antrean yang di-checkout pada menu nomor 5.<br>Sistem printer thermal siap mencetak!</p>
                </div>
                """, unsafe_allow_html=True)
                
        with col_jurnal:
            st.markdown("### 📋 Log Riwayat Transaksi (RAM)")
            if not st.session_state.riwayat_transaksi:
                st.markdown("""
                <div class="empty-graveyard-box">
                    <div style="font-size: 50px; margin-bottom: 10px;">📉</div>
                    <h4
