import streamlit as st
import random
import time
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Pencarian Posisi Rak Digital",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Pencarian Posisi Barang di Rak Digital")
st.write("Menemukan **posisi rak (indeks array)** berdasarkan ID Produk menggunakan 3 algoritma pencarian")

# ========== MEMBUAT DATA PRODUK ==========

@st.cache_data
def generate_products(n=500):
    """Generate produk dengan ID dan posisi rak (indeks array)"""
    products = []
    for i in range(n):
        products.append({
            'id': i + 1,                    # ID Produk (1, 2, 3, ...)
            'nama': f"Produk {i+1}",
            'harga': random.randint(10000, 1000000),
            'posisi_rak': i                  # Indeks array mulai dari 0
        })
    return products

# ========== FUNGSI AUTO COMPLETE ==========

def get_id_suggestions(data_list, query, max_suggestions=5):
    """
    Mendapatkan saran ID produk berdasarkan input user
    """
    if not query or len(query) < 1:
        return []
    
    suggestions = []
    query_lower = query.lower()
    
    # Cari ID yang mengandung kata kunci yang diketik
    for produk in data_list:
        id_str = str(produk['id'])
        if query_lower in id_str.lower():
            suggestions.append({
                'id': produk['id'],
                'nama': produk['nama'],
                'harga': produk['harga'],
                'posisi_rak': produk['posisi_rak']
            })
        if len(suggestions) >= max_suggestions:
            break
    
    return suggestions

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
    
    st.subheader("🎯 Pilih Algoritma Pencarian")
    algoritma_terpilih = st.radio(
        "Pilih algoritma:",
        [
            "Linear Search (O(n))",
            "Binary Search (O(log n)) - Data harus terurut",
            "Hash Map (O(1)) - Paling cepat"
        ]
    )
    
    st.divider()
    
    st.subheader("📦 Kondisi Data")
    kondisi_data = st.radio(
        "Kondisi data di gudang:",
        [
            "Data Acak (Unsorted)",
            "Data Terurut berdasarkan ID"
        ]
    )

# Generate data
products = generate_products(jumlah_produk)

# Siapkan data sesuai kondisi
if kondisi_data == "Data Acak (Unsorted)":
    data_list = products.copy()
    random.shuffle(data_list)
    st.info("📦 **Kondisi:** Data dalam keadaan ACAK")
else:
    data_list = sorted(products, key=lambda x: x['id'])
    st.success("📚 **Kondisi:** Data dalam keadaan TERURUT berdasarkan ID")


# ========== 3 ALGORITMA PENCARIAN ==========

def linear_search(data, target_id):
    """Linear Search - Mencari posisi rak (indeks array)"""
    langkah = 0
    for i, produk in enumerate(data):
        langkah += 1
        if produk['id'] == target_id:
            return i, langkah, produk
    return -1, langkah, None

def binary_search(data, target_id):
    """Binary Search - Mencari posisi rak (indeks array)"""
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
    """Hash Map Search - Pencarian instan"""
    hash_map = {}
    for idx, produk in enumerate(data):
        hash_map[produk['id']] = idx
    
    posisi = hash_map.get(target_id, -1)
    produk = data[posisi] if posisi != -1 else None
    return posisi, 1, produk


# ========== SESSION STATE UNTUK AUTO COMPLETE ==========

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_id' not in st.session_state:
    st.session_state.selected_id = None


# ========== FORM PENCARIAN DENGAN AUTO COMPLETE ==========

st.divider()
st.subheader("🔍 Cari Produk Berdasarkan ID")

st.info("💡 **Fitur Auto Complete:** Ketik angka ID, akan muncul saran produk!")

# Input dengan auto complete
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Input text dengan on_change untuk auto complete
    search_input = st.text_input(
        "Masukkan ID Produk (angka):",
        value=st.session_state.search_query,
        placeholder="Ketik angka... Contoh: 278, 500, 1000",
        help="Ketik minimal 1 angka, akan muncul saran ID yang cocok",
        key="search_input"
    )

with col2:
    cari_button = st.button("🔍 Cari Posisi Rak", type="primary", use_container_width=True)

with col3:
    if st.button("🎲 Random ID", use_container_width=True):
        random_id = str(random.randint(1, jumlah_produk))
        st.session_state.search_query = random_id
        st.session_state.selected_id = int(random_id)
        st.rerun()


# ========== AUTO COMPLETE SUGGESTIONS ==========

