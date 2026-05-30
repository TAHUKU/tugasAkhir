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

st.title("🔍 Sistem Pencarian Produk di Gudang Digital")
st.write("Menemukan posisi rak (indeks array) berdasarkan ID Produk - Bebas pilih algoritma!")

st.markdown("""
    <style>
    /* Mengubah tombol Primary (Tombol 'Cari Sekarang') menjadi warna hijau */
    div.stButton > button[kind="primary"] {
        background-color: #22c55e !important;  /* Warna hijau utama */
        color: white !important;                /* Warna teks tombol */
        border-radius: 8px;                     /* Sudut melengkung */
        border: none !important;
        transition: background-color 0.3s ease;
    }
    
    /* Efek ketika tombol disorot (hover) mouse */
    div.stButton > button[kind="primary"]:hover {
        background-color: #16a34a !important;  /* Warna hijau lebih gelap saat di-hover */
    }

    /* Kustomisasi kartu hasil pencarian dengan latar belakang hitam pekat */
    .hasil-card {
        background-color: #000000 !important;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #22c55e;
        margin-top: 15px;
    }
    
    /* Memaksa teks di dalam kartu menjadi warna putih kontras */
    .hasil-card p, .hasil-card h4, .hasil-card b {
        color: #ffffff !important;
    }
    .footer-fixed {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117; /* Warna gelap menyesuaikan tema aplikasi */
        color: #ffffff;
        text-align: center;
        padding: 10px 0;
        font-size: 12px;
        border-top: 1px solid #262730;
        z-index: 999;
    }
    </style>
    
    <div class="footer-fixed">
        <p style="margin:0;">🔍 Sistem Pencarian Produk Gudang Digital — Hakkul IT 2025.</p>
    </div>
    </style>
""", unsafe_allow_html=True)

# ========== MEMBUAT DATA PRODUK ==========

@st.cache_data
def generate_products(n=500):
    """Generate produk dengan ID unik (angka terurut secara konsisten)"""
    products = []
    for i in range(n):
        products.append({
            'id': i + 1,
            'nama': f"Produk {i+1}",
            'harga': random.randint(10000, 1000000),
            'rak': i
        })
    return products

# Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    jumlah_produk = st.slider(
        "Jumlah produk di gudang:",
        min_value=100,
        max_value=1000,
        value=500,
        step=100
    )
    
    st.divider()
    
    # ========== FITUR PILIH ALGORITMA ==========
    st.subheader("🎯 Pilih Algoritma Pencarian")
    
    algoritma_terpilih = st.radio(
        "Pilih algoritma yang ingin digunakan:",
        [
            "🔍 Linear Search",
            "📚 Binary Search",
            "⚡ Interpolation Search"
        ],
        help="Pilih algoritma sesuai kebutuhan Anda"
    )
    
    st.divider()
    
    # ========== KONDISI DATA ==========
    st.subheader("📦 Kondisi Data Gudang")
    
    kondisi_data = st.radio(
        "Bagaimana kondisi data saat ini?",
        [
            "🔄 Data Acak (Unsorted)",
            "📊 Data Terurut berdasarkan ID (Sorted)",
        ],
        help="Pilih sesuai kondisi gudang Anda saat ini"
    )
    
# ========== 3 ALGORITMA PENCARIAN ==========

def linear_search(data, target_id):
    """Linear Search - O(n)"""
    langkah = 0
    for i, produk in enumerate(data):
        langkah += 1
        if produk['id'] == target_id:
            return i, langkah
    return -1, langkah

def binary_search(data, target_id):
    """Binary Search - O(log n) - Prasyarat: data terurut berdasarkan ID"""
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
    """Interpolation Search - O(log (log n)) - Prasyarat: data terurut"""
    langkah = 0
    low = 0
    high = len(data) - 1
    
    while low <= high and data[low]['id'] <= target_id <= data[high]['id']:
        langkah += 1
        
        # Proteksi jika pembagi adalah nol (jika elemen low dan high bernilai sama)
        if data[high]['id'] == data[low]['id']:
            if data[low]['id'] == target_id:
                return low, langkah
            break
            
        # Rumus Interpolasi untuk menentukan posisi estimasi
        pos = low + int(((float(high - low) / (data[high]['id'] - data[low]['id'])) * (target_id - data[low]['id'])))
        
        # Keamanan tambahan agar indeks tidak keluar jalur array
        if pos < low or pos > high:
            break
            
        if data[pos]['id'] == target_id:
            return pos, langkah
        elif data[pos]['id'] < target_id:
            low = pos + 1
        else:
            high = pos - 1
            
    return -1, langkah

