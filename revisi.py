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
st.write("Menemukan posisi rak (indeks array) berdasarkan HARGA Produk — Bebas pilih algoritma!")

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

# ========== MEMBUAT DATA PRODUK ==========

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
    
    for i in range(n):
        kategori = local_random.choice(["Makanan", "Minuman"])
        nama_dasar = local_random.choice(list_makanan) if kategori == "Makanan" else local_random.choice(list_minuman)
        
        products.append({
            'id': i + 1,
            'nama': f"{nama_dasar} (ID: {i+1})", 
            'kategori': kategori,
            'harga': local_random.randint(5000, 50000), 
            'rak': i
        })
    return products

@st.cache_data
def dapatkan_data_gudang(kondisi_sort, filter_kat, _produk_dasar, jml_prd):
    # 1. Ambil data sesuai kuota slider sidebar
    produk_terpotong = _produk_dasar[:jml_prd]
    
    # 2. Filter berdasarkan kategori menu utama
    if filter_kat == "🍔 Makanan Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Makanan"]
    elif filter_kat == "🥤 Minuman Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Minuman"]
    else:
        data_lokal = produk_terpotong.copy()
        
    # 3. ✨ OPERASI SORTING BARU (Berdasarkan Harga & Kategori) ✨
    if kondisi_sort == "📉 Harga: Termurah ──> Termahal":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'])
    elif kondisi_sort == "📈 Harga: Termahal ──> Termurah":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'], reverse=True)
    elif kondisi_sort == "🗂️ Berdasarkan Kategori (Makanan dulu)":
        data_lokal = sorted(data_lokal, key=lambda x: (x['kategori'], x['harga']))
    else:
        # Default fallback jika tidak ada yang terpilih
        data_lokal = sorted(data_lokal, key=lambda x: x['id'])
        
    # Update posisi indeks rak saat ini (dimulai dari 0 untuk komputer)
    for indeks_baru, produk in enumerate(data_lokal):
        produk['rak_sekarang'] = indeks_baru 
        
    return data_lokal

# ========== 3 ALGORITMA PENCARIAN (BERDASARKAN PROPERTI HARGA) ==========

def linear_search(data, target_harga):
    langkah = 0 
    for i, produk in enumerate(data):
        langkah += 1
        if produk['harga'] == target_harga:
            return i, langkah
    return -1, langkah

def binary_search(data, target_harga, is_descending=False):
    langkah = 0
    left, right = 0, len(data) - 1
    while left <= right:
        langkah += 1
        mid = (left + right) // 2
        if data[mid]['harga'] == target_harga:
            return mid, langkah
        
        # Penyesuaian arah cek jika datanya terurut terbalik (termahal ke termurah)
        if not is_descending:
            if data[mid]['harga'] < target_harga:
                left = mid + 1
            else:
                right = mid - 1
        else:
            if data[mid]['harga'] > target_harga:
                left = mid + 1
            else:
                right = mid - 1
    return -1, langkah

def interpolation_search(data, target_harga, is_descending=False):
    langkah = 0
    low = 0
    high = len(data) - 1
    
    # Cek batas agar rumus estimasi tidak error keluar index
    if not is_descending:
        if target_harga < data[low]['harga'] or target_harga > data[high]['harga']:
            return -1, 0
    else:
        if target_harga > data[low]['harga'] or target_harga < data[high]['harga']:
            return -1, 0

    while low <= high:
        langkah += 1
        if data[high]['harga'] == data[low]['harga']:
            if data[low]['harga'] == target_harga:
                return low, langkah
            break
        
        pembagi = data[high]['harga'] - data[low]['harga']
        if pembagi == 0: break
            
        pos = low + int(((float(high - low) / pembagi) * (target_harga - data[low]['harga'])))
        if pos < low or pos > high:
            break
            
        if data[pos]['harga'] == target_harga:
            return pos, langkah
            
        if not is_descending:
            if data[pos]['harga'] < target_harga:
                low = pos + 1
            else:
                high = pos - 1
        else:
            if data[pos]['harga'] > target_harga:
                low = pos + 1
            else:
                high = pos - 1
    return -1, langkah

# ========== Navigation Halaman State ==========
if 'halaman_sekarang' not in st.session_state:
    st.session_state.halaman_sekarang = 1
if 'pencarian_dimulai' not in st.session_state:
    st.session_state.pencarian_dimulai = False
if 'harga_dipilih' not in st.session_state:
    st.session_state.harga_dipilih = 5000

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
    # ✨ MENU SIDEBAR SORTING BARU ✨
    st.subheader("📦 Pengurutan Data Gudang (Sorting)")
    kondisi_data = st.radio(
        "Urutkan susunan data rak berdasarkan:", 
        [
            "📉 Harga: Termurah ──> Termahal", 
            "📈 Harga: Termahal ──> Termurah", 
            "🗂️ Berdasarkan Kategori (Makanan dulu)"
        ]
    )

