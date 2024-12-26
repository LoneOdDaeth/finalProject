import tkinter as tk
from tkinter import ttk, messagebox
import threading

def start_sniffing(start_button, stop_button, save_button):
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)

def stop_sniffing(start_button, stop_button):
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def save_capture():
    messagebox.showinfo("Kaydet", "Paket yakalama kaydedildi.")

root = tk.Tk()
root.title("Wireshark Benzeri Paket Yakalama Arayüzü")
root.configure(bg="#2C2F33")  # Daha modern bir koyu renk tonu kullanıldı

# Stil ayarları
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#1E1F22",
                foreground="white",
                rowheight=25,
                fieldbackground="#1E1F22",
                font=('Arial', 10))
style.map('Treeview', background=[('selected', '#4C566A')])
style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#23272A", foreground="white")

# Paketlerin listeleneceği Treeview widget'ı
tree = ttk.Treeview(root)
tree["columns"] = ("timestamp", "src", "dst", "protocol", "length")
    
tree.heading("#0", text="No.")
tree.column("#0", width=50)
tree.heading("timestamp", text="Zaman Damgası")
tree.column("timestamp", width=150)
tree.heading("src", text="Kaynak")
tree.column("src", width=150)
tree.heading("dst", text="Hedef")
tree.column("dst", width=150)
tree.heading("protocol", text="Protokol")
tree.column("protocol", width=100)
tree.heading("length", text="Uzunluk")
tree.column("length", width=100)
    
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
    
# Butonları çerçeveye yerleştiriyoruz
button_frame = tk.Frame(root, bg="#2C2F33")
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
# Başlat/Durdur/Kaydet butonları
start_button = tk.Button(button_frame, text="Başlat", command=lambda: start_sniffing(start_button, stop_button, save_button),
                        bg="#7289DA", fg="white", activebackground="#5A78B8", activeforeground="white", font=('Arial', 10, 'bold'))
start_button.pack(side=tk.LEFT, padx=10)
    
stop_button = tk.Button(button_frame, text="Durdur", command=lambda: stop_sniffing(start_button, stop_button), state=tk.DISABLED,
                        bg="#99AAB5", fg="black", activebackground="#778D98", activeforeground="white", font=('Arial', 10, 'bold'))
stop_button.pack(side=tk.LEFT, padx=10)
    
save_button = tk.Button(button_frame, text="Kaydet", command=save_capture, state=tk.DISABLED,
                        bg="#43B581", fg="white", activebackground="#358965", activeforeground="white", font=('Arial', 10, 'bold'))
save_button.pack(side=tk.LEFT, padx=10)

tree, start_button, stop_button, save_button

root.mainloop()