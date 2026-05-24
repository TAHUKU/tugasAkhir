import streamlit as st
import random
import time
import pandas as pd

# Konfigurasi halaman utama
st.set_page_config(
    page_title="Warehouse Analytics System",
    page_icon="🔍",
    layout="wide"
)

# ====================================================================
# ALTERNATIF UI/UX: CONCEPT MINIMALIST & TABBED DASHBOARD (CLEAN & MODERN)
# ====================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Mengubah font global menjadi Plus Jakarta Sans (Sangat tren untuk Dashboard modern) */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0b0f19; /* Gelap pekat yang super clean */
    }
    
    /* SIDEBAR GLASS STYLE */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937;
    }
    
    /* Desain teks pilihan radio button di sidebar */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label p {
        font-size: 13.5px !important;
        font-weight: 400 !important;
        color: #9ca3af !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover p {
        color: #60a5fa !important;
    }

    /* MENGHILANGKAN BORDER BAWAAN CONTAINER (MEMBUATNYA BORDERLESS) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 0px !important;
    }
    
    /* GAYA TAB MODERN */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #9ca3af !important;
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
        transition: all 0.3s ease;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #3b82f6 !important; /* Warna biru neon saat aktif */
        border-bottom: 2px solid #3b82f6 !important;
    }

    /* GAYA MODERN BADGE STATUS (BORDERLESS CHIPS) */
    .status-chip {
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 13px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 25px;
    }
    .status-acak { background-color: rgba(245, 158, 11, 0.1); color: #f59e0b; }
    .status-urut { background-color: rgba(16, 185, 129, 0.1); color: #10b981; }
    .status-dinamis { background-color: rgba(239, 68, 68, 0.1); color: #ef4444; }

    /* TOMBOL GRADASI PREMIUM */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important; /* Biru Royal modern */
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    div.stButton > button[kind="secondary"] {
        background-color: #1f2937 !important;
        color: #e5e7eb !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
    
    /* Tampilan Metric Box Minimalis */
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)


# ========== DATA LOGIC GENERATOR ==========

@st.cache_data
def generate_products(n=500):
    categories = ["Makanan", "Minuman", "Elektronik", "Pakaian", "Kecantikan"]
    products = []
    random.seed(100) 
    for i in range(n):
        kategori_terpilih = random.choice(categories)
        products.append({
            'id': i + 1,
            'nama': f"{kategori_terpilih} {i+1}",
            'kategori': kategori_terpilih,
            'harga': random.randint(10000, 1000000),
            'rak': i
        })
    return products

# Sidebar Panel
with st.sidebar:
    st.markdown("## 📊 Control Panel")
    st.write("Atur ekosistem simulasi gudang.")
    
    jumlah_produk = st.slider(
        "Kapasitas Produk:",
        min_value=100,
        max_value=1000,
        value=500,
        step=100
    )
    
    st.divider()
    st.markdown("### 🔍 Metode Aktif")
    algoritma_terpilih = st.radio(
        "Pilih algoritma utama:",
        [
            "🔍 Linear Search (O(n)) - Sekuensial",
            "📚 Binary Search (O(log n)) - Logaritmik",
            "⚡ Interpolation Search (O(log (log n))) - Prediktif"
        ]
    )
    
    st.divider()
    st.markdown("### 📦 State Logistik")
    kondisi_data = st.radio(
        "Keterurutan data rak:",
        [
            "🔄 Data Acak (Unsorted)",
            "📊 Data Terurut berdasarkan ID (Sorted)",
            "🎲 Data Dinamis (sering berubah)"
        ]
    )


# ========== ALGORITMA CORE FUNCTIONS ==========

def linear_search(data, target_query):
    langkah = 0
    hasil_indeks = [] 
    for i, produk in enumerate(data):
        langkah += 1
        if isinstance(target_query, int):
            if produk['id'] == target_query:
                return [i], langkah
        else:
            q = target_query.lower()
            if q in produk['nama'].lower() or q in produk['kategori'].lower():
                hasil_indeks.append(i)
    return hasil_indeks, langkah

def binary_search(data, target_id):
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


# ========== LIFECYCLE DATA ENVIRONMENT ==========

products = generate_products(jumlah_produk)
status_html = ""

if kondisi_data == "🔄 Data Acak (Unsorted)":
    data_list = products.copy()
    random.seed(42)  
    random.shuffle(data_list)
    status_html = '<div class="status-chip status-acak">● Data Acak (Unsorted)</div>'
elif kondisi_data == "📊 Data Terurut berdasarkan ID (Sorted)":
    data_list = sorted(products, key=lambda x: x['id'])
    status_html = '<div class="status-chip status-urut">● Data Terstruktur (Sorted)</div>'
else:
    data_list = products.copy()
    random.seed(24)
    random.shuffle(data_list)
    status_html = '<div class="status-chip status-dinamis">● Data Dinamis</div>'


# ========== APP DISPLAY AREA ==========

st.markdown('<h1 style="color: #ffffff; font-weight: 700; margin-bottom: 0px; letter-spacing: -0.5px;">Gudang Digital Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #6b7280; font-size: 15px; margin-bottom: 15px;">Visualisasi pencarian & analisis perbandingan kompleksitas algoritma.</p>', unsafe_allow_html=True)

# Menampilkan status chip minimalis
st.markdown(status_html, unsafe_allow_html=True)


# ====================================================================
# KONSEP UTAMA: TABS MENU (NAVIGASI MINIMALIS MODERN)
# ====================================================================
tab_pencarian, tab_laboratorium, tab_database = st.tabs([
    "🔍 Konsol Pencarian Utama", 
    "🔬 Lab Benchmarking Simulator", 
    "📋 Data Master Gudang"
])

# ========== HELPER DAFTAR PRODUK RENDER ==========
def tampilkan_daftar_produk(daftar_item_tampil, limit=5):
    total_item = len(daftar_item_tampil)
    if total_item == 0: return
        
    batch_awal = daftar_item_tampil[:limit]
    for nomor, idx, p in batch_awal:
        st.info(f"🔢 **[{nomor}/{total_item}]** Rak {idx} ➔ **{p['nama']}** | `{p['kategori']}` | Rp {p['harga']:,.0f} (ID: {p['id']})")
        
    if total_item > limit:
        with st.expander(f"✨ Lihat {total_item - limit} Produk Lainnya..."):
            for nomor, idx, p in daftar_item_tampil[limit:]:
                st.info(f"🔢 **[{nomor}/{total_item}]** Rak {idx} ➔ **{p['nama']}** | `{p['kategori']}` | Rp {p['harga']:,.0f} (ID: {p['id']})")


# --------------------------------------------------------------------
# TAB 1: KONSOL PENCARIAN
# --------------------------------------------------------------------
with tab_pencarian:
    st.write("")
    st.markdown('<h3 style="color: #ffffff; font-size: 18px; font-weight:600;">Cari Posisi Produk</h3>', unsafe_allow_html=True)
    
    if 'input_query' not in st.session_state:
        st.session_state.input_query = "-- Pilih atau Ketik (ID / Nama / Kategori) --"

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        kategori_unik = sorted(list(set([p['kategori'] for p in data_list])))
        daftar_id = [str(p['id']) for p in products]
        daftar_nama = [p['nama'] for p in products]
        opsi_autocomplete = ["-- Pilih atau Ketik (ID / Nama / Kategori) --"] + kategori_unik + daftar_nama + daftar_id
        
        index_default = opsi_autocomplete.index(st.session_state.input_query) if st.session_state.input_query in opsi_autocomplete else 0

        target_query = st.selectbox(
            "Pilih Token:",
            options=opsi_autocomplete,
            index=index_default,
            label_visibility="collapsed"
        )
        st.session_state.input_query = target_query

    with col2:
        cari_button = st.button("🚀 Eksekusi", type="primary", use_container_width=True)

    with col3:
        random_button = st.button("🎲 Acak Kata Kunci", use_container_width=True)
        if random_button:
            p_acak = random.choice(data_list)
            st.session_state.input_query = random.choice([str(p_acak['id']), p_acak['nama'], p_acak['kategori']])
            st.rerun()

    # Eksekusi Tampilan Hasil Pencarian Tepat di Bawahnya secara borderless
    if cari_button:
        if target_query == "-- Pilih atau Ketik (ID / Nama / Kategori) --":
            st.error("❌ Mohon pilih kata kunci pencarian atau token produk terlebih dahulu!")
        else:
            is_id = target_query.isdigit()
            query_final = int(target_query) if is_id else target_query
            
            st.write("")
            st.markdown(f'<p style="color: #9ca3af; font-size: 14px; font-weight:500;">Hasil Analisis: {algoritma_terpilih.split("(")[0]}</p>', unsafe_allow_html=True)
            
            if ("Binary Search" in algoritma_terpilih or "Interpolation Search" in algoritma_terpilih) and kondisi_data != "📊 Data Terurut berdasarkan ID (Sorted)":
                st.warning("⚠️ Algoritma membutuhkan data terurut. Sistem mengaktifkan auto-sorting internal.")

            # Jalankan Algoritma
            if "Linear Search" in algoritma_terpilih:
                start_time = time.time()
                indeks_list, langkah = linear_search(data_list, query_final)
                waktu = (time.time() - start_time) * 1000
                
                c_a, c_b, c_c = st.columns(3)
                c_a.metric("Record Ditemukan", f"{len(indeks_list)} Item")
                c_b.metric("Langkah Iterasi", f"{langkah} Kali")
                c_c.metric("Waktu Proses", f"{waktu:.3f} ms")
                
                indeks_sorted = sorted(indeks_list, key=lambda x: data_list[x]['id'])
                list_tampil = [(i + 1, idx, data_list[idx]) for i, idx in enumerate(indeks_sorted)]
                if list_tampil: tampilkan_daftar_produk(list_tampil)
                else: st.error("❌ Produk tidak terdaftar.")
                    
            elif "Binary Search" in algoritma_terpilih:
                data_sorted = sorted(data_list, key=lambda x: x['id'])
                id_targets = [p['id'] for p in data_list if target_query.lower() in p['nama'].lower() or target_query.lower() in p['kategori'].lower()] if not is_id else [query_final]
                
                start_time = time.time()
                langkah_total, hasil_ditemukan = 0, []
                for tid in id_targets:
                    indeks, langkah = binary_search(data_sorted, tid)
                    langkah_total += langkah
                    if indeks != -1: hasil_ditemukan.append((indeks, data_sorted[indeks]))
                waktu = (time.time() - start_time) * 1000
                
                c_a, c_b, c_c = st.columns(3)
                c_a.metric("Record Ditemukan", f"{len(hasil_ditemukan)} Item")
                c_b.metric("Langkah Bagi-Dua", f"{langkah_total} Kali")
                c_c.metric("Waktu Proses", f"{waktu:.3f} ms")
                
                hasil_sorted = sorted(hasil_ditemukan, key=lambda x: x[1]['id'])
                list_tampil = [(i + 1, idx, p) for i, (idx, p) in enumerate(hasil_sorted)]
                if list_tampil: tampilkan_daftar_produk(list_tampil)
                else: st.error("❌ Produk tidak terdaftar.")

            else:
                data_sorted = sorted(data_list, key=lambda x: x['id'])
                id_targets = [p['id'] for p in data_list if target_query.lower() in p['nama'].lower() or target_query.lower() in p['kategori'].lower()] if not is_id else [query_final]
                
                start_time = time.time()
                langkah_total, hasil_ditemukan = 0, []
                for tid in id_targets:
                    indeks, langkah = interpolation_search(data_sorted, tid)
                    langkah_total += langkah
                    if indeks != -1: hasil_ditemukan.append((indeks, data_sorted[indeks]))
                waktu = (time.time() - start_time) * 1000
                
                c_a, c_b, c_c = st.columns(3)
                c_a.metric("Record Ditemukan", f"{len(hasil_ditemukan)} Item")
                c_b.metric("Langkah Estimasi", f"{langkah_total} Kali")
                c_c.metric("Waktu Proses", f"{waktu:.3f} ms")
                
                hasil_sorted = sorted(hasil_ditemukan, key=lambda x: x[1]['id'])
                list_tampil = [(i + 1, idx, p) for i, (idx, p) in enumerate(hasil_sorted)]
                if list_tampil: tampilkan_daftar_produk(list_tampil)
                else: st.error("❌ Produk tidak terdaftar.")


# --------------------------------------------------------------------
# TAB 2: LAB BENCHMARKING SIMULATOR
# --------------------------------------------------------------------
with tab_laboratorium:
    st.write("")
    st.markdown('<h3 style="color: #ffffff; font-size: 18px; font-weight:600;">Stress-Test Perbandingan Algoritma</h3>', unsafe_allow_html=True)
    st.write("Jalankan pengujian serentak berdasarkan kata kunci yang aktif di Tab Pencarian.")

    tombol_komparasi = st.button("📊 Mulai Pengujian Komparatif", use_container_width=True)

    if tombol_komparasi:
        if target_query == "-- Pilih atau Ketik (ID / Nama / Kategori) --":
            st.error("❌ Hubungkan kata kunci pencarian terlebih dahulu pada Tab Pencarian Utama!")
        else:
            is_id = target_query.isdigit()
            query_final = int(target_query) if is_id else target_query
            
            data_sorted = sorted(data_list, key=lambda x: x['id'])
            id_targets = [p['id'] for p in data_list if target_query.lower() in p['nama'].lower() or target_query.lower() in p['kategori'].lower()] if not is_id else [query_final]
            
            # Benchmarking
            start = time.time()
            idx_linear, steps_linear = linear_search(data_list, query_final)
            time_linear = (time.time() - start) * 1000
            
            start = time.time()
            steps_binary_total = 0
            for tid in id_targets:
                _, langkah = binary_search(data_sorted, tid)
                steps_binary_total += langkah
            time_binary = (time.time() - start) * 1000
            
            start = time.time()
            steps_inter_total = 0
            for tid in id_targets:
                _, langkah = interpolation_search(data_sorted, tid)
                steps_inter_total += langkah
            time_inter = (time.time() - start) * 1000
            
            jumlah_ditemukan = len(idx_linear) if not is_id else (1 if idx_linear and idx_linear[0] != -1 else 0)
            
            df_komparasi = pd.DataFrame({
                "Algoritma Eksperimen": ["Linear Search", "Binary Search", "Interpolation Search"],
                "Notasi Big-O": ["O(n) - Linear", "O(log n) - Logaritmik", "O(log (log n)) - Sub-Logaritmik"],
                "Langkah Komparasi": [steps_linear, steps_binary_total if jumlah_ditemukan > 0 else 0, steps_inter_total if jumlah_ditemukan > 0 else 0],
                "Waktu Eksekusi (ms)": [f"{time_linear:.4f} ms", f"{time_binary:.4f} ms", f"{time_inter:.4f} ms"]
            })
            
            st.dataframe(df_komparasi, use_container_width=True, hide_index=True)
            
            if jumlah_ditemukan > 0:
                langkah_list = [steps_linear, steps_binary_total, steps_inter_total]
                pemenang_idx = langkah_list.index(min(langkah_list))
                nama_pemenang = ["Linear Search", "Binary Search", "Interpolation Search"][pemenang_idx]
                st.success(f"⚡ **Kesimpulan:** Performa tercepat dengan jumlah langkah komparasi paling sedikit dimenangkan oleh **{nama_pemenang}**.")
            else:
                st.error("❌ Produk tidak ditemukan, kalkulasi tidak valid.")


# --------------------------------------------------------------------
# TAB 3: DATA MASTER GUDANG
# --------------------------------------------------------------------
with tab_database:
    st.write("")
    st.markdown('<h3 style="color: #ffffff; font-size: 18px; font-weight:600;">Database Logistik Global</h3>', unsafe_allow_html=True)
    
    df = pd.DataFrame(data_list)
    df_display = df[['id', 'nama', 'kategori', 'harga', 'rak']].copy()
    df_display['harga'] = df_display['harga'].apply(lambda x: f"Rp {x:,.0f}")
    df_display = df_display.rename(columns={
        'id': 'ID Produk', 'nama': 'Nama Produk', 'kategori': 'Kategori', 'harga': 'Harga', 'rak': 'Posisi Rak'
    })
    st.dataframe(df_display, use_container_width=True, height=400)