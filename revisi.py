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
st.write("Menemukan posisi rak (indeks array) berdasarkan Nama, Kategori, atau Harga Produk — Bebas pilih algoritma!")

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

# ========== MEMBUAT DATA PRODUK (FIXED INDENTASI & RETURN VALUE) ==========

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
    
    # PERBAIKAN: Seluruh proses di bawah ini MASUK ke dalam loop 'for'
    for i in range(n):
        kategori = local_random.choice(["Makanan", "Minuman"])
        
        nama_dasar = (
            local_random.choice(list_makanan)
            if kategori == "Makanan"
            else local_random.choice(list_minuman)
        )
        
        # PERMINTAAN ANDA: Harga dibuat bulat kelipatan Rp 1.000 (5000, 6000, 7000, dst.)
        harga_bulat = 5000 + (i * 1000)
        
        products.append({
            'id': i + 1,
            'nama': f"{nama_dasar} (ID: {i+1})",
            'kategori': kategori,
            'harga': harga_bulat,
            'rak': i
        })
        
    return products # WAJIB ADA: Mengirimkan data kembali ke aplikasi# MEMBENARKAN: Mengembalikan list data ke sistem Gudang

@st.cache_data
def dapatkan_data_gudang(kondisi_sort, filter_kat, _produk_dasar, jml_prd):
    produk_terpotong = _produk_dasar[:jml_prd]
    
    if filter_kat == "🍔 Makanan Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Makanan"]
    elif filter_kat == "🥤 Minuman Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Minuman"]
    else:
        data_lokal = produk_terpotong.copy()
        
    # ========== OPERASI SORTING LENGKAP & MULTI-SORTING ==========
    if kondisi_sort == "📉 Harga: Termurah ──> Termahal":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'])
    elif kondisi_sort == "📈 Harga: Termahal ──> Termurah":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'], reverse=True)
    elif kondisi_sort == "🔤 Nama Produk (A ──> Z)":
        data_lokal = sorted(data_lokal, key=lambda x: x['nama'].lower())
        
    # --- PILIHAN MULTI-SORTING BARU ---
    elif kondisi_sort == "🗂️ Kategori & Harga (Termurah)":
        # Mengurutkan kategori (A-Z), lalu harga (Kecil ke Besar)
        data_lokal = sorted(data_lokal, key=lambda x: (x['kategori'].lower(), x['harga']))
    elif kondisi_sort == "🗂️ Kategori & Harga (Termahal)":
        # Mengurutkan kategori (A-Z), lalu harga (Besar ke Kecil menggunakan tanda minus)
        data_lokal = sorted(data_lokal, key=lambda x: (x['kategori'].lower(), -x['harga']))
    # ----------------------------------
        
    else:
        data_lokal = sorted(data_lokal, key=lambda x: x['id'])
        
    for indeks_baru, produk in enumerate(data_lokal):
        produk['rak_sekarang'] = indeks_baru 
        
    return data_lokal

# ========== 3 ALGORITMA PENCARIAN ADAPTIF (FIXED LOGIKA ASCENDING) ==========

def linear_search(data, target, key_cari):
    langkah = 0 
    for i, produk in enumerate(data):
        langkah += 1
        val_data = str(produk[key_cari]).lower() if key_cari != 'harga' else produk[key_cari]
        val_target = str(target).lower() if key_cari != 'harga' else target
        
        if key_cari != 'harga':
            if val_target in val_data:  
                return i, langkah
        else:
            if int(val_data) == int(val_target):
                return i, langkah
    return -1, langkah

def binary_search(data, target, key_cari, is_descending=False):
    langkah = 0
    left, right = 0, len(data) - 1
    
    # Normalisasi target sesuai tipe data
    if key_cari == 'harga':
        val_target = int(target)
    else:
        val_target = str(target).lower().strip()
    
    while left <= right:
        langkah += 1
        mid = (left + right) // 2
        
        # Normalisasi nilai tengah (mid) sesuai tipe data
        if key_cari == 'harga':
            val_mid = int(data[mid][key_cari])
        else:
            val_mid = str(data[mid][key_cari]).lower().strip()
            
        # --- PERBAIKAN LOGIKA PENCOCOKAN (Mencegah TypeError) ---
        if key_cari == 'harga':
            if val_mid == val_target:
                return mid, langkah
        else:
            if val_target in val_mid:
                return mid, langkah
        # --------------------------------------------------------
        
        # Logika pergeseran indeks pencarian
        if not is_descending: # Urutan Menaik (Ascending)
            if val_mid < val_target:
                left = mid + 1
            else:
                right = mid - 1
        else:                 # Urutan Menurun (Descending)
            if val_mid > val_target:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1, langkah


