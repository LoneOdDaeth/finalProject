import tkinter as tk
from tkinter import scrolledtext

def show_help_window():
    help_root = tk.Toplevel()
    help_root.title("Yardım Paneli - Erlik")
    help_root.geometry("1920x1080")
    help_root.configure(bg="#2C2F33")
    help_root.overrideredirect(True)  # Kenarlıksız tam pencere

    title = tk.Label(help_root, text="📘 ERLİK YARDIM PANELİ", font=("Arial", 18, "bold"), fg="#00ff00", bg="#2C2F33")
    title.pack(pady=10)

    frame = tk.Frame(help_root, bg="#2C2F33")
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Consolas", 13), bg="#1E1F22", fg="white", insertbackground='white')
    text_area.pack(expand=True, fill=tk.BOTH)

    help_text = """\
# 🧠 Erlik Ağ Analiz Aracı

---

## 🚀 Başlarken

Bu uygulama `.pcap` uzantılı ağ trafiği dosyalarını analiz etmenizi sağlar. Sistemde yer alan modüller:

- **Profil**: Kullanıcı geçmişini ve istatistikleri görüntüleme
- **Analiz**: PCAP dosyalarını yükleyip analiz etme
- **Network Graph**: IP adresleri arasındaki bağlantıları görsel olarak inceleme
- **Export**: PDF raporlar oluşturma ve dışa aktarma
- **Admin Panel**: SMTP ve kullanıcı yönetimi
- **Helpers**: Bu yardım penceresi

---

## 🔍 Özellikler

- 📁 **PCAP Yükle ve Analiz Et**  
  Ağ trafiğini incelemek için `.pcap` dosyasını yükleyin ve analiz başlatın.

- 📊 **Grafikler**  
  Protokol dağılımı, zaman serisi ve yoğun IP adreslerini grafiklerle takip edin.

- 🌐 **Ağ Haritası**  
  IP’ler arası bağlantıları görsel olarak görün ve filtreleyin.

- 📤 **PDF Dışa Aktarımı**  
  Tüm analiz çıktıları PDF formatında arşivlenebilir ve paylaşılabilir.

- 📧 **Mail Gönderme**  
  Analiz dosyalarınızı başka kullanıcılara sistem üzerinden iletin.

---

## 🧑‍💼 Geliştirici Bilgisi

- Bu sistem Python, Dash, Pyshark ve MongoDB kullanılarak geliştirilmiştir.
- Tüm görsel arabirim `Tkinter` ile entegredir.
- Arayüz `F1` ile bu pencereyi açmanıza olanak tanır.

---

Herhangi bir hata veya öneri için sistem yöneticinize başvurun.
"""

    text_area.insert(tk.END, help_text)
    text_area.config(state=tk.DISABLED)

    close_button = tk.Button(help_root, text="Kapat", command=help_root.destroy,
                             font=("Arial", 12, "bold"), bg="#00ff00", fg="#2C2F33")
    close_button.pack(pady=10)
