import json
import random

def generate_products(n=500):
    """Generate produk dengan ID dan posisi rak (indeks array)"""
    products = []
    for i in range(n):
        products.append({
            'id': i + 1,
            'nama': f"Produk {i+1}",
            'harga': random.randint(10000, 1000000),
            'posisi_rak': i
        })
    return products

# Generate data
products = generate_products(500)
with open("data_produk_rak.json", "w") as f:
    json.dump(products, f, indent=4)

print("✅ Data produk rak telah dibuat di file data_produk_rak.json")