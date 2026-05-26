import streamlit as st
import pandas as pd

# ==========================================
# 1. STRUKTUR DATA QUEUE (LINKED LIST)
# ==========================================
class BarangNode:
    """Menyimpan data barang belanjaan per item di keranjang."""
    def __init__(self, kode, nama, harga, qty):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.qty = qty
        self.next = None

class KeranjangQueue:
    """Implementasi Queue (FIFO) untuk item barang di dalam satu transaksi."""
    def __init__(self):
        self.front = None
        self.rear = None
        self.total_item = 0
        self.total_bayar = 0

    def is_empty(self):
        return self.front is None

    def tambah_barang(self, kode, nama, harga, qty):
        """Enqueue: Memasukkan barang baru ke keranjang belanja."""
        # Jika barang dengan kode yang sama sudah ada, kita update Qty-nya saja (sesuai langkah 3)
        sekarang = self.front
        while sekarang:
            if sekarang.kode == kode:
                sekarang.qty += qty
                self.hitung_ulang_total()
                return
            sekarang = sekarang.next

        baru_node = BarangNode(kode, nama, harga, qty)
        if self.is_empty():
            self.front = baru_node
            self.rear = baru_node
        else:
            self.rear.next = baru_node
            self.rear = baru_node
        self.hitung_ulang_total()

    def hitung_ulang_total(self):
        self.total_item = 0
        self.total_bayar = 0
        sekarang = self.front
        while sekarang:
            self.total_item += sekarang.qty
            self.total_bayar += (sekarang.harga * max(1, sekarang.qty))
            sekarang = sekarang.next

    def ke_dataframe(self):
        """Mengubah antrean barang menjadi tabel agar rapi di layar laptop kasir."""
        data = []
        sekarang = self.front
        while sekarang:
            data.append({
                "Kode/SKU": sekarang.kode,
                "Nama Barang": sekarang.nama,
                "Harga Satuan": f"Rp {sekarang.harga:,}",
                "Qty": sekarang.qty,
                "Subtotal": f"Rp {(sekarang.harga * sekarang.qty):,}"
            })
            sekarang = sekarang.next
        return pd.DataFrame(data)

    def reset_keranjang(self):
        self.front = None
        self.rear = None
        self.total_item = 0
        self.total_bayar = 0

# DATABASE MINI BARANG (Untuk simulasi scanner / ketik manual)
DB_BARANG = {
    "8991001": {"nama": "Air Mineral 600ml", "harga": 5000},
    "8991002": {"nama": "Roti Tawar Kupas", "harga": 15000},
    "8991003": {"nama": "Mie Instan Goreng", "harga": 3500},
    "8991004": {"nama": "Susu UHT Cokelat", "harga": 6000},
    "APEL": {"nama": "Apel Fuji (Per Kg)", "harga": 45000},
    "JERUK": {"nama": "Jeruk Mandarin (Per Kg)", "harga": 35000}
}

