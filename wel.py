import streamlit as st
import json
import pandas as pd
from datetime import datetime
import time
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem E-commerce - 3 Algoritma Pencarian",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 Sistem E-commerce - Pencarian Produk dengan 3 Algoritma")
st.write("Temukan produk dengan harga terbaik dan rating tertinggi!")

# Load data dari JSON
@st.cache_data
def load_data():
    with open("data_produk.json", "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

df = load_data()

# ========== FUNGSI AUTO COMPLETE ==========

def get_search_suggestions(df, query, max_suggestions=5):
    """Mendapatkan saran pencarian berdasarkan input user"""
    if not query or len(query) < 1:
        return []
    
    query_lower = query.lower()
    suggestions = set()
    
    # Saran dari Nama Produk
    nama_matches = df[df['nama_produk'].str.lower().str.contains(query_lower, na=False)]
    for _, row in nama_matches.head(max_suggestions).iterrows():
        suggestions.add(("📦 " + row['nama_produk'], row['nama_produk'], 'nama'))
    
    # Saran dari Product ID
    id_matches = df[df['product_id'].str.lower().str.contains(query_lower, na=False)]
    for _, row in id_matches.head(max_suggestions).iterrows():
        suggestions.add(("🆔 " + row['product_id'], row['product_id'], 'id'))
    
    # Saran dari Kategori
    if 'kategori' in df.columns:
        kategori_matches = df[df['kategori'].str.lower().str.contains(query_lower, na=False)]
        for _, row in kategori_matches.head(max_suggestions).iterrows():
            suggestions.add(("📂 " + row['kategori'], row['kategori'], 'kategori'))
    
    # Saran berdasarkan harga
    if query.isdigit():
        harga_int = int(query) * 1000
        harga_matches = df[abs(df['harga'] - harga_int) <= 50000].head(max_suggestions)
        for _, row in harga_matches.iterrows():
            suggestions.add((f"💰 Rp {row['harga']:,.0f}", str(row['harga']), 'harga'))
    
    return list(suggestions)[:max_suggestions]


# ========== ALGORITMA SORTING ==========

def urutkan_harga_desc(arr):
    """Selection Sort - Harga tertinggi ke terendah"""
    n = len(arr)
    data_copy = arr.copy()
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if data_copy[j]['harga'] > data_copy[max_idx]['harga']:
                max_idx = j
        data_copy[i], data_copy[max_idx] = data_copy[max_idx], data_copy[i]
    return data_copy

def urutkan_rating_desc(arr):
    """Insertion Sort - Rating tertinggi ke terendah"""
    data_copy = arr.copy()
    n = len(data_copy)
    for i in range(1, n):
        key_item = data_copy[i]
        j = i - 1
        while j >= 0 and key_item['rating'] > data_copy[j]['rating']:
            data_copy[j + 1] = data_copy[j]
            j -= 1
        data_copy[j + 1] = key_item
    return data_copy

def quick_sort_harga_asc(arr):
    """Quick Sort - Harga rendah ke tertinggi"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]['harga']
    left = [x for x in arr if x['harga'] < pivot]
    middle = [x for x in arr if x['harga'] == pivot]
    right = [x for x in arr if x['harga'] > pivot]
    return quick_sort_harga_asc(left) + middle + quick_sort_harga_asc(right)

def bubble_sort_rating_asc(arr):
    """Bubble Sort - Rating rendah ke tertinggi"""
    data_copy = arr.copy()
    n = len(data_copy)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if data_copy[j]['rating'] > data_copy[j + 1]['rating']:
                data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
    return data_copy


# ========== ALGORITMA PENCARIAN ==========

def linear_search_by_id(data_list, target_id):
    """
    LINEAR SEARCH - O(n)
    Cocok untuk data kecil & tidak terurut
    """
    steps = 0
    for i, product in enumerate(data_list):
        steps += 1
        if product['product_id'].lower() == target_id.lower():
            return i, steps
    return -1, steps

def binary_search_by_id(data_list, target_id):
    """
    BINARY SEARCH - O(log n)
    Prasyarat: data sudah terurut berdasarkan product_id
    """
    steps = 0
    left, right = 0, len(data_list) - 1
    target_lower = target_id.lower()
    
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        mid_id = data_list[mid]['product_id'].lower()
        
        if mid_id == target_lower:
            return mid, steps
        elif mid_id < target_lower:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps

def create_id_index(data_list):
    """Membangun hash map index untuk pencarian O(1)"""
    id_to_index = {}
    for idx, product in enumerate(data_list):
        id_to_index[product['product_id'].lower()] = idx
    return id_to_index

def hash_search(id_index, target_id):
    """HASH MAP SEARCH - O(1)"""
    return id_index.get(target_id.lower(), -1)


# ========== SIDEBAR ==========

with st.sidebar:
    st.header("🎛️ Filter & Pengaturan")
    
    # Filter Harga
    st.subheader("💰 Filter Harga")
    min_harga = int(df['harga'].min())
    max_harga = int(df['harga'].max())
    range_harga = st.slider(
        "Range Harga (Rp)",
        min_harga, max_harga,
        (min_harga, max_harga),
        step=50000,
        format="Rp %d"
    )
    
    # Filter Rating
    st.subheader("⭐ Filter Rating")
    min_rating = st.slider("Minimal Rating", 1.0, 5.0, 1.0, 0.1, format="%.1f")
    
    # Filter Kategori
    if 'kategori' in df.columns:
        st.subheader("📂 Filter Kategori")
        semua_kategori = ["Semua"] + sorted(df['kategori'].unique().tolist())
        filter_kategori = st.selectbox("Pilih Kategori:", semua_kategori)
    else:
        filter_kategori = "Semua"
    
    # Sorting
    st.subheader("📊 Urutkan Berdasarkan")
    sort_option = st.selectbox(
        "Pilih metode sorting:",
        [
            "Tanpa Urutan",
            "Harga Tertinggi ke Terendah (Selection Sort)",
            "Harga Terendah ke Tertinggi (Quick Sort)",
            "Rating Tertinggi ke Terendah (Insertion Sort)",
            "Rating Terendah ke Tertinggi (Bubble Sort)"
        ]
    )
    
    st.divider()
    
    # Pilihan Algoritma Pencarian
    st.subheader("🔎 Algoritma Pencarian")
    search_algorithm = st.selectbox(
        "Pilih metode pencarian:",
        [
            "Linear Search (O(n)) - Data tidak terurut",
            "Binary Search (O(log n)) - Data harus terurut by ID",
            "Hash Map (O(1)) - Paling cepat"
        ]
    )
    
    # Info algoritma
    if search_algorithm == "Binary Search (O(log n)) - Data harus terurut by ID":
        st.info("⚠️ Binary Search membutuhkan data terurut berdasarkan ID")
    elif search_algorithm == "Hash Map (O(1)) - Paling cepat":
        st.success("✅ Hash Map: preprocessing 1x, pencarian O(1)")
    else:
        st.info("📌 Linear Search: sederhana, cocok untuk data kecil")
    
    # Jumlah tampil
    st.subheader("📦 Tampilkan")
    jumlah_tampil = st.slider("Jumlah produk:", 10, 100, 20, 10)


# ========== FILTER DATA ==========

df_filtered = df[
    (df['harga'] >= range_harga[0]) & 
    (df['harga'] <= range_harga[1]) &
    (df['rating'] >= min_rating)
].copy()

if 'kategori' in df.columns and filter_kategori != "Semua":
    df_filtered = df_filtered[df_filtered['kategori'] == filter_kategori]


# ========== SEARCH WITH AUTO COMPLETE ==========

st.subheader("🔍 Pencarian Produk")

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_suggestion' not in st.session_state:
    st.session_state.selected_suggestion = None

col1, col2 = st.columns([3, 1])

with col1:
    search_input = st.text_input(
        "Cari produk, ID, atau kategori:",
        value=st.session_state.search_query,
        placeholder="Ketik minimal 2 karakter...",
        key="search_input"
    )

with col2:
    st.write("")
    st.write("")
    if st.button("🔄 Reset Pencarian"):
        st.session_state.search_query = ""
        st.session_state.selected_suggestion = None
        st.rerun()

# Auto Complete
if search_input and len(search_input) >= 2:
    suggestions = get_search_suggestions(df_filtered, search_input)
    if suggestions:
        st.markdown("**💡 Saran pencarian:**")
        cols = st.columns(min(len(suggestions), 3))
        for idx, (display_text, value, _) in enumerate(suggestions):
            with cols[idx % 3]:
                if st.button(display_text, key=f"sugg_{idx}"):
                    st.session_state.search_query = value
                    st.session_state.selected_suggestion = value
                    st.rerun()
        st.markdown("---")

# Proses pencarian teks biasa
search_query = st.session_state.search_query if st.session_state.selected_suggestion else search_input

if search_query:
    search_pattern = search_query.lower()
    mask = (
        df_filtered['nama_produk'].str.lower().str.contains(search_pattern, na=False) |
        df_filtered['product_id'].str.lower().str.contains(search_pattern, na=False)
    )
    if 'kategori' in df_filtered.columns:
        mask = mask | (df_filtered['kategori'].str.lower().str.contains(search_pattern, na=False))
    
    if search_query.isdigit():
        harga_cari = int(search_query) * 1000
        mask_harga = (df_filtered['harga'] >= harga_cari - 50000) & (df_filtered['harga'] <= harga_cari + 50000)
        mask = mask | mask_harga
    
    df_search_result = df_filtered[mask]
    if not df_search_result.empty:
        st.success(f"✅ Ditemukan {len(df_search_result)} produk yang cocok dengan '{search_query}'")
        df_filtered = df_search_result
    else:
        st.warning(f"⚠️ Tidak ada produk yang cocok dengan '{search_query}'")


# ========== DEMO PENCARIAN DENGAN ALGORITMA ==========

st.divider()
st.subheader("🎯 Demo Pencarian dengan 3 Algoritma")

col_demo1, col_demo2 = st.columns([2, 1])

with col_demo1:
    search_demo_id = st.text_input(
        "Masukkan ID Produk untuk demo pencarian:",
        placeholder="Contoh: PRD001, PRD123, dll",
        key="demo_search_id"
    )

with col_demo2:
    st.write("")
    st.write("")
    if st.button("🚀 Jalankan Pencarian", key="demo_search_btn"):
        if search_demo_id:
            data_list = df_filtered.to_dict('records')
            
            if not data_list:
                st.warning("⚠️ Tidak ada data dengan filter saat ini")
            else:
                # LINEAR SEARCH
                with st.expander("📊 Hasil Pencarian", expanded=True):
                    col_linear, col_binary, col_hash = st.columns(3)
                    
                    # 1. LINEAR SEARCH
                    with col_linear:
                        st.markdown("### 1️⃣ Linear Search (O(n))")
                        start_time = time.time()
                        index_linear, steps_linear = linear_search_by_id(data_list, search_demo_id)
                        time_linear = (time.time() - start_time) * 1000
                        
                        if index_linear != -1:
                            st.success("✅ Ditemukan!")
                            st.metric("Indeks", index_linear)
                            st.metric("Langkah", steps_linear)
                            st.metric("Waktu", f"{time_linear:.3f} ms")
                        else:
                            st.error("❌ Tidak ditemukan")
                            st.metric("Langkah", steps_linear)
                            st.metric("Waktu", f"{time_linear:.3f} ms")
                    
                    # 2. BINARY SEARCH
                    with col_binary:
                        st.markdown("### 2️⃣ Binary Search (O(log n))")
                        data_sorted = sorted(data_list, key=lambda x: x['product_id'].lower())
                        start_time = time.time()
                        index_binary, steps_binary = binary_search_by_id(data_sorted, search_demo_id)
                        time_binary = (time.time() - start_time) * 1000
                        
                        if index_binary != -1:
                            st.success("✅ Ditemukan!")
                            st.metric("Indeks", index_binary)
                            st.metric("Langkah", steps_binary)
                            st.metric("Waktu", f"{time_binary:.3f} ms")
                        else:
                            st.error("❌ Tidak ditemukan")
                            st.metric("Langkah", steps_binary)
                            st.metric("Waktu", f"{time_binary:.3f} ms")
                    
                    # 3. HASH MAP SEARCH
                    with col_hash:
                        st.markdown("### 3️⃣ Hash Map (O(1))")
                        start_pre = time.time()
                        id_index = create_id_index(data_list)
                        time_pre = (time.time() - start_pre) * 1000
                        
                        start_time = time.time()
                        index_hash = hash_search(id_index, search_demo_id)
                        time_hash = (time.time() - start_time) * 1000
                        
                        if index_hash != -1:
                            st.success("✅ Ditemukan!")
                            st.metric("Indeks", index_hash)
                            st.metric("Prep Time", f"{time_pre:.3f} ms")
                            st.metric("Search Time", f"{time_hash:.3f} ms")
                        else:
                            st.error("❌ Tidak ditemukan")
                            st.metric("Waktu", f"{time_hash:.3f} ms")
                    
                    # Tampilkan detail produk jika ditemukan
                    if index_linear != -1:
                        st.divider()
                        st.subheader("📦 Detail Produk yang Ditemukan")
                        product_found = data_list[index_linear]
                        col_detail1, col_detail2 = st.columns(2)
                        with col_detail1:
                            st.write(f"**🆔 ID Produk:** {product_found['product_id']}")
                            st.write(f"**📦 Nama Produk:** {product_found['nama_produk']}")
                        with col_detail2:
                            st.write(f"**💰 Harga:** Rp {product_found['harga']:,.0f}")
                            st.write(f"**⭐ Rating:** {product_found['rating']}")
        else:
            st.warning("⚠️ Masukkan ID produk terlebih dahulu")


# ========== SORTING DATA UTAMA ==========

data_list = df_filtered.to_dict('records')

if sort_option == "Harga Tertinggi ke Terendah (Selection Sort)":
    with st.spinner("Mengurutkan dengan Selection Sort..."):
        data_list = urutkan_harga_desc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk")
elif sort_option == "Harga Terendah ke Tertinggi (Quick Sort)":
    with st.spinner("Mengurutkan dengan Quick Sort..."):
        data_list = quick_sort_harga_asc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk")
elif sort_option == "Rating Tertinggi ke Terendah (Insertion Sort)":
    with st.spinner("Mengurutkan dengan Insertion Sort..."):
        data_list = urutkan_rating_desc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk")
elif sort_option == "Rating Terendah ke Tertinggi (Bubble Sort)":
    with st.spinner("Mengurutkan dengan Bubble Sort..."):
        data_list = bubble_sort_rating_asc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk")

df_sorted = pd.DataFrame(data_list)
df_display = df_sorted.head(jumlah_tampil)


# ========== METRIK ==========

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Produk", len(df))
with col2:
    st.metric("Total (Filter)", len(df_filtered))
with col3:
    if not df_filtered.empty:
        st.metric("Harga Tertinggi", f"Rp {df_filtered['harga'].max():,.0f}")
    else:
        st.metric("Harga Tertinggi", "Rp 0")
with col4:
    if not df_filtered.empty:
        st.metric("Rating Tertinggi", f"{df_filtered['rating'].max():.1f}")
    else:
        st.metric("Rating Tertinggi", "0")
with col5:
    st.metric("Algoritma Aktif", search_algorithm.split()[0])


# ========== TABEL PRODUK ==========

if not df_display.empty:
    st.subheader(f"📋 Menampilkan {len(df_display)} produk")
    
    columns_to_show = ['nomer', 'product_id', 'nama_produk', 'harga', 'rating']
    if 'kategori' in df_display.columns:
        columns_to_show.insert(3, 'kategori')
    
    df_display_display = df_display[columns_to_show].copy()
    df_display_display['harga'] = df_display_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    df_display_display['rating'] = df_display_display['rating'].apply(lambda x: f"{x} ⭐")
    
    rename_map = {
        'nomer': 'No.', 'product_id': 'ID Produk', 'nama_produk': 'Nama Produk',
        'harga': 'Harga', 'rating': 'Rating'
    }
    if 'kategori' in df_display_display.columns:
        rename_map['kategori'] = 'Kategori'
    
    df_display_display = df_display_display.rename(columns=rename_map)
    st.dataframe(df_display_display, use_container_width=True)
else:
    st.warning("⚠️ Tidak ada produk yang sesuai")


# ========== PERBANDINGAN ALGORITMA ==========

with st.expander("📊 Perbandingan 3 Algoritma Pencarian"):
    comparison_data = {
        "Algoritma": ["Linear Search", "Binary Search", "Hash Map"],
        "Kompleksitas Waktu": ["O(n)", "O(log n)", "O(1)"],
        "Kompleksitas Ruang": ["O(1)", "O(1)", "O(n)"],
        "Prasyarat": ["Data boleh acak", "Data harus terurut", "Perlu preprocessing"],
        "Kelebihan": ["Sederhana", "Cepat untuk data besar", "Paling cepat O(1)"],
        "Kekurangan": ["Lambat untuk data besar", "Data harus sorted", "Butuh memori ekstra"],
        "Cocok untuk": ["Data < 1000 item", "Data statis & terurut", "Pencarian sangat sering"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    # Simulasi grafik
    n_values = np.arange(10, 1001, 50)
    linear_times = n_values
    binary_times = np.log2(n_values) * 10
    hash_times = np.ones_like(n_values) * 5
    
    chart_data = pd.DataFrame({
        'Jumlah Data (n)': n_values,
        'Linear Search O(n)': linear_times,
        'Binary Search O(log n)': binary_times,
        'Hash Map O(1)': hash_times
    })
    st.line_chart(chart_data.set_index('Jumlah Data (n)'))
    st.caption("📌 Grafik simulasi: Semakin rendah garis, semakin cepat algoritma")


# ========== STATISTIK ==========

with st.expander("📈 Statistik & Visualisasi"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Top 10 Harga Tertinggi")
        if data_list:
            top_harga = urutkan_harga_desc(data_list)[:10]
            st.dataframe(pd.DataFrame(top_harga)[['nama_produk', 'harga', 'rating']])
    with col2:
        st.subheader("🏆 Top 10 Rating Tertinggi")
        if data_list:
            top_rating = urutkan_rating_desc(data_list)[:10]
            st.dataframe(pd.DataFrame(top_rating)[['nama_produk', 'rating', 'harga']])
    
    if not df_filtered.empty:
        st.subheader("📊 Distribusi Harga")
        st.bar_chart(df_filtered['harga'].value_counts().head(20))


# ========== FOOTER ==========
st.divider()
st.caption(f"🔄 Data terakhir diperbarui: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("💡 Sistem ini menggunakan 3 algoritma pencarian: Linear Search (O(n)), Binary Search (O(log n)), dan Hash Map (O(1))")