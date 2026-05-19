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
# ALGORITMA PENCARIAN (Mengembalikan index data jika ketemu, -1 jika tidak)
# =====================================================================

def linier_search(data, target_id):
    for i, produk in enumerate(data):
        # Menggunakan .upper() agar pencarian tidak sensitif huruf kapital/kecil
        if produk['product_id'].upper() == target_id.upper():
            return i
    return -1

def binary_search(data, target_id):
    left, right = 0, len(data) - 1
    target_id = target_id.upper()
    
    while left <= right:
        mid = (left + right) // 2
        current_id = data[mid]['product_id'].upper()
        
        if current_id == target_id:
            return mid
        elif current_id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def interpolation_search(data, target_id):
    low, high = 0, len(data) - 1
    target_id = target_id.upper()
    
    # Fungsi pembantu untuk mengambil angka saja dari "PRD-0005" -> 5
    def ambil_angka_id(id_str):
        try:
            return int(id_str.split("-")[1])
        except:
            return -1

    target_num = ambil_angka_id(target_id)
    if target_num == -1: return -1

    while low <= high and ambil_angka_id(data[low]['product_id']) <= target_num <= ambil_angka_id(data[high]['product_id']):
        if low == high:
            if data[low]['product_id'].upper() == target_id:
                return low
            break
        
        low_num = ambil_angka_id(data[low]['product_id'])
        high_num = ambil_angka_id(data[high]['product_id'])
        
        if high_num == low_num: # Menghindari pembagian dengan nol
            break
            
        # Rumus posisi Interpolation Search
        pos = low + int(((target_num - low_num) * (high - low)) / (high_num - low_num))
        
        if data[pos]['product_id'].upper() == target_id:
            return pos
        elif data[pos]['product_id'].upper() < target_id:
            low = pos + 1
        else:
            high = pos - 1
            
    return -1

# =====================================================================
# ALUR UTAMA PROGRAM CLI
# =====================================================================

def main():
    # 1. Ambil data dari JSON
    data_produk = muat_data_json()
    if data_produk is None:
        return 

    # 2. Menu Pilihan Algoritma
    print("\n=== APLIKASI PENCARIAN PRODUK ===")
    print("Mau search pakai algoritma apa?")
    print("1. Linear Search")
    print("2. Binary Search")
    print("3. Interpolation Search")
    
    pilihan = input("Mau pakek algoritma nomer berapa: ").strip()
    if pilihan not in ["1", "2", "3"]:
        print("❌ Pilihan tidak valid!")
        return

    # 3. Minta input ID dari user
    masukan_id = input("\nMasukan ID Produk (Contoh: PRD-0005): ").strip()

    # 4. Jalankan algoritma berdasarkan pilihan
    index_ketemu = -1
    nama_algo = ""
    
    if pilihan == "1":
        index_ketemu = linier_search(data_produk, masukan_id)
        nama_algo = "Linear Search"
    elif pilihan == "2":
        index_ketemu = binary_search(data_produk, masukan_id)
        nama_algo = "Binary Search"
    elif pilihan == "3":
        index_ketemu = interpolation_search(data_produk, masukan_id)
        nama_algo = "Interpolation Search"

    # 5. Tampilkan hasil berdasarkan indeks yang didapatkan
    if index_ketemu != -1:
        barang = data_produk[index_ketemu]
        print(f"\n✅ Data ID ditemukan! (Menggunakan {nama_algo})")
        print(f"Nama Produk : {barang['nama_produk']}")
        print(f"Kategori    : {barang['kategori']}")
        print(f"Harga       : Rp{barang['harga']:,}")
        print(f"Rating      : {barang['rating']} ⭐")
    else:
        print(f"\n❌ Data ID '{masukan_id}' tidak ditemukan dengan {nama_algo}.")

if __name__ == "__main__":
    main()