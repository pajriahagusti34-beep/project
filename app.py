import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. STRUKTUR DATA UTAMA (NODE & QUEUE)
# ==========================================
class BarangBelanja:
    """Menyimpan data item produk yang dibeli oleh pelanggan."""
    def __init__(self, kode, nama, harga, qty):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.qty = qty

class PelangganNode:
    """Node untuk menyimpan data satu pelanggan beserta keranjang belanjanya dalam Antrean."""
    def __init__(self, id_antrean, nama_pelanggan="Pelanggan Umum"):
        self.id_antrean = id_antrean
        self.nama = nama_pelanggan
        self.keranjang = []  # Berisi list objek BarangBelanja
        self.member_id = None
        self.kode_voucher = None
        self.next = None

class AntreanKasirQueue:
    """Implementasi Queue (FIFO) untuk mengelola antrean pelanggan di depan meja kasir."""
    def __init__(self):
        self.front = None
        self.rear = None
        self.total_antrean = 0
        self.counter_id = 1

    def is_empty(self):
        return self.front is None

    def tambah_pelanggan(self, nama="Pelanggan Umum"):
        """Enqueue: Menambahkan pelanggan baru ke barisan antrean kasir."""
        baru = PelangganNode(f"TRX-{self.counter_id:03d}", nama)
        self.counter_id += 1
        if self.is_empty():
            self.front = baru
            self.rear = baru
        else:
            self.rear.next = baru
            self.rear = baru
        self.total_antrean += 1
        return baru

    def selesaikan_pelanggan_depan(self):
        """Dequeue: Menghapus pelanggan terdepan setelah transaksi selesai dibayar."""
        if self.is_empty():
            return None
        di_proses = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.total_antrean -= 1
        return di_proses

    def dapatkan_list_antrean(self):
        """Mengambil semua daftar pelanggan yang sedang mengantre untuk ditampilkan di monitor."""
        daftar = []
        sekarang = self.front
        while sekarang:
            total_item = sum(item.qty for item in sekarang.keranjang)
            total_harga = sum(item.harga * item.qty for item in sekarang.keranjang)
            daftar.append({
                "ID Transaksi": sekarang.id_antrean,
                "Nama Pembeli": sekarang.nama,
                "Total Jenis Barang": len(sekarang.keranjang),
                "Total Qty": total_item,
                "Estimasi Tagihan": f"Rp {total_harga:,}"
            })
            sekarang = sekarang.next
        return daftar

# ==========================================
# 2. SEED DATABASE PRODUK SUPERMARKET
# ==========================================
DB_PRODUK = {
    "8991001": {"nama": "Air Mineral Premium 600ml", "harga": 4500, "kategori": "Minuman"},
    "8991002": {"nama": "Roti Tawar Gandum Super", "harga": 18500, "kategori": "Makanan"},
    "8991003": {"nama": "Mie Instan Rasa Soto", "harga": 3100, "kategori": "Makanan"},
    "8991004": {"nama": "Susu UHT Full Cream 1L", "harga": 19000, "kategori": "Minuman"},
    "8991005": {"nama": "Kopi Instan Sehat isi 10", "harga": 14200, "kategori": "Minuman"},
    "8991006": {"nama": "Sabun Mandi Cair Organik", "harga": 26500, "kategori": "Kebutuhan Rumah"},
    "8991007": {"nama": "Deterjen Bubuk Anti Noda", "harga": 17000, "kategori": "Kebutuhan Rumah"},
    "APEL": {"nama": "Apel Malang Fresh (Per Kg)", "harga": 32000, "kategori": "Buah & Sayur"},
    "TOMAT": {"nama": "Tomat Hidroponik (Per Kg)", "harga": 15000, "kategori": "Buah & Sayur"}
}

# ==========================================
# 3. KONFIGURASI HALAMAN & CSS GRADASI
# ==========================================
st.set_page_config(page_title="Sistem Komputer Kasir Pro v2.0", page_icon="💻", layout="wide")

