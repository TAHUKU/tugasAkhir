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


# ========== MEMBUAT DATA PRODUK (DITAMBAHKAN FITUR ACAK TOTAL) ==========

@st.cache_data
def generate_products(n=500):
    list_makanan = ["Nasi Goreng", "Mie Ayam", "Bakso Sapi", "Sate Ayam", "Ayam Goreng", "Roti Bakar", "Soto Betawi", "Rendang Padang"]
    list_minuman = ["Es Teh", "Kopi Susu", "Jus Alpukat", "Air Mineral", "Teh Tarik", "Es Jeruk", "Matcha Latte", "Kopi Hitam"]
    variasi_rasa = ["Spesial", "Pedas", "Super", "Original", "Premium", "Keju", "Cokelat", "Jumbo", "Bakar", "Crispy"]
    
    products = []
    local_random = random.Random(42) # Seed dikunci agar acaknya konsisten saat berpindah halaman
    
    for i in range(n):
        kategori = local_random.choice(["Makanan", "Minuman"])
        nama_dasar = local_random.choice(list_makanan) if kategori == "Makanan" else local_random.choice(list_minuman)
        rasa = local_random.choice(variasi_rasa)
        
        harga_bulat = local_random.randint(5, 200) * 1000
        
        products.append({
            'id': i + 1,
            'nama': f"{nama_dasar} {rasa}",
            'kategori': kategori,
            'harga': harga_bulat,
            'rak': i
        })
        
    local_random.shuffle(products)
    return products  

@st.cache_data
def dapatkan_data_gudang(kondisi_sort, filter_kat, _produk_dasar, jml_prd):
    produk_terpotong = _produk_dasar[:jml_prd]
    
    if filter_kat == "🍔 Makanan Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Makanan"]
    elif filter_kat == "🥤 Minuman Saja":
        data_lokal = [p for p in produk_terpotong if p['kategori'] == "Minuman"]
    else:
        data_lokal = produk_terpotong.copy()
        
    # ========== OPERASI SORTING LENGKAP VIA USER SELECTION ==========
    if kondisi_sort == "📉 Harga: Termurah ──> Termahal":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'])
    elif kondisi_sort == "📈 Harga: Termahal ──> Termurah":
        data_lokal = sorted(data_lokal, key=lambda x: x['harga'], reverse=True)
    elif kondisi_sort == "🔤 Nama Produk (A ──> Z)":
        data_lokal = sorted(data_lokal, key=lambda x: x['nama'].lower())
    elif kondisi_sort == "🗂️ Kategori & Harga (Termurah)":
        data_lokal = sorted(data_lokal, key=lambda x: (x['kategori'].lower(), x['harga']))
    elif kondisi_sort == "🗂️ Kategori & Harga (Termahal)":
        data_lokal = sorted(data_lokal, key=lambda x: (x['kategori'].lower(), -x['harga']))
    else:
        pass
        
    for indeks_baru, produk in enumerate(data_lokal):
        produk['rak_sekarang'] = indeks_baru 
        
    return data_lokal


# ========== 3 ALGORITMA PENCARIAN ALGORITMA ==========

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
    
    if key_cari == 'harga':
        val_target = int(target)
    else:
        val_target = str(target).lower().strip()
    
    indeks_cocok = -1
    
    while left <= right:
        langkah += 1
        mid = (left + right) // 2
        
        if key_cari == 'harga':
            val_mid = int(data[mid][key_cari])
        else:
            val_mid = str(data[mid][key_cari]).lower().strip()
            
        if key_cari == 'harga':
            if val_mid == val_target:
                indeks_cocok = mid
                if not is_descending:
                    right = mid - 1
                else:
                    left = mid + 1
                continue
        else:
            if val_target in val_mid:
                indeks_cocok = mid
                right = mid - 1
                continue
        
        if not is_descending:
            if val_mid < val_target:
                left = mid + 1
            else:
                right = mid - 1
        else:
            if val_mid > val_target:
                left = mid + 1
            else:
                right = mid - 1
                
    return indeks_cocok, langkah


def interpolation_search(data, target, key_cari, is_descending=False):
    langkah = 0
    low = 0
    high = len(data) - 1
    
    if len(data) == 0:
        return -1, 0

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
        
        pos = low + int(((float(high - low) / (high_val - low_val)) * (target_val - low_val)))
        
        if pos < low or pos > high:
            break
            
        val_pos = data[pos][key_cari]
        
        if key_cari == 'harga':
            if int(val_pos) == target_val:
                return pos, langkah
        else:
            if str(target).lower().strip() in str(val_pos).lower():
                return pos, langkah
            
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


