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
            'id': i + 1,           # ID Produk (angka)
            'nama': f"Produk {i+1}",
            'harga': random.randint(10000, 1000000),
            'posisi_rak': i        # Posisi rak = indeks array
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
    
    st.subheader("🎯 Pilih Algoritma Pencarian")
    algoritma_terpilih = st.radio(
        "Pilih algoritma:",
        [
            "Linear Search (O(n))",
            "Binary Search (O(log n)) - Data harus terurut",
            "Interpolation Search (O(log n)) - Data harus terurut"
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
    """Linear Search - Mencari posisi rak"""
    langkah = 0
    for i, produk in enumerate(data):
        langkah += 1
        if produk['id'] == target_id:
            return i, langkah, produk
    return -1, langkah, None

def binary_search(data, target_id):
    """Binary Search - Mencari posisi rak (data harus terurut)"""
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

# def hash_search(data, target_id):
#     """Hash Map Search - Pencarian instan"""
#     # Preprocessing: buat mapping ID → posisi rak
#     hash_map = {}
#     for idx, produk in enumerate(data):
#         hash_map[produk['id']] = idx
    
#     # Pencarian O(1)
#     posisi = hash_map.get(target_id, -1)
#     produk = data[posisi] if posisi != -1 else None
#     return posisi, 1, produk

# def interpolation_search(data, target_id):
#     """Interpolation Search - Mencari posisi rak (data harus terurut)"""
#     # data.sort()
#     data.sort(key=lambda x: x['id'])
#     low, high = 0, len(data) - 1

#     while low <= high and target_id >= data[low] and target_id <= data[high]:
#         if low == high:
#             if data[low] == target_id:
#                 return low
#             return -1
        
#         # posisi = low + int(((float(high - low) / (data[high] - data[low])) * (target_id - data[low])))
#         posisi = low + int(((high - low) / (data[high]['id'] - data[low]['id'])) * (target_id_int - data[low]['id']))
        
#         if data[posisi] == target_id:
#             return posisi
        
#         if data[posisi] < target_id:
#             low = posisi + 1
#         else:
#             high = posisi - 1
    
#     return -1
def interpolation_search(data, target_id):
    """Interpolation Search - Mencari posisi rak (data HARUS sudah terurut sebelum masuk ke fungsi ini)"""
    langkah = 0
    low, high = 0, len(data) - 1  # Ganti data_sorted menjadi data

    while low <= high and target_id >= data[low]['id'] and target_id <= data[high]['id']:
        langkah += 1
        
        if low == high:
            if data[low]['id'] == target_id:
                return low, langkah, data[low]
            return -1, langkah, None
        
        # Rumus Interpolasi (Ganti data_sorted menjadi data)
        posisi = low + int(((high - low) / (data[high]['id'] - data[low]['id'])) * (target_id - data[low]['id']))
        
        if data[posisi]['id'] == target_id:
            return posisi, langkah, data[posisi]
        
        if data[posisi]['id'] < target_id:
            low = posisi + 1
        else:
            high = posisi - 1
            
    return -1, langkah, None


# ========== FORM PENCARIAN MANUAL ==========

st.divider()
st.subheader("🔍 Cari Produk Berdasarkan ID")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # INPUT MANUAL - user harus ngetik sendiri ID nya
    target_id = st.text_input(
        "Masukkan ID Produk (angka):",
        value="",
        placeholder="278, 500, 1000",
        help="Ketikkan ID produk yang ingin dicari, lalu tekan tombol Cari"
    )

with col2:
    cari_button = st.button("🔍 Cari Posisi Rak", type="primary", use_container_width=True)

with col3:
    # Tombol random ID, tapi ID akan muncul di input dan TIDAK berubah kecuali user klik lagi
    if st.button("🎲 Random ID", use_container_width=True):
        random_id = str(random.randint(1, jumlah_produk))
        target_id = random_id
        st.rerun()


# ========== HASIL PENCARIAN ==========

if cari_button:
    # Validasi input: apakah kosong atau bukan angka
    if not target_id:
        st.error("❌ Silakan masukkan ID produk terlebih dahulu!")
    elif not target_id.isdigit():
        st.error(f"❌ '{target_id}' bukan angka yang valid! ID produk harus berupa angka.")
    else:
        target_id_int = int(target_id)
        
        # Validasi apakah ID dalam range
        if target_id_int < 1 or target_id_int > jumlah_produk:
            st.warning(f"⚠️ ID {target_id_int} berada di luar range! ID produk yang tersedia: 1 - {jumlah_produk}")
        else:
            st.divider()
            st.subheader("📊 Hasil Pencarian Posisi Rak")
            
            # Peringatan untuk Binary Search
            if "Binary Search" in algoritma_terpilih and kondisi_data != "Data Terurut berdasarkan ID":
                st.warning("⚠️ Binary Search membutuhkan data TERURUT! Hasil mungkin tidak akurat.")
            
            # Jalankan algoritma sesuai pilihan
            if "Linear Search" in algoritma_terpilih:
                with st.spinner("Menjalankan Linear Search..."):
                    start_time = time.time()
                    posisi, langkah, produk = linear_search(data_list, target_id_int)
                    waktu = (time.time() - start_time) * 1000
                
                st.success(f"**Algoritma:** Linear Search (O(n))")
                
                # TAMPILKAN HASIL
                if posisi != -1:
                    st.markdown(f"""
                    ### ✅ Produk Ditemukan!
                    
                    | Informasi | Hasil |
                    |-----------|-------|
                    | **ID Produk yang Dicari** | {target_id} |
                    | **Nama Produk** | {produk['nama']} |
                    | **Harga** | Rp {produk['harga']:,.0f} |
                    | **📍 Posisi Rak (Indeks Array)** | **{posisi}** |
                    | **Jumlah Langkah Pencarian** | {langkah} |
                    | **Waktu Eksekusi** | {waktu:.3f} ms |
                    """)
                    
                    # Visualisasi posisi rak
                    st.progress(min(posisi / len(data_list), 1.0))
                    st.caption(f"📊 Posisi rak {posisi} dari {len(data_list)-1} rak yang tersedia")
                else:
                    st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan di rak manapun!")
                    st.metric("Jumlah Langkah Pencarian", langkah)
            
            elif "Binary Search" in algoritma_terpilih:
                # Pastikan data terurut untuk binary search
                data_sorted = sorted(data_list, key=lambda x: x['id'])
                
                with st.spinner("Menjalankan Binary Search..."):
                    start_time = time.time()
                    posisi, langkah, produk = binary_search(data_sorted, target_id_int)
                    waktu = (time.time() - start_time) * 1000
                
                st.success(f"**Algoritma:** Binary Search (O(log n))")
                
                if posisi != -1:
                    st.markdown(f"""
                    ### ✅ Produk Ditemukan!
                    
                    | Informasi | Hasil |
                    |-----------|-------|
                    | **ID Produk yang Dicari** | {target_id} |
                    | **Nama Produk** | {produk['nama']} |
                    | **Harga** | Rp {produk['harga']:,.0f} |
                    | **📍 Posisi Rak (Indeks Array)** | **{posisi}** |
                    | **Jumlah Langkah Pencarian** | {langkah} |
                    | **Waktu Eksekusi** | {waktu:.3f} ms |
                    """)
                    
                    # Visualisasi posisi rak
                    st.progress(min(posisi / len(data_sorted), 1.0))
                    st.caption(f"📊 Posisi rak {posisi} dari {len(data_sorted)-1} rak yang tersedia")
                else:
                    st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan!")
                    st.metric("Jumlah Langkah Pencarian", langkah)
            
            else:  # Hash Map
                # with st.spinner("Menjalankan Hash Map Search..."):
                #     start_time = time.time()
                #     posisi, langkah, produk = hash_search(data_list, target_id_int)
                #     waktu = (time.time() - start_time) * 1000
                with st.spinner("Menjalankan Interpolation Search..."):
                    start_time = time.time()
                    posisi, langkah, produk = interpolation_search(data_list, target_id_int)
                    waktu = (time.time() - start_time) * 1000
                
                st.success(f"**Algoritma:** Interpolation Search (O(log n))")
                
                if posisi != -1:
                    st.markdown(f"""
                    ### ✅ Produk Ditemukan!
                    
                    | Informasi | Hasil |
                    |-----------|-------|
                    | **ID Produk yang Dicari** | {target_id} |
                    | **Nama Produk** | {produk['nama']} |
                    | **Harga** | Rp {produk['harga']:,.0f} |
                    | **📍 Posisi Rak (Indeks Array)** | **{posisi}** |
                    | **Jumlah Langkah Pencarian** | {langkah} (langsung dari interpolation) |
                    | **Waktu Eksekusi** | {waktu:.3f} ms |
                    """)
                    
                    # Visualisasi posisi rak
                    st.progress(min(posisi / len(data_list), 1.0))
                    st.caption(f"📊 Posisi rak {posisi} dari {len(data_list)-1} rak yang tersedia")
                else:
                    st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan!")


# ========== TABEL POSISI RAK SEMUA PRODUK ==========

with st.expander("📋 Lihat Seluruh Data & Posisi Rak"):
    df = pd.DataFrame(data_list)
    df_display = df[['id', 'nama', 'harga', 'posisi_rak']].copy()
    df_display['harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    df_display = df_display.rename(columns={
        'id': 'ID Produk',
        'nama': 'Nama Produk',
        'harga': 'Harga',
        'posisi_rak': '📍 Posisi Rak (Indeks)'
    })
    st.dataframe(df_display, use_container_width=True, height=400)
    st.caption(f"💡 **Posisi Rak** adalah indeks array dimana produk disimpan. Dari 0 hingga {len(data_list)-1}")


# ========== CONTOH PENGGUNAAN ==========

# with st.expander("📖 Contoh Penggunaan"):
#     st.markdown(f"""
#     ### Cara Mencari Produk:
    
#     1. **Ketikkan ID produk** di kolom input (contoh: 278, 500, 750)
#     2. **Pilih algoritma** yang ingin digunakan di sidebar
#     3. **Klik tombol "Cari Posisi Rak"**
#     4. Lihat hasil: **📍 Posisi Rak (Indeks Array)** adalah output utama!
    
#     ### Contoh Input:
#     - Jika ingin mencari ID = 278, cukup ketik `278`
#     - Jika ingin mencari ID = 500, cukup ketik `500`
    
#     ### Tombol Random ID:
#     - Klik "🎲 Random ID" untuk mengisi input dengan ID acak
#     - ID akan muncul di kolom input, lalu Anda bisa klik "Cari"
#     - ID TIDAK akan berubah sendiri, hanya berubah jika Anda klik Random lagi atau ketik manual
#     """)


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
                
                # Linear Search
                start = time.time()
                pos_linear, steps_linear, prod_linear = linear_search(data_list, compare_id_int)
                time_linear = (time.time() - start) * 1000
                
                # Binary Search
                start = time.time()
                pos_binary, steps_binary, prod_binary = binary_search(data_sorted, compare_id_int)
                time_binary = (time.time() - start) * 1000
                
                # Hash Map
                # start = time.time()
                # pos_hash, steps_hash, prod_hash = hash_search(data_list, compare_id_int)
                # time_hash = (time.time() - start) * 1000
                
                # interpolation search
                start = time.time()
                pos_inter, steps_hash, prod_hash = interpolation_search(data_sorted, compare_id_int)
                time_inter = (time.time() - start) * 1000
                
                # Tabel perbandingan FOKUS pada POSISI RAK
                comparison = pd.DataFrame({
                    "Algoritma": ["Linear Search", "Binary Search", "Interpolation search"],
                    "📍 Posisi Rak": [
                        pos_linear if pos_linear != -1 else "Tidak ditemukan",
                        pos_binary if pos_binary != -1 else "Tidak ditemukan",
                        pos_inter if pos_inter != -1 else "Tidak ditemukan"
                    ],
                    "Jumlah Langkah": [steps_linear, steps_binary, steps_hash],
                    "Waktu (ms)": [f"{time_linear:.3f}", f"{time_binary:.3f}", f"{time_inter:.3f}"]
                })
                
                st.dataframe(comparison, use_container_width=True, hide_index=True)
                
                if pos_linear != -1:
                    st.success(f"📦 **Produk {prod_linear['nama']}** (ID: {compare_id}) berada di **Posisi Rak {pos_linear}**")

st.caption(f"🔄 Data terakhir diperbarui: {time.strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("🎯 Tugas: Menemukan POSISI RAK (INDEKS ARRAY) berdasarkan ID Produk yang diINPUT MANUAL")