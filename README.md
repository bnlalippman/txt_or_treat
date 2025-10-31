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
python3 txt_or_treat.py
```

This will create a file called `txt_or_treat.pcap` in the current directory.

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

> [!IMPORTANT]
> You will need to use the flag to "decrypt" the pumpkin ascii art in Part 2

## Part 2: Extract the pumpkin

Once you discover the packet containing the flag, you will need that to extract the pumpkin ascii art.

Extracting the pumpkin will require three steps:
1. Extract the data
2. Clean up the data
3. Determine the file type of the data
4. Use the flag to extract the pumpkin ascii art