# Update session state saat user mengetik
if search_input != st.session_state.search_query:
    st.session_state.search_query = search_input
    st.session_state.selected_id = None

# Tampilkan saran auto complete jika user sedang mengetik
if search_input and len(search_input) >= 1 and st.session_state.selected_id is None:
    suggestions = get_id_suggestions(data_list, search_input, max_suggestions=5)
    
    if suggestions:
        st.markdown("**💡 Saran ID Produk (klik untuk pilih):**")
        
        # Tampilkan saran dalam bentuk tombol
        cols = st.columns(min(len(suggestions), 5))
        for idx, suggestion in enumerate(suggestions[:5]):
            with cols[idx % 5]:
                if st.button(
                    f"🆔 {suggestion['id']}", 
                    key=f"suggest_{suggestion['id']}_{idx}",
                    use_container_width=True
                ):
                    st.session_state.search_query = str(suggestion['id'])
                    st.session_state.selected_id = suggestion['id']
                    st.rerun()
        
        # Tampilkan preview produk yang disarankan
        with st.expander("📦 Lihat detail produk yang disarankan"):
            for suggestion in suggestions[:3]:
                st.markdown(f"""
                - **ID {suggestion['id']}** - {suggestion['nama']} - Rp {suggestion['harga']:,.0f} - Posisi Rak: {suggestion['posisi_rak']}
                """)
        
        st.markdown("---")
    elif len(search_input) >= 1:
        st.warning(f"⚠️ Tidak ada ID yang mengandung angka '{search_input}'")


# ========== PROSES PENCARIAN ==========

# Gunakan ID yang dipilih dari auto complete atau dari input manual
target_id_to_search = None

if st.session_state.selected_id is not None:
    target_id_to_search = st.session_state.selected_id
    target_id_display = str(st.session_state.selected_id)
elif search_input and search_input.isdigit():
    target_id_to_search = int(search_input)
    target_id_display = search_input
else:
    target_id_to_search = None
    target_id_display = search_input

