def cari_log_suhu(data_suhu, suhu_target):
    # Data harus diurutkan terlebih dahulu agar algoritma ini bekerja
    data_suhu.sort() 
    low, high = 0, len(data_suhu) - 1
    
    while low <= high and suhu_target >= data_suhu[low] and suhu_target <= data_suhu[high]:
        # Jika low == high, kita sudah menemukan atau menyempitkan ke satu elemen
        if low == high:
            if data_suhu[low] == suhu_target: 
                return low
            return -1
        
        # Rumus Interpolasi (seperti mencari kata di kamus berdasarkan huruf depan)
        # Menghitung posisi estimasi berdasarkan nilai target
        posisi = low + int(((float(high - low) / (data_suhu[high] - data_suhu[low])) * (suhu_target - data_suhu[low])))
        
        if data_suhu[posisi] == suhu_target:
            return posisi
        
        if data_suhu[posisi] < suhu_target:
            low = posisi + 1
        else:
            high = posisi - 1
    
    return -1

# Gunakan data yang masuk akal untuk sensor (biasanya naik atau sudah disortir)
log_sensor = [20, 20, 30, 40, 60, 88, 100]
target = 30

index = cari_log_suhu(log_sensor, target)

if index != -1:
    print(f"Suhu {target} ditemukan pada indeks ke-{index} (setelah diurutkan)")
else:
    print(f"Suhu {target} tidak ditemukan.")
