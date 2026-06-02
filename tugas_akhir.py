import streamlit as st
import random
import time
import pandas as pd
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="3 Algoritma Pencarian Produk",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Analisis Algoritma SEARCHING dan SORTING Berbasis Web")
st.write("Menemukan posisi rak (indeks array) berdasarkan ID Produk - Bebas pilih algoritma yang tersdia")

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

# ========== MEMBUAT DATA PRODUK (NAMA MAKANAN & MINUMAN REALISTIS) ==========
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
    # Menggunakan seed lokal di generator agar nama yang terbuat selalu konsisten setiap di-generate
    local_random = random.Random(100) 
    
    for i in range(n):
        kategori = local_random.choice(["Makanan", "Minuman"])
        nama_dasar = local_random.choice(list_makanan) if kategori == "Makanan" else local_random.choice(list_minuman)
        
        products.append({
            'id': i + 1,
            'nama': f"{nama_dasar} (ID: {i+1})", # Ditambah ID di nama agar membedakan duplikasi nama acak
            'kategori': kategori,
            'harga': local_random.randint(5000, 50000), # Rentang harga disesuaikan dengan makanan/minuman
            'rak': i
        })
    return products

@st.cache_data
def dapatkan_data_gudang(kondisi, filter_kat, _produk_dasar, jml_prd):
    produk_terpotong = _produk_dasar[:jml_prd]
    
    if filter_kat == "🍔 Makanan Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Makanan"]
    elif filter_kat == "🥤 Minuman Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Minuman"]
    else:
        data_lokal = produk_terpotong.copy()
        
    if kondisi == "🔄 Data Acak (Unsorted)":
        random.seed(42)
        random.shuffle(data_lokal)
    else:
        data_lokal = sorted(data_lokal, key=lambda x: x['id'])
        
    for indeks_baru, produk in enumerate(data_lokal):
        produk['rak_sekarang'] = indeks_baru 
        
    return data_lokal

# ========== 3 ALGORITMA PENCARIAN ==========
def linear_search(data, target_id):
    langkah = 0 
    for i, produk in enumerate(data):
        langkah += 1
        if produk['id'] == target_id:
            return i, langkah
    return -1, langkah

def binary_search(data, target_id):
    langkah = 0
    left, right = 0, len(data) - 1
    while left <= right:
        langkah += 1
        mid = (left + right) // 2
        if data[mid]['id'] == target_id:
            return mid, langkah
        elif data[mid]['id'] < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return -1, langkah

def interpolation_search(data, target_id):
    langkah = 0
    low = 0
    high = len(data) - 1
    while low <= high and data[low]['id'] <= target_id <= data[high]['id']:
        langkah += 1
        if data[high]['id'] == data[low]['id']:
            if data[low]['id'] == target_id:
                return low, langkah
            break
        
        pembagi = data[high]['id'] - data[low]['id']
        if pembagi == 0: break
            
        pos = low + int(((float(high - low) / pembagi) * (target_id - data[low]['id'])))
        if pos < low or pos > high:
            break
        if data[pos]['id'] == target_id:
            return pos, langkah
        elif data[pos]['id'] < target_id:
            low = pos + 1
        else:
            high = pos - 1
    return -1, langkah

# ==========4.PAGE FUNCTIONS==========
if 'halaman_sekarang' not in st.session_state:
    st.session_state.halaman_sekarang = 1
    
if 'pencarian_dimulai' not in st.session_state:
    st.session_state.pencarian_dimulai = False

def ke_halaman_sebelumnya():
    if st.session_state.halaman_sekarang > 1:
        st.session_state.halaman_sekarang -= 1

def ke_halaman_selanjutnya():
    st.session_state.halaman_sekarang += 1

# ==========5.SIDEBAR==========

with st.sidebar:
    st.header("⚙️ Pengaturan")
    jumlah_produk = st.slider("Jumlah produk di gudang:", min_value=100, max_value=1000, value=250, step=100)
    
    st.divider()
    st.subheader("🛒 Filter Kategori")
    filter_kategori = st.radio(
        "Tampilkan kategori produk:",
        ["🔄 Campuran (Semua)", "🍔 Makanan Saja", "🥤 Minuman Saja"]
    )
    
    st.divider()
    st.subheader("🎯 Pilih Algoritma Pencarian")
    algoritma_terpilih = st.radio("Pilih algoritma yang ingin digunakan:", ["🔍 Linear Search", "📚 Binary Search", "⚡ Interpolation Search"])
    
    st.divider()
    st.subheader("📦 Kondisi Data Gudang")
    kondisi_data = st.radio("Bagaimana kondisi data saat ini?", ["🔄 Data Acak (Unsorted)", "📊 Data Terurut berdasarkan ID (Sorted)"])


