import streamlit as st
import random
import time
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Rak Digital Pro",
    page_icon="📦",
    layout="wide"
)

# Custom CSS untuk mempercantik UI
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div.stButton > button:first-child {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ========== DATA ENGINE ==========

@st.cache_data
def generate_products(n=500):
    products = []
    for i in range(n):
        products.append({
            'id': i + 1,
            'nama': f"Produk {chr(65 + (i % 26))}{i+100}", # Nama lebih variatif
            'harga': random.randint(10000, 1000000),
            'posisi_rak': i
        })
    return products

# ========== SEARCH ALGORITHMS ==========

def linear_search(data, target_id):
    langkah = 0
    for i, produk in enumerate(data):
        langkah += 1
        if produk['id'] == target_id:
            return i, langkah, produk
    return -1, langkah, None

def binary_search(data, target_id):
    langkah = 0
    left, right = 0, len(data) - 1
    while left <= right:
        langkah += 1
        mid = (left + right) // 2
        if data[mid]['id'] == target_id:
            return mid, langkah, data[mid]
        elif data[mid]['id'] < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return -1, langkah, None

def hash_search(data, target_id):
    # Hash map dibangun sekali (idealnya di luar fungsi pencarian untuk O(1))
    hash_map = {p['id']: (idx, p) for idx, p in enumerate(data)}
    if target_id in hash_map:
        pos, prod = hash_map[target_id]
        return pos, 1, prod
    return -1, 1, None

# ========== SIDEBAR LAYOUT ==========

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/407/407826.png", width=100)
    st.title("Gudang Digital")
    st.divider()
    
    jumlah_produk = st.select_slider(
        "Kapasitas Gudang (Item):",
        options=[100, 500, 1000, 5000, 10000],
        value=500
    )
    
    kondisi_data = st.radio(
        "Susunan Barang di Rak:",
        ["Terurut (ID 1-N)", "Berantakan (Acak)"]
    )
    
    st.info("💡 **Tips:** Binary Search hanya bekerja maksimal pada data yang terurut.")

# Data Preparation
products = generate_products(jumlah_produk)
if kondisi_data == "Berantakan (Acak)":
    data_list = products.copy()
    random.shuffle(data_list)
else:
    data_list = products

# ========== MAIN UI ==========

st.title("📦 Sistem Pencarian Posisi Rak")
st.write(f"Mengelola **{jumlah_produk}** item di dalam database gudang.")

# Tab untuk memisahkan fitur
tab_search, tab_compare, tab_data = st.tabs(["🔍 Pencarian Tunggal", "🔬 Analisis Algoritma", "📋 Inventaris Data"])

with tab_search:
    search_col1, search_col2 = st.columns([1, 2])
    
    with search_col1:
        st.subheader("Parameter Cari")
        target_id = st.text_input("Masukkan ID Produk:", placeholder="Contoh: 123")
        
        algoritma = st.selectbox(
            "Gunakan Strategi:",
            ["Linear Search", "Binary Search", "Hash Map"]
        )
        
        btn_cari = st.button("Mulai Pencarian", type="primary", use_container_width=True)
        if st.button("🎲 ID Acak", use_container_width=True):
            st.session_state.target_id = str(random.randint(1, jumlah_produk))
            st.rerun()

    with search_col2:
        st.subheader("Hasil Lokasi")
        if btn_cari and target_id:
            try:
                tid = int(target_id)
                start_t = time.perf_counter()
                
                # Eksekusi
                if algoritma == "Linear Search":
                    pos, steps, prod = linear_search(data_list, tid)
                elif algoritma == "Binary Search":
                    # Force sort untuk simulasi binary search yang benar
                    ds = sorted(data_list, key=lambda x: x['id'])
                    pos, steps, prod = binary_search(ds, tid)
                else:
                    pos, steps, prod = hash_search(data_list, tid)
                
                end_t = time.perf_counter()
                durasi = (end_t - start_t) * 1000

                if pos != -1:
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Posisi Indeks", f"#{pos}")
                    m2.metric("Langkah", steps)
                    m3.metric("Waktu", f"{durasi:.4f} ms")
                    
                    st.success(f"**Barang Ditemukan!** {prod['nama']} berada di rak indeks ke-{pos}")
                    
                    # Detail Card
                    with st.expander("Lihat Detail Produk", expanded=True):
                        c1, c2 = st.columns(2)
                        c1.write(f"**ID:** {prod['id']}")
                        c1.write(f"**Nama:** {prod['nama']}")
                        c2.write(f"**Harga:** Rp {prod['harga']:,}")
                        st.progress(pos/jumlah_produk)
                else:
                    st.error("Produk tidak ditemukan di sistem.")
            except ValueError:
                st.warning("Masukkan ID dalam bentuk angka!")
        else:
            st.info("Silakan masukkan ID dan klik Cari untuk melihat hasil.")

with tab_compare:
    st.subheader("Perbandingan Efisiensi")
    comp_id = st.number_input("Input ID untuk Test:", min_value=1, max_value=jumlah_produk, value=jumlah_produk//2)
    
    if st.button("Jalankan Benchmark"):
        # Setup data
        ds_sorted = sorted(data_list, key=lambda x: x['id'])
        
        results = []
        for name, func, data_in in [
            ("Linear", linear_search, data_list),
            ("Binary", binary_search, ds_sorted),
            ("Hash Map", hash_search, data_list)
        ]:
            s = time.perf_counter()
            p, stp, _ = func(data_in, comp_id)
            e = time.perf_counter()
            results.append({
                "Algoritma": name,
                "Langkah": stp,
                "Waktu (ms)": (e - s) * 1000,
                "Kompleksitas": "O(n)" if name == "Linear" else ("O(log n)" if name == "Binary" else "O(1)")
            })
        
        st.table(pd.DataFrame(results))
        st.caption("Kesimpulan: Hash Map memberikan akses instan, sementara Linear Search melambat seiring bertambahnya data.")

with tab_data:
    st.subheader("Daftar Rak Saat Ini")
    df = pd.DataFrame(data_list)
    st.dataframe(df, use_container_width=True, height=400)

st.divider()
st.caption(f"Sistem Manajemen Rak Digital v2.0 | {time.strftime('%H:%M:%S')}")