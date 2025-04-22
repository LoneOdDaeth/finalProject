import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pyshark
import os

# Temalar (login.py ile aynı)
COLORS = {
    "bg": "#2C2F33",
    "fg": "#00ff00",
    "entry_bg": "#1E1F22",
    "button_bg": "#2C2F33",
    "button_active_bg": {"login": "#00ff00", "signup": "#00ff00"},
    "button_active_fg": "#2C2F33"
}
FONTS = {
    "label": ('Arial', 12, 'bold'),
    "entry": ('Arial', 12),
    "button": ('Arial', 12, 'bold'),
    "kendiButon": ('Arial', 12)
}

def run_sniffer():
    sniffer_root = tk.Toplevel()
    app = PacketSnifferGUI(sniffer_root)

class PacketSnifferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyShark Sniffer")
        self.root.geometry("1920x1080")
        self.root.overrideredirect(True)  # Tam ekran modu
        
        # Arka plan rengi ayarla
        self.root.configure(bg=COLORS["bg"])

        # Üst çubuk
        title_bar = tk.Frame(self.root, bg=COLORS["bg"], relief="raised", bd=2)
        title_bar.pack(side="top", fill="x")

        tk.Label(title_bar, text="Canlı Ağ Trafiği", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"]).pack(side="left", padx=10)
        
        # Kapat butonu
        tk.Button(title_bar, text="X", bg=COLORS["button_bg"], fg=COLORS["fg"],
                  command=self.root.destroy, font=FONTS["kendiButon"], width=3).pack(side="right")

        # Kontrol butonları
        control_frame = tk.Frame(self.root, bg=COLORS["bg"])
        control_frame.pack(anchor='nw', fill=tk.X)

        self.start_button = tk.Button(control_frame, text="▶ Başla", command=self.start_sniffing,
                                      bg=COLORS["button_bg"], fg=COLORS["fg"], font=FONTS["button"],
                                      activebackground=COLORS["button_active_bg"]["login"],
                                      activeforeground=COLORS["button_active_fg"])
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(control_frame, text="■ Durdur", command=self.stop_sniffing, state=tk.DISABLED,
                                     bg=COLORS["button_bg"], fg=COLORS["fg"], font=FONTS["button"],
                                     activebackground="red", activeforeground="white")
        self.stop_button.pack(side=tk.LEFT, padx=0, pady=10)
        
        # Kaydet butonu - başla ve durdur ile aynı hizaya
        self.save_button = tk.Button(control_frame, text="💾 Kaydet", command=self.save_and_return,
                                    bg=COLORS["button_bg"], fg=COLORS["fg"], font=FONTS["button"],
                                    activebackground=COLORS["button_active_bg"]["login"],
                                    activeforeground=COLORS["button_active_fg"])
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Treeview teması
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1E1F22",  # Koyu arka plan
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#1E1F22",
                        font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#00ff00')])
        
        # Sütun başlıkları için stil
        style.configure("Treeview.Heading",
                        background="#2C2F33",
                        foreground="#00ff00",
                        font=('Arial', 12, 'bold'))

        # Paket tablosu
        self.tree = ttk.Treeview(self.root, columns=("No", "Protocol", "Source", "Destination"), show="headings", style="Treeview")
        self.tree.heading("No", text="No")
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Destination", text="Destination")
        
        # Kolon genişlikleri
        self.tree.column("No", width=80, anchor="center")
        self.tree.column("Protocol", width=120, anchor="center")
        self.tree.column("Source", width=180)
        self.tree.column("Destination", width=180)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Renk tagları 
        self.tree.tag_configure("TCP", background="#1e3f1e")  # Yeşilimsi
        self.tree.tag_configure("UDP", background="#1e3b4f")  # Mavimsi
        self.tree.tag_configure("ICMP", background="#504d1e")  # Sarımsı
        self.tree.tag_configure("OTHER", background="#333333")  # Gri

        self.packet_list = []
        self.capture = None
        self.sniffing = False
        self.capture_file = None  # Capture file için değişken
        self.tree.bind("<Double-1>", self.on_double_click)

    def start_sniffing(self):
        if self.sniffing:
            return
        self.sniffing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Geçici capture dosyası oluştur
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.capture_file = os.path.join(self.temp_dir, "temp_capture.pcap")
        
        # Output file belirtilerek capture başlat
        self.capture = pyshark.LiveCapture(interface="Wi-Fi", output_file=self.capture_file)
        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True)
        self.sniff_thread.start()

    def stop_sniffing(self):
        self.sniffing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.capture:
            self.capture.close()

    def sniff_packets(self):
        for packet in self.capture.sniff_continuously():
            if not self.sniffing:
                break
            try:
                proto = packet.highest_layer
                src = packet.ip.src
                dst = packet.ip.dst
            except AttributeError:
                continue

            packet_number = len(self.packet_list) + 1
            self.packet_list.append(packet)
            tag = proto if proto in ["TCP", "UDP", "ICMP"] else "OTHER"
            item = self.tree.insert("", tk.END, values=(packet_number, proto, src, dst), tags=(tag,))
            self.tree.see(item)

    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        index = int(self.tree.item(selected_item[0])["values"][0]) - 1
        packet = self.packet_list[index]
        print(f"\n=== Paket #{index + 1} ===\n")
        try:
            _ = packet.layers
        except Exception as e:
            print("Paket yüklenemedi:", e)
            return
        for layer in packet.layers:
            print(f"[{layer.layer_name.upper()}]")
            try:
                fields = getattr(layer, '_all_fields', {})
                for field in fields:
                    print(f"  {field.showname}")
            except Exception as e:
                print(f"  [HATA]: {e}")
            print("")
    
    def save_and_return(self):
        # Sniffing çalışıyorsa durdur
        if self.sniffing:
            self.stop_sniffing()
        
        # Eğer hiç paket yakalanmamışsa uyar
        if not self.packet_list:
            messagebox.showwarning("Uyarı", "Kaydedilecek paket bulunmamaktadır!")
            return
        
        # Kaydetme dialog'unu aç
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pcap",
            filetypes=[("PCAP dosyaları", "*.pcap"), ("Tüm dosyalar", "*.*")],
            title="Paket kaydını nereye kaydetmek istersiniz?"
        )
        
        if file_path:
            try:
                # Eğer capture_file oluşturulduysa, dosyayı kullanıcının istediği yere kopyala
                if self.capture_file and os.path.exists(self.capture_file):
                    import shutil
                    shutil.copy2(self.capture_file, file_path)
                    
                    # Başarı mesajı göster
                    messagebox.showinfo("Başarılı", f"Paketler {file_path} konumuna kaydedildi!")
                    
                    # Sadece pencereyi kapat ve önceki ekrana dön
                    self.root.destroy()
                else:
                    messagebox.showerror("Hata", "Capture dosyası bulunamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu: {str(e)}")