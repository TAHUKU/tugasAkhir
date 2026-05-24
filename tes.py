import streamlit as st
import random
import time
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="3 Algoritma Pencarian Produk",
    page_icon="🔮",
    layout="wide"
)

# ====================================================================
# CYBERPUNK / VIBE CODING ULTRA GLOW CSS
# ====================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    /* Global Styling - Deep Purple Void */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #050112 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e0d7ff !important;
    }

    /* Sidebar - Cyberpunk Terminal Dark */
    section[data-testid="stSidebar"] {
        background-color: #0b032d !important;
        border-right: 1px solid #4c1d95;
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 {
        color: #d8b4fe !important;
        text-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
    }
    section[data-testid="stSidebar"] .stRadio label p {
        font-size: 13.5px !important;
        color: #a78bfa !important;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Mengubah Gaya Judul Utama */
    h1 {
        color: #a855f7 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
        letter-spacing: -1px;
    }
    h2, h3, h4 {
        color: #c4b5fd !important;
    }

    /* Container Box - Glassmorphism Efek Kaca */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(30, 27, 75, 0.25) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(139, 92, 246, 0.35) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7);
    }

    /* Expander Box Styling */
    div[data-testid="stExpander"] {
        background: rgba(15, 12, 41, 0.4) !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        border-radius: 10px !important;
    }

    /* TOMBOL UTAMA (PRIMARY) - NEON VIOLET GLOW */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.5);
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.8);
    }
    
    /* TOMBOL KEDUA (SECONDARY) - CYBER INK */
    div.stButton > button[kind="secondary"] {
        background-color: rgba(15, 12, 41, 0.6) !important;
        color: #c4b5fd !important;
        border: 1px solid #5b21b6 !important;
        border-radius: 10px !important;
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #a855f7 !important;
        color: white !important;
    }

    /* METRIC BOX DIGITAL GLOW */
    [data-testid="stMetricValue"] {
        color: #06b6d4 !important; /* Warna Cyan khas Sci-Fi */
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700 !important;
        text-shadow: 0 0 12px rgba(6, 182, 212, 0.6);
    }
    [data-testid="stMetricLabel"] {
        color: #a78bfa !important;
    }

    /* Beri sentuhan warna ungu pada input angka */
    div[data-testid="stNumberInput"] input {
        background-color: #0f0b26 !important;
        color: #ffffff !important;
        border: 1px solid #5b21b6 !important;
    }
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
            'nama': f"Node Item X-{i+1}",
            'harga': random.randint(10000, 1000000),
            'rak': i
        })
    return products

# Sidebar
with st.sidebar:
    st.header("⚡ SYSTEM CONFIG")
    
    jumlah_produk = st.slider(
        "Kapasitas Array Gudang (n):",
        min_value=100,
        max_value=1000,
        value=500,
        step=100
    )
    
    st.divider()
    
    # ========== FITUR PILIH ALGORITMA ==========
    st.subheader("🔮 Core Engine Logic")
    
    algoritma_terpilih = st.radio(
        "Pilih algoritma yang ingin digunakan:",
        [
            "🔍 Linear Search (O(n)) - Cek satu per satu",
            "📚 Binary Search (O(log n)) - Bagi dua array (butuh data terurut)",
            "⚡ Interpolation Search (O(log (log n))) - Estimasi posisi seperti cari kamus (butuh data terurut)"
        ],
        help="Pilih algoritma sesuai kebutuhan Anda"
    )
    
    st.divider()
    
    # ========== KONDISI DATA ==========
    st.subheader("🌐 Data Entropy Level")
    
    kondisi_data = st.radio(
        "Bagaimana kondisi data saat ini?",
        [
            "🔄 Data Acak (Unsorted)",
            "📊 Data Terurut berdasarkan ID (Sorted)",
            "🎲 Data Dinamis (sering berubah)"
        ],
        help="Pilih sesuai kondisi gudang Anda saat ini"
    )
    
    st.divider()
    # Info algoritma
    with st.expander("ℹ️ Terminal Docs: 3 Algoritma"):
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

# ========== HEADER CORE SYSTEM ==========

st.title("🔮 SYSTEM ANALYTICS: GUDANG DIGITAL")
st.write("Menemukan posisi indeks memori rak berdasarkan ID sasaran secara real-time.")

# ========== GENERATE DATA SESUAI KONDISI ==========

products = generate_products(jumlah_produk)

# Siapkan data berdasarkan kondisi yang dipilih
if kondisi_data == "🔄 Data Acak (Unsorted)":
    data_list = products.copy()
    random.seed(42)  
    random.shuffle(data_list)
    st.info("🔄 **LOG // STATUS:** System detected HIGH ENTROPY (Data Terdistribusi Acak)")
    
