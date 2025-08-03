#!/data/data/com.termux/files/usr/bin/bash

# ===============================
# Install Script for Wordlist-Zen
# by Khenzl
# ===============================

# Warna
G='\033[1;32m'
R='\033[1;31m'
W='\033[0m'

clear
echo -e "${G}[•] Memulai instalasi Wordlist-Zen...${W}"

echo -e "${G}[•] Update & Upgrade...${W}"
pkg update -y && pkg upgrade -y

echo -e "${G}[•] Menginstal dependencies Termux...${W}"
pkg install python -y
pkg install bash -y
termux-setup-storage

echo -e "${G}[•] Menginstal Python modules...${W}"
pip install -r requirements.txt

echo -e "${G}[✔] Instalasi selesai.${W}"
echo -e "${G}[✔] Jalankan tool dengan: ${W}python wordlist_zen.py"