# ==========================================
# 2. CONFIG & THEME GRADASI WARNA
# ==========================================
st.set_page_config(page_title="Laptop Kasir - Supermarket POS", page_icon="💻", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
    }
    .kasir-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        color: #1e1e1e;
        margin-bottom: 20px;
    }
    .screen-total {
        background-color: #222;
        color: #00FF66;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 6px;
        font-size: 32px;
        text-align: right;
        font-weight: bold;
        border: 3px solid #444;
    }
    .struk-box {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Courier New', monospace;
        padding: 20px;
        border: 2px dashed #333;
        border-radius: 4px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'kasir_nama' not in st.session_state:
    st.session_state.kasir_nama = ""
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = KeranjangQueue()
if 'member_aktif' not in st.session_state:
    st.session_state.member_aktif = None
if 'diskon_voucher' not in st.session_state:
    st.session_state.diskon_voucher = 0
if 'halaman_bayar' not in st.session_state:
    st.session_state.halaman_bayar = False
if 'riwayat_struk' not in st.session_state:
    st.session_state.riwayat_struk = None

keranjang = st.session_state.keranjang

# ==========================================
# 4. INTERFACE APLIKASI KASIR
# ==========================================

# --- LANGKAH 1: LOGIN KASIR ---
if not st.session_state.is_logged_in:
    st.markdown('<div class="kasir-box">', unsafe_allow_html=True)
    st.subheader("🔐 LOGIN SISTEM KASIR LAPTOP")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username Kasir:", value="KASIR_01")
    with col2:
        password = st.text_input("Password:", type="password", value="1234")
    
    if st.button("Masuk ke Menu Penjualan (Log In)", type="primary"):
        if username and password == "1234":
            st.session_state.is_logged_in = True
            st.session_state.kasir_nama = username
            st.success("Berhasil masuk ke sistem transaksi!")
            st.rerun()
        else:
            st.error("Password salah! (Gunakan password default: 1234)")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Header Info Laptop Kasir Aktif
    st.sidebar.markdown(f"### 👤 Operator: {st.session_state.kasir_nama}")
    st.sidebar.markdown(f"📦 **Total Items:** {keranjang.total_item} Pcs")
    if st.sidebar.button("🚪 Log Out / Ganti Shift"):
        st.session_state.is_logged_in = False
        st.session_state.keranjang.reset_keranjang()
        st.rerun()

    # TAMPILAN UTAMA KASIR
    col_kiri, col_kanan = st.columns([7, 5])

    with col_kiri:
        st.markdown('<div class="kasir-box">', unsafe_allow_html=True)
        st.markdown("### 💻 MONITOR UTAMA TRANSAKSI")
        
        # Monitor Display Harga Besar ala Supermarket
        diskon_total = st.session_state.diskon_voucher + (int(keranjang.total_bayar * 0.05) if st.session_state.member_aktif else 0)
        total_akhir = max(0, keranjang.total_bayar - diskon_total)
        st.markdown(f'<div class="screen-total">TOTAL: Rp {total_akhir:,}</div>', unsafe_allow_html=True)
        st.write("")

        # --- LANGKAH 2 & 3: INPUT BARANG & UBAH QTY ---
        st.markdown("#### 📥 2 & 3. Input Barang Belanjaan & Qty")
        c1, c2, c3 = st.columns([5, 3, 4])
        with c1:
            input_kode = st.text_input("Barcode Scanner / Ketik Manual SKU / Nama Barang:", key="input_kode", placeholder="Contoh: 8991001 atau APEL")
        with c2:
            input_qty = st.number_input("Jumlah (Qty / Berat):", min_value=1, value=1, step=1)
        with c3:
            st.write("##")
            if st.button("⚡ Input ke Sistem (Enter)", use_container_width=True, type="secondary"):
                if input_kode:
                    kode_bersih = input_kode.strip()
                    if kode_bersih in DB_BARANG:
                        barang = DB_BARANG[kode_bersih]
                        keranjang.tambah_barang(kode_bersih, barang['nama'], barang['harga'], input_qty)
                        st.toast(f"Berhasil menginput {barang['nama']} sebanyak {input_qty}!")
                    else:
                        # Simulasi Cari Nama Manual
                        ditemukan = False
                        for k, v in DB_BARANG.items():
                            if kode_bersih.lower() in v['nama'].lower():
                                keranjang.tambah_barang(k, v['nama'], v['harga'], input_qty)
                                st.toast(f"Berhasil menginput {v['nama']} sebanyak {input_qty}!")
                                ditemukan = True
                                break
                        if not ditemukan:
                            st.error("Barang tidak terdaftar di database!")
        
        # Hint Kamus Database Mini untuk memudahkan Tester Tugas
        with st.expander("💡 Lihat Daftar Barcode/SKU Dummy Supermarket"):
            st.json(DB_BARANG)

        # Tabel Keranjang Belanja Aktif saat ini
        st.markdown("#### 🛒 Daftar Item di Keranjang")
        if not keranjang.is_empty():
            df_keranjang = keranjang.to_dataframe()
            st.dataframe(df_keranjang, use_container_width=True, hide_index=True)
        else:
            st.info("Keranjang kosong. Silakan scan atau masukkan barcode barang pembeli.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- LANGKAH 4: INPUT MEMBER / DISKON ---
        st.markdown('<div class="kasir-box">', unsafe_allow_html=True)
        st.markdown("#### 🎫 4. Input Kartu Member & Voucher Diskon")
        c_mem, c_voc = st.columns(2)
        with c_mem:
            no_member = st.text_input("Scan Kartu Member / No HP Pembeli:", placeholder="Masukkan No. HP (Dapat diskon 5%)")
            if no_member:
                st.session_state.member_aktif = no_member
                st.caption(f"✅ Member Terbaca: **{no_member}** (Diskon 5% Aktif)")
            else:
                st.session_state.member_aktif = None
        with c_voc:
            kode_voucher = st.text_input("Input Kupon Potongan Fisik (Voucher):", placeholder="Contoh: DISKON10K")
            if kode_voucher.upper() == "DISKON10K":
                st.session_state.diskon_voucher = 10000
                st.caption("✅ Voucher Valid: Potongan **Rp 10,000**")
            else:
                st.session_state.diskon_voucher = 0
        st.markdown('</div>', unsafe_allow_html=True)

    with col_kanan:
        # --- LANGKAH 5: MENU PEMBAYARAN ---
        st.markdown('<div class="kasir-box">', unsafe_allow_html=True)
        st.markdown("### 💳 5. Menu Pembayaran (Shortcut F12)")
        
        if keranjang.is_empty():
            st.warning("Masukkan barang terlebih dahulu untuk mengaktifkan menu pembayaran.")
        else:
            metode = st.radio("Pilih Metode Pembayaran Pembeli:", ["Tunai (Cash)", "Non-Tunai (Debit/Kredit/QRIS)"])
            
            st.divider()
            if metode == "Tunai (Cash)":
                st.info("💰 MODE TUNAI")
                uang_diterima = st.number_input("Uang Diterima / Cash Received (Rp):", min_value=0, step=5000, value=total_akhir)
                kembalian = uang_diterima - total_akhir
                
                if kembalian >= 0:
                    st.markdown(f"### 💵 Kembalian: **Rp {kembalian:,}**")
                else:
                    st.error(f"❌ Uang Kurang: Rp {abs(kembalian):,}")
            
            else:
                st.info("💳 MODE NON-TUNAI")
                st.markdown(f"Total Tagihan EDC: **Rp {total_akhir:,}**")
                no_ref = st.text_input("Masukkan Nomor Referensi (Trace/Ref Number dari Mesin EDC):", placeholder="Contoh: 123456")
                if not no_ref:
                    st.caption("⚠️ Masukkan nomor referensi struk EDC untuk memvalidasi pembayaran.")

            st.divider()
            
            # --- LANGKAH 6: CETAK STRUK & SELESAI ---
            st.markdown("#### 🖨️ 6. Finalisasi Transaksi")
            bisa_proses = False
            if metode == "Tunai (Cash)" and uang_diterima >= total_akhir:
                bisa_proses = True
            elif metode == "Non-Tunai (Debit/Kredit/QRIS)" and no_ref:
                bisa_proses = True

            if st.button("💥 SELESAI & CETAK STRUK (Press Enter)", type="primary", use_container_width=True, disabled=not bisa_proses):
                # Simpan struk ke state riwayat sebelum keranjang direset
                struk_items = []
                skrg = keranjang.front
                while skrg:
                    struk_items.append((skrg.nama, skrg.qty, skrg.harga))
                    skrg = skrg.next
                
                st.session_state.riwayat_struk = {
                    "kasir": st.session_state.kasir_nama,
                    "items": struk_items,
                    "subtotal": keranjang.total_bayar,
                    "diskon": diskon_total,
                    "total": total_akhir,
                    "metode": metode,
                    "bayar": uang_diterima if metode == "Tunai (Cash)" else total_akhir,
                    "kembali": kembalian if metode == "Tunai (Cash)" else 0,
                    "member": st.session_state.member_aktif,
                    "ref": no_ref if metode == "Non-Tunai (Debit/Kredit/QRIS)" else "-"
                }
                
                # Simulasi Laci Kasir Terbuka otomatis & Reset Layar Bersih kembali ke awal
                st.balloons()
                if metode == "Tunai (Cash)":
                    st.toast("🔓 [KLIK!] Laci Kas (Cash Drawer) otomatis terbuka!")
                
                keranjang.reset_keranjang()
                st.session_state.member_aktif = None
                st.session_state.diskon_voucher = 0
                st.success("Transaksi Sukses! Layar dibersihkan untuk antrean berikutnya.")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # BOX SIMULATOR PRINTER NOTA / STRUK FISIK YANG KELUAR
        if st.session_state.riwayat_struk:
            st.markdown("#### 📜 Struk Fisik Terakhir Terpindai (Hasil Cetak Printer)")
            r = st.session_state.riwayat_struk
            st.markdown('<div class="struk-box">', unsafe_allow_html=True)
            st.markdown("<center><b>SUPERMARKET MAJU JAYA</b><br>Jakarta Selatan</center>", unsafe_allow_html=True)
            st.text("-" * 38)
            st.text(f"Kasir : {r['kasir']}")
            st.text(f"Member: {r['member'] if r['member'] else '-'}")
            st.text("-" * 38)
            for nama, qty, harga in r['items']:
                st.text(f"{nama[:20]:<20} {qty:>2}x  Rp{harga:>6,}")
            st.text("-" * 38)
            st.text(f"Subtotal          : Rp {r['subtotal']:,}")
            st.text(f"Diskon/Potongan   : Rp {r['diskon']:,}")
            st.text(f"TOTAL AKHIR       : Rp {r['total']:,}")
            st.text(f"Metode Bayar      : {r['metode']}")
            st.text(f"Bayar             : Rp {r['bayar']:,}")
            st.text(f"Kembalian         : Rp {r['kembali']:,}")
            if r['ref'] != "-":
                st.text(f"No. Ref EDC       : {r['ref']}")
            st.text("-" * 38)
            st.markdown("<center>TERIMA KASIH<br>Selamat Belanja Kembali!</center>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Clear Riwayat Cetakan Struk"):
                st.session_state.riwayat_struk = None
                st.rerun()