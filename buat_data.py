import json
import random

def data_barang(num=200):
    dataset = []
    kategori_list = ["Elektronik", "Fashion", "Makanan", "Olahraga", "Buku", "Kecantikan", "Otomotif", "Perabotan"]
    
    for i in range(num):
        dataset.append({
            "nomer": i + 1,
            "product_id": f"PRD-{i:04d}",
            "nama_produk": f"Produk-{i}",
            "kategori": random.choice(kategori_list),  # Tambahkan kategori
            "harga": random.randint(5, 500) * 1000,
            "rating": round(random.uniform(1.0, 5.0), 1)
        })
    return dataset

# Generate data
data_awal = data_barang(200)
with open("data_produk.json", "w") as f:
    json.dump(data_awal, f, indent=4)

print("✅ Data produk telah dibuat di file data_produk.json dengan kategori!")