import tkinter as tk
from tkinter import ttk

# Data contoh
documents = [
    "Python adalah bahasa pemrograman",
    "Mesin pencari bekerja dengan indexing",
    "Tkinter digunakan untuk membuat GUI",
    "Python cocok untuk machine learning",
    "Search engine dapat dibuat dengan Python"
]

# Fungsi pencarian
def search():
    keyword = entry.get().lower()
    result_box.delete(0, tk.END)

    if keyword == "":
        return

    found = False

    for doc in documents:
        if keyword in doc.lower():
            result_box.insert(tk.END, doc)
            found = True

    if not found:
        result_box.insert(tk.END, "Tidak ada hasil ditemukan")

# Window utama
root = tk.Tk()
root.title("Mini Search Engine")
root.geometry("500x350")

# Judul
title = tk.Label(root, text="Mesin Search Python", font=("Arial", 16))
title.pack(pady=10)

# Frame search
frame = tk.Frame(root)
frame.pack(pady=10)

# Input
entry = ttk.Entry(frame, width=35)
entry.pack(side=tk.LEFT, padx=5)

# Tombol search
btn = ttk.Button(frame, text="Search", command=search)
btn.pack(side=tk.LEFT)

# List hasil
result_box = tk.Listbox(root, width=70, height=12)
result_box.pack(pady=10)

# Run aplikasi
root.mainloop()