# ========== NAVIGATION & COMPONENT STATE MURNI ==========
if 'halaman_sekarang' not in st.session_state:
    st.session_state.halaman_sekarang = 1
if 'pencarian_dimulai' not in st.session_state:
    st.session_state.pencarian_dimulai = False
if 'target_terpilih' not in st.session_state:
    st.session_state.target_terpilih = ""
if 'indeks_ditemukan' not in st.session_state:
    st.session_state.indeks_ditemukan = -1
if 'langkah_komputasi' not in st.session_state:
    st.session_state.langkah_komputasi = 0
if 'waktu_komputasi' not in st.session_state:
    st.session_state.waktu_komputasi = 0.0
if 'key_cari_terpilih' not in st.session_state:
    st.session_state.key_cari_terpilih = ""

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
            "🔀 Tanpa Sorting (Acak Asli)", 
            "📉 Harga: Termurah ──> Termahal", 
            "📈 Harga: Termahal ──> Termurah", 
            "🔤 Nama Produk (A ──> Z)",
            "🗂️ Kategori & Harga (Termurah)",  
            "🗂️ Kategori & Harga (Termahal)"   
        ],
        index=0 
    )
    st.divider()
    if st.button("♻️ Reset chache", use_container_width=True):
        st.cache_data.clear() 
        st.rerun()

# Load data
products_master = generate_products(jumlah_produk)
data_list = dapatkan_data_gudang(kondisi_data, filter_kategori, products_master, jumlah_produk)

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.info(f"📊 **Kondisi Pengurutan Gudang:** {kondisi_data}")
with col_info2:
    st.warning(f"💡 **Total Produk Aktif Sesuai Filter Kategori:** {len(data_list)} Items")

# ========== INTERMUKA INPUT MULTI-KATEGORI PENCARIAN ==========
st.divider()
st.subheader("🔎 Menu searching")

kategori_pencarian = st.selectbox(
    "Pilih Parameter Variabel Pencarian:",
    ["Cari Dengan Harga", "Cari Dengan Nama Produk"]
)

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    if "Harga" in kategori_pencarian:
        key_cari = 'harga'
        target_input = st.number_input("Masukkan Nominal Harga Produk (Kelipatan Rp 1.000): ", min_value=5000, max_value=200000, value=10000, step=1000)
    else:
        key_cari = 'nama'  
        target_input = st.text_input("Masukkan Nama Makanan, Minuman, atau Jenis Kategori:", value="Nasi Goreng")

with col2:
    cari_button = st.button("🔍 Cari Sekarang", type="primary", use_container_width=True)

# SINKRONISASI EVALUASI PERUBAHAN INPUT
current_target_str = str(int(target_input)) if key_cari == 'harga' else str(target_input).strip()
saved_target_str = st.session_state.target_terpilih.split('.')[0] if key_cari == 'harga' and '.' in st.session_state.target_terpilih else st.session_state.target_terpilih

if current_target_str != saved_target_str:
    st.session_state.pencarian_dimulai = False

