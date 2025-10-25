from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, RandShort, wrpcap, send
import base64

FLAG = "RkxBR3toYXBweV9oYWxsb3dlZW5fMjAyNX0="
PRETEXT = "WU9VX0ZPVU5EX0FfTEVUVEVSX0ZPUl9USEVfS0VZXw=="

PUMPKIN = r"""
                  ___
               ___)__|_
          .-*'          '*-,
         /      /|   |\     \
        ;      /_|   |_\     ;
        ;   |\           /|  ;
        ;   | ''--...--'' |  ;
         \  ''---.....--''  /
          ''*-.,_______,.-*'  
"""

def generate_flag() -> dict[str, str]:
    flag = {}
    flag_decoded = base64.b64decode(FLAG).decode('utf-8')
    pretext_decoded = base64.b64decode(PRETEXT).decode('utf-8')
    for letter in flag_decoded:
        flag_part = pretext_decoded + letter
        hex_part = ''.join(f"{ord(char)}" for char in flag_part)
        flag[letter] = hex_part
    return flag

def xor(data: str, key: str) -> bytes:
    data_bytes = data.encode('utf-8')
    key_bytes = key.encode('utf-8')
    xored = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data_bytes)])
    return xored

def generate_key_packets():
    packets = []
    flag_dict = generate_flag()
    for letter, hex_value in flag_dict.items():
        qname = f"{hex_value}.pumpkin.example."
        dns_a_query = (
                IP(dst="1.2.3.4") /
                UDP(sport=RandShort(), dport=53) /
                DNS(rd=1, qd=DNSQR(qname=qname, qtype="A"))
        )
        dns_a_response = (
                IP(src="1.2.3.4", dst="192.168.1.1") /
                UDP(sport=53, dport=RandShort()) /
                DNS(
                    id=0x1337,
                    qr=1,
                    aa=1,
                    qd=DNSQR(qname=qname, qtype="A"),
                    an=DNSRR(
                        rrname=qname,
                        type="A",
                        ttl=300,
                        rdata="10.13.37.1"
                    )
                )
        )
        packets.extend([dns_a_query, dns_a_response])
    return packets

def generate_txt_packets():
    packets = []
    dns_txt_qry = (
        IP(dst="1.2.3.4")/
        UDP(sport=RandShort(), dport=53)/
        DNS(
            rd=1,
            qd=DNSQR(qname="pumpkin.example.", qtype="TXT")
        )
    )

    dns_txt_resp = (
        IP(src="1.2.3.4", dst="192.168.1.1") /
        UDP(sport=53, dport=RandShort()) /
        DNS(
            id=0x1337,
            qr=1,
            aa=1,
            qd=DNSQR(qname="pumpkin.example.", qtype="TXT"),
            an=DNSRR(
                rrname="pumpkin.example.",
                type="TXT",
                ttl=300,
                rdata=PUMPKIN
            )
        )
    )
    packets.extend([dns_txt_qry, dns_txt_resp])
    return packets

key_packets = generate_key_packets()
txt_packets = generate_txt_packets()
all_packets = key_packets + txt_packets

wrpcap("txt_or_treat.pcap", all_packets)
print("[+] Saved txt_or_treat.pcap")