if cari_button:
    if not target_id_display:
        st.error("❌ Silakan masukkan ID produk terlebih dahulu!")
    elif not target_id_display.isdigit():
        st.error(f"❌ '{target_id_display}' bukan angka yang valid! ID produk harus berupa angka.")
    else:
        target_id_int = int(target_id_display)
        
        if target_id_int < 1 or target_id_int > jumlah_produk:
            st.warning(f"⚠️ ID {target_id_int} berada di luar range! ID produk yang tersedia: 1 - {jumlah_produk}")
        else:
            st.divider()
            st.subheader("📊 Hasil Pencarian Posisi Rak")
            
            if "Binary Search" in algoritma_terpilih and kondisi_data != "Data Terurut berdasarkan ID":
                st.warning("⚠️ Binary Search membutuhkan data TERURUT! Hasil mungkin tidak akurat.")
            
            if "Linear Search" in algoritma_terpilih:
                with st.spinner("Menjalankan Linear Search..."):
                    start_time = time.time()
                    posisi, langkah, produk = linear_search(data_list, target_id_int)
                    waktu = (time.time() - start_time) * 1000
                
                st.success(f"**Algoritma:** Linear Search (O(n))")
                
                if posisi != -1:
                    nomor_urut = posisi + 1
                    
                    st.markdown(f"""
                    ### ✅ Produk Ditemukan!
                    
                    | Informasi | Hasil |
                    |-----------|-------|
                    | **ID Produk yang Dicari** | {target_id_int} |
                    | **Nama Produk** | {produk['nama']} |
                    | **Harga** | Rp {produk['harga']:,.0f} |
                    | **📍 Posisi Rak (Indeks Array)** | **{posisi}** (mulai dari 0) |
                    | **📋 Nomor Urut di Tabel** | **{nomor_urut}** (mulai dari 1) |
                    | **Jumlah Langkah Pencarian** | {langkah} |
                    | **Waktu Eksekusi** | {waktu:.3f} ms |
                    """)
                    
                    st.progress(min(posisi / len(data_list), 1.0))
                    st.caption(f"📊 Posisi rak {posisi} (indeks ke-{posisi}) dari total {len(data_list)} rak")
                else:
                    st.error(f"❌ Produk dengan ID {target_id_int} tidak ditemukan!")
                    st.metric("Jumlah Langkah Pencarian", langkah)
            
            elif "Binary Search" in algoritma_terpilih:
                data_sorted = sorted(data_list, key=lambda x: x['id'])
                
                with st.spinner("Menjalankan Binary Search..."):
                    start_time = time.time()
                    posisi, langkah, produk = binary_search(data_sorted, target_id_int)
                    waktu = (time.time() - start_time) * 1000
                
                st.success(f"**Algoritma:** Binary Search (O(log n))")
                
                if posisi != -1:
                    nomor_urut = posisi + 1
                    
                    st.markdown(f"""
                    ### ✅ Produk Ditemukan!
                    
                    | Informasi | Hasil |
                    |-----------|-------|
                    | **ID Produk yang Dicari** | {target_id_int} |
                    | **Nama Produk** | {produk['nama']} |
                    | **Harga** | Rp {produk['harga']:,.0f} |
                    | **📍 Posisi Rak (Indeks Array)** | **{posisi}** (mulai dari 0) |
                    | **📋 Nomor Urut di Tabel** | **{nomor_urut}** (mulai dari 1) |
                    | **Jumlah Langkah Pencarian** | {langkah} |
                    | **Waktu Eksekusi** | {waktu:.3f} ms |
                    """)
                    
                    st.progress(min(posisi / len(data_sorted), 1.0))
                    st.caption(f"📊 Posisi rak {posisi} (indeks ke-{posisi}) dari total {len(data_sorted)} rak")
                else:
                    st.error(f"❌ Produk dengan ID {target_id_int} tidak ditemukan!")
                    st.metric("Jumlah Langkah Pencarian", langkah)
            
            else:
                with st.spinner("Menjalankan Hash Map Search..."):
                    start_time = time.time()
                    posisi, langkah, produk = hash_search(data_list, target_id_int)
                    waktu = (time.time() - start_time) * 1000
                
                st.success(f"**Algoritma:** Hash Map (O(1))")
                
                if posisi != -1:
                    nomor_urut = posisi + 1
                    
                    st.markdown(f"""
                    ### ✅ Produk Ditemukan!
                    
                    | Informasi | Hasil |
                    |-----------|-------|
                    | **ID Produk yang Dicari** | {target_id_int} |
                    | **Nama Produk** | {produk['nama']} |
                    | **Harga** | Rp {produk['harga']:,.0f} |
                    | **📍 Posisi Rak (Indeks Array)** | **{posisi}** (mulai dari 0) |
                    | **📋 Nomor Urut di Tabel** | **{nomor_urut}** (mulai dari 1) |
                    | **Jumlah Langkah Pencarian** | {langkah} (langsung dari hash map) |
                    | **Waktu Eksekusi** | {waktu:.3f} ms |
                    """)
                    
                    st.progress(min(posisi / len(data_list), 1.0))
                    st.caption(f"📊 Posisi rak {posisi} (indeks ke-{posisi}) dari total {len(data_list)} rak")
                else:
                    st.error(f"❌ Produk dengan ID {target_id_int} tidak ditemukan!")


# ========== TABEL POSISI RAK SEMUA PRODUK ==========

