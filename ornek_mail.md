PCAP ANALİZ RAPORU
===================

1. GENEL BİLGİLER
------------------
- Dosya Adı: network_capture_2025_03_24.pcap
- Analiz Tarihi: 24 Mart 2025
- Analizi Yapan: Alparslan Özuygur
- Toplam Paket Sayısı: 14,382
- Zaman Aralığı: 2025-03-24 10:15:03 - 2025-03-24 10:27:45
- Toplam Veri Boyutu: 8.2 MB

2. PROTOKOL DAĞILIMI
---------------------
- TCP: %62 (8,908 paket)
- UDP: %30 (4,314 paket)
- ICMP: %6  (863 paket)
- Diğer: %2  (297 paket)

(Not: Pie chart ve bar chart ile görselleştirme yapılabilir.)

3. KAYNAK VE HEDEF IP DAĞILIMLARI
----------------------------------
En çok trafik üreten kaynak ve hedef IP adresleri:

| IP Adresi       | Rol    | Paket Sayısı |
|------------------|--------|--------------|
| 192.168.1.10     | Kaynak | 5,429        |
| 192.168.1.12     | Kaynak | 3,182        |
| 8.8.8.8          | Hedef  | 1,203        |
| 104.16.132.229   | Hedef  | 974          |
| 172.217.16.142   | Hedef  | 891          |

4. ZAMAN SERİSİ ANALİZİ
------------------------
- Trafik yoğunluğu 10:20 - 10:22 arasında belirgin şekilde artmıştır.
- 10:21:37 zamanında kısa süreli bir trafik patlaması gözlemlendi (256 paket/sn).

5. ŞÜPHELİ AKTİVİTELER (VARSA)
-------------------------------
- 172.217.16.142 IP adresine saniyede 100'ün üzerinde ICMP paketi gönderilmiş.
- 192.168.1.12 cihazı, 53 numaralı UDP portundan yoğun dış DNS isteği göndermiş.
- 104.16.132.229 adresiyle yoğun HTTP trafiği, kaynağı incelenmeli.

6. GENEL DEĞERLENDİRME
------------------------
- Sistem trafiği genel olarak olağan gözükmektedir.
- 192.168.1.12 IP’si DNS flood denemesi yapıyor olabilir, firewall kuralları kontrol edilmelidir.
- ICMP trafiği göz önüne alınarak IDS sistemine loglar aktarılmalı.

7. EKLER
---------
- Grafikler:
  - protokol_dagilimi_pie.png
  - kaynak_ip_bar.png
  - zaman_grafiği_line.png
- Ham analiz çıktısı: analysis_2025_03_24.json
- PCAP SHA256 Hash: `3a2c1bce2d09b5e5f8a0cf6b77c6eec44c771bbf6209c2cfad05ed3ec96e4ef3`

