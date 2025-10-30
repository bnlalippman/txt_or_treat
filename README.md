# TXT or Treat!

Welcome to "TXT or Treat"! This year for Halloween we're carving packets instead of pumpkins.

The objective of this lab is to find the ASCII art pumpkin in the network traffic.

# Getting Started

## Requirements
- Python 3.11+
- Wireshark
- Tshark

## Setup

1. Clone the repository:
```bash
git clone git@github.com:bnlalippman/txt_or_treat.git
```

2. Setup a virtual environment:
```bash
cd txt_or_treat
python -m venv .venv
source .venv/bin/activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Run this script to generate your PCAP!
```bash
python3 src/txt_or_treat.py
```

This will create a file called `txt_or_treat.pcap` in the current directory.

# How to Play

## Objective

1. Find the flag
2. Extract the pumpkin
```
                                      .,'
                                   .''.'
                                  .' .'
                      _.ood0Pp._ ,'  `.~ .q?00doo._
                  .od00Pd0000Pdb._. . _:db?000b?000bo.
                .?000Pd0000Pd0000PdbMb?0000b?000b?0000b.
              .d0000Pd0000Pd0000Pd0000b?0000b?000b?0000b.
              d0000Pd0000Pd00000Pd0000b?00000b?0000b?000b.
              00000Pd0000Pd0000Pd00000b?00000b?0000b?0000b
              ?0000b?0000b?0000b?00000Pd00000Pd0000Pd0000P
              ?0000b?0000b?0000b?00000Pd00000Pd0000Pd000P
              `?0000b?0000b?0000b?0000Pd0000Pd0000Pd000P'
                `?000b?0000b?000b?0000Pd000Pd0000Pd000P
                  `~?00b?000b?000b?000Pd00Pd000Pd00P'
                      `~?0b?0b?000b?0Pd0Pd000PdP~'
```

## Part 1: Find the flag

- The flag will be in the following format: `FLAG{i_am_a_flag_2025}`
- The flag will be 26 characters long (including the word FLAG and the brackets `{}`) 
- The flag may contain the following characters: `a-z0-9_{}`

> [!IMPORTANT]
> You will need to use the flag to "decrypt" the pumpkin ascii art in Part 2

## Part 2: Extract the pumpkin

Once you discover the packet containing the flag, you will need that to extract the pumpkin ascii art.

Extracting the pumpkin will require three steps:
1. Determine which field in the protocol contains the pumpkin data
2. Base64 decode that data
3. Use the flag to "decrypt" the data