elif kondisi_data == "📊 Data Terurut berdasarkan ID (Sorted)":
    data_list = sorted(products, key=lambda x: x['id'])
    st.success("📊 **LOG // STATUS:** System detected ZERO ENTROPY (Data Terstruktur Rapi)")
    
else:  # Data Dinamis
    data_list = products.copy()
    random.seed(24)
    random.shuffle(data_list)
    st.warning("🎲 **LOG // STATUS:** System detected DYNAMIC FLUX (Data Dinamis Fleksibel)")

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
        
        if data[high]['id'] == data[low]['id']:
            if data[low]['id'] == target_id:
                return low, langkah
            break
            
        pos = low + int(((float(high - low) / (data[high]['id'] - data[low]['id'])) * (target_id - data[low]['id'])))
        
        if pos < low or pos > high:
            break
            
        if data[pos]['id'] == target_id:
            return pos, langkah
        elif data[pos]['id'] < target_id:
            low = pos + 1
        else:
            high = pos - 1
            
    return -1, langkah

# ========== ANTARMUKA PENGGUNA ==========

st.divider()
st.subheader("🔎 Terminal Target Input")

if 'input_id' not in st.session_state:
    st.session_state.input_id = 1

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    target_id = st.number_input(
        "Masukkan ID Node/Produk sasaran:",
        min_value=1,
        max_value=jumlah_produk,
        value=st.session_state.input_id,
        step=1,
        key="id_produk_input"
    )
    st.session_state.input_id = target_id

with col2:
    st.write("") 
    st.write("") 
    cari_button = st.button("🚀 Run Search Execution", type="primary", use_container_width=True)

with col3:
    st.write("") 
    st.write("") 
    random_button = st.button("🎲 Randomize Query ID", use_container_width=True)
    if random_button:
        st.session_state.input_id = random.randint(1, jumlah_produk)
        st.rerun()

# ========== EKSEKUSI PENCARIAN ==========

if cari_button:
    st.divider()
    st.subheader("📊 Output Execution Log")
    
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.warning("⚠️ **Peringatan:** Algoritma berbasis bagi-dua atau estimasi rumus membutuhkan data TERURUT! Hasil mungkin tidak akurat atau tidak ditemukan.")
        st.caption("💡 Saran: Pilih kondisi data 'Data Terurut' untuk hasil maksimal, atau gunakan Linear Search.")
    
    if "Linear Search" in algoritma_terpilih:
        with st.spinner("Menjalankan Linear Search..."):
            start_time = time.time()
            indeks, langkah = linear_search(data_list, target_id)
            waktu = (time.time() - start_time) * 1000
            
        st.success(f"✅ **Algoritma Terpilih: Linear Search (O(n))**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Memory Address (Indeks)", indeks if indeks != -1 else "❌ Not Found")
        with col_b:
            st.metric("Total Iterasi (Langkah)", langkah)
        with col_c:
            st.metric("Latency Proses", f"{waktu:.3f} ms")
        
        if indeks != -1:
            produk = data_list[indeks]
            st.info(f"📦 **Node Detected:** {produk['nama']} | 💰 Harga: Rp {produk['harga']:,.0f}")
        else:
            st.error(f"❌ Node Target ID {target_id} tidak terdaftar!")
    
    elif "Binary Search" in algoritma_terpilih:
        data_sorted = sorted(data_list, key=lambda x: x['id'])
        
        with st.spinner("Menjalankan Binary Search..."):
            start_time = time.time()
            indeks, langkah = binary_search(data_sorted, target_id)
            waktu = (time.time() - start_time) * 1000
            
        st.success(f"✅ **Algoritma Terpilih: Binary Search (O(log n))**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Memory Address (Indeks)", indeks if indeks != -1 else "❌ Not Found")
        with col_b:
            st.metric("Total Iterasi (Langkah)", langkah)
        with col_c:
            st.metric("Latency Proses", f"{waktu:.3f} ms")
        
        if indeks != -1:
            produk = data_sorted[indeks]
            st.info(f"📦 **Node Detected:** {produk['nama']} | 💰 Harga: Rp {produk['harga']:,.0f}")
        else:
            st.error(f"❌ Node Target ID {target_id} tidak terdaftar!")
    
    else:  # Interpolation Search
        data_sorted = sorted(data_list, key=lambda x: x['id'])
        
        with st.spinner("Menjalankan Interpolation Search..."):
            start_time = time.time()
            indeks, langkah = interpolation_search(data_sorted, target_id)
            waktu = (time.time() - start_time) * 1000
        
        st.success(f"✅ **Algoritma Terpilih: Interpolation Search (O(log (log n)))**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Memory Address (Indeks)", indeks if indeks != -1 else "❌ Not Found")
        with col_b:
            st.metric("Total Iterasi (Langkah)", langkah)
        with col_c:
            st.metric("Latency Proses", f"{waktu:.3f} ms")
        
        if indeks != -1:
            produk = data_sorted[indeks]
            st.info(f"📦 **Node Detected:** {produk['nama']} | 💰 Harga: Rp {produk['harga']:,.0f}")
        else:
            st.error(f"❌ Node Target ID {target_id} tidak terdaftar!")
            
