from src.packets import *
from src.art import *

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