# ==========6.lOAD DATA SESAUI FILTER, KATEGORI, DAN KONDISI==========
products_master = generate_products(jumlah_produk)
data_list = dapatkan_data_gudang(kondisi_data, filter_kategori, products_master, jumlah_produk)

id_tersedia = [p['id'] for p in data_list]

if not id_tersedia:
    st.error("Tidak ada data produk yang cocok dengan filter tersebut.")
    st.stop()


# ==========6.KONDISI YANG AKTIF==========
col_info1, col_info2 = st.columns(2)
with col_info1:
    if kondisi_data == "🔄 Data Acak (Unsorted)":
        st.info("🔄 **Kondisi Data:** Data dalam keadaan ACAK (tidak terurut)")
    else:
        st.success("📊 **Kondisi Data:** Data dalam keadaan TERURUT berdasarkan ID")
with col_info2:
    st.warning(f"💡 **Total Produk Aktif Sesuai Filter:** {len(data_list)} Items")

# ==========7.SEARCHING==========
st.divider()
st.subheader("🔎 Cari Produk")

if "id_dipilih" not in st.session_state or st.session_state.id_dipilih not in id_tersedia:
    st.session_state.id_dipilih = id_tersedia[0]

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
with col1:
    target_id = st.number_input(
        "Masukkan ID Produk yang dicari: ", 
        min_value=1, 
        max_value=jumlah_produk, 
        value=st.session_state.id_dipilih,
        key="id_produk_input"
    )
    st.session_state.id_dipilih = target_id

with col2:
    st.write("<style>div.row-widget.stButton { margin-top: 28px; }</style>", unsafe_allow_html=True) 
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