# ========== DEMO PERBANDINGAN KETIGANYA ==========
st.divider()
with st.expander("🔬 Lab Simulator: Cross-Algorithm Benchmarking"):
    st.write("Stress-test perbandingan kecepatan 3 algoritma secara real-time serentak:")
    
    bandingkan_button = st.button("📊 Initialize Comparison Test", use_container_width=True, key="btn_banding")
    
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
        
        comparison_data = {
            "Algoritma Eksperimen": ["Linear Search", "Binary Search", "Interpolation Search"],
            "State Ditemukan": [
                "✅" if idx_linear != -1 else "❌",
                "✅" if idx_binary != -1 else "❌",
                "✅" if idx_inter != -1 else "❌"
            ],
            "Posisi Indeks": [
                idx_linear if idx_linear != -1 else "-",
                idx_binary if idx_binary != -1 else "-",
                idx_inter if idx_inter != -1 else "-"
            ],
            "Beban Kerja (Langkah)": [steps_linear, steps_binary, steps_inter],
            "Durasi Komputasi (ms)": [f"{time_linear:.3f} ms", f"{time_binary:.3f} ms", f"{time_inter:.3f} ms"]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        times = [time_linear, time_binary, time_inter]
        fastest_idx = times.index(min(times))
        fastest_names = ["Linear Search", "Binary Search", "Interpolation Search"]
        st.success(f"⚡ **OPTIMAL PERFORMANCE:** Komputasi paling ringan diraih oleh **{fastest_names[fastest_idx]}** dengan rekor waktu {min(times):.3f} ms!")

# ========== TABEL DATA PRODUK ==========

with st.expander("📋 Database Global Explorer"):
    df = pd.DataFrame(data_list)
    df_display = df[['id', 'nama', 'harga', 'rak']].copy()
    df_display['harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    df_display = df_display.rename(columns={
        'id': 'ID Produk',
        'nama': 'Nama Produk',
        'harga': 'Harga',
        'rak': 'Posisi Rak'
    })
    st.dataframe(df_display, use_container_width=True, height=400)
    
# ========== VISUALISASI KECEPATAN ==========
with st.expander("📊 Grafik Teoretis Kompleksitas Algoritma"):
    st.subheader("Kurva Efisiensi Waktu (n = Skala Data)")
    
    ukuran_data = list(range(100, 1001, 100))
    linear_times = [x for x in ukuran_data]
    binary_times = [x * 0.1 for x in ukuran_data]
    inter_times = [1.5 for _ in ukuran_data] 
    
    chart_data = pd.DataFrame({
        'Jumlah Data': ukuran_data,
        'Linear Search O(n)': linear_times,
        'Binary Search O(log n)': binary_times,
        'Interpolation Search O(log (log n))': inter_times
    })
    
    st.line_chart(chart_data.set_index('Jumlah Data'))
    st.caption("📌 **Petunjuk Kurva:** Semakin mendatar dan rendah garis grafik, membuktikan efisiensi komputasi algoritma jauh lebih baik saat menangani Big Data.")

# ========== REKOMENDASI BERDASARKAN PILIHAN USER ==========

st.divider()
st.subheader("💡 Terminal Synergy Logic Analysis")

col_rec1, col_rec2 = st.columns(2)

with col_rec1:
    st.markdown(f"**Algoritma Aktif:** {algoritma_terpilih.split('(')[0].strip()}")
    st.markdown(f"**Struktur Memori:** {kondisi_data}")

with col_rec2:
    if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.error("❌ **COMPATIBILITY FAILURE:** Interpolation/Binary Search mendeteksi data acak! Logika pencarian tidak valid secara matematis.")
    else:
        st.success("✅ **COMPATIBILITY SYSTEM OPERATIONAL:** Struktur data pendukung telah sinkron dengan persyaratan algoritma.")

st.caption(f"⚡ Live Matrix Syncing | Terminal Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")