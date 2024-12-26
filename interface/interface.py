# import platform
# import subprocess

# # Detaylı işletim sistemi bilgileri
# os_system = platform.system()

# if os_system == "Windows":



# print(f"İşletim Sistemi: {os_system}")

import subprocess

# Komutu tanımla
command = "netsh interface show interface"

# Komutu çalıştır ve çıktıyı al
process = subprocess.run(command, capture_output=True, text=True, shell=True)

# Çıktıyı yazdır
print(process.stdout)