# ========== GENERATE DATA SESUAI KONDISI ==========

products = generate_products(jumlah_produk)

# Siapkan data berdasarkan kondisi yang dipilih
if kondisi_data == "🔄 Data Acak (Unsorted)":
    data_list = products.copy()
    random.seed(42)  # Mengunci seed agar data acaknya konstan dan tidak berubah sendiri tiap halaman direfresh
    random.shuffle(data_list)
    st.info("🔄 **Kondisi Data:** Data dalam keadaan ACAK (tidak terurut)")
    
else:
     kondisi_data == "📊 Data Terurut berdasarkan ID (Sorted)"
     data_list = sorted(products, key=lambda x: x['id'])
     st.success("📊 **Kondisi Data:** Data dalam keadaan TERURUT berdasarkan ID")

# ========== ANTARMUKA PENGGUNA (1 BARIS SEJAJAR) ==========

st.divider()
st.subheader("🔎 Cari Produk")

# Menggunakan 2 kolom agar kolom input dan tombol pencarian sejajar dalam satu baris horizontal
col1, col2 = st.columns([3, 1])

with col1:
    target_id = st.number_input(
        "Masukkan ID Produk yang dicari: ",
        min_value=1,
        max_value=jumlah_produk,
        value=1,
        step=1,
        key="id_produk_input"
    )

with col2:
    st.write("<style>div.row-widget.stButton { margin-top: 28px; }</style>", unsafe_allow_html=True) 
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

# ========== EKSEKUSI PENCARIAN ==========

