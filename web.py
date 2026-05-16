import streamlit as st
import json
import pandas as pd
from datetime import datetime


# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem E-commerce",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 Sistem E-commerce - Pencarian Produk")
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
    """
    Mendapatkan saran pencarian berdasarkan input user
    Saran diambil dari nama_produk, product_id, dan kategori (jika ada)
    """
    if not query or len(query) < 1:
        return []
    
    query_lower = query.lower()
    suggestions = set()  # Gunakan set untuk menghindari duplikat
    
    # 1. Saran dari Nama Produk
    nama_matches = df[df['nama_produk'].str.lower().str.contains(query_lower, na=False)]
    for _, row in nama_matches.head(max_suggestions).iterrows():
        suggestions.add(("📦 " + row['nama_produk'], row['nama_produk'], 'nama'))
    
    # 2. Saran dari Product ID
    id_matches = df[df['product_id'].str.lower().str.contains(query_lower, na=False)]
    for _, row in id_matches.head(max_suggestions).iterrows():
        suggestions.add(("🆔 " + row['product_id'], row['product_id'], 'id'))
    
    # 3. Saran dari Kategori (jika ada)
    if 'kategori' in df.columns:
        kategori_matches = df[df['kategori'].str.lower().str.contains(query_lower, na=False)]
        for _, row in kategori_matches.head(max_suggestions).iterrows():
            suggestions.add(("📂 " + row['kategori'], row['kategori'], 'kategori'))
    
    # 4. Saran berdasarkan rentang harga (jika query berupa angka)
    if query.isdigit():
        harga_int = int(query) * 1000
        harga_matches = df[abs(df['harga'] - harga_int) <= 50000].head(max_suggestions)
        for _, row in harga_matches.iterrows():
            suggestions.add((f"💰 Rp {row['harga']:,.0f}", str(row['harga']), 'harga'))
    
    # Konversi ke list dan batasi jumlah
    suggestions_list = list(suggestions)[:max_suggestions]
    
    return suggestions_list

# ========== FUNGSI SORTING ==========

# Selection Sort (Harga: Tertinggi ke Terendah)
def urutkan_harga_desc(arr):
    """Selection Sort - Mengurutkan harga dari tertinggi ke terendah"""
    n = len(arr)
    data_copy = arr.copy()
    
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if data_copy[j]['harga'] > data_copy[max_idx]['harga']:
                max_idx = j
        data_copy[i], data_copy[max_idx] = data_copy[max_idx], data_copy[i]
    return data_copy

# Insertion Sort (Rating: Tertinggi ke Terendah)
def urutkan_rating_desc(arr):
    """Insertion Sort - Mengurutkan rating dari tertinggi ke terendah"""
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

