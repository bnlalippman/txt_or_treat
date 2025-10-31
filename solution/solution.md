## Part 1: Find the flag

What is with that long hex encoded subdomain? 

Let's extract it in our terminal so we can work with the data. We can use `tshark` to do this:

```bash
tshark -r txt_or_treat.pcap -Y 'dns.qry.type == 1 && dns.qry.name contains "pumpkin.local"' -T fields -e dns.qry.name  | cut -d . -f 1 | xxd -r -p
```

That looks like our flag!

## Part 2: Extract the pumpkin

Now that we have the flag, we can move on to extracting the pumpkin ASCII art.

We notice one of the DNS TXT records contains a long base64 encoded string. Let's extract the data using `tshark`:
```bash
tshark -r txt_or_treat.pcap \
  -Y 'dns.flags.response == 1 && dns.qry.name == "big.pumpkin.local"' \
  -T fields -e dns.txt > data
```

The data looks like it's base64 encoded. However, there are some characters that do not belong in base64. Let's clean it up so we can decode it:
```bash
sed 's/[" ,]//g' data > data.b64
```

Let's decode the base64 data to see what we have:
```bash
base64 -D -i data.b64
```

What is this data? Let's do a hex dump to see if we can identify it:
```bash
base64 -D -i data.b64 | xxd
```

We notice that the data starts with `50 4b 03 04`, which indicates that it is pkzip format.
```bash
base64 -D -i data.b64 | xxd
00000000: 504b 0304 1400 0900 0800 f43e 5f5b 97dc  PK.........>_[..
00000010: 5874 6300 0000 bc00 0000 0b00 1c00 7075  Xtc...........pu
00000020: 6d70 6b69 6e2e 7478 7455 5409 0003 bca3  mpkin.txtUT.....
00000030: 0469 bca3 0469 7578 0b00 0104 f501 0000  .i...iux........
00000040: 0414 0000 0098 0df5 aec7 30e7 d773 1a1f  ..........0..s..
00000050: 191d 7c27 7a99 13db 5923 3a2b 672b 77e7  ..|'z...Y#:+g+w.
00000060: 6f83 c351 a54a b75f a26d c254 43f1 154c  o..Q.J._.m.TC..L
00000070: 7ff1 6c86 d4a3 5ecf 57c8 6649 c86f 093c  ..l...^.W.fI.o.<
00000080: 6457 7606 685c ca9a 8800 d280 fdd9 3bc2  dWv.h\........;.
00000090: 161f 69b7 78ef a4d2 aa65 2c0b 73f3 5c6d  ..i.x....e,.s.\m
000000a0: a041 93cd cf2c 441b 504b 0708 97dc 5874  .A...,D.PK....Xt
000000b0: 6300 0000 bc00 0000 504b 0102 1e03 1400  c.......PK......
000000c0: 0900 0800 f43e 5f5b 97dc 5874 6300 0000  .....>_[..Xtc...
000000d0: bc00 0000 0b00 1800 0000 0000 0100 0000  ................
000000e0: a481 0000 0000 7075 6d70 6b69 6e2e 7478  ......pumpkin.tx
000000f0: 7455 5405 0003 bca3 0469 7578 0b00 0104  tUT......iux....
00000100: f501 0000 0414 0000 0050 4b05 0600 0000  .........PK.....
00000110: 0001 0001 0051 0000 00b8 0000 0000 00    .....Q.........
```

We can extract the zip file using the flag we found earlier:
```bash
base64 -D -i data.b64 -o pumpkin.zip
unzip -P 'FLAG{halloween_2025}' pumpkin.zip
```

## Easter Egg

There are several animal ascii arts hidden in the pcap as well. Can you find them all?

To extract animal ascii arts, you can use the following command:
```bash
tshark -r txt_or_treat.pcap -Y 'dns.qry.name contains "pumpkin.local"' -T fields -e dns.txt | xargs -0 printf "%b\n"
```