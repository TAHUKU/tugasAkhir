import streamlit as st
import random
import time
import pandas as pd
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Algoritma Gudang",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Analisis Algoritma SEARCHING dan SORTING Berbasis Web")
st.write("Menemukan posisi rak (indeks array) berdasarkan Nama, Kategori, atau Harga Produk — Bebas pilih algoritma!")

st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #22c55e !important;
        color: white !important;
        border-radius: 8px;
        border: none !important;
        transition: background-color 0.3s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #16a34a !important;
    }
    .hasil-card {
        background-color: #000000 !important;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #22c55e;
        margin-top: 15px;
    }
    .hasil-card p, .hasil-card h4, .hasil-card b {
        color: #ffffff !important;
    }
    .footer-fixed {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #ffffff;
        text-align: center;
        padding: 10px 0;
        font-size: 12px;
        border-top: 1px solid #262730;
        z-index: 999;
    }
    </style>
    <div class="footer-fixed">
        <p style="margin:0;">🔍 Sistem Pencarian Produk Gudang Digital — Hakkul IT 2026.</p>
    </div>
""", unsafe_allow_html=True)

# ========== MEMBUAT DATA PRODUK (FIXED INDENTASI & RETURN VALUE) ==========

@st.cache_data
def generate_products(n=500):
    list_makanan = [
        "Nasi Goreng", "Mie Ayam", "Bakso Sapi", "Sate Ayam", "Ayam Goreng", 
        "Roti Bakar", "Keripik Singkong", "Biskuit Cokelat", "Martabak Manis", 
        "Gado-Gado", "Soto Betawi", "Rendang Padang", "Siomay Bandung", "Batagor"
    ]
    list_minuman = [
        "Es Teh Manis", "Kopi Susu", "Jus Alpukat", "Air Mineral", "Teh Tarik", 
        "Es Jeruk", "Susu UHT", "Soda Gembira", "Matcha Latte", "Es Dawet", 
        "Kopi Hitam", "Lemon Tea", "Smoothie Mangga", "Wedang Jahe"
    ]
    
    products = []
    local_random = random.Random(100) 
    
    # PERBAIKAN: Seluruh proses di bawah ini MASUK ke dalam loop 'for'
    for i in range(n):
        kategori = local_random.choice(["Makanan", "Minuman"])
        
        nama_dasar = (
            local_random.choice(list_makanan)
            if kategori == "Makanan"
            else local_random.choice(list_minuman)
        )
        
        # PERMINTAAN ANDA: Harga dibuat bulat kelipatan Rp 1.000 (5000, 6000, 7000, dst.)
        harga_bulat = 5000 + (i * 1000)
        
        products.append({
            'id': i + 1,
            'nama': f"{nama_dasar} (ID: {i+1})",
            'kategori': kategori,
            'harga': harga_bulat,
            'rak': i
        })
        
    return products # WAJIB ADA: Mengirimkan data kembali ke aplikasi# MEMBENARKAN: Mengembalikan list data ke sistem Gudang

@st.cache_data
def dapatkan_data_gudang(kondisi_sort, filter_kat, _produk_dasar, jml_prd):
    produk_terpotong = _produk_dasar[:jml_prd]
    
    if filter_kat == "🍔 Makanan Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Makanan"]
    elif filter_kat == "🥤 Minuman Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Minuman"]
    else:
        data_lokal = produk_terpotong.copy()
        
    # ========== OPERASI SORTING LENGKAP ==========
    if kondisi_sort == "📉 Harga: Termurah ──> Termahal":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'])
    elif kondisi_sort == "📈 Harga: Termahal ──> Termurah":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'], reverse=True)
    elif kondisi_sort == "🔤 Nama Produk (A ──> Z)":
        data_lokal = sorted(data_lokal, key=lambda x: x['nama'].lower())
    elif kondisi_sort == "🗂️ Berdasarkan Kategori (Makanan dulu)":
        data_lokal = sorted(data_lokal, key=lambda x: (x['kategori'], x['harga']))
    else:
        data_lokal = sorted(data_lokal, key=lambda x: x['id'])
        
    for indeks_baru, produk in enumerate(data_lokal):
        produk['rak_sekarang'] = indeks_baru 
        
    return data_lokal

# ========== 3 ALGORITMA PENCARIAN ADAPTIF (FIXED LOGIKA ASCENDING) ==========

def linear_search(data, target, key_cari):
    langkah = 0 
    for i, produk in enumerate(data):
        langkah += 1
        val_data = str(produk[key_cari]).lower() if key_cari != 'harga' else produk[key_cari]
        val_target = str(target).lower() if key_cari != 'harga' else target
        
        if key_cari != 'harga':
            if val_target in val_data:  
                return i, langkah
        else:
            if int(val_data) == int(val_target):
                return i, langkah
    return -1, langkah

def binary_search(data, target, key_cari, is_descending=False):
    langkah = 0
    left, right = 0, len(data) - 1
    
    if key_cari == 'harga':
        val_target = int(target) # Perbaikan: Membandingkan angka matematika murni
    else:
        val_target = str(target).lower()
    
    while left <= right:
        langkah += 1
        mid = (left + right) // 2
        
        if key_cari == 'harga':
            val_mid = int(data[mid][key_cari])
        else:
            val_mid = str(data[mid][key_cari]).lower()
        
        if val_mid == val_target:
            return mid, langkah
        
        if not is_descending: # Jalur jika data dari Termurah ke Termahal (Ascending)
            if val_mid < val_target:
                left = mid + 1
            else:
                right = mid - 1
        else:                 # Jalur jika data dari Termahal ke Termurah (Descending)
            if val_mid > val_target:
                left = mid + 1
            else:
                right = mid - 1
    return -1, langkah

def interpolation_search(data, target, key_cari, is_descending=False):
    langkah = 0
    low = 0
    high = len(data) - 1
    
    if key_cari == 'harga':
        target_val = int(target)
    else:
        target_val = ord(str(target)[0].lower()) if target else 0
        
    def get_numeric_value(item):
        if key_cari == 'harga':
            return int(item['harga']) # Angka matematika asli untuk perhitungan jarak
        return ord(str(item[key_cari])[0].lower()) if item[key_cari] else 0
        
    if low > high:
        return -1, 0
        
    low_val = get_numeric_value(data[low])
    high_val = get_numeric_value(data[high])
    
    if not is_descending:
        if target_val < low_val or target_val > high_val:
            return -1, 0
    else:
        if target_val > low_val or target_val < high_val:
            return -1, 0

    while low <= high:
        langkah += 1
        low_val = get_numeric_value(data[low])
        high_val = get_numeric_value(data[high])
        
        if high_val == low_val:
            if key_cari == 'harga':
                if int(data[low]['harga']) == target_val: return low, langkah
            else:
                if str(data[low][key_cari]).lower() == str(target).lower(): return low, langkah
            break
        
        # Rumus posisi interpolasi angka murni terbebas dari bias string
        pos = low + int(((float(high - low) / (high_val - low_val)) * (target_val - low_val)))
        if pos < low or pos > high:
            break
            
        if key_cari == 'harga':
            val_pos = int(data[pos]['harga'])
        else:
            val_pos = str(data[pos][key_cari]).lower()
            
        actual_target = target_val if key_cari == 'harga' else str(target).lower()
        
        if val_pos == actual_target:
            return pos, langkah
            
        if not is_descending:
            if val_pos < actual_target:
                low = pos + 1
            else:
                high = pos - 1
        else:
            if val_pos > actual_target:
                low = pos + 1
            else:
                high = pos - 1
    return -1, langkah

# ========== NAVIGATION STATE ==========
if 'halaman_sekarang' not in st.session_state:
    st.session_state.halaman_sekarang = 1
if 'pencarian_dimulai' not in st.session_state:
    st.session_state.pencarian_dimulai = False
if 'target_terpilih' not in st.session_state:
    st.session_state.target_terpilih = ""
if 'indeks_ditemukan' not in st.session_state:
    st.session_state.indeks_ditemukan = -1

def ke_halaman_sebelumnya():
    if st.session_state.halaman_sekarang > 1:
        st.session_state.halaman_sekarang -= 1

def ke_halaman_selanjutnya():
    st.session_state.halaman_sekarang += 1

# ========== SIDEBAR CONFIGURATION ==========
with st.sidebar:
    st.header("⚙️ Pengaturan")
    jumlah_produk = st.slider("Jumlah produk di gudang:", min_value=100, max_value=1000, value=250, step=100)
    
    st.divider()
    st.subheader("🛒 Filter Kategori Utama")
    filter_kategori = st.radio(
        "Tampilkan kategori produk:",
        ["🔄 Campuran (Semua)", "🍔 Makanan Saja", "🥤 Minuman Saja"]
    )
    
    st.divider()
    st.subheader("🎯 Pilih Algoritma Pencarian")
    algoritma_terpilih = st.radio("Pilih algoritma yang ingin digunakan:", ["🔍 Linear Search", "📚 Binary Search", "⚡ Interpolation Search"])
    
    st.divider()
    st.subheader("📦 Pengurutan Data Gudang (Sorting)")
    kondisi_data = st.radio(
        "Urutkan susunan data rak berdasarkan:", 
        [
            "📉 Harga: Termurah ──> Termahal", 
            "📈 Harga: Termahal ──> Termurah", 
            "🔤 Nama Produk (A ──> Z)",
            "🗂️ Berdasarkan Kategori (Makanan dulu)"
        ]
    )
    # Letakkan ini di bagian paling bawah blok 'with st.sidebar:'
    st.divider()
    if st.button("♻️ Paksa Reset Data & Cache", use_container_width=True):
        st.cache_data.clear() # Menghapus semua memori cache Streamlit
        st.rerun()

# Load data
products_master = generate_products(jumlah_produk)
data_list = dapatkan_data_gudang(kondisi_data, filter_kategori, products_master, jumlah_produk)

# Informasi Atas mengenai item yang aktif
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info(f"📊 **Kondisi Pengurutan Gudang:** {kondisi_data}")
with col_info2:
    st.warning(f"💡 **Total Produk Aktif Sesuai Filter Kategori:** {len(data_list)} Items")

# ========== INTERMUKA INPUT MULTI-KATEGORI PENCARIAN ==========
st.divider()
st.subheader("🔎 Menu Operasi Pencarian Pintar")

kategori_pencarian = st.selectbox(
    "Pilih Parameter Variabel Pencarian:",
    ["Nominal Harga Barang (Angka Bulat)", "Nama Spesifik Produk (Huruf/Teks)", "Kategori Menu (Makanan / Minuman)"]
)

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    if "Harga" in kategori_pencarian:
        key_cari = 'harga'
        maks_harga_dinamis = int(5000 + (jumlah_produk * 1000))
        target_input = st.number_input("Masukkan Nominal Harga Produk (Kelipatan Rp 1.000): ", min_value=5000, max_value=maks_harga_dinamis, value=5000, step=1000)
    elif "Nama" in kategori_pencarian:
        key_cari = 'nama'
        target_input = st.text_input("Masukkan Kata Kunci Nama Makanan/Minuman (Contoh: Nasi Goreng, Ayam):", value="Nasi Goreng")
    else:
        key_cari = 'kategori'
        target_input = st.selectbox("Pilih Kategori:", ["Makanan", "Minuman"])

with col2:
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

# ========== EKSEKUSI SEARCHING OPERASI ==========
if cari_button:
    st.session_state.pencarian_dimulai = True
    st.session_state.target_terpilih = str(target_input) # Merekam input yang benar-benar diketik user
    
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    valid_sort = False
    if "Harga" in kondisi_data and key_cari == 'harga':
        valid_sort = True
    elif "Nama" in kondisi_data and key_cari == 'nama':
        valid_sort = True
    elif "Kategori" in kondisi_data and key_cari == 'kategori':
        valid_sort = True

    # Tentukan arah DESC/ASC secara akurat berdasarkan pilihan radio
    is_desc = kondisi_data == "📈 Harga: Termahal ──> Termurah"

    
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and not valid_sort:
        st.error(f"❌ **Gagal Eksekusi:** Algoritma Binary atau Interpolation Search mendesak data terurut berdasarkan kunci pencarian yang sama! Struktur urutan saat ini ({kondisi_data}) tidak sesuai dengan variabel pencarian ({key_cari.upper()}).")
    else:
        indeks_ditemukan = -1
        
        if "Linear Search" in algoritma_terpilih:
            with st.spinner("Menjalankan Linear Search..."):
                start_time = time.time()
                indeks, langkah = linear_search(data_list, target_input, key_cari)
                waktu = (time.time() - start_time) * 1000
            nama_algo_info = "Linear Search (O(n))"
            indeks_ditemukan = indeks
            st.session_state.indeks_ditemukan = indeks
                
        elif "Binary Search" in algoritma_terpilih:
            with st.spinner("Menjalankan Binary Search..."):
                start_time = time.time()
                indeks, langkah = binary_search(data_list, target_input, key_cari, is_descending=is_desc)
                waktu = (time.time() - start_time) * 1000
            nama_algo_info = "Binary Search (O(log n))"
            indeks_ditemukan = indeks
            st.session_state.indeks_ditemukan = indeks
        
        else:
            with st.spinner("Menjalankan Interpolation Search..."):
                start_time = time.time()
                indeks, langkah = interpolation_search(data_list, target_input, key_cari, is_descending=is_desc)
                waktu = (time.time() - start_time) * 1000
            nama_algo_info = "Interpolation Search (O(log (log n)))"
            indeks_ditemukan = indeks
            st.session_state.indeks_ditemukan = indeks

        if indeks_ditemukan != -1:
            st.success(f"✅ **Algoritma Berhasil: {nama_algo_info}**")
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("Posisi Rak (Indeks Array)", indeks_ditemukan)
            with col_b: st.metric("Jumlah Langkah Komputasi", langkah)
            with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
            
            produk = data_list[indeks_ditemukan]
            st.markdown(f"""
            <div class="hasil-card">
                <h4>📦 Spesifikasi Item Ditemukan</h4>
                <p><b>Nama Barang:</b> {produk['nama']}</p>
                <p><b>Kategori:</b> {produk['kategori']}</p>
                <p><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
                <hr style="border: 0.5px solid #555; margin: 10px 0;">
                <p style="color: #60a5fa;"><b>🔢 Nomor Urut Daftar Barang:</b> {indeks_ditemukan + 1}</p>
                <p style="color: #fca5a5;"><b>💻 Posisi Indeks Array Komputer:</b> {indeks_ditemukan}</p>
            </div>
            """, unsafe_allow_html=True)

            baris_per_halaman = 10
            halaman_tujuan = (indeks_ditemukan // baris_per_halaman) + 1
            if st.session_state.halaman_sekarang != halaman_tujuan:
                st.session_state.halaman_sekarang = halaman_tujuan
                st.rerun()
        else:
            st.session_state.indeks_ditemukan = -1
            st.error(f"❌ Kriteria produk dengan data '{target_input}' tidak berhasil diidentifikasi di struktur rak aktif saat ini.")

if str(target_input) != st.session_state.target_terpilih:
    st.session_state.pencarian_dimulai = False
    st.session_state.indeks_ditemukan = -1

# ========== EXPANDER DEMO PERBANDINGAN ALGORITMA ==========
st.divider()
with st.expander("🔬 Perbandingkan Ketiga Algoritma Sekaligus"):
    st.write("Lihat perbandingan kecepatan 3 algoritma secara simultan berdasarkan susunan rak aktif")
    if st.button("📊 Bandingkan Semua Algoritma", use_container_width=True, key="btn_banding"):
        if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and not valid_sort:
            st.error("Proses perbandingan komparatif gagal: Kondisi sorting data gudang di sidebar harus disesuaikan terlebih dahulu agar setara dengan jenis kata kunci yang Anda masukkan saat ini.")
        else:
            start = time.time(); idx_l, steps_l = linear_search(data_list, target_input, key_cari); t_l = (time.time() - start) * 1000
            start = time.time(); idx_b, steps_b = binary_search(data_list, target_input, key_cari, is_descending=is_desc); t_b = (time.time() - start) * 1000
            start = time.time(); idx_i, steps_i = interpolation_search(data_list, target_input, key_cari, is_descending=is_desc); t_i = (time.time() - start) * 1000
            
            comparison_data = {
                "Algoritma": ["Linear Search", "Binary Search", "Interpolation Search"],
                "Ditemukan": ["✅" if idx_l != -1 else "❌", "✅" if idx_b != -1 else "❌", "✅" if idx_i != -1 else "❌"],
                "Posisi Indeks Rak": [idx_l, idx_b, idx_i],
                "Langkah": [steps_l, steps_b, steps_i],
                "Waktu (ms)": [f"{t_l:.3f}", f"{t_b:.3f}", f"{t_i:.3f}"]
            }
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

# ========== TABEL UTAMA DATA PRODUK ==========
with st.expander("📋 Lihat Semua Data Produk", expanded=True):
    df = pd.DataFrame(data_list)
    if not df.empty:
        df_display = df[['id', 'nama', 'kategori', 'harga', 'rak_sekarang']].copy()
        df_display['Harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
        df_display = df_display.rename(columns={
            'id': 'ID Produk', 
            'nama': 'Nama Produk', 
            'kategori': 'Kategori', 
            'rak_sekarang': 'Posisi Indeks Array'
        })
        
        kolom_tampil = ['ID Produk', 'Nama Produk', 'Kategori', 'Harga', 'Posisi Indeks Array']
        baris_per_halaman = 10
        total_data = len(df_display)
        total_halaman = math.ceil(total_data / baris_per_halaman)
        
        if st.session_state.halaman_sekarang > total_halaman:
            st.session_state.halaman_sekarang = 1

        col_prev, col_info, col_next = st.columns([1, 4, 1])
        with col_prev:
            st.button("⬅️ Sebelumnya", use_container_width=True, disabled=(st.session_state.halaman_sekarang == 1), on_click=ke_halaman_sebelumnya, key="nav_prev")
        with col_info:
            st.markdown(f"""
                <div style='text-align: center; padding-top: 5px;'>
                    Halaman <b>{st.session_state.halaman_sekarang}</b> dari <b>{total_halaman}</b> <br>
                    <span style='color: gray; font-size: 0.85rem;'>Menampilkan data ke-{((st.session_state.halaman_sekarang-1) * baris_per_halaman) + 1} sampai {min(st.session_state.halaman_sekarang * baris_per_halaman, total_data)} dari {total_data} produk</span>
                </div>
            """, unsafe_allow_html=True)
        with col_next:
            st.button("Selanjutnya ➡️", use_container_width=True, disabled=(st.session_state.halaman_sekarang == total_halaman), on_click=ke_halaman_selanjutnya, key="nav_next")
                
        st.write("") 
        
        start_idx = (st.session_state.halaman_sekarang - 1) * baris_per_halaman
        end_idx = start_idx + baris_per_halaman
        df_halaman = df_display.iloc[start_idx:end_idx][kolom_tampil].copy()
        
        nomor_urut = list(range(start_idx + 1, start_idx + len(df_halaman) + 1))
        df_halaman.insert(0, 'No', nomor_urut)
        
        def beri_warna_baris(row):
            if st.session_state.pencarian_dimulai and st.session_state.indeks_ditemukan != -1:
                match_found = False
                if key_cari == 'harga' and row['Harga'] == f"Rp {int(st.session_state.target_terpilih):,.0f}":
                    match_found = True
                elif key_cari == 'nama' and st.session_state.target_terpilih.lower() in row['Nama Produk'].lower():
                    match_found = True
                elif key_cari == 'kategori' and row['Kategori'].lower() == st.session_state.target_terpilih.lower():
                    match_found = True
                    
                if match_found:
                    return ['background-color: #15803d; color: white; font-weight: bold;'] * len(row)
            return [''] * len(row)
        
        df_berwarna = df_halaman.style.apply(beri_warna_baris, axis=1)
        st.dataframe(df_berwarna, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Tidak ada data untuk ditampilkan di dalam gudang.")

# ========== FOOTER INFORMASI TEKNIS ==========
with st.expander("ℹ️ Panduan Karakteristik Pencarian"):
    st.markdown("""
    * **Jaminan Deteksi**: Angka dan huruf dibandingkan secara terpisah sesuai aturan tipe data primitif, memperbaiki error komparasi string biner di mode urutan menaik.
    """)