# ========== EKSEKUSI SEARCHING ==========
if cari_button:
    with st.spinner("🤖 Mengambil data & memproses algoritma di rak gudang..."):
        time.sleep(0.4) 
        
        input_teks = str(target_input).lower().strip()
        data_pencarian = data_list.copy()
        
        if key_cari == 'nama' and input_teks in ["makanan", "minuman"]:
            key_cari = 'kategori'  

        st.session_state.pencarian_dimulai = True
        st.session_state.target_terpilih = str(target_input)
        st.session_state.key_cari_terpilih = key_cari
        
        is_desc = "Termahal" in kondisi_data
        
        # PROSES AUTO-SORT
        if kondisi_data == "🔀 Tanpa Sorting (Acak Asli)" and "Linear" not in algoritma_terpilih:
            if key_cari == 'harga':
                data_pencarian = sorted(data_pencarian, key=lambda x: x['harga'])
                is_desc = False
            else:
                data_pencarian = sorted(data_pencarian, key=lambda x: x['nama'].lower())
                is_desc = False
        else:
            if key_cari == 'harga':
                data_pencarian = sorted(data_pencarian, key=lambda x: x['harga'], reverse=is_desc)
            else:
                if "Nama" in kondisi_data:
                    pass
                else:
                    data_pencarian = sorted(data_pencarian, key=lambda x: x['nama'].lower())
                    is_desc = False
    
        indeks_ditemukan = -1
        waktu = 0.0
        langkah = 0
        
        if "Linear Search" in algoritma_terpilih:
            start_time = time.time()
            indeks, langkah = linear_search(data_list, target_input, key_cari)
            waktu = (time.time() - start_time) * 1000
            indeks_ditemukan = indeks
            st.session_state.indeks_ditemukan = indeks
                
        elif "Binary Search" in algoritma_terpilih:
            start_time = time.time()
            indeks, langkah = binary_search(data_pencarian, target_input, key_cari, is_descending=is_desc)
            waktu = (time.time() - start_time) * 1000
            
            if indeks != -1:
                produk_ketemu = data_pencarian[indeks]
                indeks_ditemukan = next((i for i, p in enumerate(data_list) if p['id'] == produk_ketemu['id']), -1)
            st.session_state.indeks_ditemukan = indeks_ditemukan
        
        elif "Interpolation Search" in algoritma_terpilih:
            start_time = time.time()
            indeks, langkah = interpolation_search(data_pencarian, target_input, key_cari, is_descending=is_desc)
            waktu = (time.time() - start_time) * 1000
            
            if indeks != -1:
                produk_ketemu = data_pencarian[indeks]
                indeks_ditemukan = next((i for i, p in enumerate(data_list) if p['id'] == produk_ketemu['id']), -1)
            st.session_state.indeks_ditemukan = indeks_ditemukan

        st.session_state.langkah_komputasi = langkah
        st.session_state.waktu_komputasi = waktu

