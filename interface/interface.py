import platform
import subprocess

# Detaylı işletim sistemi bilgileri
os_system = platform.system()

# print(f"İşletim Sistemi: {os_system}")

interfaces = []  # Arayüz bilgilerini kaydedeceğimiz liste

if os_system == "Windows":
    command = "netsh interface show interface"
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = process.stdout  # Komut çıktısı

    # Çıktıyı satırlara ayır
    lines = output.splitlines()

    # Çıktının veri içeren kısmını bul
    for line in lines[3:]:  # İlk 3 satır başlık olduğu için atlanır
        if line.strip():  # Boş satırları atla
            parts = line.split()  # Verileri ayır
            # Sadece arayüz adını ekle
            interface_name = " ".join(parts[3:])  # Arayüz adı birden fazla kelime olabilir
            interfaces.append(interface_name)  # Direkt adı ekle

    print(interfaces)

elif os_system == "Linux":
    command = "ls /sys/class/net/"
    process = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = process.stdout
    lines = output.splitlines()  # Komut çıktısını satırlara ayır

    for line in lines:
        if line.strip():  # Boş satırları atla
            interfaces.append(line.strip())  # Arayüz adını ekle

    print(interfaces)