# Quick Sort (Harga: Rendah ke Tertinggi)
def quick_sort_harga_asc(arr):
    """Quick Sort - Mengurutkan harga dari rendah ke tertinggi"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]['harga']
    left = [x for x in arr if x['harga'] < pivot]
    middle = [x for x in arr if x['harga'] == pivot]
    right = [x for x in arr if x['harga'] > pivot]
    
    return quick_sort_harga_asc(left) + middle + quick_sort_harga_asc(right)

# Bubble Sort (Rating: Rendah ke Tertinggi)
def bubble_sort_rating_asc(arr):
    """Bubble Sort - Mengurutkan rating dari rendah ke tertinggi"""
    data_copy = arr.copy()
    n = len(data_copy)
    
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if data_copy[j]['rating'] > data_copy[j + 1]['rating']:
                data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
    return data_copy

# ========== SIDEBAR FILTER ==========

with st.sidebar:
    st.header("🎛️ Filter & Sortir")
    
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
    min_rating = st.slider(
        "Minimal Rating",
        1.0, 5.0, 1.0,
        0.1,
        format="%.1f"
    )
    
    # Filter Kategori (hanya jika kolom 'kategori' ada)
    if 'kategori' in df.columns:
        st.subheader("📂 Filter Kategori")
        semua_kategori = ["Semua"] + sorted(df['kategori'].unique().tolist())
        filter_kategori = st.selectbox("Pilih Kategori:", semua_kategori)
    else:
        filter_kategori = "Semua"
    
    # Pilihan Sorting
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
    
    # Jumlah produk yang ditampilkan
    st.subheader("📦 Tampilkan")
    jumlah_tampil = st.slider("Jumlah produk:", 10, 100, 20, 10)

# ========== FILTER DATA ==========

# Filter berdasarkan harga dan rating
df_filtered = df[
    (df['harga'] >= range_harga[0]) & 
    (df['harga'] <= range_harga[1]) &
    (df['rating'] >= min_rating)
].copy()

# Filter kategori (jika ada dan tidak "Semua")
if 'kategori' in df.columns and filter_kategori != "Semua":
    df_filtered = df_filtered[df_filtered['kategori'] == filter_kategori]

# ========== SEARCH WITH AUTO COMPLETE ==========

st.subheader("🔍 Pencarian Produk")

# Inisialisasi session state untuk search
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_suggestion' not in st.session_state:
    st.session_state.selected_suggestion = None

# Menggunakan columns untuk layout search
col1, col2 = st.columns([3, 1])

with col1:
    # Input text dengan auto complete
    search_input = st.text_input(
        "Cari produk, ID, atau kategori:",
        value=st.session_state.search_query,
        placeholder="Ketik minimal 2 karakter... Contoh: Produk, PRD, Elektronik, atau harga (misal: 50000)",
        key="search_input"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    if st.button("🔄 Reset Pencarian"):
        st.session_state.search_query = ""
        st.session_state.selected_suggestion = None
        st.rerun()

# Auto Complete Suggestions
if search_input and len(search_input) >= 2:
    suggestions = get_search_suggestions(df_filtered, search_input)
    
    if suggestions:
        st.markdown("**💡 Saran pencarian:**")
        
        # Tampilkan suggestions dalam format tombol
        cols = st.columns(min(len(suggestions), 3))
        for idx, (display_text, value, search_type) in enumerate(suggestions):
            col_idx = idx % 3
            with cols[col_idx]:
                if st.button(display_text, key=f"suggestion_{idx}"):
                    st.session_state.search_query = value
                    st.session_state.selected_suggestion = value
                    st.rerun()
        
        st.markdown("---")
    else:
        st.info("ℹ️ Tidak ada saran. Coba kata kunci lain.")

# Proses pencarian berdasarkan input
search_query = st.session_state.search_query if st.session_state.selected_suggestion else search_input

if search_query:
    # Pencarian multi-kolom
    search_pattern = search_query.lower()
    
    # Cari di berbagai kolom
    mask = (
        df_filtered['nama_produk'].str.lower().str.contains(search_pattern, na=False) |
        df_filtered['product_id'].str.lower().str.contains(search_pattern, na=False)
    )
    
    # Tambahkan pencarian di kategori jika ada
    if 'kategori' in df_filtered.columns:
        mask = mask | (df_filtered['kategori'].str.lower().str.contains(search_pattern, na=False))
    
    # Pencarian berdasarkan rentang harga (jika query berupa angka)
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
        st.info("💡 Coba saran pencarian di atas atau gunakan kata kunci lain")

# ========== SORTING DATA ==========

# Konversi ke list of dict untuk sorting manual
data_list = df_filtered.to_dict('records')

if sort_option == "Harga Tertinggi ke Terendah (Selection Sort)":
    with st.spinner("Mengurutkan dengan Selection Sort..."):
        data_list = urutkan_harga_desc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk dengan Selection Sort")
        
elif sort_option == "Harga Terendah ke Tertinggi (Quick Sort)":
    with st.spinner("Mengurutkan dengan Quick Sort..."):
        data_list = quick_sort_harga_asc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk dengan Quick Sort")
        
elif sort_option == "Rating Tertinggi ke Terendah (Insertion Sort)":
    with st.spinner("Mengurutkan dengan Insertion Sort..."):
        data_list = urutkan_rating_desc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk dengan Insertion Sort")
        
elif sort_option == "Rating Terendah ke Tertinggi (Bubble Sort)":
    with st.spinner("Mengurutkan dengan Bubble Sort..."):
        data_list = bubble_sort_rating_asc(data_list)
        st.success(f"✅ Berhasil mengurutkan {len(data_list)} produk dengan Bubble Sort")

# Konversi kembali ke DataFrame
df_sorted = pd.DataFrame(data_list)

# Batasi jumlah tampil
df_display = df_sorted.head(jumlah_tampil)

# ========== TAMPILAN UTAMA ==========

# Metrik
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Produk", len(df))
with col2:
    st.metric("Total Produk (Filter)", len(df_filtered))
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
    if search_query:
        st.metric("Hasil Pencarian", len(df_filtered))

# Tampilkan data dalam bentuk tabel
if not df_display.empty:
    st.subheader(f"📋 Menampilkan {len(df_display)} produk")
    
    # Pilih kolom yang akan ditampilkan
    columns_to_show = ['nomer', 'product_id', 'nama_produk', 'harga', 'rating']
    if 'kategori' in df_display.columns:
        columns_to_show.insert(3, 'kategori')
    
    # Format untuk ditampilkan
    df_display_display = df_display[columns_to_show].copy()
    df_display_display['harga'] = df_display_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    df_display_display['rating'] = df_display_display['rating'].apply(lambda x: f"{x} ⭐")
    
    # Rename kolom
    rename_map = {
        'nomer': 'No.',
        'product_id': 'ID Produk',
        'nama_produk': 'Nama Produk',
        'harga': 'Harga',
        'rating': 'Rating'
    }
    if 'kategori' in df_display_display.columns:
        rename_map['kategori'] = 'Kategori'
    
    df_display_display = df_display_display.rename(columns=rename_map)
    
    st.dataframe(df_display_display, use_container_width=True)
    
    # Tampilkan dalam format card
    with st.expander("🃏 Tampilkan dalam format Grid"):
        cols = st.columns(3)
        for idx, row in df_display.head(30).iterrows():
            with cols[idx % 3]:
                with st.container(border=True):
                    st.subheader(f"📦 {row['nama_produk']}")
                    st.write(f"🆔 ID: {row['product_id']}")
                    if 'kategori' in row:
                        st.write(f"🏷️ Kategori: {row['kategori']}")
                    st.write(f"💰 **Rp {row['harga']:,.0f}**")
                    st.write(f"⭐ Rating: {row['rating']}")
                    
                    # Progress bar untuk rating
                    st.progress(row['rating'] / 5.0)
                    
                    # Tombol aksi
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🛒 Beli", key=f"buy_{row['product_id']}"):
                            st.toast(f"Menambahkan {row['nama_produk']} ke keranjang!", icon="✅")
                    with col2:
                        if st.button(f"❤️ Wishlist", key=f"wish_{row['product_id']}"):
                            st.toast(f"{row['nama_produk']} ditambahkan ke wishlist!", icon="❤️")
    
else:
    st.warning("⚠️ Tidak ada produk yang sesuai dengan filter yang dipilih.")

# ========== STATISTIK ==========

with st.expander("📈 Statistik & Visualisasi"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 Produk dengan Harga Tertinggi")
        if data_list:
            top_harga = urutkan_harga_desc(data_list)[:10]
            top_harga_df = pd.DataFrame(top_harga)
            columns_to_show_stat = ['nama_produk', 'harga', 'rating']
            if 'kategori' in top_harga_df.columns:
                columns_to_show_stat.insert(1, 'kategori')
            st.dataframe(top_harga_df[columns_to_show_stat])
    
    with col2:
        st.subheader("🏆 Top 10 Produk dengan Rating Tertinggi")
        if data_list:
            top_rating = urutkan_rating_desc(data_list)[:10]
            top_rating_df = pd.DataFrame(top_rating)
            columns_to_show_stat = ['nama_produk', 'rating', 'harga']
            if 'kategori' in top_rating_df.columns:
                columns_to_show_stat.insert(1, 'kategori')
            st.dataframe(top_rating_df[columns_to_show_stat])
    
    # Chart distribusi
    if not df_filtered.empty:
        st.subheader("📊 Distribusi Harga Produk")
        st.bar_chart(df_filtered['harga'].value_counts().head(20))
        
        st.subheader("📊 Distribusi Rating")
        rating_counts = df_filtered['rating'].value_counts().sort_index()
        st.line_chart(rating_counts)
    
    # Search history (opsional)
    if search_query:
        st.subheader("🔍 Informasi Pencarian Terakhir")
        st.info(f"Anda mencari: **{search_query}** - Menemukan **{len(df_filtered)}** produk")

# ========== FOOTER ==========
st.divider()
st.caption(f"🔄 Data terakhir diperbarui: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("💡 Fitur Auto Complete: Ketik minimal 2 karakter untuk mendapatkan saran pencarian dari nama produk, ID, kategori, atau harga!")