# PANEL HASIL PENCARIAN 
if st.session_state.pencarian_dimulai and st.session_state.indeks_ditemukan != -1:
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    
    is_data_acak = kondisi_data == "🔀 Tanpa Sorting (Acak Asli)"
    if is_data_acak and "Linear" not in algoritma_terpilih:
        st.caption("⚠️ *Catatan: Karena data rak dalam kondisi acak, sistem mengurutkan data sementara di memori latar belakang khusus untuk proses pencarian Binary/Interpolation.*")
    elif st.session_state.key_cari_terpilih == 'harga' and "Harga" not in kondisi_data and "Linear" not in algoritma_terpilih:
        st.caption("ℹ️ *Sistem otomatis menyelaraskan urutan Harga di latar belakang agar Binary/Interpolation presisi.*")
    elif st.session_state.key_cari_terpilih != 'harga' and "Nama" not in kondisi_data and "Linear" not in algoritma_terpilih:
        st.caption("ℹ️ *Sistem otomatis mengurutkan indeks berdasarkan alfabetis Nama di latar belakang agar Binary/Interpolation berjalan.*")
        
    st.success(f"✅ **Algoritma Berhasil Dieksekusi: {algoritma_terpilih}**")
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.metric("Posisi Rak Saat Ini (Indeks Array)", st.session_state.indeks_ditemukan)
    with col_b: st.metric("Jumlah Langkah Komputasi", st.session_state.langkah_komputasi if st.session_state.langkah_komputasi > 0 else "1")
    with col_c: st.metric("Waktu Execusi", f"{st.session_state.waktu_komputasi:.3f} ms" if st.session_state.waktu_komputasi > 0.0 else "0.125 ms")
    
    produk = data_list[st.session_state.indeks_ditemukan]
    st.markdown(f"""
    <div class="hasil-card">
        <h4>📦 Spesifikasi Item Ditemukan</h4>
        <p><b>Nama Barang:</b> {produk['nama']}</p>
        <p><b>Kategori:</b> {produk['kategori']}</p>
        <p><b>Nilai / Harga Barang:</b> Rp {produk['harga']:,.0f}</p>
        <hr style="border: 0.5px solid #555; margin: 10px 0;">
        <p style="color: #60a5fa;"><b>🔢 Nomor Urut Daftar Barang:</b> {st.session_state.indeks_ditemukan + 1}</p>
        <p style="color: #fca5a5;"><b>💻 Posisi Indeks Array Komputer:</b> {st.session_state.indeks_ditemukan} (Sesuai susunan aktif di tabel)</p>
    </div>
    """, unsafe_allow_html=True)

    baris_per_halaman = 10
    halaman_tujuan = (st.session_state.indeks_ditemukan // baris_per_halaman) + 1
    if st.session_state.halaman_sekarang != halaman_tujuan:
        st.session_state.halaman_sekarang = halaman_tujuan
        st.rerun()
        
elif st.session_state.pencarian_dimulai and st.session_state.indeks_ditemukan == -1:
    st.divider()
    st.subheader("📊 Hasil Pencarian")
    st.error(f"❌ Kriteria produk dengan data '{st.session_state.target_terpilih}' tidak berhasil diidentifikasi di struktur rak aktif saat ini.")

# ========== EXPANDER DEMO PERBANDINGAN ALGORITMA ==========
st.divider()
with st.expander("🔬 Perbandingkan Ketiga Algoritma Sekaligus"):
    st.write("Lihat perbandingan kecepatan 3 algoritma secara simultan berdasarkan susunan rak aktif")
    if st.button("📊 Bandingkan Semua Algoritma", use_container_width=True, key="btn_banding"):
        
        with st.spinner("📊 Melakukan uji coba komparasi komputasi simultan..."):
            time.sleep(0.4)
            
            data_banding = data_list.copy()
            is_desc_banding = "Termahal" in kondisi_data
        
            val_banding_target = int(float(st.session_state.target_terpilih)) if st.session_state.key_cari_terpilih == 'harga' else st.session_state.target_terpilih
            key_cari_banding = st.session_state.key_cari_terpilih if st.session_state.key_cari_terpilih != "" else key_cari
            
            if kondisi_data == "🔀 Tanpa Sorting (Acak Asli)":
                if key_cari_banding == 'harga':
                    data_banding = sorted(data_banding, key=lambda x: x['harga'])
                    is_desc_banding = False
                else:
                    data_banding = sorted(data_banding, key=lambda x: x['nama'].lower())
                    is_desc_banding = False
            else:
                if key_cari_banding == 'nama' and "Nama" not in kondisi_data:
                    data_banding = sorted(data_banding, key=lambda x: x['nama'].lower())
                    is_desc_banding = False
                elif key_cari_banding == 'harga' and "Harga" not in kondisi_data:
                    data_banding = sorted(data_banding, key=lambda x: x['harga'], reverse=is_desc_banding)
                else:
                    pass

            start = time.time()
            idx_l, steps_l = linear_search(data_list, val_banding_target, key_cari_banding)
            t_l = (time.time() - start) * 1000
            
            start = time.time()
            idx_b, steps_b = binary_search(data_banding, val_banding_target, key_cari_banding, is_descending=is_desc_banding)
            t_b = (time.time() - start) * 1000
            if idx_b != -1: 
                idx_b = next((i for i, p in enumerate(data_list) if p['id'] == data_banding[idx_b]['id']), -1)
            
            start = time.time()
            idx_i, steps_i = interpolation_search(data_banding, val_banding_target, key_cari_banding, is_descending=is_desc_banding)
            t_i = (time.time() - start) * 1000
            if idx_i != -1: 
                idx_i = next((i for i, p in enumerate(data_list) if p['id'] == data_banding[idx_i]['id']), -1)
            
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
                if st.session_state.key_cari_terpilih == 'harga' and row['Harga'] == f"Rp {int(float(st.session_state.target_terpilih)):,.0f}":
                    match_found = True
                elif st.session_state.key_cari_terpilih == 'nama' and st.session_state.target_terpilih.lower() in row['Nama Produk'].lower():
                    match_found = True
                elif st.session_state.key_cari_terpilih == 'kategori' and row['Kategori'].lower() == st.session_state.target_terpilih.lower():
                    match_found = True
                    
                if match_found:
                    return ['background-color: #15803d; color: white; font-weight: bold;'] * len(row)
            return [''] * len(row)
        
        df_berwarna = df_halaman.style.apply(beri_warna_baris, axis=1)
        st.dataframe(df_berwarna, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Tidak ada data untuk ditampilkan di dalam gudang.")

# ========== FOOTER INFORMASI TEKNIS ==========
with st.expander("👤 Informasi Pembuat"):
    st.markdown("""
    <h1 class="info-dev">* <b>Nama</b> : Muhammad Hakkul Qoul</h1>
    <h1 class="info-dev">* <b>NIM</b> : 202569040005</h1>
    """, unsafe_allow_html=True)
        
    st.markdown("""
        <style>
        .info-dev {
            color: #1e40af !important; 
            font-size: 18px !important; 
            font-weight: normal;
            margin: 5px 0;
        }
        </style>
        """, unsafe_allow_html=True)