with st.expander("📋 Lihat Seluruh Data & Posisi Rak"):
    df = pd.DataFrame(data_list)
    df_display = df[['id', 'nama', 'harga', 'posisi_rak']].copy()
    
    df_display['nomor_urut'] = df_display['posisi_rak'] + 1
    df_display['harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    
    df_display = df_display.rename(columns={
        'id': 'ID Produk',
        'nama': 'Nama Produk',
        'harga': 'Harga',
        'posisi_rak': '📍 Posisi Rak (Indeks Array)',
        'nomor_urut': '📋 Nomor Urut (Mulai 1)'
    })
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    st.info("""
    **Penjelasan Perbedaan:**
    - **📍 Posisi Rak (Indeks Array)** = Mulai dari **0** (posisi sebenarnya dalam memori)
    - **📋 Nomor Urut** = Mulai dari **1** (nomor yang terlihat di tabel)
    
    **Rumus:** `Nomor Urut = Posisi Rak + 1`
    """)


# ========== FITUR AUTO COMPLETE SEARCH (PENCARIAN LANGSUNG) ==========

with st.expander("🔎 Cari Langsung dengan Auto Complete"):
    st.write("Ketik ID di kolom bawah, lalu pilih dari saran yang muncul")
    
    quick_search = st.text_input(
        "Cari ID produk:",
        placeholder="Ketik angka...",
        key="quick_search"
    )
    
    if quick_search and len(quick_search) >= 1:
        suggestions = get_id_suggestions(data_list, quick_search, max_suggestions=10)
        
        if suggestions:
            for sugg in suggestions:
                col_a, col_b, col_c, col_d = st.columns([1, 3, 2, 2])
                with col_a:
                    st.write(f"**🆔 {sugg['id']}**")
                with col_b:
                    st.write(sugg['nama'])
                with col_c:
                    st.write(f"Rp {sugg['harga']:,.0f}")
                with col_d:
                    if st.button(f"Cari", key=f"quick_{sugg['id']}"):
                        st.session_state.search_query = str(sugg['id'])
                        st.session_state.selected_id = sugg['id']
                        st.rerun()
                st.divider()
        else:
            st.warning(f"Tidak ada ID yang mengandung '{quick_search}'")


# ========== CONTOH PENGGUNAAN AUTO COMPLETE ==========

with st.expander("📖 Cara Menggunakan Auto Complete"):
    st.markdown("""
    ### Fitur Auto Complete:
    
    1. **Ketik angka** di kolom pencarian (minimal 1 angka)
    2. **Saran ID** akan muncul di bawah kolom input
    3. **Klik saran ID** yang diinginkan untuk memilih
    4. ID akan terisi otomatis
    5. **Klik tombol "Cari Posisi Rak"** untuk mencari
    
    ### Contoh:
    - Ketik `27` → akan muncul saran: 27, 127, 227, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279
    - Klik `278` → ID terisi 278
    - Klik "Cari" → sistem mencari posisi rak dari ID 278
    
    ### Keuntungan Auto Complete:
    - ✅ Tidak perlu mengingat ID lengkap
    - ✅ Menghindari kesalahan pengetikan
    - ✅ Melihat preview produk sebelum mencari
    - ✅ Lebih cepat dan efisien
    """)


# ========== PERBANDINGAN KETIGANYA ==========

with st.expander("🔬 Bandingkan Ketiga Algoritma"):
    st.write("Masukkan ID yang sama untuk melihat perbandingan kecepatan 3 algoritma")
    
    compare_id = st.text_input(
        "ID untuk perbandingan:",
        value="",
        placeholder="Masukkan ID produk",
        key="compare_id"
    )
    
    if st.button("Bandingkan Semua Algoritma", key="compare_btn"):
        if not compare_id:
            st.warning("⚠️ Silakan masukkan ID terlebih dahulu!")
        elif not compare_id.isdigit():
            st.warning(f"⚠️ '{compare_id}' bukan angka yang valid!")
        else:
            compare_id_int = int(compare_id)
            
            if compare_id_int < 1 or compare_id_int > jumlah_produk:
                st.warning(f"⚠️ ID {compare_id_int} di luar range! Range: 1 - {jumlah_produk}")
            else:
                data_sorted = sorted(data_list, key=lambda x: x['id'])
                
                start = time.time()
                pos_linear, steps_linear, prod_linear = linear_search(data_list, compare_id_int)
                time_linear = (time.time() - start) * 1000
                
                start = time.time()
                pos_binary, steps_binary, prod_binary = binary_search(data_sorted, compare_id_int)
                time_binary = (time.time() - start) * 1000
                
                start = time.time()
                pos_hash, steps_hash, prod_hash = hash_search(data_list, compare_id_int)
                time_hash = (time.time() - start) * 1000
                
                comparison = pd.DataFrame({
                    "Algoritma": ["Linear Search", "Binary Search", "Hash Map"],
                    "📍 Posisi Rak": [
                        pos_linear if pos_linear != -1 else "Tidak ditemukan",
                        pos_binary if pos_binary != -1 else "Tidak ditemukan",
                        pos_hash if pos_hash != -1 else "Tidak ditemukan"
                    ],
                    "📋 Nomor Urut": [
                        pos_linear + 1 if pos_linear != -1 else "-",
                        pos_binary + 1 if pos_binary != -1 else "-",
                        pos_hash + 1 if pos_hash != -1 else "-"
                    ],
                    "Jumlah Langkah": [steps_linear, steps_binary, steps_hash],
                    "Waktu (ms)": [f"{time_linear:.3f}", f"{time_binary:.3f}", f"{time_hash:.3f}"]
                })
                
                st.dataframe(comparison, use_container_width=True, hide_index=True)
                
                if pos_linear != -1:
                    st.success(f"📦 **Produk {prod_linear['nama']}** (ID: {compare_id}) berada di **Posisi Rak {pos_linear}**")

st.caption(f"🔄 Data terakhir diperbarui: {time.strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("🎯 Fitur Auto Complete: Ketik angka untuk mendapatkan saran ID produk")