def interpolation_search(data, target, key_cari, is_descending=False):
    langkah = 0
    low = 0
    high = len(data) - 1
    
    if len(data) == 0:
        return -1, 0

    # Fungsi pembantu untuk mengubah nilai menjadi angka murni untuk rumus posisi
    def get_numeric_value(item_val):
        if key_cari == 'harga':
            return int(item_val)
        teks = str(item_val).lower().strip()
        return ord(teks[0]) if len(teks) > 0 else 0

    if key_cari == 'harga':
        target_val = int(target)
    else:
        target_val = get_numeric_value(target)
        
    while low <= high:
        langkah += 1
        low_val = get_numeric_value(data[low][key_cari])
        high_val = get_numeric_value(data[high][key_cari])
        
        if target_val < min(low_val, high_val) or target_val > max(low_val, high_val):
            break
            
        if high_val == low_val:
            val_low = data[low][key_cari]
            if key_cari == 'harga' and int(val_low) == target_val: 
                return low, langkah
            elif key_cari != 'harga' and str(target).lower().strip() in str(val_low).lower(): 
                return low, langkah
            break
        
        # Rumus utama Interpolation Search
        pos = low + int(((float(high - low) / (high_val - low_val)) * (target_val - low_val)))
        
        if pos < low or pos > high:
            break
            
        val_pos = data[pos][key_cari]
        
        # --- PERBAIKAN LOGIKA PENCOCOKAN ---
        if key_cari == 'harga':
            if int(val_pos) == target_val:
                return pos, langkah
        else:
            if str(target).lower().strip() in str(val_pos).lower():
                return pos, langkah
        # -----------------------------------
            
        pos_numeric = get_numeric_value(val_pos)
        if not is_descending:
            if pos_numeric < target_val:
                low = pos + 1
            else:
                high = pos - 1
        else:
            if pos_numeric > target_val:
                low = pos + 1
            else:
                high = pos - 1
                
    return -1, langkah
# ========== NAVIGATION STATE ==========
if 'halaman_sekarang' not in st.session_state:
    st.session_state.halaman_sekarang = 1
if 'pencarian_dimulai' not in st.session_state:
    st.session_state.pencarian_dimulai = False
if 'target_terpilih' not in st.session_state:
    st.session_state.target_terpilih = ""
if 'indeks_ditemukan' not in st.session_state:
    st.session_state.indeks_ditemukan = -1

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
    
    st.subheader("📦 Pengurutan Data Gudang (Sorting)")
    kondisi_data = st.radio(
        "Urutkan susunan data rak berdasarkan:", 
        [
            "📉 Harga: Termurah ──> Termahal", 
            "📈 Harga: Termahal ──> Termurah", 
            "🔤 Nama Produk (A ──> Z)",
            "🗂️ Kategori & Harga (Termurah)",  # Opsi Baru
            "🗂️ Kategori & Harga (Termahal)"   # Opsi Baru
        ]
    )
    # Letakkan ini di bagian paling bawah blok 'with st.sidebar:'
    st.divider()
    if st.button("♻️ Paksa Reset Data & Cache", use_container_width=True):
        st.cache_data.clear() # Menghapus semua memori cache Streamlit
        st.rerun()

# Load data
products_master = generate_products(jumlah_produk)
data_list = dapatkan_data_gudang(kondisi_data, filter_kategori, products_master, jumlah_produk)

# Informasi Atas mengenai item yang aktif
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info(f"📊 **Kondisi Pengurutan Gudang:** {kondisi_data}")
with col_info2:
    st.warning(f"💡 **Total Produk Aktif Sesuai Filter Kategori:** {len(data_list)} Items")

# ========== INTERMUKA INPUT MULTI-KATEGORI PENCARIAN ==========
# ========== INTERMUKA INPUT MULTI-KATEGORI PENCARIAN ==========
# ========== INTERMUKA INPUT 2 PILIHAN (SEDERHANA & PINTAR) ==========
st.divider()
st.subheader("🔎 Menu Operasi Pencarian Pintar")

# Disederhanakan menjadi 2 pilihan sesuai permintaan Anda
kategori_pencarian = st.selectbox(
    "Pilih Parameter Variabel Pencarian:",
    ["Nominal Harga Barang (Angka Bulat)", "Nama Produk / Kategori Menu (Teks)"]
)

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    if "Harga" in kategori_pencarian:
        key_cari = 'harga'
        maks_harga_dinamis = int(5000 + (jumlah_produk * 1000))
        target_input = st.number_input("Masukkan Nominal Harga Produk (Kelipatan Rp 1.000): ", min_value=5000, max_value=maks_harga_dinamis, value=5000, step=1000)
    else:
        key_cari = 'nama'  # Default mencari ke teks nama produk
        target_input = st.text_input("Masukkan Nama Makanan, Minuman, atau Jenis Kategori:", value="Nasi Goreng")