# CSS Kustom untuk tampilan latar belakang gradasi malam ke fajar yang premium
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    }
    .pos-container {
        background-color: rgba(255, 255, 255, 0.97);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
        color: #2c3e50;
        margin-bottom: 25px;
    }
    .led-display {
        background-color: #0d0d0d;
        color: #ff3f34;
        font-family: 'Digital-7', 'Courier New', monospace;
        padding: 20px;
        border-radius: 8px;
        font-size: 40px;
        text-align: right;
        font-weight: bold;
        letter-spacing: 2px;
        border: 4px inset #444;
        box-shadow: inset 0px 0px 15px rgba(0,0,0,0.9);
    }
    .struk-kertas {
        background-color: #f9f9f9;
        color: #111111;
        font-family: 'Courier New', monospace;
        padding: 18px;
        border-left: 5px solid #ffa801;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. MANAJEMEN SESSION STATE
# ==========================================
if 'login_sukses' not in st.session_state:
    st.session_state.login_sukses = False
if 'nama_kasir' not in st.session_state:
    st.session_state.nama_kasir = ""
if 'antrean_global' not in st.session_state:
    # Inisialisasi antrean dan isi dengan beberapa antrean default
    q = AntreanKasirQueue()
    p1 = q.tambah_pelanggan("Siti Rahma")
    p1.keranjang.append(BarangBelanja("8991001", DB_PRODUK["8991001"]["nama"], DB_PRODUK["8991001"]["harga"], 3))
    p1.keranjang.append(BarangBelanja("8991004", DB_PRODUK["8991004"]["nama"], DB_PRODUK["8991004"]["harga"], 1))
    
    q.tambah_pelanggan("Budi Wijaya")
    st.session_state.antrean_global = q

if 'omset_shift' not in st.session_state:
    st.session_state.omset_shift = 0.0
if 'transaksi_tercetak' not in st.session_state:
    st.session_state.transaksi_tercetak = None

antrean_global = st.session_state.antrean_global

# ==========================================
# 5. ALUR INTERFACE (UI)
# ==========================================

# --- GERBANG LOGIN KASIR ---
if not st.session_state.login_sukses:
    st.markdown('<div class="pos-container" style="max-width: 500px; margin: 100px auto;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/5087/5087579.png", width=70)
    st.subheader("🖥️ LOGIN COMPUTER POS SYSTEM")
    st.caption("Supermarket Enterprise v2.0 - POS Terminal")
    
    user_input = st.text_input("ID Operator / Kasir:", value="KASIR_MAIN_01")
    pass_input = st.text_input("PIN Akses:", type="password", value="1234")
    
    if st.button("Buka Kunci Terminal Kasir", type="primary", use_container_width=True):
        if pass_input == "1234":
            st.session_state.login_sukses = True
            st.session_state.nama_kasir = user_input
            st.rerun()
        else:
            st.error("PIN Akses Salah! (Gunakan PIN default: 1234)")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- TERMINAL UTAMA KASIR TELAH DIBUKA ---
    
    # KANVAS SIDEBAR (INFORMASI SHIFT & MANAGEMENT ANTREAN)
    st.sidebar.markdown(f"### 🧑‍💻 Operator Aktif: `{st.session_state.nama_kasir}`")
    st.sidebar.markdown("---")
    
    # Form untuk menambahkan antrean orang baru yang datang ke kasir
    st.sidebar.markdown("#### ➕ Tambah Antrean Baru")
    nama_baru = st.sidebar.text_input("Nama Pelanggan Baru:", placeholder="Misal: Ibu Endang")
    if st.sidebar.button("Masukkan ke Barisan Antrean", use_container_width=True):
        if nama_baru.strip() != "":
            antrean_global.tambah_pelanggan(nama_baru.strip())
            st.sidebar.success(f"Pelanggan '{nama_baru}' ditambahkan ke ekor antrean!")
            time.sleep(0.5)
            st.rerun()
            
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 📊 Ringkasan Finansial Shift")
    st.sidebar.metric(label="Total Omset Penjualan (Shift Ini)", value=f"Rp {st.session_state.omset_shift:,}")
    
    if st.sidebar.button("🔄 Reset Seluruh Terminal"):
        st.session_state.antrean_global = AntreanKasirQueue()
        st.session_state.omset_shift = 0.0
        st.session_state.transaksi_tercetak = None
        st.rerun()

    # LAYOUT UTAMA MONITOR LAPTOP
    if antrean_global.is_empty():
        st.markdown('<div class="pos-container">', unsafe_allow_html=True)
        st.success("🎉 Semua Antrean Kosong! Tidak ada pelanggan di depan kasir saat ini.")
        st.info("Silakan gunakan menu di panel kiri untuk memasukkan antrean pelanggan baru.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Pelanggan aktif yang sedang berada paling depan di meja kasir (Struktur Data Queue Front)
        p_aktif = antrean_global.front
        
        col_kiri, col_kanan = st.columns([7, 5])
        
        with col_kiri:
            st.markdown('<div class="pos-container">', unsafe_allow_html=True)
            st.markdown(f"### 🛒 MELAYANI: `{p_aktif.nama}` ({p_aktif.id_antrean})")
            
            # 1. MONITOR DIGITAL LED TOTAL BIAYA (REAL-TIME KALKULASI)
            subtotal_kotor = sum(item.harga * item.qty for item in p_aktif.keranjang)
            potongan_member = int(subtotal_kotor * 0.05) if p_aktif.member_id else 0
            potongan_voucher = 12500 if p_aktif.kode_voucher == "SUPERHEMAT" else 0
            total_diskon = potongan_member + potongan_voucher
            
            nilai_pajak = int((subtotal_kotor - total_diskon) * 0.11) if subtotal_kotor > 0 else 0
            total_bersih = max(0, (subtotal_kotor - total_diskon) + nilai_pajak)
            
            st.markdown(f'<div class="led-display">Rp {total_bersih:,}</div>', unsafe_allow_html=True)
            st.write("")
            
            # 2. INPUT METODE BARANG (SCANNER / CARI MANUAL KATEGORI)
            st.markdown("#### 📥 Input Barang Belanjaan")
            tab_scan, tab_cari = st.tabs(["📟 Barcode Scanner / SKU", "🔍 Cari Katalog Produk"])
            
            with tab_scan:
                c_scan, c_qty = st.columns([7, 3])
                with c_scan:
                    sku_scan = st.text_input("Arahkan Laser Scanner / Ketik Kode SKU:", key="sku_scan", placeholder="Contoh: 8991001 atau APEL")
                with c_qty:
                    qty_scan = st.number_input("Qty Input:", min_value=1, value=1, step=1, key="qty_scan")
                
                if st.button("Simpan ke Komputer Kasir", type="secondary"):
                    if sku_scan:
                        sku_bersih = sku_scan.strip()
                        if sku_bersih in DB_PRODUK:
                            # Cek apakah barang sudah ada di keranjang pelanggan aktif ini
                            ada = False
                            for item in p_aktif.keranjang:
                                if item.kode == sku_bersih:
                                    item.qty += qty_scan
                                    ada = True
                                    break
                            if not ada:
                                p_aktif.keranjang.append(BarangBelanja(sku_bersih, DB_PRODUK[sku_bersih]["nama"], DB_PRODUK[sku_bersih]["harga"], qty_scan))
                            st.rerun()
                        else:
                            st.error("Kode Barcode/SKU tidak terdaftar!")
            
            with tab_cari:
                st.caption("Pilih produk langsung dari katalog supermarket:")
                pilihan_produk = st.selectbox("Pilih Item Produk:", options=list(DB_PRODUK.keys()), format_func=lambda x: f"{DB_PRODUK[x]['nama']} - Rp {DB_PRODUK[x]['harga']:,}")
                qty_pilih = st.number_input("Jumlah Beli:", min_value=1, value=1, step=1, key="qty_pilih")
                if st.button("Tambah Item Terpilih", type="secondary"):
                    ada = False
                    for item in p_aktif.keranjang:
                        if item.kode == pilihan_produk:
                            item.qty += qty_pilih
                            ada = True
                            break
                    if not ada:
                        p_aktif.keranjang.append(BarangBelanja(pilihan_produk, DB_PRODUK[pilihan_produk]["nama"], DB_PRODUK[pilihan_produk]["harga"], qty_pilih))
                    st.rerun()

            # 3. FITUR EDIT KERANJANG BELANJA YANG DINAMIS
            st.markdown("#### 📋 Daftar Isi Keranjang Belanja")
            if len(p_aktif.keranjang) == 0:
                st.info("Keranjang belanja milik pelanggan ini masih kosong.")
            else:
                # Membuat tabel manajemen manual item keranjang
                for idx, item in enumerate(p_aktif.keranjang):
                    col_nm, col_qt, col_sub, col_hapus = st.columns([5, 3, 2, 2])
                    with col_nm:
                        st.markdown(f"**{item.nama}**\n<br><small style='color:gray;'>SKU: {item.kode} @ Rp {item.harga:,}</small>", unsafe_allow_html=True)
                    with col_qt:
                        baru_qty = st.number_input("Qty", min_value=1, value=item.qty, step=1, key=f"qty_{item.kode}_{idx}")
                        item.qty = baru_qty
                    with col_sub:
                        st.markdown(f"**Rp {item.harga * item.qty:,}**")
                    with col_hapus:
                        if st.button("❌", key=f"del_{item.kode}_{idx}"):
                            p_aktif.keranjang.pop(idx)
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # 4. KARTU MEMBER & KUPON VOUCHER DISCOUNT
            st.markdown('<div class="pos-container">', unsafe_allow_html=True)
            st.markdown("#### 🎫 Kartu Anggota / Voucher Potongan")
            c_m, c_v = st.columns(2)
            with c_m:
                input_m = st.text_input("Nomor Member Pelanggan:", value=p_aktif.member_id if p_aktif.member_id else "", placeholder="Ketik No. HP / Scan Kartu")
                if input_m:
                    p_aktif.member_id = input_m
                    st.caption("✅ **Diskon Anggota Aktif (5%)**")
                else:
                    p_aktif.member_id = None
            with c_v:
                input_v = st.text_input("Kode Kupon Fisik:", value=p_aktif.kode_voucher if p_aktif.kode_voucher else "", placeholder="Contoh: SUPERHEMAT")
                if input_v.upper() == "SUPERHEMAT":
                    p_aktif.kode_voucher = "SUPERHEMAT"
                    st.caption("✅ **Kupon Valid (Potongan Rp 12,500)**")
                elif input_v:
                    st.caption("❌ Kupon Kedaluwarsa/Salah")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_kanan:
            # 5. MEJA FINISH CHECKOUT & PEMBAYARAN
            st.markdown('<div class="pos-container">', unsafe_allow_html=True)
            st.markdown("### 💳 EKSEKUSI PEMBAYARAN KASIR")
            
            if len(p_aktif.keranjang) == 0:
                st.warning("Tambahkan minimal 1 jenis barang untuk membuka menu pembayaran.")
            else:
                # Ringkasan Nota Kalkulator Finansial Kasir
                st.markdown(f"""
                * Total Belanja Kotor: **Rp {subtotal_kotor:,}**
                * Total Potongan Harga: -Rp {total_diskon:,}
                * PPN (11%): +Rp {nilai_pajak:,}
                ---
                ### Total Bersih Tagihan: Rp {total_bersih:,}
                """)
                
                opsi_bayar = st.radio("Metode Pembayaran Pembeli:", ["TUNAI / CASH", "NON-TUNAI (QRIS / DEBIT)"])
                
                bisa_checkout = False
                uang_tunai = 0
                kembalian_tunai = 0
                id_referensi_edc = "-"
                
                if opsi_bayar == "TUNAI / CASH":
                    uang_tunai = st.number_input("Jumlah Uang Tunai Diterima (Rp):", min_value=0, step=5000, value=int(total_bersih))
                    kembalian_tunai = uang_tunai - total_bersih
                    if kembalian_tunai >= 0:
                        st.success(f"💰 Uang Kembalian: **Rp {kembalian_tunai:,}**")
                        bisa_checkout = True
                    else:
                        st.error(f"⚠️ Uang Kurang Senilai: Rp {abs(kembalian_tunai):,}")
                else:
                    id_referensi_edc = st.text_input("Input Trace/Ref Number Mesin EDC / QRIS Bank:")
                    if id_referensi_edc.strip() != "":
                        bisa_checkout = True
                    else:
                        st.caption("⚠️ Wajib memasukkan nomor referensi struk mesin EDC/QRIS.")

                st.write("")
                # EKSEKUSI TOMBOL DEQUEUE STRUKTUR DATA QUEUE
                if st.button("🖨️ SELESAIKAN TRANSAKSI & CETAK STRUK", type="primary", use_container_width=True, disabled=not bisa_checkout):
                    # Ambil data struk dari pelanggan depan sebelum dihapus (Dequeue)
                    pelanggan_keluar = antrean_global.selesaikan_pelanggan_depan()
                    
                    if pelanggan_keluar:
                        # Tambahkan ke omset shift kasir
                        st.session_state.omset_shift += total_bersih
                        
                        # Simpan berkas ke logger printer struk samping
                        st.session_state.transaksi_tercetak = {
                            "id_trx": pelanggan_keluar.id_antrean,
                            "nama_pembeli": pelanggan_keluar.nama,
                            "operator": st.session_state.nama_kasir,
                            "items": [(i.nama, i.qty, i.harga) for i in pelanggan_keluar.keranjang],
                            "kotor": subtotal_kotor,
                            "diskon": total_diskon,
                            "pajak": nilai_pajak,
                            "total": total_bersih,
                            "metode": opsi_bayar,
                            "bayar": uang_tunai if opsi_bayar == "TUNAI / CASH" else total_bersih,
                            "kembali": kembalian_tunai if opsi_bayar == "TUNAI / CASH" else 0,
                            "ref": id_referensi_edc
                        }
                        
                        st.balloons()
                        st.toast("🔓 [KLIK!] Laci Uang Kasir Terbuka otomatis!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # 6. MODUL PRINTER NOTA TERMALSUPERMARKET (OUTPUT FISIK)
            if st.session_state.transaksi_tercetak:
                st.markdown("#### 📜 Printer Output Termal Struk")
                t = st.session_state.transaksi_tercetak
                st.markdown('<div class="struk-kertas">', unsafe_allow_html=True)
                st.markdown("<center><b>✨ SWALAYAN MAJU SEJAHTERA ✨</b><br>Terminal POS - Jakarta</center><br>", unsafe_allow_html=True)
                st.text(f"No Trx  : {t['id_trx']}")
                st.text(f"Kasir   : {t['operator']}")
                st.text(f"Pembeli : {t['nama_pembeli']}")
                st.text("=" * 38)
                for n_item, q_item, h_item in t['items']:
                    st.text(f"{n_item[:20]:<20} {q_item:>2}x  Rp{h_item:>6,}")
                st.text("=" * 38)
                st.text(f"Subtotal        : Rp {t['kotor']:,}")
                st.text(f"Diskon/Potongan : Rp {t['diskon']:,}")
                st.text(f"PPN (11%)       : Rp {t['pajak']:,}")
                st.text("-" * 38)
                st.text(f"TOTAL NETTO     : Rp {t['total']:,}")
                st.text(f"Metode Bayar    : {t['metode']}")
                st.text(f"Bayar Tunai     : Rp {t['bayar']:,}")
                st.text(f"Kembalian       : Rp {t['kembali']:,}")
                if t['ref'] != "-":
                    st.text(f"No. Ref EDC     : {t['ref']}")
                st.text("=" * 38)
                st.markdown("<center>BARANG YANG SUDAH DIBELI<br>TIDAK DAPAT DITUKAR KEMBALI.<br>TERIMA KASIH ATAS KUNJUNGAN ANDA</center>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("Bersihkan Histori Printer Struk", use_container_width=True):
                    st.session_state.transaksi_tercetak = None
                    st.rerun()

        # 7. MONITOR DAFTAR TUNGGU ANTRIAN (QUEUE VISUALIZATION)
        st.markdown('<div class="pos-container">', unsafe_allow_html=True)
        st.markdown("### 📋 MONITOR DATA ANTRIAN KASIR (QUEUE DISPLAY)")
        st.caption("Menampilkan urutan pembeli berikutnya yang sedang berdiri mengantre di belakang pembeli aktif saat ini.")
        
        list_antrean_aktif = antrean_global.dapatkan_list_antrean()
        if len(list_antrean_aktif) <= 1:
            st.caption("💡 Tidak ada antrean pembeli lain di belakang pembeli aktif.")
        else:
            # Tampilkan dalam bentuk dataframe tabular dari indeks ke-1 sampai terakhir
            df_antrean = pd.DataFrame(list_antrean_aktif[1:])
            st.dataframe(df_antrean, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
