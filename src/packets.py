from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, RandShort, wrpcap
from art import *
import base64
import random

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

def generate_txt_packets(data):
    packets = []
    dns_txt_qry = (
        IP(dst="1.2.3.4")/
        UDP(sport=RandShort(), dport=53)/
        DNS(
            rd=1,
            qd=DNSQR(qname="pumpkin.local.", qtype="TXT")
        )
    )

    dns_txt_resp = (
        IP(src="1.2.3.4", dst="192.168.1.1") /
        UDP(sport=53, dport=RandShort()) /
        DNS(
            id=0x1337,
            qr=1,
            aa=1,
            qd=DNSQR(qname="pumpkin.local.", qtype="TXT"),
            an=DNSRR(
                rrname="pumpkin.local.",
                type="TXT",
                ttl=300,
                rdata=data
            )
        )
    )
    packets.extend([dns_txt_qry, dns_txt_resp])
    return packets

def generate_halloween_dns_packets():
    packets = []
    for _ in range(50):
        word1, word2 = random.sample(HALLOWEEN_WORDLIST, 2)
        qname = f"{word1}.{word2}.local"
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
                    rdata="10.66.6.6"
                )
            )
        )
        packets.extend([dns_a_query, dns_a_response])
    return packets


def main():
    # Generate flag key packets
    key_packets = generate_key_packets()

    # Generate TXT packets with pumpkin art
    pumpkin_xored = xor(PUMPKIN, base64.b64decode(FLAG).decode('utf-8'))
    pumpkin_b64_encoded = base64.b64encode(pumpkin_xored).decode('utf-8')
    pumpkin_txt_packets = generate_txt_packets(pumpkin_b64_encoded)

    # Generate animal TXT packets
    cool_bear_txt_packets = generate_txt_packets(COOL_BEAR)
    bear_txt_packets = generate_txt_packets(BEAR)
    hippo_txt_packets = generate_txt_packets(HIPPO)
    squirrel_txt_packets = generate_txt_packets(SQUIRREL)
    deer_txt_packets = generate_txt_packets(DEER)
    dog_txt_packets = generate_txt_packets(DOG)

    # Generate random halloween DNS packets
    halloween_dns_packets = generate_halloween_dns_packets()


    # Combine all packets and randomly shuffle
    all_packets = key_packets + pumpkin_txt_packets + \
        cool_bear_txt_packets + bear_txt_packets + \
        hippo_txt_packets + squirrel_txt_packets + \
        deer_txt_packets + dog_txt_packets + \
        halloween_dns_packets

    random.shuffle(all_packets)

    wrpcap("txt_or_treat.pcap", all_packets)
    print("[+] Saved txt_or_treat.pcap")

if __name__ == "__main__":
    main()