# Load data sesuai setingan database
products_master = generate_products(jumlah_produk)
data_list = dapatkan_data_gudang(kondisi_data, filter_kategori, products_master, jumlah_produk)
harga_tersedia = [p['harga'] for p in data_list]

# Informasi Atas mengenai item yang aktif
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info(f"📊 **Kondisi Pengurutan Gudang:** {kondisi_data}")
with col_info2:
    st.warning(f"💡 **Total Produk Aktif Sesuai Filter Kategori:** {len(data_list)} Items")

# ========== INTERMUKA INPUT PENCARIAN HARGA ==========
st.divider()
st.subheader("🔎 Cari Berdasarkan Harga")

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
with col1:
    target_harga = st.number_input(
        "Masukkan Nominal Harga Produk yang dicari (Rp): ", 
        min_value=5000, 
        max_value=50000, 
        value=st.session_state.harga_dipilih,
        step=500,
        key="harga_produk_input"
    )

with col2:
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

# ========== EKSEKUSI SEARCHING OPERASI ==========
if cari_button:
    st.session_state.pencarian_dimulai = True
    st.session_state.harga_dipilih = st.session_state.harga_produk_input
    
    target_harga = st.session_state.harga_dipilih
    
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    # Validasi keberadaan harga produk di rak saat ini
    if target_harga not in harga_tersedia:
        st.error(f"❌ Produk dengan harga Rp {target_harga:,.0f} tidak ditemukan pada susunan rak saat ini!")
        st.caption("💡 Petunjuk: Silakan lihat daftar tabel di bawah untuk melihat pilihan nominal harga yang tersedia di rak saat ini.")
    else:
        # Validasi kecocokan algoritma dengan syarat sorting
        is_sorted_harga = "Harga:" in kondisi_data
        is_desc = "Termahal" in kondisi_data
        
        if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and not is_sorted_harga:
            st.error("❌ **Gagal Eksekusi:** Algoritma Binary & Interpolation Search mutlak membutuhkan data yang terurut berdasarkan **Harga** (bukan berdasarkan Kategori)!")
        else:
            indeks_ditemukan = -1
            
            # 1. LINEAR SEARCH
            if "Linear Search" in algoritma_terpilih:
                with st.spinner("Menjalankan Linear Search..."):
                    start_time = time.time()
                    indeks, langkah = linear_search(data_list, target_harga)
                    waktu = (time.time() - start_time) * 1000
                st.success(f"✅ **Algoritma: Linear Search (O(n))**")
                col_a, col_b, col_c = st.columns(3)
                with col_a: st.metric("Posisi Rak (Indeks)", indeks)
                with col_b: st.metric("Jumlah Langkah", langkah)
                with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
                indeks_ditemukan = indeks
                    
            # 2. BINARY SEARCH
            elif "Binary Search" in algoritma_terpilih:
                with st.spinner("Menjalankan Binary Search..."):
                    start_time = time.time()
                    indeks, langkah = binary_search(data_list, target_harga, is_descending=is_desc)
                    waktu = (time.time() - start_time) * 1000
                st.success(f"✅ **Algoritma: Binary Search (O(log n))**")
                col_a, col_b, col_c = st.columns(3)
                with col_a: st.metric("Posisi Rak (Indeks)", indeks)
                with col_b: st.metric("Jumlah Langkah", langkah)
                with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
                indeks_ditemukan = indeks
            
            # 3. INTERPOLATION SEARCH
            else:
                with st.spinner("Menjalankan Interpolation Search..."):
                    start_time = time.time()
                    indeks, langkah = interpolation_search(data_list, target_harga, is_descending=is_desc)
                    waktu = (time.time() - start_time) * 1000
                st.success(f"✅ **Algoritma: Interpolation Search (O(log (log n)))**")
                col_a, col_b, col_c = st.columns(3)
                with col_a: st.metric("Posisi Rak (Indeks)", indeks)
                with col_b: st.metric("Jumlah Langkah", langkah)
                with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
                indeks_ditemukan = indeks

            if indeks_ditemukan != -1:
                produk = data_list[indeks_ditemukan]
                nomor_urut_barang = indeks_ditemukan + 1  
                posisi_indeks_array = indeks_ditemukan     
                
                st.markdown(f"""
                <div class="hasil-card">
                    <h4>📦 Spesifikasi Item Ditemukan</h4>
                    <p><b>Nama Barang:</b> {produk['nama']}</p>
                    <p><b>Kategori:</b> {produk['kategori']}</p>
                    <p><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
                    <hr style="border: 0.5px solid #555; margin: 10px 0;">
                    <p style="color: #60a5fa;"><b>🔢 Nomor Urut Barang:</b> {nomor_urut_barang}</p>
                    <p style="color: #fca5a5;"><b>💻 Posisi Indeks Array:</b> {posisi_indeks_array}</p>
                </div>
                """, unsafe_allow_html=True)

                # Melompat ke halaman tabel otomatis tempat item berada
                baris_per_halaman = 10
                halaman_tujuan = (indeks_ditemukan // baris_per_halaman) + 1
                if st.session_state.halaman_sekarang != halaman_tujuan:
                    st.session_state.halaman_sekarang = halaman_tujuan
                    st.rerun()

# Reset status hijau tabel jika user mengubah angka input pencarian
if st.session_state.harga_produk_input != st.session_state.harga_dipilih:
    st.session_state.pencarian_dimulai = False

# ========== EXPANDER DEMO PERBANDINGAN ALGORITMA ==========
st.divider()
with st.expander("🔬 Perbandingkan Ketiga Algoritma Sekaligus"):
    st.write("Lihat perbandingan kecepatan 3 algoritma secara real-time berdasarkan susunan rak aktif")
    bandingkan_button = st.button("📊 Bandingkan Semua Algoritma", use_container_width=True, key="btn_banding")
    if bandingkan_button:
        current_target = st.session_state.harga_dipilih
        if current_target not in harga_tersedia:
            st.error("Nominal harga tersebut tidak tersedia pada kombinasi rak saat ini.")
        elif "Harga:" not in kondisi_data:
            st.error("Perbandingan simultan diblokir: Data harus diurutkan berdasarkan Harga terlebih dahulu agar Binary & Interpolation tidak mengalami kegagalan logika loop!")
        else:
            is_desc = "Termahal" in kondisi_data
            start = time.time(); idx_l, steps_l = linear_search(data_list, current_target); t_l = (time.time() - start) * 1000
            start = time.time(); idx_b, steps_b = binary_search(data_list, current_target, is_descending=is_desc); t_b = (time.time() - start) * 1000
            start = time.time(); idx_i, steps_i = interpolation_search(data_list, current_target, is_descending=is_desc); t_i = (time.time() - start) * 1000
            
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
    
    # Fungsi mewarnai baris tabel yang memiliki kecocokan harga pencarian
    def beri_warna_baris(row):
        if st.session_state.pencarian_dimulai and row['Harga'] == f"Rp {st.session_state.harga_dipilih:,.0f}" and st.session_state.harga_dipilih in harga_tersedia:
            return ['background-color: #15803d; color: white; font-weight: bold;'] * len(row)
        return [''] * len(row)
    
    df_berwarna = df_halaman.style.apply(beri_warna_baris, axis=1)
    st.dataframe(df_berwarna, use_container_width=True, hide_index=True)

# ========== FOOTER INFORMASI TEKNIS ==========
with st.expander("ℹ️ Penjelasan 3 Algoritma Searching Berdasarkan Harga"):
    st.markdown("""
    **1. Linear Search** — Memeriksa nilai harga satu per satu dari rak awal hingga akhir. Tetap berfungsi optimal terlepas dari apakah susunan harga di gudang sudah disorting atau masih acak.\n
    **2. Binary Search** — Memotong data susunan rak menjadi setengah bagian terus menerus. Algoritma ini mewajibkan data terurut secara numerik berdasarkan **Harga** (baik dari murah ke mahal, atau sebaliknya).\n
    **3. Interpolation Search** — Memprediksi letak posisi harga menggunakan rumus matematika jarak nilai. Sangat kilat jika rentang sebaran harga produk di gudang terdistribusi secara merata.
    """)

st.divider()
st.subheader("💡 Analisis Kombinasi Pilihan Algoritma & Filter")
col_rec1, col_rec2 = st.columns(2)
with col_rec1:
    st.markdown(f"**Algoritma yang aktif:** {algoritma_terpilih.split('(')[0].strip()}")
    st.markdown(f"**Metode Pengurutan (Sorting):** {kondisi_data}")
    st.markdown(f"**Filter Kategori Produk:** {filter_kategori}")
with col_rec2:
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and "Harga:" not in kondisi_data:
        st.error("❌ **Kombinasi Tidak Valid:** Interpolation/Binary Search mutlak memerlukan struktur data yang TERURUT BERDASARKAN HARGA agar kalkulasi rumusnya bekerja.")
    else:
        st.success("✅ **Kombinasi Logis Sempurna:** Algoritma yang Anda pilih bekerja secara harmonis dengan struktur pengurutan data pendukung.")

st.caption(f"🔄 Halaman diperbarui secara statis | Waktu Sistem: {time.strftime('%Y-%m-%d %H:%M:%S')}")