if cari_button:
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    # Peringatan jika Binary/Interpolation Search dipilih tapi data tidak terurut
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.warning("⚠️ **Peringatan:** Algoritma berbasis bagi-dua atau estimasi rumus membutuhkan data TERURUT! Hasil mungkin tidak akurat atau tidak ditemukan.")
        st.caption("💡 Saran: Pilih kondisi data 'Data Terurut' untuk hasil maksimal, atau gunakan Linear Search.")
    
    # Eksekusi sesuai algoritma yang dipilih
    if "Linear Search" in algoritma_terpilih:
        with st.spinner("Menjalankan Linear Search..."):
            start_time = time.time()
            indeks, langkah = linear_search(data_list, target_id)
            waktu = (time.time() - start_time) * 1000
            
        st.success(f"✅ **Algoritma: Linear Search (O(n))**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Posisi Rak (Indeks)", indeks if indeks != -1 else "❌ Tidak ditemukan")
        with col_b:
            st.metric("Jumlah Langkah", langkah)
        with col_c:
            st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
        
        if indeks != -1:
            produk = data_list[indeks]
            st.markdown(f"""
            <div class="hasil-card">
                <h4 style="margin-top: 0;">📦 Spesifikasi Item Ditemukan</h4>
                <p style="margin-bottom: 8px;"><b>Nama Barang:</b> {produk['nama']}</p>
                <p style="margin-bottom: 0;"><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan dalam {langkah} langkah!")
    
    elif "Binary Search" in algoritma_terpilih:
        # Memastikan data terurut khusus untuk pemrosesan Binary Search
        data_sorted = sorted(data_list, key=lambda x: x['id'])
        
        with st.spinner("Menjalankan Binary Search..."):
            start_time = time.time()
            indeks, langkah = binary_search(data_sorted, target_id)
            waktu = (time.time() - start_time) * 1000
            
        st.success(f"✅ **Algoritma: Binary Search (O(log n))**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Posisi Rak (Indeks)", indeks if indeks != -1 else "❌ Tidak ditemukan")
        with col_b:
            st.metric("Jumlah Langkah", langkah)
        with col_c:
            st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
        
        if indeks != -1:
            produk = data_sorted[indeks]
            st.markdown(f"""
            <div class="hasil-card">
                <h4 style="margin-top: 0;">📦 Spesifikasi Item Ditemukan</h4>
                <p style="margin-bottom: 8px;"><b>Nama Barang:</b> {produk['nama']}</p>
                <p style="margin-bottom: 0;"><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan dalam {langkah} langkah!")
    
    else:  # Interpolation Search
        # Memastikan data terurut khusus untuk pemrosesan Interpolation Search
        data_sorted = sorted(data_list, key=lambda x: x['id'])
        
        with st.spinner("Menjalankan Interpolation Search..."):
            start_time = time.time()
            indeks, langkah = interpolation_search(data_sorted, target_id)
            waktu = (time.time() - start_time) * 1000
        
        st.success(f"✅ **Algoritma: Interpolation Search (O(log (log n)))**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Posisi Rak (Indeks)", indeks if indeks != -1 else "❌ Tidak ditemukan")
        with col_b:
            st.metric("Jumlah Langkah", langkah)
        with col_c:
            st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
        
        if indeks != -1:
            produk = data_sorted[indeks]
            st.markdown(f"""
            <div class="hasil-card">
                <h4 style="margin-top: 0;">📦 Spesifikasi Item Ditemukan</h4>
                <p style="margin-bottom: 8px;"><b>Nama Barang:</b> {produk['nama']}</p>
                <p style="margin-bottom: 0;"><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan dalam {langkah} langkah!")
            
# ========== DEMO PERBANDINGAN KETIGANYA ==========
st.divider()
with st.expander("🔬 Demo: Bandingkan Ketiga Algoritma Sekaligus"):
    st.write("Lihat perbandingan kecepatan 3 algoritma secara real-time berdasarkan ID pilihanmu di atas")
    
    bandingkan_button = st.button("📊 Bandingkan Semua Algoritma", use_container_width=True, key="btn_banding")
    
    if bandingkan_button:
        data_sorted = sorted(data_list, key=lambda x: x['id'])
        
        # Linear Search
        start = time.time()
        idx_linear, steps_linear = linear_search(data_list, target_id)
        time_linear = (time.time() - start) * 1000
        
        # Binary Search
        start = time.time()
        idx_binary, steps_binary = binary_search(data_sorted, target_id)
        time_binary = (time.time() - start) * 1000
        
        # Interpolation Search
        start = time.time()
        idx_inter, steps_inter = interpolation_search(data_sorted, target_id)
        time_inter = (time.time() - start) * 1000
        
        # Tampilkan hasil perbandingan
        comparison_data = {
            "Algoritma": ["Linear Search", "Binary Search", "Interpolation Search"],
            "Ditemukan": [
                "✅" if idx_linear != -1 else "❌",
                "✅" if idx_binary != -1 else "❌",
                "✅" if idx_inter != -1 else "❌"
            ],
            "Posisi Indeks": [
                idx_linear if idx_linear != -1 else "-",
                idx_binary if idx_binary != -1 else "-",
                idx_inter if idx_inter != -1 else "-"
            ],
            "Langkah": [steps_linear, steps_binary, steps_inter],
            "Waktu (ms)": [f"{time_linear:.3f}", f"{time_binary:.3f}", f"{time_inter:.3f}"]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        # Highlight pemenang
        times = [time_linear, time_binary, time_inter]
        fastest_idx = times.index(min(times))
        fastest_names = ["Linear Search", "Binary Search", "Interpolation Search"]
        st.success(f"⚡ **Paling cepat:** {fastest_names[fastest_idx]} dengan waktu {min(times):.3f} ms!")

        
# ========== TABEL DATA PRODUK ==========

# ========== TABEL DATA PRODUK (NAVIGASI TOMBOL SEBELUMNYA / SELANJUTNYA) ==========

with st.expander("📋 Lihat Semua Data Produk"):
    df = pd.DataFrame(data_list)
    df_display = df[['id', 'nama', 'harga', 'rak']].copy()
    df_display['harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    df_display = df_display.rename(columns={
        'id': 'ID Produk',
        'nama': 'Nama Produk',
        'harga': 'Harga',
        'rak': 'Posisi Rak'
    })
    
    # 1. Parameter Konfigurasi Paginasi
    baris_per_halaman = 10
    total_data = len(df_display)
    total_halaman = math.ceil(total_data / baris_per_halaman)
    
    # 2. Inisialisasi Session State untuk menyimpan halaman aktif saat ini
    if 'halaman_sekarang' not in st.session_state:
        st.session_state.halaman_sekarang = 1
        
    # Validasi keamanan: jika slider jumlah data diperkecil di sidebar, 
    # pastikan halaman sekarang tidak melebihi total halaman yang baru.
    if st.session_state.halaman_sekarang > total_halaman:
        st.session_state.halaman_sekarang = 1

    # 3. Membuat Layout Baris Navigasi (Tombol - Teks Info - Tombol)
    col_prev, col_info, col_next = st.columns([1, 4, 1])
    
    with col_prev:
        # Tombol akan mati (disabled) jika berada di halaman pertama
        if st.button("⬅️ Sebelumnya", use_container_width=True, disabled=(st.session_state.halaman_sekarang == 1)):
            st.session_state.halaman_sekarang -= 1
            st.rerun()
            
    with col_info:
        # Menampilkan teks informasi halaman aktif di tengah-tengah tombol
        st.markdown(f"""
            <div style='text-align: center; padding-top: 5px;'>
                Halaman <b>{st.session_state.halaman_sekarang}</b> dari <b>{total_halaman}</b> <br>
                <span style='color: gray; font-size: 0.85rem;'>Menampilkan data ke-{((st.session_state.halaman_sekarang-1) * baris_per_halaman) + 1} sampai {min(st.session_state.halaman_sekarang * baris_per_halaman, total_data)} dari {total_data} produk</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col_next:
        # Tombol akan mati (disabled) jika sudah mencapai halaman terakhir
        if st.button("Selanjutnya ➡️", use_container_width=True, disabled=(st.session_state.halaman_sekarang == total_halaman)):
            st.session_state.halaman_sekarang += 1
            st.rerun()
            
    st.write("") # Memberi jarak vertikal sedikit sebelum tabel
    
    # 4. Memotong Data Sesuai Urutan Halaman Aktif (Slicing Index)
    start_idx = (st.session_state.halaman_sekarang - 1) * baris_per_halaman
    end_idx = start_idx + baris_per_halaman
    df_halaman = df_display.iloc[start_idx:end_idx]
    
    # 5. Tampilkan Tabel Ringkas (Hanya berisi 10 baris)
    st.dataframe(df_halaman, use_container_width=True)

# ========== REKOMENDASI BERDASARKAN PILIHAN USER ==========
with st.expander("ℹ️ Detail 3 Algoritma"):
        st.markdown("""
        **1. Linear Search (O(n))**
        - Cara: Cek satu per satu dari awal
        - Kelebihan: Data boleh acak, mudah implementasi
        - Kekurangan: Lambat untuk data besar
        - Cocok: Data < 500 produk
        
        **2. Binary Search (O(log n))**
        - Cara: Bagi array menjadi 2 bagian setiap kali
        - Kelebihan: Cepat untuk data besar
        - Kekurangan: Data HARUS terurut dulu
        - Cocok: Data terurut & stabil
        
        **3. Interpolation Search (O(log (log n)))**
        - Cara: Menggunakan rumus posisi berdasarkan nilai target (seperti mencari nama di kamus)
        - Kelebihan: Lebih cepat dari Binary Search jika data terurut dan tersebar merata
        - Kekurangan: Data HARUS terurut, performa buruk jika sebaran data tidak rata
        - Cocok: Data terurut dengan interval yang konsisten
        """)

st.divider()
st.subheader("💡 Analisis Kombinasi Pilihan Anda")

col_rec1, col_rec2 = st.columns(2)

with col_rec1:
    st.markdown(f"**Algoritma yang aktif:** {algoritma_terpilih.split('(')[0].strip()}")
    st.markdown(f"**Kondisi data gudang:** {kondisi_data}")

with col_rec2:
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.error("❌ **Kombinasi Tidak Valid:** Interpolation/Binary Search mutlak memerlukan data yang berurutan secara logis agar rumusnya bekerja.")
    else:
        st.success("✅ **Kombinasi Logis Sempurna:** Algoritma yang kamu pilih sudah bekerja sesuai dengan struktur data pendukungnya.")

st.caption(f"🔄 Halaman diperbarui secara statis | Waktu Sistem: {time.strftime('%Y-%m-%d %H:%M:%S')}")