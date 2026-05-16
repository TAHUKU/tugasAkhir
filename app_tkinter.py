import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
import time
from datetime import datetime

class AplikasiPencarianRak:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Pencarian Posisi Barang di Rak Digital")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variabel
        self.jumlah_produk = tk.IntVar(value=500)
        self.algoritma_var = tk.StringVar(value="Linear Search (O(n))")
        self.kondisi_var = tk.StringVar(value="Data Acak (Unsorted)")
        self.target_id = tk.StringVar()
        self.data_list = []
        self.data_sorted = []
        
        # Warna
        self.colors = {
            'bg': '#f0f0f0',
            'header': '#2c3e50',
            'button': '#3498db',
            'success': '#27ae60',
            'warning': '#e67e22',
            'error': '#e74c3c'
        }
        
        self.setup_ui()
        self.generate_data()
        
    def setup_ui(self):
        # Frame Utama
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['header'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📦 Pencarian Posisi Barang di Rak Digital", 
                               font=('Arial', 20, 'bold'), bg=self.colors['header'], fg='white')
        title_label.pack(pady=20)
        
        # Sidebar (kiri)
        sidebar_frame = tk.Frame(main_frame, bg=self.colors['bg'], width=280)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Konten Utama (kanan)
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ========== SIDEBAR ==========
        # Pengaturan
        settings_frame = tk.LabelFrame(sidebar_frame, text="⚙️ Pengaturan", 
                                       font=('Arial', 12, 'bold'), bg=self.colors['bg'])
        settings_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        # Jumlah produk
        tk.Label(settings_frame, text="Jumlah produk di gudang:", 
                bg=self.colors['bg']).pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        jumlah_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        jumlah_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.jumlah_slider = tk.Scale(jumlah_frame, from_=100, to=1000, 
                                      orient=tk.HORIZONTAL, variable=self.jumlah_produk,
                                      bg=self.colors['bg'], highlightthickness=0,
                                      command=self.on_jumlah_change)
        self.jumlah_slider.pack(fill=tk.X)
        
        self.jumlah_label = tk.Label(jumlah_frame, text="500", bg=self.colors['bg'])
        self.jumlah_label.pack()
        
        tk.Frame(settings_frame, height=10, bg=self.colors['bg']).pack()
        
        # Algoritma
        algo_frame = tk.LabelFrame(sidebar_frame, text="🎯 Pilih Algoritma Pencarian",
                                   font=('Arial', 12, 'bold'), bg=self.colors['bg'])
        algo_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        algoritma_list = [
            "Linear Search (O(n))",
            "Binary Search (O(log n)) - Data harus terurut",
            "Interpolation Search (O(log n)) - Data harus terurut"
        ]
        
        for algo in algoritma_list:
            tk.Radiobutton(algo_frame, text=algo, variable=self.algoritma_var,
                          value=algo, bg=self.colors['bg'], anchor=tk.W).pack(fill=tk.X, padx=10, pady=2)
        
        # Kondisi data
        kondisi_frame = tk.LabelFrame(sidebar_frame, text="📦 Kondisi Data",
                                      font=('Arial', 12, 'bold'), bg=self.colors['bg'])
        kondisi_frame.pack(fill=tk.X, pady=(0, 10), padx=5)
        
        kondisi_list = [
            "Data Acak (Unsorted)",
            "Data Terurut berdasarkan ID"
        ]
        
        for kondisi in kondisi_list:
            tk.Radiobutton(kondisi_frame, text=kondisi, variable=self.kondisi_var,
                          value=kondisi, bg=self.colors['bg'], anchor=tk.W,
                          command=self.on_kondisi_change).pack(fill=tk.X, padx=10, pady=2)
        
        # Tombol generate ulang
        tk.Button(sidebar_frame, text="🔄 Generate Ulang Data", 
                 command=self.generate_data, bg=self.colors['button'], fg='white',
                 font=('Arial', 10, 'bold'), cursor='hand2').pack(fill=tk.X, padx=5, pady=10)
        
        # ========== KONTEN UTAMA ==========
        # Form pencarian
        search_frame = tk.LabelFrame(content_frame, text="🔍 Cari Produk Berdasarkan ID",
                                     font=('Arial', 14, 'bold'), bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        input_frame = tk.Frame(search_frame, bg='white')
        input_frame.pack(padx=10, pady=10)
        
        tk.Label(input_frame, text="Masukkan ID Produk (angka):", 
                font=('Arial', 11), bg='white').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.id_entry = tk.Entry(input_frame, textvariable=self.target_id, width=20,
                                 font=('Arial', 11))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.cari_button = tk.Button(input_frame, text="🔍 Cari Posisi Rak", 
                                     command=self.cari_produk, bg=self.colors['button'],
                                     fg='white', font=('Arial', 10, 'bold'), cursor='hand2')
        self.cari_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.random_button = tk.Button(input_frame, text="🎲 Random ID", 
                                       command=self.random_id, bg='#95a5a6',
                                       fg='white', font=('Arial', 10, 'bold'), cursor='hand2')
        self.random_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Hasil pencarian
        self.result_frame = tk.LabelFrame(content_frame, text="📊 Hasil Pencarian Posisi Rak",
                                          font=('Arial', 14, 'bold'), bg='white')
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD,
                                                      font=('Courier', 10), bg='white')
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Progress bar untuk posisi rak
        self.progress_frame = tk.Frame(self.result_frame, bg='white')
        self.progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.progress_label = tk.Label(self.progress_frame, text="Posisi Rak:", bg='white')
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Tab untuk tabel data dan perbandingan
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Seluruh Data
        data_tab = tk.Frame(notebook, bg='white')
        notebook.add(data_tab, text="📋 Seluruh Data & Posisi Rak")
        
        self.tree_frame = tk.Frame(data_tab)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_treeview()
        
        # Tab 2: Perbandingan Algoritma
        compare_tab = tk.Frame(notebook, bg='white')
        notebook.add(compare_tab, text="🔬 Bandingkan Algoritma")
        
        compare_frame = tk.Frame(compare_tab, bg='white')
        compare_frame.pack(padx=20, pady=20)
        
        tk.Label(compare_frame, text="ID untuk perbandingan:", 
                font=('Arial', 11), bg='white').pack(anchor=tk.W)
        
        compare_id_frame = tk.Frame(compare_frame, bg='white')
        compare_id_frame.pack(fill=tk.X, pady=5)
        
        self.compare_id_entry = tk.Entry(compare_id_frame, width=20, font=('Arial', 11))
        self.compare_id_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(compare_id_frame, text="Bandingkan Semua Algoritma",
                 command=self.bandingkan_algoritma, bg=self.colors['button'],
                 fg='white', cursor='hand2').pack(side=tk.LEFT)
        
        self.compare_result_text = scrolledtext.ScrolledText(compare_frame, wrap=tk.WORD,
                                                              height=15, font=('Courier', 10),
                                                              bg='white')
        self.compare_result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Footer
        footer_frame = tk.Frame(content_frame, bg='#ecf0f1', height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.footer_label = tk.Label(footer_frame, text="", bg='#ecf0f1', font=('Arial', 9))
        self.footer_label.pack(pady=5)
        self.update_footer()
        
    def setup_treeview(self):
        # Treeview untuk menampilkan data
        columns = ('ID Produk', 'Nama Produk', 'Harga', '📍 Posisi Rak (Indeks)')
        
        # Scrollbar
        scroll_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings',
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Atur kolom
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_treeview(self):
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Tambah data baru
        for produk in self.data_list[:100]:  # Tampilkan 100 pertama
            self.tree.insert('', tk.END, values=(
                produk['id'],
                produk['nama'],
                f"Rp {produk['harga']:,.0f}",
                produk['posisi_rak']
            ))
    
    def update_footer(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.footer_label.config(text=f"🔄 Data terakhir diperbarui: {now} | 🎯 Tugas: Menemukan POSISI RAK (INDEKS ARRAY) berdasarkan ID Produk")
        self.root.after(1000, self.update_footer)
    
    def on_jumlah_change(self, val):
        self.jumlah_label.config(text=str(int(float(val))))
        self.generate_data()
    
    def on_kondisi_change(self):
        self.generate_data()
    
    def generate_data(self):
        """Generate data produk"""
        n = self.jumlah_produk.get()
        products = []
        for i in range(n):
            products.append({
                'id': i + 1,
                'nama': f"Produk {i+1}",
                'harga': random.randint(10000, 1000000),
                'posisi_rak': i
            })
        
        # Atur kondisi data
        if self.kondisi_var.get() == "Data Acak (Unsorted)":
            self.data_list = products.copy()
            random.shuffle(self.data_list)
            self.result_text.insert(tk.END, "📦 Kondisi: Data dalam keadaan ACAK\n")
        else:
            self.data_list = sorted(products, key=lambda x: x['id'])
            self.result_text.insert(tk.END, "📚 Kondisi: Data dalam keadaan TERURUT berdasarkan ID\n")
        
        self.data_sorted = sorted(self.data_list, key=lambda x: x['id'])
        self.update_treeview()
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"✅ Data berhasil digenerate! Total {n} produk.\n")
        
    def random_id(self):
        random_id = random.randint(1, self.jumlah_produk.get())
        self.target_id.set(str(random_id))
        self.id_entry.focus()
    
    # ========== ALGORITMA PENCARIAN ==========
    
    def linear_search(self, data, target_id):
        """Linear Search"""
        langkah = 0
        for i, produk in enumerate(data):
            langkah += 1
            if produk['id'] == target_id:
                return i, langkah, produk
        return -1, langkah, None
    
    def binary_search(self, data, target_id):
        """Binary Search"""
        langkah = 0
        left, right = 0, len(data) - 1
        
        while left <= right:
            langkah += 1
            mid = (left + right) // 2
            
            if data[mid]['id'] == target_id:
                return mid, langkah, data[mid]
            elif data[mid]['id'] < target_id:
                left = mid + 1
            else:
                right = mid - 1
        return -1, langkah, None
    
    def interpolation_search(self, data, target_id):
        """Interpolation Search"""
        langkah = 0
        low, high = 0, len(data) - 1
        
        while low <= high and target_id >= data[low]['id'] and target_id <= data[high]['id']:
            langkah += 1
            
            if low == high:
                if data[low]['id'] == target_id:
                    return low, langkah, data[low]
                return -1, langkah, None
            
            posisi = low + int(((high - low) / (data[high]['id'] - data[low]['id'])) * 
                              (target_id - data[low]['id']))
            
            if data[posisi]['id'] == target_id:
                return posisi, langkah, data[posisi]
            
            if data[posisi]['id'] < target_id:
                low = posisi + 1
            else:
                high = posisi - 1
                
        return -1, langkah, None
    
    def cari_produk(self):
        """Fungsi pencarian utama"""
        target = self.target_id.get()
        
        if not target:
            messagebox.showwarning("Peringatan", "Silakan masukkan ID produk terlebih dahulu!")
            return
        
        if not target.isdigit():
            messagebox.showerror("Error", f"'{target}' bukan angka yang valid!")
            return
        
        target_id_int = int(target)
        jumlah = self.jumlah_produk.get()
        
        if target_id_int < 1 or target_id_int > jumlah:
            messagebox.showwarning("Peringatan", f"ID {target_id_int} di luar range! Range: 1 - {jumlah}")
            return
        
        # Peringatan untuk binary search
        if "Binary Search" in self.algoritma_var.get() and self.kondisi_var.get() != "Data Terurut berdasarkan ID":
            messagebox.showwarning("Peringatan", "Binary Search membutuhkan data TERURUT! Hasil mungkin tidak akurat.")
        
        # Jalankan algoritma
        self.result_text.delete(1.0, tk.END)
        
        if "Linear Search" in self.algoritma_var.get():
            start_time = time.time()
            posisi, langkah, produk = self.linear_search(self.data_list, target_id_int)
            waktu = (time.time() - start_time) * 1000
            algoritma = "Linear Search (O(n))"
            
        elif "Binary Search" in self.algoritma_var.get():
            start_time = time.time()
            posisi, langkah, produk = self.binary_search(self.data_sorted, target_id_int)
            waktu = (time.time() - start_time) * 1000
            algoritma = "Binary Search (O(log n))"
            
        else:  # Interpolation Search
            if self.kondisi_var.get() != "Data Terurut berdasarkan ID":
                messagebox.showwarning("Peringatan", "Interpolation Search membutuhkan data TERURUT!")
                return
            start_time = time.time()
            posisi, langkah, produk = self.interpolation_search(self.data_sorted, target_id_int)
            waktu = (time.time() - start_time) * 1000
            algoritma = "Interpolation Search (O(log n))"
        
        # Tampilkan hasil
        self.result_text.insert(tk.END, f"✅ Algoritma: {algoritma}\n")
        self.result_text.insert(tk.END, "="*60 + "\n\n")
        
        if posisi != -1:
            self.result_text.insert(tk.END, f"✅ Produk Ditemukan!\n\n")
            self.result_text.insert(tk.END, f"ID Produk yang Dicari: {target}\n")
            self.result_text.insert(tk.END, f"Nama Produk: {produk['nama']}\n")
            self.result_text.insert(tk.END, f"Harga: Rp {produk['harga']:,.0f}\n")
            self.result_text.insert(tk.END, f"📍 Posisi Rak (Indeks Array): {posisi}\n")
            self.result_text.insert(tk.END, f"Jumlah Langkah Pencarian: {langkah}\n")
            self.result_text.insert(tk.END, f"Waktu Eksekusi: {waktu:.3f} ms\n")
            
            # Update progress bar
            progress_value = (posisi / len(self.data_list)) * 100
            self.progress_bar['value'] = progress_value
            self.progress_label.config(text=f"Posisi Rak: {posisi} dari {len(self.data_list)-1} rak yang tersedia")
        else:
            self.result_text.insert(tk.END, f"❌ Produk dengan ID {target} tidak ditemukan!\n")
            self.result_text.insert(tk.END, f"Jumlah Langkah Pencarian: {langkah}\n")
            self.progress_bar['value'] = 0
    
    def bandingkan_algoritma(self):
        """Bandingkan ketiga algoritma"""
        compare_id = self.compare_id_entry.get()
        
        if not compare_id:
            messagebox.showwarning("Peringatan", "Silakan masukkan ID untuk perbandingan!")
            return
        
        if not compare_id.isdigit():
            messagebox.showerror("Error", f"'{compare_id}' bukan angka yang valid!")
            return
        
        target_id_int = int(compare_id)
        jumlah = self.jumlah_produk.get()
        
        if target_id_int < 1 or target_id_int > jumlah:
            messagebox.showwarning("Peringatan", f"ID {target_id_int} di luar range! Range: 1 - {jumlah}")
            return
        
        self.compare_result_text.delete(1.0, tk.END)
        self.compare_result_text.insert(tk.END, "🔬 PERBANDINGAN KETIGA ALGORITMA\n")
        self.compare_result_text.insert(tk.END, "="*60 + "\n\n")
        
        # Linear Search
        start = time.time()
        pos_linear, steps_linear, prod_linear = self.linear_search(self.data_list, target_id_int)
        time_linear = (time.time() - start) * 1000
        
        # Binary Search
        start = time.time()
        pos_binary, steps_binary, prod_binary = self.binary_search(self.data_sorted, target_id_int)
        time_binary = (time.time() - start) * 1000
        
        # Interpolation Search
        start = time.time()
        pos_inter, steps_inter, prod_inter = self.interpolation_search(self.data_sorted, target_id_int)
        time_inter = (time.time() - start) * 1000
        
        # Tampilkan hasil perbandingan
        self.compare_result_text.insert(tk.END, f"{'Algoritma':<30} {'Posisi Rak':<15} {'Langkah':<10} {'Waktu (ms)':<12}\n")
        self.compare_result_text.insert(tk.END, "-"*70 + "\n")
        self.compare_result_text.insert(tk.END, f"{'Linear Search':<30} {pos_linear if pos_linear != -1 else 'Tidak ditemukan':<15} {steps_linear:<10} {time_linear:<12.3f}\n")
        self.compare_result_text.insert(tk.END, f"{'Binary Search':<30} {pos_binary if pos_binary != -1 else 'Tidak ditemukan':<15} {steps_binary:<10} {time_binary:<12.3f}\n")
        self.compare_result_text.insert(tk.END, f"{'Interpolation Search':<30} {pos_inter if pos_inter != -1 else 'Tidak ditemukan':<15} {steps_inter:<10} {time_inter:<12.3f}\n")
        
        if pos_linear != -1:
            self.compare_result_text.insert(tk.END, f"\n📦 Produk {prod_linear['nama']} (ID: {compare_id}) berada di Posisi Rak {pos_linear}\n")

# ========== MAIN ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiPencarianRak(root)
    root.mainloop()