with col2:
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

# ========== EKSEKUSI SEARCHING OPERASI ==========
if cari_button:
    input_teks = str(target_input).lower().strip()
    data_pencarian = data_list.copy()
    
    # KECERDASAN BUATAN: Jika user memilih Teks dan yang diinput adalah keyword kategori murni
    if key_cari == 'nama' and input_teks in ["makanan", "minuman"]:
        key_cari = 'kategori'  # Alihkan pencarian ke kolom kategori agar akurat

    st.session_state.pencarian_dimulai = True
    st.session_state.target_terpilih = str(target_input)
    
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    # --- HANDLING AUTO-SORTING BELAKANG LAYAR AGAR BINARY/INTERPOLATION TIDAK EROR ---
    valid_sort = True
    is_desc = "Termahal" in kondisi_data
    
    if key_cari == 'nama' and "Nama" not in kondisi_data:
        # Jika mencari nama tapi rak di sidebar tidak urut nama, kita urutkan di background
        data_pencarian = sorted(data_pencarian, key=lambda x: x['nama'].lower())
        is_desc = False
        st.caption("ℹ️ *Sistem otomatis mengurutkan indeks berdasarkan alfabetis Nama di latar belakang agar Binary/Interpolation berjalan.*")
        
    elif key_cari == 'harga' and "Harga" not in kondisi_data:
        # Jika mencari harga tapi rak di sidebar tidak urut harga murni, kita urutkan di background
        data_pencarian = sorted(data_pencarian, key=lambda x: x['harga'], reverse=is_desc)
        st.caption("ℹ️ *Sistem otomatis menyelaraskan urutan Harga di latar belakang agar Binary/Interpolation presisi.*")
        
    elif key_cari == 'kategori' and "Kategori" not in kondisi_data:
        # Jika mencari kategori murni tapi rak di sidebar tidak mendukung
        data_pencarian = sorted(data_pencarian, key=lambda x: x['kategori'].lower())
        is_desc = False
        st.caption("ℹ️ *Sistem otomatis mengelompokkan Kategori di latar belakang agar Binary/Interpolation berjalan.*")

    # Jalankan Algoritma
    indeks_ditemukan = -1
    
    if "Linear Search" in algoritma_terpilih:
        with st.spinner("Menjalankan Linear Search..."):
            start_time = time.time()
            indeks, langkah = linear_search(data_list, target_input, key_cari)
            waktu = (time.time() - start_time) * 1000
        nama_algo_info = "Linear Search (O(n))"
        indeks_ditemukan = indeks
        st.session_state.indeks_ditemukan = indeks
            
    elif "Binary Search" in algoritma_terpilih:
        with st.spinner("Menjalankan Binary Search..."):
            start_time = time.time()
            indeks, langkah = binary_search(data_pencarian, target_input, key_cari, is_descending=is_desc)
            waktu = (time.time() - start_time) * 1000
        nama_algo_info = "Binary Search (O(log n))"
        
        if indeks != -1:
            produk_ketemu = data_pencarian[indeks]
            indeks_ditemukan = next(i for i, p in enumerate(data_list) if p['id'] == produk_ketemu['id'])
        st.session_state.indeks_ditemukan = indeks_ditemukan
    
    else:
        with st.spinner("Menjalankan Interpolation Search..."):
            start_time = time.time()
            indeks, langkah = interpolation_search(data_pencarian, target_input, key_cari, is_descending=is_desc)
            waktu = (time.time() - start_time) * 1000
        nama_algo_info = "Interpolation Search (O(log (log n)))"
        
        if indeks != -1:
            produk_ketemu = data_pencarian[indeks]
            indeks_ditemukan = next(i for i, p in enumerate(data_list) if p['id'] == produk_ketemu['id'])
        st.session_state.indeks_ditemukan = indeks_ditemukan

    # Menampilkan Hasil Ke Layar
    if indeks_ditemukan != -1:
        st.success(f"✅ **Algoritma Berhasil: {nama_algo_info}**")
        col_a, col_b, col_c = st.columns(3)
        with col_a: st.metric("Posisi Rak Saat Ini (Indeks Array)", indeks_ditemukan)
        with col_b: st.metric("Jumlah Langkah Komputasi", langkah)
        with col_c: st.metric("Waktu Eksekusi", f"{waktu:.3f} ms")
        
        produk = data_list[indeks_ditemukan]
        st.markdown(f"""
        <div class="hasil-card">
            <h4>📦 Spesifikasi Item Ditemukan</h4>
            <p><b>Nama Barang:</b> {produk['nama']}</p>
            <p><b>Kategori:</b> {produk['kategori']}</p>
            <p><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
            <hr style="border: 0.5px solid #555; margin: 10px 0;">
            <p style="color: #60a5fa;"><b>🔢 Nomor Urut Daftar Barang:</b> {indeks_ditemukan + 1}</p>
            <p style="color: #fca5a5;"><b>💻 Posisi Indeks Array Komputer:</b> {indeks_ditemukan} (Sesuai susunan rak aktif)</p>
        </div>
        """, unsafe_allow_html=True)

        baris_per_halaman = 10
        halaman_tujuan = (indeks_ditemukan // baris_per_halaman) + 1
        if st.session_state.halaman_sekarang != halaman_tujuan:
            st.session_state.halaman_sekarang = halaman_tujuan
            st.rerun()
    else:
        st.session_state.indeks_ditemukan = -1
        st.error(f"❌ Kriteria produk dengan data '{target_input}' tidak berhasil diidentifikasi di struktur rak aktif saat ini.")

if str(target_input) != st.session_state.target_terpilih:
    st.session_state.pencarian_dimulai = False
    st.session_state.indeks_ditemukan = -1

# ========== EXPANDER DEMO PERBANDINGAN ALGORITMA ==========
st.divider()
with st.expander("🔬 Perbandingkan Ketiga Algoritma Sekaligus"):
    st.write("Lihat perbandingan kecepatan 3 algoritma secara simultan berdasarkan susunan rak aktif")
    if st.button("📊 Bandingkan Semua Algoritma", use_container_width=True, key="btn_banding"):
        
        data_banding = data_list.copy()
        is_desc_banding = "Termahal" in kondisi_data
        key_cari_banding = key_cari
        
        # Logika penyelarasan banding balik layar
        if key_cari_banding == 'nama' and "Nama" not in kondisi_data:
            data_banding = sorted(data_banding, key=lambda x: x['nama'].lower())
            is_desc_banding = False
        elif key_cari_banding == 'harga' and "Harga" not in kondisi_data:
            data_banding = sorted(data_banding, key=lambda x: x['harga'], reverse=is_desc_banding)
        elif key_cari_banding == 'kategori' and "Kategori" not in kondisi_data:
            data_banding = sorted(data_banding, key=lambda x: x['kategori'].lower())
            is_desc_banding = False

        start = time.time(); idx_l, steps_l = linear_search(data_list, target_input, key_cari_banding); t_l = (time.time() - start) * 1000
        
        start = time.time(); idx_b, steps_b = binary_search(data_banding, target_input, key_cari_banding, is_descending=is_desc_banding); t_b = (time.time() - start) * 1000
        if idx_b != -1: idx_b = next(i for i, p in enumerate(data_list) if p['id'] == data_banding[idx_b]['id'])
        
        start = time.time(); idx_i, steps_i = interpolation_search(data_banding, target_input, key_cari_banding, is_descending=is_desc_banding); t_i = (time.time() - start) * 1000
        if idx_i != -1: idx_i = next(i for i, p in enumerate(data_list) if p['id'] == data_banding[idx_i]['id'])
        
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
    if not df.empty:
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
            if st.session_state.pencarian_dimulai and st.session_state.indeks_ditemukan != -1:
                match_found = False
                if key_cari == 'harga' and row['Harga'] == f"Rp {int(st.session_state.target_terpilih):,.0f}":
                    match_found = True
                elif key_cari == 'nama' and st.session_state.target_terpilih.lower() in row['Nama Produk'].lower():
                    match_found = True
                elif key_cari == 'kategori' and row['Kategori'].lower() == st.session_state.target_terpilih.lower():
                    match_found = True
                    
                if match_found:
                    return ['background-color: #15803d; color: white; font-weight: bold;'] * len(row)
            return [''] * len(row)
        
        df_berwarna = df_halaman.style.apply(beri_warna_baris, axis=1)
        st.dataframe(df_berwarna, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Tidak ada data untuk ditampilkan di dalam gudang.")

# ========== FOOTER INFORMASI TEKNIS ==========
with st.expander("ℹ️ Panduan Karakteristik Pencarian"):
    st.markdown("""
    * **Jaminan Deteksi**: Angka dan huruf dibandingkan secara terpisah sesuai aturan tipe data primitif, memperbaiki error komparasi string biner di mode urutan menaik.
    """)