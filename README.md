# TXT or Treat!

Welcome to "TXT or Treat"! This year for Halloween we're carving packets instead of pumpkins.

# Getting Started

## Requirements

To play the game, you'll need:
- Python >=3.11
- Wireshark
- Tshark

## Setup

1. Clone the repository:
```bash
git clone git@github.com:bnlalippman/txt_or_treat.git
```

2. Setup a virtual environment and install dependencies:
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
python3 txt_or_treat.py
```

# How to Play

## Objective

1. Find the flag
2. Extract the pumpkin
```
                  ___
               ___)__|_
          .-*'          '*-,
         /      /|   |\     \
        ;      /_|   |_\     ;
        ;   |\           /|  ;
        ;   | ''--...--'' |  ;
         \  ''---.....--''  /
          ''*-.,_______,.-*'  
```

## Part 1: Find the flag

- The flag will be in the following format: `FLAG{i_am_a_flag_2025}`
- The flag will be 20 characters long and may contain the following characters: `a-z`, `0-9`, and `_`
- You will need to use the FULL flag to finish the game

## Part 2: Extract the pumpkin

Once you discover the packet containing the flag, you will need that to extract the pumpkin ascii art.

Extracting the pumpkin will require three steps:
1. Determine which field contains the pumpkin data
2. Base64 decode the data
3. Use the flag to "decrypt" the data