import json

def muat_data_json():
    """Fungsi untuk membaca data dari file JSON"""
    try:
        with open("data_produk.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ File data_produk.json tidak ditemukan!")
        print("💡 Silakan jalankan file 'buat_data.py' terlebih dahulu untuk membuat data.")
        return None

# =====================================================================
# ALGORITMA PENCARIAN (Mengembalikan tuple: (index, jumlah_langkah))
# =====================================================================

def linier_search(data, target_id):
    langkah = 0
    for i, produk in enumerate(data):
        langkah += 1  # Setiap memeriksa satu data, langkah bertambah
        if produk['product_id'].upper() == target_id.upper():
            return i, langkah
    return -1, langkah

def binary_search(data, target_id):
    left, right = 0, len(data) - 1
    target_id = target_id.upper()
    langkah = 0
    
    while left <= right:
        langkah += 1  # Setiap tebakan/pembagian data, langkah bertambah
        mid = (left + right) // 2
        current_id = data[mid]['product_id'].upper()
        
        if current_id == target_id:
            return mid, langkah
        elif current_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return -1, langkah

def interpolation_search(data, target_id):
    low, high = 0, len(data) - 1
    target_id = target_id.upper()
    langkah = 0
    
    def ambil_angka_id(id_str):
        try:
            return int(id_str.split("-")[1])
        except:
            return -1

    target_num = ambil_angka_id(target_id)
    if target_num == -1: return -1, langkah

    while low <= high and ambil_angka_id(data[low]['product_id']) <= target_num <= ambil_angka_id(data[high]['product_id']):
        langkah += 1  # Setiap kalkulasi posisi, langkah bertambah
        if low == high:
            if data[low]['product_id'].upper() == target_id:
                return low, langkah
            break
        
        low_num = ambil_angka_id(data[low]['data_produk'] if 'data_produk' in data[low] else data[low]['product_id'])
        # Mengantisipasi jika struktur key berbeda, disesuaikan ke product_id
        low_num = ambil_angka_id(data[low]['product_id'])
        high_num = ambil_angka_id(data[high]['product_id'])
        
        if high_num == low_num:
            break
            
        pos = low + int(((target_num - low_num) * (high - low)) / (high_num - low_num))
        
        # Proteksi index out of bounds
        if pos < low or pos > high:
            break

        if data[pos]['product_id'].upper() == target_id:
            return pos, langkah
        elif data[pos]['product_id'].upper() < target_id:
            low = pos + 1
        else:
            high = pos - 1
            
    return -1, langkah

# =====================================================================
# ALUR UTAMA PROGRAM CLI
# =====================================================================

def main():
    data_produk = muat_data_json()
    if data_produk is None:
        return 

    print("\n=== APLIKASI PENCARIAN PRODUK ===")
    print("Mau search pakai algoritma apa?")
    print("1. Linear Search")
    print("2. Binary Search")
    print("3. Interpolation Search")
    
    pilihan = input("Mau pakek algoritma nomer berapa: ").strip()
    if pilihan not in ["1", "2", "3"]:
        print("❌ Pilihan tidak valid!")
        return

    # Menerima input berupa angka saja
    masukan_angka = input("\nMasukan Angka ID Produk (Contoh: 5 atau 10): ").strip()
    
    # Validasi memastikan input adalah angka
    if not masukan_angka.isdigit():
        print("❌ Input harus berupa angka!")
        return
        
    # Mengubah angka (misal: "5") menjadi format "PRD-0005"
    masukan_id = f"PRD-{masukan_angka.zfill(4)}"
    print(f"🔍 Mencari ID Produk: {masukan_id}...")

    index_ketemu = -1
    jumlah_langkah = 0
    nama_algo = ""
    
    if pilihan == "1":
        index_ketemu, jumlah_langkah = linier_search(data_produk, masukan_id)
        nama_algo = "Linear Search"
    elif pilihan == "2":
        index_ketemu, jumlah_langkah = binary_search(data_produk, masukan_id)
        nama_algo = "Binary Search"
    elif pilihan == "3":
        index_ketemu, jumlah_langkah = interpolation_search(data_produk, masukan_id)
        nama_algo = "Interpolation Search"

    # Tampilkan hasil akhir
    if index_ketemu != -1:
        barang = data_produk[index_ketemu]
        print(f"\n✅ Data ditemukan pada indeks ke-{index_ketemu}!")
        print(f"⚡ Dibutuhkan {jumlah_langkah} langkah menggunakan {nama_algo}.")
        print("-" * 40)
        print(f"Nama Produk : {barang['nama_produk']}")
        print(f"Kategori    : {barang['kategori']}")
        print(f"Harga       : Rp{barang['harga']:,}")
        print(f"Rating      : {barang['rating']} ⭐")
    else:
        print(f"\n❌ Data ID '{masukan_id}' tidak ditemukan setelah {jumlah_langkah} langkah dengan {nama_algo}.")

if __name__ == "__main__":
    main()