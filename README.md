# Wordlist-Zen 🔐
Custom Wordlist Generator for Pentest by Khenzl

## 📌 Deskripsi
Wordlist-Zen adalah tool sederhana yang dibuat untuk membantu Anda menghasilkan file wordlist dengan kombinasi nama, angka, tanggal, dan karakter tambahan lainnya secara otomatis.

Tool ini sangat cocok digunakan oleh penetration tester, ethical hacker, atau siapa saja yang butuh wordlist custom dengan cepat di Termux.

---

## ✅ Fitur
- Membuat wordlist berdasarkan nama dan tanggal lahir
- Menambahkan kombinasi karakter khusus dan angka
- Simpan otomatis ke file `wordlist.txt`
- Ringan dan berjalan di Termux

---

## 🚀 Cara Instalasi

```
pkg update && pkg upgrade

pkg install git

termux-serup-storage

git clone https://github.com/Khenzl/Wordlist-Zen

cd Wordlist-Zen

chmod +x install.sh

bash install.sh

python wordlist_zen.py
