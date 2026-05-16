# ==============================================================================
# 1. BAGIAN IMPORT LIBRARY (Alat-alat yang akan digunakan)
# ==============================================================================
import streamlit as st  # Untuk membuat tampilan aplikasi web interaktif
import pandas as pd     # Untuk mengolah data dan menampilkan tabel (DataFrame)
import random           # Untuk membuat angka acak atau mengacak data
import time             # Untuk menghitung waktu eksekusi atau menampilkan jam

# ==============================================================================
# 2. KONFIGURASI HALAMAN WEB (Opsional, tapi bagus untuk estetika)
# ==============================================================================
st.set_page_config(
    page_title="Aplikasi Kosong Streamlit", # Judul yang muncul di tab browser
    page_icon="🚀",                         # Emoji yang muncul di tab browser
    layout="wide"                           # Tampilan web melebar (bukan kotak di tengah)
)

# ==============================================================================
# 3. BAGIAN LOGIKA & ALGORITMA (Back-End)
# Tempat Anda menulis fungsi-fungsi Python, perhitungan matematika, atau algoritma
# ==============================================================================
def fungsi_contoh_algoritma():
    # Tulis logika atau algoritma Anda di sini
    pass


# ==========================================
# KODE UNTUK MENGGANTI WARNA BACKGROUND
# ==========================================

# ==============================================================================
# 4. BAGIAN TAMPILAN APLIKASI WEB (Front-End / User Interface)
# Tempat Anda mendesain apa saja yang akan dilihat oleh pengguna di browser
# ==============================================================================


# Membuat Sidebar (Menu Samping)
with st.sidebar:
    st.header("⚙️ Menu Samping")
    st.write("Komponen tombol atau input di sini akan muncul di sebelah kiri.")

# Membuat Kolom di Halaman Utama
kolom1, kolom2 = st.columns(2)

with kolom1:
    st.subheader("Bagian Kiri")
    st.write("Tempat untuk memasukkan input, teks, atau tombol.")

with kolom2:
    st.subheader("Bagian Kanan")
    st.write("Tempat untuk menampilkan hasil, grafik, atau tabel Pandas.")
    
# Menampilkan Judul Utama
st.title("🚀 Template Aplikasi Kosong")
st.write("Ini adalah halaman kosong yang siap Anda isi dengan kode program Anda.")

import streamlit as st

# ==========================================
# KODE UNTUK MENGGANTI WARNA BACKGROUND
# ==========================================
st.markdown(
    """
    <style>
    /* 1. Mengubah background halaman utama */
    .stApp { 
        background-color: #0022FF; /* Warna biru utama Anda */
    }
    
    /* 2. Mengubah background sidebar (Menu Samping) */
    [data-testid="stSidebar"] { 
        background-color: #0022FF; /* Disamakan menjadi biru */
    }
    
    /* 3. PERBAIKAN: Mengubah background bagian header atas agar ikut berwarna biru */
    header[data-testid="stHeader"] {
        background-color: #0022FF !important; /* Memaksa warna header jadi biru */
    }
    
    /* 4. Mengubah warna semua teks agar kontras (Putih) */
    .stApp, [data-testid="stSidebar"], header[data-testid="stHeader"] {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# ISI APLIKASI ANDA DI BAWAH INI
# ==========================================
st.title("Aplikasi dengan Background Baru 🎨")
st.write("Warna latar belakang aplikasi ini sudah berhasil diubah menggunakan kode CSS.")

