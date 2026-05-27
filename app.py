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

# --- CUSTOM CSS: TEMA MODERN LIGHT & FRESH (ELEGANT RETAIL) ---
custom_css = """
<style>
    /* Background Utama Aplikasi */
    .stApp {
        background-color: #f8fafc !important;
    }
    
    /* Pewarnaan Teks Global agar Kontras dengan Background Terang */
    h1, h2, h3, h4, h5, h6, p, span, div, .stText {
        color: #1e293b !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Label Input & Widget Form */
    [data-testid="stWidgetLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    /* Desain Sidebar Kiri */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #334155 !important;
    }
    
    /* Desain Kotak Kontainer (Clean Box) Menjadi Lebih Elegan */
    .clean-box {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 6px solid #10b981 !important; /* Aksen Hijau FreshMart */
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* Input Text Area & Form Control */
    textarea, input {
        color: #0f172a !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Warna Angka Statik (Metric Widget) */
    [data-testid="stMetricValue"] {
        color: #0f766e !important; /* Warna Teal Elegan */
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #64748b !important;
    }
    
    /* Style Khusus untuk Text Jurnal Berwarna Hijau */
    .clean-box p {
        color: #1e293b !important;
    }
    
    /* --- STYLE KHUSUS UNTUK STRUK NOTA KASIR --- */
    .struk-container {
        background-color: #fffde7 !important; /* Warna kertas nota sedikit krem estetik */
        color: #111111 !important;
        font-family: 'Courier New', Courier, monospace !important;
        padding: 20px;
        border-radius: 6px;
        box-sizing: border-box;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 15px auto;
        border: 1px dashed #bcccb4;
    }
    .struk-container pre {
        background-color: transparent !important;
        color: #111111 !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        font-family: 'Courier New', Courier, monospace !important;
        white-space: pre-wrap !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- INISIALISASI DATA DI SESSION STATE ---
if 'antrean_kasir' not in st.session_state or st.session_state.antrean_kasir is None:
    st.session_state.antrean_kasir = QueueSupermarket()
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'riwayat_transaksi' not in st.session_state:
    st.session_state.riwayat_transaksi = []
if 'struk_terakhir' not in st.session_state:
    st.session_state.struk_terakhir = None

# MASTER DATABASE: 20 PRODUK SUPERMARKET
if 'database_produk' not in st.session_state:
    st.session_state.database_produk = {
        "Minyak Goreng 2L": 36000,
        "Susu UHT Full Cream 1L": 18500,
        "Mie Instan Goreng": 3500,
        "Beras Premium 5kg": 75000,
        "Gula Pasir 1kg": 17000,
        "Teh Celup Isi 25": 6000,
        "Kopi Bubuk 100g": 12000,
        "Roti Tawar Kupas": 15000,
        "Mentega Serbaguna": 8500,
        "Kecap Manis Bango": 24000,
        "Saus Sambal Botol": 14500,
        "Sabun Mandi Cair": 22000,
        "Shampoo Anti Dandruff": 28000,
        "Pasta Gigi Herbal": 12500,
        "Deterjen Bubuk 800g": 19500,
        "Cairan Pencuci Piring": 10500,
        "Air Mineral 600ml": 3500,
        "Keripik Kentang Snack": 11000,
        "Cokelat Batang Premium": 16000,
        "Tisu Wajah 200 sheets": 9000
    }

antrean = st.session_state.antrean_kasir

# ==========================================
# HALAMAN 1: LOGIN
# ==========================================
if not st.session_state.is_logged_in:
    col_l, col_m, col_r = st.columns([1, 1.1, 1])
    
    with col_m:
        st.markdown('<div style="text-align:center; margin-top:60px; margin-bottom:20px;">', unsafe_allow_html=True)
        logo_url = "https://global.ac.id/wp-content/uploads/2021/01/logo-global-80.png"
        st.image(logo_url, width=130)
        st.markdown('<h1 style="font-size: 28px; font-weight: 600; letter-spacing: 1px; margin-top:15px;">FreshMart Express</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #64748b; font-size: 13px;">Sistem Informasi Manajemen Antrean Kasir</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        username = st.text_input("Username / NIK Pegawai:")
        password = st.text_input("Password:", type="password")
        
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Kredensial yang Anda masukkan salah.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: DASHBOARD UTAMA
# ==========================================
else:
    st.sidebar.markdown("<h3 style='letter-spacing: 1px; font-weight:600; margin-bottom:0;'>FreshMart Express</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#64748b; font-size:12px; margin-top:0;'>Otoritas Kasir: Aktif</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio(
        "Menu Navigasi:",
        [
            "Beranda Utama", 
            "Daftar Produk Toko",
            "Monitor Antrean", 
            "Tambah Pelanggan Baru", 
            "Proses Pembayaran (Checkout)", 
            "Riwayat Jurnal Transaksi"
        ]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Keluar Sistem", type="secondary", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.struk_terakhir = None
        st.rerun()

    # MENU 1: BERANDA UTAMA
    if menu == "Beranda Utama":
        st.markdown('<h1 style="margin-bottom:0px;">Statistik Toko & Kasir</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b; margin-bottom:25px;">Ringkasan aktivitas operasional retail secara real-time</p>', unsafe_allow_html=True)
        
        panjang_antrean = 0
        curr = antrean.head
        while curr:
            panjang_antrean += 1
            curr = curr.next
            
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Antrean Aktif Saat Ini", value=f"{panjang_antrean} Orang")
        with col_m2:
            st.metric(label="Pelanggan Sukses Dilayani", value=f"{antrean.total_pelanggan_dilayani} Orang")
        with col_m3:
            st.metric(label="Estimasi Jurnal Selesai", value=f"{len(st.session_state.riwayat_transaksi)} Transaksi")

        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

        st.markdown('<h3>Status Jalur Kasir Utama</h3>', unsafe_allow_html=True)
        if antrean.is_empty():
            st.info("Kondisi Jalur Kasir: Kosong / Standby Melayani Pelanggan.")
        else:
            pelanggan_sekarang = antrean.head
            st.markdown(f"""
            <div class="clean-box" style="border-left: 6px solid #10b981 !important; background: rgba(16, 185, 129, 0.05) !important; border-color: rgba(16, 185, 129, 0.3) !important;">
                <p style="margin: 0; font-size: 13px; color: #10b981; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">Sedang Diproses Terdepan</p>
                <h4 style="margin: 5px 0 10px 0; font-size: 22px;">{pelanggan_sekarang.nama}</h4>
                <p style="margin: 0; color: #334155; font-size: 14px;">Membawa <b>{len(pelanggan_sekarang.list_belanjaan)} item</b> dengan akumulasi nilai belanja sebesar <b>Rp {pelanggan_sekarang.total_harga:,}</b>.</p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("ℹ️ Lihat Dokumentasi Alur Logika Struktur Data (FIFO)"):
            st.write("**Prinsip Kerja:** Menggunakan metode antrean murni (*Queue*). Pelanggan yang pertama kali datang (*Enqueue*) akan diposisikan pada urutan paling depan (`head`) dan wajib diselesaikan terlebih dahulu (*Dequeue*).")
            st.write("**Manajemen Memori:** Dibangun menggunakan konsep *Linked List Singly* dinamis di mana setiap pelanggan bertindak sebagai objek *Node* independen yang menunjuk elemen di belakangnya.")

    # MENU 2: LIHAT DAFTAR PRODUK
    elif menu == "Daftar Produk Toko":
        st.markdown('<h2>Katalog Produk Aktif (20 Item)</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="clean-box">', unsafe_allow_html=True)
        nomor_urut = 1
        for nama_barang, harga_barang in st.session_state.database_produk.items():
            st.markdown(f"<p style='font-size:15px; margin-bottom:6px;'>{nomor_urut}. <b>{nama_barang}</b> — Rp {harga_barang:,}</p>", unsafe_allow_html=True)
            nomor_urut += 1
        st.markdown('</div>', unsafe_allow_html=True)

    # MENU 3: MONITOR ANTREAN
    elif menu == "Monitor Antrean":
        st.markdown('<h2>Urutan Barisan Pelanggan</h2>', unsafe_allow_html=True)
        antrean_teks = antrean.dapatkan_antrean_string()
        st.text_area("Data Node Memori saat ini (FIFO):", value=antrean_teks, height=200, disabled=True)

    # MENU 4: TAMBAH PELANGGAN BARU
    elif menu == "Tambah Pelanggan Baru":
        st.markdown('<h2>Registrasi Kedatangan Pelanggan</h2>', unsafe_allow_html=True)
        
        with st.form("form_tambah", clear_on_submit=True):
            nama_input = st.text_input("Nama Pelanggan:")
            
            pilihan_barang = st.multiselect(
                "Pilih Barang Yang Dibeli (Bisa klik lebih dari satu):",
                options=list(st.session_state.database_produk.keys())
            )
            
            submit_button = st.form_submit_button("Masukkan ke Antrean")
            
            if submit_button:
                if not nama_input.strip():
                    st.warning("Kolom nama wajib diisi.")
                elif not pilihan_barang:
                    st.warning("Pelanggan minimal harus membeli 1 barang untuk mengantre.")
                else:
                    total_harga_hitung = sum(st.session_state.database_produk[item] for item in pilihan_barang)
                    st.session_state.antrean_kasir.tambah_pelanggan(nama_input, pilihan_barang, total_harga_hitung)
                    st.success(f"Sukses! Pelanggan '{nama_input}' berhasil ditambahkan ke antrean.")
                    st.rerun()

    # MENU 5: PROSES CHECKOUT
    elif menu == "Proses Pembayaran (Checkout)":
        st.markdown('<h2>Meja Transaksi Utama</h2>', unsafe_allow_html=True)
        
        col_kiri, col_kanan = st.columns([1.2, 1])
        
        with col_kiri:
            if antrean.is_empty():
                st.info("Sistem siap. Tidak ada antrean pelanggan saat ini.")
            else:
                pelanggan_depan = antrean.head
                
                st.write(f"Pelanggan Terdepan: **{pelanggan_depan.nama}**")
                st.write("Daftar belanjaan yang dibawa:")
                
                st.markdown('<div class="clean-box" style="background-color: #f1f5f9 !important; border-left-color: #0f766e !important;">', unsafe_allow_html=True)
                for b in pelanggan_depan.list_belanjaan:
                    st.write(f"- {b} (Rp {st.session_state.database_produk[b]:,})")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.write(f"### Total Invoice: **Rp {pelanggan_depan.total_harga:,}**")
                
                st.markdown("---")
                uang_bayar = st.number_input("Masukkan Jumlah Uang Tunai (Rp):", min_value=0, step=500, value=0)
                
                if uang_bayar > 0:
                    if uang_bayar < pelanggan_depan.total_harga:
                        kekurangan = pelanggan_depan.total_harga - uang_bayar
                        st.error(f"Uang tunai kurang! Kurang sebesar: Rp {kekurangan:,}")
                    else:
                        kembalian = uang_bayar - pelanggan_depan.total_harga
                        st.success(f"### Uang Kembalian: **Rp {kembalian:,}**")
                
                if st.button("Selesaikan Pembayaran & Cetak Nota", type="primary", use_container_width=True):
                    if uang_bayar < pelanggan_depan.total_harga:
                        st.error("Transaksi ditolak. Harap masukkan jumlah uang tunai yang cukup.")
                    else:
                        kembalian_final = uang_bayar - pelanggan_depan.total_harga
                        
                        # --- PROSES MEMBUAT TEMPLATE STRUK FISIK KASIR ---
                        no_transaksi = f"TRX-{random.randint(10000, 99999)}"
                        item_struk = ""
                        for b in pelanggan_depan.list_belanjaan:
                            harga = st.session_state.database_produk[b]
                            # Format tata letak teks agar rata kiri-kanan rapi khas struk belanja
                            item_struk += f"{b:<24} Rp{harga:>8,}\n"
                        
                        template_struk = f"""
========================================
           FRESHMART EXPRESS            
        Sistem Antrean Kasir FIFO       
========================================
No. Trans : {no_transaksi}
Pelanggan : {pelanggan_depan.nama}
Kasir     : Admin Aktif
----------------------------------------
{item_struk}----------------------------------------
TOTAL             : Rp{pelanggan_depan.total_harga:>8,}
TUNAI/CASH        : Rp{uang_bayar:>8,}
KEMBALIAN         : Rp{kembalian_final:>8,}
----------------------------------------
  Terima Kasih Atas Kunjungan Anda!   
========================================
"""
                        # Simpan ke session state agar tetap tampil setelah di-refresh/rerun
                        st.session_state.struk_terakhir = template_struk
                        
                        dilayani = st.session_state.antrean_kasir.layani_pelanggan()
                        if dilayani:
                            catatan = f"Pelanggan {dilayani.nama} • Total: Rp {dilayani.total_harga:,} • Cash: Rp {uang_bayar:,} • Kembali: Rp {kembalian_final:,} [Selesai]"
                            st.session_state.riwayat_transaksi.append(catatan)
                            st.rerun()

        # KOLOM KANAN: UNTUK MENAMPILKAN NOTA/STRUK YANG SUDAH DICETAK
        with col_kanan:
            st.markdown("### 📄 Nota Transaksi Terakhir")
            if st.session_state.struk_terakhir:
                st.markdown(f"""
                <div class="struk-container">
                    <pre>{st.session_state.struk_terakhir}</pre>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("Belum ada struk transaksi yang dicetak di sesi ini.")

    # MENU 6: RIWAYAT TRANSAKSI KELUAR
    elif menu == "Riwayat Jurnal Transaksi":
        st.markdown('<h2>Jurnal Rekap Transaksi</h2>', unsafe_allow_html=True)
        
        if not st.session_state.riwayat_transaksi:
            st.info("Jurnal transaksi harian masih kosong.")
        else:
            st.markdown('<div class="clean-box">', unsafe_allow_html=True)
            for item in st.session_state.riwayat_transaksi:
                st.markdown(f"<p style='color: #10b981 !important; font-weight: 500;'>✓ {item}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
