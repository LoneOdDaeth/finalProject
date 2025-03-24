from scapy.all import rdpcap, IP
from collections import Counter
import os

def analyze_pcap(file_path):
    packets = rdpcap(file_path)

    total_packets = len(packets)
    protocol_counter = Counter()
    src_ips = set()
    dst_ips = set()
    timestamps = []
    src_ip_counter = Counter()

    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

            src_ips.add(src_ip)
            dst_ips.add(dst_ip)
            src_ip_counter[src_ip] += 1

            proto = pkt[IP].proto
            if proto == 6:
                protocol_counter["TCP"] += 1
            elif proto == 17:
                protocol_counter["UDP"] += 1
            elif proto == 1:
                protocol_counter["ICMP"] += 1
            else:
                protocol_counter["Other"] += 1

            timestamps.append(float(pkt.time))

    summary = {
        "total_packets": total_packets,
        "protocols": dict(protocol_counter),
        "unique_src_ips": list(src_ips),
        "unique_dst_ips": list(dst_ips),
        "src_ip_counts": dict(src_ip_counter),
        "timestamps": timestamps,
        "time_range": (
            float(min(timestamps)) if timestamps else None,
            float(max(timestamps)) if timestamps else None
        )
    }

    return summary