# ==========8.EKSEKUSI SEARCHING ==========
if cari_button:
    st.session_state.pencarian_dimulai = True
    
    target_id = st.session_state.id_produk_input 
    st.session_state.id_dipilih = target_id
    
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    if target_id not in id_tersedia:
        st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan pada filter kategori **{filter_kategori}** saat ini!")
        st.caption("💡 Petunjuk: Coba ubah filter kategori di sidebar menjadi 'Campuran (Semua)' atau cari ID produk lain.")
    else:
        if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
            st.warning("⚠️ **Peringatan:** Algoritma berbasis bagi-dua atau estimasi rumus membutuhkan data TERURUT!")
        
        indeks_ditemukan = -1
        
        # 1. LINEAR SEARCH
        if "Linear Search" in algoritma_terpilih:
            with st.spinner("Menjalankan Linear Search..."):
                start_time = time.time()
                indeks, langkah = linear_search(data_list, target_id)
                waktu = (time.time() - start_time) * 1000
            st.success(f"✅ **Algoritma: Linear Search**")
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("Posisi Rak (Indeks)", indeks)
            with col_b: st.metric("Jumlah Langkah", langkah)
            with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
            indeks_ditemukan = indeks
                
        # 2. BINARY SEARCH
        elif "Binary Search" in algoritma_terpilih:
            data_sorted = sorted(data_list, key=lambda x: x['id'])
            with st.spinner("Menjalankan Binary Search..."):
                start_time = time.time()
                indeks, langkah = binary_search(data_sorted, target_id)
                waktu = (time.time() - start_time) * 1000
            st.success(f"✅ **Algoritma: Binary Search**")
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.metric("Posisi Rak (Indeks)", indeks)
            with col_b: st.metric("Jumlah Langkah", langkah)
            with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
            indeks_ditemukan = indeks
        
        # 3. INTERPOLATION SEARCH
        else:
            data_sorted = sorted(data_list, key=lambda x: x['id'])
            with st.spinner("Menjalankan Interpolation Search..."):
                start_time = time.time()
                indeks, langkah = interpolation_search(data_sorted, target_id)
                waktu = (time.time() - start_time) * 1000
            st.success(f"✅ **Algoritma: Interpolation Search**")
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

            baris_per_halaman = 10
            halaman_tujuan = (indeks_ditemukan // baris_per_halaman) + 1
            if st.session_state.halaman_sekarang != halaman_tujuan:
                st.session_state.halaman_sekarang = halaman_tujuan
                st.rerun()

if st.session_state.id_produk_input != st.session_state.id_dipilih:
    st.session_state.pencarian_dimulai = False

# ==========9.PERBANDINGAN KETIGA ALGORITMA ==========
st.divider()
with st.expander("🔬 Perbandingan Ketiga Algoritma Sekaligus"):
    st.write("Lihat perbandingan kecepatan 3 algoritma secara real-time berdasarkan filter yang aktif")
    bandingkan_button = st.button("📊 Bandingkan Semua Algoritma", use_container_width=True, key="btn_banding")
    if bandingkan_button:
        current_target = st.session_state.id_dipilih
        if current_target not in id_tersedia:
            st.error("Produk tidak ada di dalam filter kategori saat ini. Tidak bisa dibandingkan.")
        else:
            data_sorted = sorted(data_list, key=lambda x: x['id'])
            start = time.time(); idx_l, steps_l = linear_search(data_list, current_target); t_l = (time.time() - start) * 1000
            start = time.time(); idx_b, steps_b = binary_search(data_sorted, current_target); t_b = (time.time() - start) * 1000
            start = time.time(); idx_i, steps_i = interpolation_search(data_sorted, current_target); t_i = (time.time() - start) * 1000
            
            comparison_data = {
                "Algoritma": ["Linear Search", "Binary Search", "Interpolation Search"],
                "Ditemukan": ["✅" if idx_l != -1 else "❌", "✅" if idx_b != -1 else "❌", "✅" if idx_i != -1 else "❌"],
                "Posisi Indeks Rak": [idx_l, idx_b, idx_i],
                "Langkah": [steps_l, steps_b, steps_i],
                "Waktu (ms)": [f"{t_l:.3f}", f"{t_b:.3f}", f"{t_i:.3f}"]
            }
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

# ==========10.TABEL DATA PRODUK ==========
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
    
    def beri_warna_baris(row):
        if st.session_state.pencarian_dimulai and row['ID Produk'] == st.session_state.id_dipilih and st.session_state.id_dipilih in id_tersedia:
            return ['background-color: #15803d; color: white; font-weight: bold;'] * len(row)
        return [''] * len(row)
    
    df_berwarna = df_halaman.style.apply(beri_warna_baris, axis=1)
    st.dataframe(df_berwarna, use_container_width=True, hide_index=True)

# ==========11.PENJELASAN MASING-MASING ALGORITMA ==========
with st.expander("ℹ️ Penjelasan 3 Algoritma searching"):
    st.markdown("""
    **1. Linear Search ** - Memeriksa satu per satu indeks dari awal sampai akhir tidak peduli data itu terurut atau pun acak.\n
    **2. Binary Search ** - Membagi data menjadi setengah bagian secara terus-menerus. Algoritma ini mewajibkan data dalam kondisi **Terurut (Sorted)** berdasarkan ID Produk.\n
    **3. Interpolation Search ** - Menggunakan formula estimasi posisi (seperti mencari kata di kamus fisik). Performa optimal jika data terurut dengan kenaikan nilai ID yang konstan dan merata, data wajib terurut agar bisa digunakan.
    """)

st.divider()
st.subheader("💡 Analisis Kombinasi Pilihan Algoritma & Filter")
col_rec1, col_rec2 = st.columns(2)
with col_rec1:
    st.markdown(f"**Algoritma yang aktif:** {algoritma_terpilih.split('(')[0].strip()}")
    st.markdown(f"**Kondisi data gudang:** {kondisi_data}")
    st.markdown(f"**Kategori filter:** {filter_kategori}")
with col_rec2:
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.error("❌ **Kombinasi Tidak Valid:** Interpolation/Binary Search mutlak memerlukan struktur data yang BERURUTAN agar perhitungannya akurat.")
    else:
        st.success("✅ **Kombinasi Logis Sempurna:** Algoritma yang Anda pilih bekerja secara harmonis dengan struktur dan filter data pendukung.")

st.caption(f"🔄 Halaman diperbarui secara statis | Waktu Sistem: {time.strftime('%Y-%m-%d %H:%M:%S')}")