import customtkinter as ctk
from tkinter import messagebox
import json
import random
import time
from datetime import datetime

# Setting tema CustomTkinter
ctk.set_appearance_mode("dark")  # Mode: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"

class AplikasiPencarianRak:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Pencarian Posisi Barang di Rak Digital")
        self.root.geometry("1400x800")
        
        # Variabel
        self.jumlah_produk = 500
        self.algoritma_var = ctk.StringVar(value="Linear Search (O(n))")
        self.kondisi_var = ctk.StringVar(value="Data Acak (Unsorted)")
        self.target_id = ctk.StringVar()
        self.data_list = []
        self.data_sorted = []
        
        # Setup UI
        self.setup_ui()
        self.generate_data()
        
    def setup_ui(self):
        # Grid layout - menggunakan method yang benar untuk CTk
        self.root.grid_columnconfigure(0, weight=0)  # Sidebar
        self.root.grid_columnconfigure(1, weight=1)  # Main content
        self.root.grid_rowconfigure(0, weight=1)
        
        # ========== SIDEBAR ==========
        self.sidebar = ctk.CTkFrame(self.root, width=280, corner_radius=10)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar.grid_propagate(False)
        
        # Header Sidebar
        header_label = ctk.CTkLabel(self.sidebar, text="⚙️ Pengaturan", 
                                    font=ctk.CTkFont(size=20, weight="bold"))
        header_label.pack(pady=(20, 10))
        
        # Jumlah Produk
        jumlah_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        jumlah_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(jumlah_frame, text="Jumlah produk di gudang:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w")
        
        self.jumlah_slider = ctk.CTkSlider(jumlah_frame, from_=100, to=1000, 
                                           number_of_steps=9,
                                           command=self.on_jumlah_change)
        self.jumlah_slider.pack(fill="x", pady=5)
        self.jumlah_slider.set(500)
        
        self.jumlah_label = ctk.CTkLabel(jumlah_frame, text="500")
        self.jumlah_label.pack()
        
        # Perbaikan: Mengganti CTkSeparator dengan CTkFrame tipis
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30").pack(fill="x", padx=15, pady=10)
        
        # Pilihan Algoritma
        algo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        algo_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(algo_frame, text="🎯 Pilih Algoritma Pencarian:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        algoritma_list = [
            "Linear Search (O(n))",
            "Binary Search (O(log n)) - Data harus terurut",
            "Interpolation Search (O(log n)) - Data harus terurut"
        ]
        
        for algo in algoritma_list:
            rb = ctk.CTkRadioButton(algo_frame, text=algo, variable=self.algoritma_var, 
                                   value=algo, font=ctk.CTkFont(size=12))
            rb.pack(anchor="w", pady=5)
        
        # Perbaikan: Mengganti CTkSeparator dengan CTkFrame tipis
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30").pack(fill="x", padx=15, pady=10)
        
        # Kondisi Data
        kondisi_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        kondisi_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(kondisi_frame, text="📦 Kondisi Data:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkRadioButton(kondisi_frame, text="Data Acak (Unsorted)", 
                          variable=self.kondisi_var, 
                          value="Data Acak (Unsorted)",
                          command=self.on_kondisi_change).pack(anchor="w", pady=5)
        
        ctk.CTkRadioButton(kondisi_frame, text="Data Terurut berdasarkan ID", 
                          variable=self.kondisi_var,
                          value="Data Terurut berdasarkan ID",
                          command=self.on_kondisi_change).pack(anchor="w", pady=5)
        
        # Perbaikan: Mengganti CTkSeparator dengan CTkFrame tipis
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30").pack(fill="x", padx=15, pady=10)
        
        # Tombol Generate
        self.generate_btn = ctk.CTkButton(self.sidebar, text="🔄 Generate Ulang Data", 
                                          command=self.generate_data,
                                          height=40, font=ctk.CTkFont(size=14))
        self.generate_btn.pack(padx=15, pady=10)
        
        # ========== MAIN CONTENT ==========
        self.main_content = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, height=80, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(header_frame, text="📦 Pencarian Posisi Barang di Rak Digital",
                                   font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(header_frame, 
                                      text="Menemukan posisi rak (indeks array) berdasarkan ID Produk menggunakan 3 algoritma pencarian",
                                      font=ctk.CTkFont(size=14))
        subtitle_label.pack()
        
        # Form Pencarian
        search_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=0)
        search_frame.grid_columnconfigure(2, weight=0)
        search_frame.grid_columnconfigure(3, weight=0)
        search_frame.grid_columnconfigure(4, weight=1)
        
        # Label
        ctk.CTkLabel(search_frame, text="Masukkan ID Produk (angka):", 
                    font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10, pady=15, sticky="w")
        
        # Entry
        self.id_entry = ctk.CTkEntry(search_frame, width=200, height=40,
                                     font=ctk.CTkFont(size=14),
                                     textvariable=self.target_id)
        self.id_entry.grid(row=0, column=1, padx=10, pady=15)
        
        # Tombol Cari
        self.cari_btn = ctk.CTkButton(search_frame, text="🔍 Cari Posisi Rak", 
                                      command=self.cari_produk,
                                      height=40, width=150,
                                      fg_color="#2ecc71", hover_color="#27ae60")
        self.cari_btn.grid(row=0, column=2, padx=10, pady=15)
        
        # Tombol Random
        self.random_btn = ctk.CTkButton(search_frame, text="🎲 Random ID", 
                                        command=self.random_id,
                                        height=40, width=120,
                                        fg_color="#e74c3c", hover_color="#c0392b")
        self.random_btn.grid(row=0, column=3, padx=10, pady=15)
        
        # Status kondisi
        self.status_label = ctk.CTkLabel(search_frame, text="", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=0, column=4, padx=10, pady=15, sticky="e")
        
        # Hasil Pencarian
        result_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        result_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        result_frame.grid_rowconfigure(0, weight=0)
        result_frame.grid_rowconfigure(1, weight=0)
        result_frame.grid_rowconfigure(2, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(result_frame, text="📊 Hasil Pencarian Posisi Rak",
                    font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, pady=10)
        
        # Progress bar
        progress_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
        progress_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Posisi Rak:", font=ctk.CTkFont(size=12))
        self.progress_label.grid(row=0, column=0, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=20, corner_radius=10)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=5)
        self.progress_bar.set(0)
        
        # Text area untuk hasil
        self.result_text = ctk.CTkTextbox(result_frame, font=ctk.CTkFont(size=12))
        self.result_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        # ========== TABVIEW ==========
        self.tabview = ctk.CTkTabview(self.main_content, corner_radius=10)
        self.tabview.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Tab 1: Seluruh Data
        tab_data = self.tabview.add("📋 Seluruh Data & Posisi Rak")
        self.setup_data_tab(tab_data)
        
        # Tab 2: Perbandingan Algoritma
        tab_compare = self.tabview.add("🔬 Bandingkan Algoritma")
        self.setup_compare_tab(tab_compare)
        
        # Footer
        footer_frame = ctk.CTkFrame(self.main_content, height=30, fg_color="transparent")
        footer_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.footer_label = ctk.CTkLabel(footer_frame, text="", font=ctk.CTkFont(size=10))
        self.footer_label.pack()
        self.update_footer()
        
    def setup_data_tab(self, parent):
        """Setup tab untuk menampilkan seluruh data"""
        scroll_frame = ctk.CTkScrollableFrame(parent, label_text="Data Produk (100 produk pertama)")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.data_frame = scroll_frame
        
        # Label header
        headers = ["ID Produk", "Nama Produk", "Harga", "📍 Posisi Rak"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(scroll_frame, text=header, 
                                 font=ctk.CTkFont(size=12, weight="bold"),
                                 fg_color="#3498db", corner_radius=5, padx=10, pady=5)
            label.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
        
    def setup_compare_tab(self, parent):
        """Setup tab untuk perbandingan algoritma"""
        # Frame input
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(input_frame, text="ID untuk perbandingan:", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        
        self.compare_id_entry = ctk.CTkEntry(input_frame, width=150)
        self.compare_id_entry.pack(side="left", padx=5)
        
        self.compare_btn = ctk.CTkButton(input_frame, text="Bandingkan Semua Algoritma",
                                         command=self.bandingkan_algoritma,
                                         fg_color="#3498db", hover_color="#2980b9")
        self.compare_btn.pack(side="left", padx=5)
        
        # Text area untuk hasil perbandingan
        self.compare_result_text = ctk.CTkTextbox(parent, font=ctk.CTkFont(size=12))
        self.compare_result_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def update_treeview(self):
        """Update tampilan data"""
        for widget in self.data_frame.winfo_children():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()
        
        for idx, produk in enumerate(self.data_list[:100], start=1):
            id_label = ctk.CTkLabel(self.data_frame, text=str(produk['id']), 
                                   font=ctk.CTkFont(size=12), padx=5, pady=2)
            id_label.grid(row=idx, column=0, padx=2, pady=1, sticky="ew")
            
            nama_label = ctk.CTkLabel(self.data_frame, text=produk['nama'], 
                                     font=ctk.CTkFont(size=12), padx=5, pady=2)
            nama_label.grid(row=idx, column=1, padx=2, pady=1, sticky="ew")
            
            harga_label = ctk.CTkLabel(self.data_frame, text=f"Rp {produk['harga']:,.0f}", 
                                      font=ctk.CTkFont(size=12), padx=5, pady=2)
            harga_label.grid(row=idx, column=2, padx=2, pady=1, sticky="ew")
            
            posisi_label = ctk.CTkLabel(self.data_frame, text=str(produk['posisi_rak']), 
                                       font=ctk.CTkFont(size=12), padx=5, pady=2)
            posisi_label.grid(row=idx, column=3, padx=2, pady=1, sticky="ew")
    
    def update_footer(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.footer_label.configure(text=f"🔄 Data terakhir diperbarui: {now} | 🎯 Tugas: Menemukan POSISI RAK (INDEKS ARRAY) berdasarkan ID Produk")
        self.root.after(1000, self.update_footer)
    
    def on_jumlah_change(self, value):
        self.jumlah_label.configure(text=str(int(value)))
        self.jumlah_produk = int(value)
        self.generate_data()
    
    def on_kondisi_change(self):
        self.generate_data()
    
    def generate_data(self):
        """Generate data produk"""
        n = int(self.jumlah_slider.get())
        products = []
        for i in range(n):
            products.append({
                'id': i + 1,
                'nama': f"Produk {i+1}",
                'harga': random.randint(10000, 1000000),
                'posisi_rak': i
            })
        
        if self.kondisi_var.get() == "Data Acak (Unsorted)":
            self.data_list = products.copy()
            random.shuffle(self.data_list)
            self.status_label.configure(text="📦 Data ACAK", text_color="#f39c12")
        else:
            self.data_list = sorted(products, key=lambda x: x['id'])
            self.status_label.configure(text="📚 Data TERURUT", text_color="#2ecc71")
        
        self.data_sorted = sorted(self.data_list, key=lambda x: x['id'])
        self.update_treeview()
        
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"✅ Data berhasil digenerate! Total {n} produk.\n")
    
    def random_id(self):
        random_id = random.randint(1, int(self.jumlah_slider.get()))
        self.target_id.set(str(random_id))
        self.id_entry.focus()
    
    # ========== ALGORITMA PENCARIAN ==========
    
    def linear_search(self, data, target_id):
        langkah = 0
        for i, produk in enumerate(data):
            langkah += 1
            if produk['id'] == target_id:
                return i, langkah, produk
        return -1, langkah, None
    
    def binary_search(self, data, target_id):
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
        langkah = 0
        low, high = 0, len(data) - 1
        
        while low <= high and target_id >= data[low]['id'] and target_id <= data[high]['id']:
            langkah += 1
            
            if low == high:
                if data[low]['id'] == target_id:
                    return low, langkah, data[low]
                return -1, langkah, None
            
            if data[high]['id'] == data[low]['id']:
                break
                
            posisi = low + int(((high - low) / (data[high]['id'] - data[low]['id'])) * (target_id - data[low]['id']))
            
            if posisi < low or posisi > high:
                break
            
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
        jumlah = int(self.jumlah_slider.get())
        
        if target_id_int < 1 or target_id_int > jumlah:
            messagebox.showwarning("Peringatan", f"ID {target_id_int} di luar range! Range: 1 - {jumlah}")
            return
        
        if "Binary Search" in self.algoritma_var.get() and self.kondisi_var.get() != "Data Terurut berdasarkan ID":
            messagebox.showwarning("Peringatan", "Binary Search membutuhkan data TERURUT! Hasil mungkin tidak akurat.")
        
        self.result_text.delete("1.0", "end")
        
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
        
        self.result_text.insert("end", f"✅ Algoritma: {algoritma}\n")
        self.result_text.insert("end", "="*60 + "\n\n")
        
        if posisi != -1:
            self.result_text.insert("end", f"✅ Produk Ditemukan!\n\n")
            self.result_text.insert("end", f"ID Produk yang Dicari: {target}\n")
            self.result_text.insert("end", f"Nama Produk: {produk['nama']}\n")
            self.result_text.insert("end", f"Harga: Rp {produk['harga']:,.0f}\n")
            self.result_text.insert("end", f"📍 Posisi Rak (Indeks Array): {posisi}\n")
            self.result_text.insert("end", f"Jumlah Langkah Pencarian: {langkah}\n")
            self.result_text.insert("end", f"Waktu Eksekusi: {waktu:.3f} ms\n")
            
            if len(self.data_list) > 0:
                progress_value = posisi / len(self.data_list)
                self.progress_bar.set(progress_value)
                self.progress_label.configure(text=f"Posisi Rak: {posisi} dari {len(self.data_list)-1} rak yang tersedia")
        else:
            self.result_text.insert("end", f"❌ Produk dengan ID {target} tidak ditemukan!\n")
            self.result_text.insert("end", f"Jumlah Langkah Pencarian: {langkah}\n")
            self.progress_bar.set(0)
    
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
        jumlah = int(self.jumlah_slider.get())
        
        if target_id_int < 1 or target_id_int > jumlah:
            messagebox.showwarning("Peringatan", f"ID {target_id_int} di luar range! Range: 1 - {jumlah}")
            return
        
        self.compare_result_text.delete("1.0", "end")
        self.compare_result_text.insert("1.0", "🔬 PERBANDINGAN KETIGA ALGORITMA\n")
        self.compare_result_text.insert("end", "="*60 + "\n\n")
        
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
        
        self.compare_result_text.insert("end", f"{'Algoritma':<35} {'Posisi Rak':<15} {'Langkah':<10} {'Waktu (ms)':<12}\n")
        self.compare_result_text.insert("end", "-"*75 + "\n")
        self.compare_result_text.insert("end", f"{'Linear Search':<35} {pos_linear if pos_linear != -1 else 'Tidak ditemukan':<15} {steps_linear:<10} {time_linear:<12.3f}\n")
        self.compare_result_text.insert("end", f"{'Binary Search':<35} {pos_binary if pos_binary != -1 else 'Tidak ditemukan':<15} {steps_binary:<10} {time_binary:<12.3f}\n")
        self.compare_result_text.insert("end", f"{'Interpolation Search':<35} {pos_inter if pos_inter != -1 else 'Tidak ditemukan':<15} {steps_inter:<10} {time_inter:<12.3f}\n")
        
        if pos_linear != -1:
            self.compare_result_text.insert("end", f"\n📦 Produk {prod_linear['nama']} (ID: {compare_id}) berada di Posisi Rak {pos_linear}\n")

# ========== MAIN ==========
if __name__ == "__main__":
    root = ctk.CTk()
    app = AplikasiPencarianRak(root)
    root.mainloop()