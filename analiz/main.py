import pyshark
import json

# PCAP dosyanın yolu
pcap_file = "test.pcap"

# JSON dosya adı
json_file = "pcap_analysis.json"

# JSON için boş liste
packet_data = []

# Maksimum analiz edilecek paket sayısı
packet_limit = 100

# 'with' bloğu kullanarak otomatik kaynak yönetimi sağla
with pyshark.FileCapture(pcap_file) as cap:
    for i, packet in enumerate(cap):
        try:
            packet_info = {
                "Packet No": i+1,
                "Time": str(packet.sniff_time) if hasattr(packet, 'sniff_time') else "N/A",
                "Length": packet.length if hasattr(packet, 'length') else "N/A",
                "Highest Layer": packet.highest_layer if hasattr(packet, 'highest_layer') else "N/A",
                "Source IP": packet.ip.src if hasattr(packet, 'ip') else "N/A",
                "Destination IP": packet.ip.dst if hasattr(packet, 'ip') else "N/A",
                "Source Port": packet[packet.transport_layer].srcport if hasattr(packet, 'transport_layer') else "N/A",
                "Destination Port": packet[packet.transport_layer].dstport if hasattr(packet, 'transport_layer') else "N/A",
                "Protocol": packet.transport_layer if hasattr(packet, 'transport_layer') else "N/A"
            }

            packet_data.append(packet_info)

            if i >= packet_limit - 1:
                break
        except Exception:
            continue

# JSON dosyasına yaz
with open(json_file, "w") as f:
    json.dump(packet_data, f, indent=4)

print(f"PCAP analizi başarıyla '{json_file}' dosyasına kaydedildi!")
