import streamlit as st
import random
import time
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="3 Algoritma Pencarian Produk",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Sistem Pencarian Produk di Gudang Digital")
st.write("Menemukan posisi rak (indeks array) berdasarkan ID Produk - Bebas pilih algoritma!")

# ========== MEMBUAT DATA PRODUK ==========

@st.cache_data
def generate_products(n=500):
    """Generate produk dengan ID unik (angka)"""
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
            "🔍 Linear Search (O(n)) - Cek satu per satu",
            "📚 Binary Search (O(log n)) - Bagi dua array (butuh data terurut)",
            "⚡ Hash Map (O(1)) - Pencarian instan (butuh preprocessing)"
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
            "🎲 Data Dinamis (sering berubah)"
        ],
        help="Pilih sesuai kondisi gudang Anda saat ini"
    )
    
    st.divider()
    
    # Info algoritma
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
        
        **3. Hash Map (O(1))**
        - Cara: Mapping ID → indeks pakai dictionary
        - Kelebihan: Paling cepat (instan)
        - Kekurangan: Butuh memori tambahan
        - Cocok: Pencarian sangat sering
        """)


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

def build_hash_map(data):
    """Membangun Hash Map - Preprocessing O(n)"""
    hash_map = {}
    for idx, produk in enumerate(data):
        hash_map[produk['id']] = idx
    return hash_map

def hash_search(hash_map, target_id):
    """Hash Map Search - O(1)"""
    return hash_map.get(target_id, -1)


# ========== GENERATE DATA SESUAI KONDISI ==========

products = generate_products(jumlah_produk)

# Siapkan data berdasarkan kondisi yang dipilih
if kondisi_data == "🔄 Data Acak (Unsorted)":
    data_list = products.copy()
    random.shuffle(data_list)
    st.info("🔄 **Kondisi Data:** Data dalam keadaan ACAK (tidak terurut)")
    
elif kondisi_data == "📊 Data Terurut berdasarkan ID (Sorted)":
    data_list = sorted(products, key=lambda x: x['id'])
    st.success("📊 **Kondisi Data:** Data dalam keadaan TERURUT berdasarkan ID")
    
else:  # Data Dinamis
    data_list = products.copy()
    random.shuffle(data_list)
    st.warning("🎲 **Kondisi Data:** Data DINAMIS (sering berubah-ubah)")


# ========== ANTARMUKA PENGGUNA ==========

st.divider()
st.subheader("🔎 Cari Produk")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    target_id = st.number_input(
        "Masukkan ID Produk yang dicari:",
        min_value=1,
        max_value=jumlah_produk,
        value=random.randint(1, jumlah_produk),
        step=1
    )

with col2:
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

with col3:
    random_button = st.button("🎲 Random ID", use_container_width=True)
    if random_button:
        target_id = random.randint(1, jumlah_produk)
        st.rerun()


# ========== EKSEKUSI PENCARIAN ==========

if cari_button:
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    # Peringatan jika Binary Search dipilih tapi data tidak terurut
    if "Binary Search" in algoritma_terpilih and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.warning("⚠️ **Peringatan:** Binary Search membutuhkan data TERURUT! Hasil mungkin tidak akurat atau tidak ketemu.")
        st.caption("💡 Saran: Pilih kondisi data 'Data Terurut' untuk Binary Search, atau gunakan algoritma lain.")
    
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
            st.info(f"📦 **Produk ditemukan:** {produk['nama']} | 💰 Harga: Rp {produk['harga']:,.0f}")
        else:
            st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan dalam {langkah} langkah!")
    
    elif "Binary Search" in algoritma_terpilih:
        # Untuk binary search, pastikan data terurut dulu
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
            st.info(f"📦 **Produk ditemukan:** {produk['nama']} | 💰 Harga: Rp {produk['harga']:,.0f}")
        else:
            st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan dalam {langkah} langkah!")
    
    else:  # Hash Map
        with st.spinner("Membangun Hash Map (preprocessing)..."):
            start_pre = time.time()
            hash_map = build_hash_map(data_list)
            waktu_pre = (time.time() - start_pre) * 1000
        
        with st.spinner("Menjalankan Hash Search..."):
            start_search = time.time()
            indeks = hash_search(hash_map, target_id)
            waktu_search = (time.time() - start_search) * 1000
        
        st.success(f"✅ **Algoritma: Hash Map (O(1))**")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("Posisi Rak (Indeks)", indeks if indeks != -1 else "❌ Tidak ditemukan")
        with col_b:
            st.metric("Waktu Preprocessing", f"{waktu_pre:.3f} ms")
        with col_c:
            st.metric("Waktu Pencarian", f"{waktu_search:.3f} ms")
        with col_d:
            st.metric("Total Waktu", f"{waktu_pre + waktu_search:.3f} ms")
        
        if indeks != -1:
            produk = data_list[indeks]
            st.info(f"📦 **Produk ditemukan:** {produk['nama']} | 💰 Harga: Rp {produk['harga']:,.0f}")
        else:
            st.error(f"❌ Produk dengan ID {target_id} tidak ditemukan!")


# ========== DEMO PERBANDINGAN KETIGANYA ==========

st.divider()
with st.expander("🔬 Demo: Bandingkan Ketiga Algoritma Sekaligus"):
    st.write("Masukkan ID dan lihat perbandingan kecepatan 3 algoritma secara real-time")
    
    col_demo1, col_demo2 = st.columns([2, 1])
    with col_demo1:
        demo_id = st.number_input("ID untuk demo perbandingan:", min_value=1, max_value=jumlah_produk, value=target_id, key="demo_id")
    with col_demo2:
        bandingkan_button = st.button("📊 Bandingkan Semua Algoritma", use_container_width=True)
    
    if bandingkan_button:
        # Siapkan data terurut untuk binary search
        data_sorted = sorted(data_list, key=lambda x: x['id'])
        
        # Linear Search
        start = time.time()
        idx_linear, steps_linear = linear_search(data_list, demo_id)
        time_linear = (time.time() - start) * 1000
        
        # Binary Search
        start = time.time()
        idx_binary, steps_binary = binary_search(data_sorted, demo_id)
        time_binary = (time.time() - start) * 1000
        
        # Hash Map
        start_pre = time.time()
        hash_map_demo = build_hash_map(data_list)
        time_pre = (time.time() - start_pre) * 1000
        
        start = time.time()
        idx_hash = hash_search(hash_map_demo, demo_id)
        time_hash = (time.time() - start) * 1000
        
        # Tampilkan hasil perbandingan
        comparison_data = {
            "Algoritma": ["Linear Search", "Binary Search", "Hash Map"],
            "Ditemukan": [
                "✅" if idx_linear != -1 else "❌",
                "✅" if idx_binary != -1 else "❌",
                "✅" if idx_hash != -1 else "❌"
            ],
            "Posisi": [
                idx_linear if idx_linear != -1 else "-",
                idx_binary if idx_binary != -1 else "-",
                idx_hash if idx_hash != -1 else "-"
            ],
            "Langkah": [steps_linear, steps_binary, "-"],
            "Waktu (ms)": [f"{time_linear:.3f}", f"{time_binary:.3f}", f"{time_hash:.3f}"]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        # Highlight pemenang
        times = [time_linear, time_binary, time_hash]
        fastest_idx = times.index(min(times))
        fastest_names = ["Linear Search", "Binary Search", "Hash Map"]
        st.success(f"⚡ **Paling cepat:** {fastest_names[fastest_idx]} dengan waktu {min(times):.3f} ms!")


# ========== TABEL DATA PRODUK ==========

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
    st.dataframe(df_display, use_container_width=True, height=400)


# ========== VISUALISASI KECEPATAN ==========

with st.expander("📊 Visualisasi Perbandingan Algoritma"):
    st.subheader("Grafik Kecepatan Teoritis (n = jumlah data)")
    
    ukuran_data = list(range(100, 1001, 100))
    linear_times = [x for x in ukuran_data]
    binary_times = [x * 0.01 for x in ukuran_data]
    hash_times = [1 for _ in ukuran_data]
    
    chart_data = pd.DataFrame({
        'Jumlah Data': ukuran_data,
        'Linear Search O(n)': linear_times,
        'Binary Search O(log n)': binary_times,
        'Hash Map O(1)': hash_times
    })
    
    st.line_chart(chart_data.set_index('Jumlah Data'))
    st.caption("📌 **Grafik simulasi:** Semakin rendah garis, semakin cepat algoritma")
    
    # Tabel rekomendasi
    st.subheader("🎯 Tabel Rekomendasi Pemilihan Algoritma")
    rekomendasi = pd.DataFrame({
        "Kondisi Data": ["Data Acak", "Data Terurut", "Data Dinamis", "Pencarian Jarang", "Pencarian Sering"],
        "Rekomendasi": ["Linear Search", "Binary Search", "Hash Map", "Linear Search", "Hash Map"],
        "Alasan": ["Tidak perlu sorting", "Manfaatkan urutan", "Preprocessing sekali", "Overhead kecil", "Kecepatan maksimal"]
    })
    st.dataframe(rekomendasi, use_container_width=True, hide_index=True)


# ========== REKOMENDASI BERDASARKAN PILIHAN USER ==========

st.divider()
st.subheader("💡 Rekomendasi untuk Pilihan Anda Saat Ini")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Algoritma yang dipilih:** {algoritma_terpilih.split('(')[0].strip()}")
    st.markdown(f"**Kondisi data:** {kondisi_data}")

with col2:
    # Berikan saran
    if "Binary Search" in algoritma_terpilih and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
        st.warning("⚠️ **Saran:** Binary Search tidak optimal untuk data tidak terurut. Pertimbangkan:")
        st.markdown("- Ubah kondisi data ke 'Data Terurut'")
        st.markdown("- Atau pilih Linear Search / Hash Map")
    elif "Linear Search" in algoritma_terpilih and jumlah_produk > 500:
        st.info("💡 **Saran:** Data cukup besar (>500). Linear Search mungkin lambat. Coba Binary Search atau Hash Map.")
    elif "Hash Map" in algoritma_terpilih and kondisi_data == "🔄 Data Acak (Unsorted)":
        st.success("✅ **Saran bagus!** Hash Map sangat cocok untuk data acak dan pencarian cepat.")
    else:
        st.success("✅ Kombinasi algoritma dan kondisi data sudah sesuai!")

st.caption(f"🔄 Data terakhir diperbarui: {time.strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("🏢 Sistem E-Commerce - Bebas pilih 3 Algoritma Pencarian Produk")