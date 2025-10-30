from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, RandShort, wrpcap
import base64
import random

COMPROMISED_HOST = "10.0.0.2"
DNS_HOST = "10.0.0.10"
ATTACKER_HOST = "203.0.113.6"
ATTACKER_DOMAIN = "pumpkin.local"
FLAG = "RkxBR3toYXBweV9oYWxsb3dlZW5fMjAyNX0="
PRETEXT = "WU9VX0ZPVU5EX0FfTEVUVEVSX0ZPUl9USEVfS0VZXw=="
HALLOWEEN_WORDLIST = ("ghost", "witch", "pumpkin", "candy", "spooky",
                      "haunted", "costume", "trick", "treat", "skeleton",
                      "dark", "bat", "zombie", "vampire", "reeses", "skittles",
                      "kitkat", "snickers", "twix", "sourpatch", "airhead")

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

def generate_key_packets() -> list:
    packets = []
    flag_dict = generate_flag()
    for letter, hex_value in flag_dict.items():
        qname = f"{hex_value}.{ATTACKER_DOMAIN}"
        dns_a_query = (
                IP(src=COMPROMISED_HOST,dst=DNS_HOST) /
                UDP(sport=RandShort(), dport=53) /
                DNS(rd=1, qd=DNSQR(qname=qname, qtype="A"))
        )
        dns_a_response = (
                IP(src=DNS_HOST, dst=COMPROMISED_HOST) /
                UDP(sport=53, dport=RandShort()) /
                DNS(
                    id=0x1337,
                    qr=1,
                    aa=1,
                    qd=DNSQR(qname=qname, qtype="A"),
                    an=DNSRR(
                        rrname=f"{qname}.",
                        type="A",
                        ttl=300,
                        rdata=ATTACKER_HOST
                    )
                )
        )
        packets.extend([dns_a_query, dns_a_response])
    return packets

def generate_txt_packets(data: str) -> list:
    packets = []
    dns_txt_qry = (
        IP(src=COMPROMISED_HOST, dst=DNS_HOST)/
        UDP(sport=RandShort(), dport=53)/
        DNS(
            rd=1,
            qd=DNSQR(qname=ATTACKER_DOMAIN, qtype="TXT")
        )
    )

    dns_txt_resp = (
        IP(src=DNS_HOST, dst=COMPROMISED_HOST) /
        UDP(sport=53, dport=RandShort()) /
        DNS(
            id=0x1337,
            qr=1,
            aa=1,
            qd=DNSQR(qname=ATTACKER_DOMAIN, qtype="TXT"),
            an=DNSRR(
                rrname=f"{ATTACKER_DOMAIN}.",
                type="TXT",
                ttl=300,
                rdata=data
            )
        )
    )
    packets.extend([dns_txt_qry, dns_txt_resp])
    return packets

def generate_halloween_dns_packets() -> list:
    packets = []
    for _ in range(50):
        word1, word2 = random.sample(HALLOWEEN_WORDLIST, 2)
        qname = f"{word1}.{word2}.local"
        last_octet = random.randint(3, 254)
        random_dns_traffic_host = f"10.0.0.{last_octet}"
        dns_answer = f"203.0.113.{last_octet}"
        dns_a_query = (
            IP(src=random_dns_traffic_host, dst=DNS_HOST) /
            UDP(sport=RandShort(), dport=53) /
            DNS(rd=1, qd=DNSQR(qname=qname, qtype="A"))
        )
        dns_a_response = (
            IP(src=DNS_HOST, dst=random_dns_traffic_host) /
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
                    rdata=dns_answer
                )
            )
        )
        packets.extend([dns_a_query, dns_a_response])
    return packets