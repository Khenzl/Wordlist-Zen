import itertools
import sys
import os
import hashlib
import datetime
import signal
from collections import Counter
import statistics
from colorama import Fore, Style, init

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

init(autoreset=True)
os.makedirs("results", exist_ok=True)
output_file = "results/wordlist_generated.txt"

# CTRL+C Handler
def signal_handler(sig, frame):
    if in_process:
        print(f"\n{Fore.RED}[!] Proses dihentikan.{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}[ENTER]{Style.RESET_ALL} untuk kembali ke Menu Utama...")
        main()
    else:
        print(f"\n{Fore.RED}[!] Keluar dari aplikasi.{Style.RESET_ALL}")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

in_process = False

# Fungsi Hash
def hash_word(word, algorithm):
    import hashlib
    word = word.strip().encode('utf-8')
    if algorithm == "md5":
        return hashlib.md5(word).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(word).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(word).hexdigest()

# Identifikasi Hash
def identifikasi_hash(hash_str):
    if len(hash_str) == 32:
        return "MD5"
    elif len(hash_str) == 40:
        return "SHA1"
    elif len(hash_str) == 64:
        return "SHA256"
    return "UNKNOWN"

# Banner
banner = f"""{Fore.CYAN}
                                                 
▗▖ ▗▖ ▄▄▄   ▄▄▄ ▐▌▗▖   ▄  ▄▄▄   ■    ▗▄▄▄▄▖▗▞▀▚▖▄▄▄▄  
▐▌ ▐▌█   █ █    ▐▌▐▌   ▄ ▀▄▄ ▗▄▟▙▄▖     ▗▞▘▐▛▀▀▘█   █ 
▐▌ ▐▌▀▄▄▄▀ █ ▗▞▀▜▌▐▌   █ ▄▄▄▀  ▐▌     ▗▞▘  ▝▚▄▄▖█   █ 
▐▙█▟▌        ▝▚▄▟▌▐▙▄▄▖█       ▐▌ ▐▌ ▐▙▄▄▄▖           
      Khenzl | Sang Topi Hitam ▐▌ v.1.0 | 29 Juli 2025
                                                 {Style.RESET_ALL}"""
# Menu Utama
def menu():
    global in_process
    in_process = False
    clear_screen()
    print(banner)
    print(f"{Fore.GREEN} ================ Menu Wordlist-Zen =================\n")
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Membuat Wordlist Tertarget")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Kombinasi Brute Force (Angka/Huruf)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Gabungkan Wordlist.txt")
    print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Filter Wordlist Berdasarkan Panjang")
    print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} Hapus Duplikat")
    print(f"{Fore.YELLOW}[6]{Style.RESET_ALL} Enkripsi Wordlist (MD5/SHA1/SHA256)")
    print(f"{Fore.YELLOW}[7]{Style.RESET_ALL} Dekripsi Hash via Wordlist")
    print(f"{Fore.YELLOW}[8]{Style.RESET_ALL} Analisis Wordlist")
    print(f"{Fore.YELLOW}[9]{Style.RESET_ALL} Sortir Dan Unikkan Wordlist")
    print(f"{Fore.RED}[0] Keluar{Style.RESET_ALL}")
    return input(f"\n{Fore.CYAN}[?]{Style.RESET_ALL} Pilih menu: ").strip()

# Membuat Wordlist Tertarget
def gather_target_info():
    clear_screen()
    print(banner)
    print(f"\n{Fore.GREEN}Masukkan data target untuk membuat wordlist.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Tekan Ctrl+C untuk membatalkan Input.{Style.RESET_ALL}\n")


    name = input(f"{Fore.CYAN}Nama Lengkap:\n>> {Style.RESET_ALL}").strip()
    nickname = input(f"{Fore.CYAN}Nama Panggilan:\n>> {Style.RESET_ALL}").strip()
    birthdate = input(f"{Fore.CYAN}Tanggal Lahir (ddmmyyyy):\n>> {Style.RESET_ALL}").strip()
    birthplace = input(f"{Fore.CYAN}Tempat Lahir:\n>> {Style.RESET_ALL}").strip()
    address = input(f"{Fore.CYAN}Alamat:\n>> {Style.RESET_ALL}").strip()
    phone = input(f"{Fore.CYAN}Nomor HP:\n>> {Style.RESET_ALL}").strip()
    fav_word = input(f"{Fore.CYAN}Kata Favorit:\n>> {Style.RESET_ALL}").strip()
    pet_name = input(f"{Fore.CYAN}Nama Hewan Peliharaan:\n>> {Style.RESET_ALL}").strip()
    additional = input(f"{Fore.CYAN}Kata kunci tambahan (pisahkan dengan koma):\n>> {Style.RESET_ALL}").strip().split(",")

    base_words = [name, nickname, birthdate, birthplace, address, phone, fav_word, pet_name] + additional
    return list(set([w.lower() for w in base_words if w]))

def generate_targeted_wordlist():
    base_words = gather_target_info()

    try:
        min_len = int(input(f"\n{Fore.GREEN}Panjang minimal:\n>> {Style.RESET_ALL}"))
        max_len = int(input(f"{Fore.GREEN}Panjang maksimal:\n>> {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}[ERROR] Input panjang tidak valid.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Tekan Ctrl+C untuk membatalkan..{Style.RESET_ALL}\n")

    folder_name = "wordlist"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(folder_name, f"wordlist_{timestamp}.txt")

    print(f"{Fore.BLUE}[INFO] Membuat wordlist...{Style.RESET_ALL}")
    count = 0

    with open(output_file, "w") as f:
        for word in base_words:
            if min_len <= len(word) <= max_len:
                f.write(word + "\n")
                count += 1
            for word2 in base_words:
                for combo in [word + word2, word2 + word]:
                    if min_len <= len(combo) <= max_len:
                        f.write(combo + "\n")
                        count += 1

    print(f"\n{Fore.GREEN}[OK]{Style.RESET_ALL} Wordlist berhasil dibuat: {output_file} ({count} kata)\n")
    input(f"{Fore.CYAN}Tekan ENTER untuk kembali ke menu utama...{Style.RESET_ALL}")

# Generator Brute Force
def brute_force_generator():
    clear_screen()
    print(banner)
    global in_process
    os.makedirs("Wordlist_BF", exist_ok=True)

    print(f"\n{Fore.CYAN}========= Brute Force Wordlist Generator =========\n{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Wordlist Angka (mis. 0000-9999)")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Wordlist Huruf Kecil (a-z)")
    print(f"{Fore.YELLOW}[3]{Style.RESET_ALL} Wordlist Kombinasi Huruf + Angka (a-z, 0-9)")
    print(f"{Fore.YELLOW}[4]{Style.RESET_ALL} Wordlist Kombinasi Huruf + Angka + Simbol")
    print(f"{Fore.YELLOW}[5]{Style.RESET_ALL} Wordlist Kombinasi Huruf + Angka + Simbol + Awalan/Akhiran")
    print(f"{Fore.RED}[0] Kembali ke Menu Utama")

    pilihan = input(f"\n{Fore.CYAN}[?]{Style.RESET_ALL} Pilih jenis wordlist [default: 1]: ").strip() or "1"

    if pilihan == "0":
        return

    try:
        min_len = input(f"{Fore.CYAN}Panjang minimum:\n>> {Style.RESET_ALL}").strip()
        max_len = input(f"{Fore.CYAN}Panjang maksimum:\n>> {Style.RESET_ALL}").strip()
        min_len = int(min_len) if min_len else 1
        max_len = int(max_len) if max_len else 9
    except ValueError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Panjang harus berupa angka.")
        return

    if min_len > max_len or min_len <= 0:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Panjang minimum tidak boleh lebih dari maksimum dan harus > 0.")
        return

    charset = ""
    prefix = ""
    suffix = ""

    if pilihan == "1":
        charset = "0123456789"
    elif pilihan == "2":
        charset = "abcdefghijklmnopqrstuvwxyz"
    elif pilihan == "3":
        charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    elif pilihan == "4":
        charset = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
    elif pilihan == "5":
        charset = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
        prefix = input(f"\n{Fore.CYAN}[>] Masukkan awalan (prefix) [kosongkan jika tidak ada]: {Style.RESET_ALL}").strip()
        suffix = input(f"{Fore.CYAN}[>] Masukkan akhiran (suffix) [kosongkan jika tidak ada]: {Style.RESET_ALL}").strip()
    else:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Pilihan tidak tersedia.")
        return

    # Buat nama file unik
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"Wordlist_BF/bruteforce_{timestamp}.txt"
    count = 0

    print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Membuat kombinasi, mohon tunggu...")
    in_process = True

    try:
        with open(file_path, "w") as f:
            for length in range(min_len, max_len + 1):
                for combo in itertools.product(charset, repeat=length):
                    word = ''.join(combo)
                    if pilihan == "5":
                        word = f"{prefix}{word}{suffix}"
                    try:
                        f.write(word + "\n")
                        count += 1
                    except OSError as e:
                        if "No space left on device" in str(e):
                            print(f"\n{Fore.RED}[FATAL]{Style.RESET_ALL} Memory device full. Program dihentikan.")
                            sys.exit(1)
                        else:
                            raise
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[DIBATALKAN]{Style.RESET_ALL} Proses dihentikan oleh pengguna.")
        return

    in_process = False
    print(f"\n{Fore.GREEN}[OK]{Style.RESET_ALL} Wordlist selesai dibuat: {file_path}")
    print(f"{Fore.CYAN}Total kombinasi: {count} baris{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}[ENTER]{Style.RESET_ALL} untuk kembali ke menu...")

# Gabungkan Wordlist
def merge_wordlists():
    clear_screen()
    print(banner)
    print(f"{Fore.GREEN}Masukkan path file wordlist yang ingin digabungkan...")
    print(f"{Fore.YELLOW}Ketik 'done' jika sudah selesai memasukkan semua path.\n")

    file_paths = []
    while True:
        path = input(Fore.CYAN + "[>] Path file: " + Style.RESET_ALL).strip()
        if path.lower() == "done":
            break
        elif not os.path.exists(path):
            print(Fore.RED + "[!] File tidak ditemukan, coba lagi." + Style.RESET_ALL)
        else:
            file_paths.append(path)

    if len(file_paths) < 2:
        print(Fore.RED + "[!] Minimal 2 file untuk digabungkan." + Style.RESET_ALL)
        input(Fore.YELLOW + "[ENTER] untuk kembali..." + Style.RESET_ALL)
        return

    # Pastikan folder tujuan ada
    output_dir = "Wordlist_Gabungan"
    os.makedirs(output_dir, exist_ok=True)

    # Buat nama file otomatis
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_dir, f"hasil_merge_{timestamp}.txt")

    try:
        with open(output_file, "w") as outfile:
            for file in file_paths:
                with open(file, "r") as infile:
                    content = infile.read()
                    outfile.write(content)
                    if not content.endswith("\n"):
                        outfile.write("\n")

        print(Fore.GREEN + f"\n[✓] Wordlist berhasil digabung ke: {output_file}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal menggabungkan: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# Filter Wordlist Berdasarkan Panjang dan Pola
def filter_wordlist():
    clear_screen()
    print(banner)
    
    file_path = input(Fore.GREEN + "[>] Masukkan path file wordlist: " + Style.RESET_ALL).strip()
    if not os.path.exists(file_path):
        print(Fore.RED + "[!] File tidak ditemukan." + Style.RESET_ALL)
        input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
        return

    try:
        min_length = int(input(Fore.YELLOW + "[>] Panjang minimum kata (angka): " + Style.RESET_ALL))
        max_length = int(input(Fore.YELLOW + "[>] Panjang maksimum kata (angka): " + Style.RESET_ALL))
    except ValueError:
        print(Fore.RED + "[!] Input harus berupa angka!" + Style.RESET_ALL)
        input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
        return

    print(Fore.GREEN + "\nPilih Filter Tambahan:")
    print("[1] Hanya angka")
    print("[2] Hanya huruf")
    print("[3] Huruf dan angka (alphanumeric)")
    print("[4] Pola regex khusus")
    print(Fore.RED + "[0] Lewati filter tambahan\n" + Style.RESET_ALL)

    filter_choice = input(Fore.CYAN + "[>] Pilihan: " + Style.RESET_ALL).strip()

    regex_pattern = None
    if filter_choice == "1":
        regex_pattern = r"^\d+$"
    elif filter_choice == "2":
        regex_pattern = r"^[a-zA-Z]+$"
    elif filter_choice == "3":
        regex_pattern = r"^[a-zA-Z0-9]+$"
    elif filter_choice == "4":
        regex_pattern = input(Fore.YELLOW + "[>] Masukkan pola regex (cth: ^admin): " + Style.RESET_ALL).strip()
    elif filter_choice == "0":
        regex_pattern = None
    else:
        print(Fore.RED + "[!] Pilihan tidak valid." + Style.RESET_ALL)
        input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
        return

    # Pastikan folder output ada
    output_dir = "Wordlist_Pola"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_dir, f"hasil_filter_{timestamp}.txt")

    try:
        with open(file_path, "r") as infile:
            lines = infile.readlines()

        filtered = []
        for line in lines:
            word = line.strip()
            if min_length <= len(word) <= max_length:
                if regex_pattern:
                    if re.fullmatch(regex_pattern, word):
                        filtered.append(word)
                else:
                    filtered.append(word)

        with open(output_file, "w") as out:
            for word in filtered:
                out.write(word + "\n")

        print(Fore.GREEN + f"\n[✓] Total {len(filtered)} kata disimpan di: {output_file}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal memfilter: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# Hapus Duplikat Wordlist
def remove_duplicates():
    clear_screen()
    print(banner)
    path = input(Fore.GREEN + "[>] Masukkan path file wordlist: " + Style.RESET_ALL).strip()
    if not os.path.exists(path):
        print(Fore.RED + "[!] File tidak ditemukan!" + Style.RESET_ALL)
        input(Fore.YELLOW + "[ENTER] untuk kembali..." + Style.RESET_ALL)
        return

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()

        total = len(lines)
        unique_lines = sorted(set([line.strip() for line in lines if line.strip() != ""]))
        duplicates = total - len(unique_lines)

        print(Fore.YELLOW + f"\nTotal baris: {total}")
        print(f"Duplikat ditemukan: {duplicates}")
        print(f"Baris unik setelah diproses: {len(unique_lines)}" + Style.RESET_ALL)

        print(Fore.CYAN + "\n[1] Simpan sebagai file baru")
        print("[2] Timpa file asli")
        print(Fore.RED + "[0] Kembali\n" + Style.RESET_ALL)

        pilihan = input(Fore.YELLOW + "[?] Pilih opsi: " + Style.RESET_ALL)

        if pilihan == "1":
            nama_output = input(Fore.CYAN + "[>] Nama file output (cth: hasil_bersih.txt): " + Style.RESET_ALL).strip()
            if not nama_output.endswith(".txt"):
                nama_output += ".txt"
        elif pilihan == "2":
            nama_output = path
        elif pilihan == "0":
            return
        else:
            print(Fore.RED + "[!] Opsi tidak valid!" + Style.RESET_ALL)
            input(Fore.YELLOW + "[ENTER] untuk kembali..." + Style.RESET_ALL)
            return

        with open(nama_output, 'w', encoding='utf-8') as out:
            for line in unique_lines:
                out.write(line + "\n")

        print(Fore.GREEN + f"\n[✓] Duplikat berhasil dihapus. File disimpan sebagai: {nama_output}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[ERROR] Terjadi kesalahan: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# Enkripsi Wordlist
def hash_word(word, algo):
    if algo == "md5":
        return hashlib.md5(word.encode()).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(word.encode()).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(word.encode()).hexdigest()
    else:
        return None

def encrypt_wordlist():
    clear_screen()
    print(banner)
    print(Fore.GREEN + "\n========== Enkripsi (MD5 / SHA1 / SHA256) ===========\n" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Pilih sumber data:")
    print(" [1] Enkripsi dari file wordlist")
    print(" [2] Enkripsi dari input manual")
    print(Fore.RED + " [0] Kembali" + Style.RESET_ALL)

    mode = input(Fore.CYAN + "\n[>] Pilihan Anda: " + Style.RESET_ALL).strip()
    if mode == "0":
        return

    if mode not in ["1", "2"]:
        print(Fore.RED + "[!] Pilihan tidak valid!" + Style.RESET_ALL)
        input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + "\nPilih Algoritma Enkripsi:")
    print(" [1] MD5")
    print(" [2] SHA1")
    print(" [3] SHA256")
    print(Fore.RED + " [0] Kembali" + Style.RESET_ALL)

    algo = input(Fore.CYAN + "[>] Pilihan Anda: " + Style.RESET_ALL).strip()
    if algo == "0":
        return

    if algo not in ["1", "2", "3"]:
        print(Fore.RED + "[!] Pilihan tidak valid!" + Style.RESET_ALL)
        input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
        return

    algo_dict = {"1": "md5", "2": "sha1", "3": "sha256"}
    algo_name = algo_dict[algo]

    # Siapkan folder dan file output
    output_dir = "Enkripsi_Wordlist"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_dir, f"hasil_enkripsi_{algo_name}_{timestamp}.txt")

    lines = []

    if mode == "1":
        path = input(Fore.YELLOW + "[>] Masukkan path file wordlist: " + Style.RESET_ALL).strip()
        if not os.path.exists(path):
            print(Fore.RED + "[!] File tidak ditemukan." + Style.RESET_ALL)
            input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
            return
        try:
            with open(path, "r", encoding='utf-8', errors='ignore') as infile:
                lines = infile.read().splitlines()
        except Exception as e:
            print(Fore.RED + f"[ERROR] Gagal membaca file: {e}" + Style.RESET_ALL)
            return
    else:
        print(Fore.YELLOW + "\nMasukkan teks yang ingin dienkripsi.")
        print("Ketik 'done' jika sudah selesai.\n")
        while True:
            teks = input(Fore.CYAN + "[>] Teks: " + Style.RESET_ALL).strip()
            if teks.lower() == "done":
                break
            elif teks == "":
                continue
            lines.append(teks)

    if not lines:
        print(Fore.RED + "[!] Tidak ada data untuk dienkripsi." + Style.RESET_ALL)
        input(Fore.RED + "\n[0] Kembali..." + Style.RESET_ALL)
        return

    try:
        with open(output_file, "w") as outfile:
            for line in lines:
                hashed = hash_word(line, algo_name)
                outfile.write(f"{hashed}\n")

        print(Fore.GREEN + f"\n[✓] Data berhasil dienkripsi ke file: {output_file}" + Style.RESET_ALL)

        preview = input(Fore.CYAN + "[?] Tampilkan 10 baris pertama hasil enkripsi? (y/n): " + Style.RESET_ALL).strip().lower()
        if preview == 'y':
            with open(output_file, "r") as f:
                print(Fore.YELLOW + "\n--- Pratinjau Hasil ---")
                for i, line in enumerate(f):
                    print(Fore.GREEN + f"{i+1:02d}. {line.strip()}")
                    if i == 9:
                        break

        print(Fore.CYAN + f"\n[INFO] Hasil enkripsi disimpan otomatis di folder: {output_dir}/" + Style.RESET_ALL)
        print(Fore.GREEN + f"[✓] Nama File: {os.path.basename(output_file)}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[ERROR] Gagal mengenkripsi: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# Dekripsi Wordlist (Via Api/Lokal)
def identifikasi_hash(hash_str):
    length = len(hash_str)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    else:
        return "UNKNOWN"

def dekripsi_lokal(hash_target, jenis_hash, wordlist_path):
    print(Fore.YELLOW + "[*] Mencoba dekripsi lokal via wordlist...")
    try:
        with open(wordlist_path, "r", errors="ignore") as file:
            for kata in file:
                kata = kata.strip()
                if jenis_hash == "MD5":
                    hasil = hashlib.md5(kata.encode()).hexdigest()
                elif jenis_hash == "SHA1":
                    hasil = hashlib.sha1(kata.encode()).hexdigest()
                elif jenis_hash == "SHA256":
                    hasil = hashlib.sha256(kata.encode()).hexdigest()
                else:
                    continue

                if hasil == hash_target:
                    print(Fore.GREEN + f"[✓] Berhasil didekripsi: {hash_target} = {kata}")
                    return kata
    except Exception as e:
        print(Fore.RED + f"[!] Gagal membaca wordlist: {e}")
    print(Fore.RED + "[X] Tidak ditemukan di wordlist.")
    return None

def dekripsi_api(hash_target):
    print(Fore.YELLOW + "[*] Mencoba dekripsi via API...")
    try:
        url = f"https://api.hashlookup.dev/{hash_target}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            if data.get("plain"):
                print(Fore.GREEN + f"[✓] Ditemukan via API: {hash_target} = {data['plain']}")
                return data['plain']
            else:
                print(Fore.RED + "[X] Tidak ditemukan via API.")
        else:
            print(Fore.RED + f"[!] Error API: {r.status_code}")
    except Exception as e:
        print(Fore.RED + f"[!] Error koneksi API: {e}")
    return None

def dekripsi_wordlist_tool():
    clear_screen()
    print(banner)
    print(Fore.GREEN + "\n========== Dekripsi Wordlist ===========\n" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Pilih Jenis Hash:")
    print("[1] Input hash manual")
    print("[2] Input file berisi daftar hash")
    print(Fore.RED + "[0] Kembali\n" + Style.RESET_ALL)

    opsi = input(Fore.CYAN + "[>] Pilih opsi: " + Style.RESET_ALL).strip()

    hasil_dekripsi = []

    if opsi == "1":
        hash_target = input("Masukkan hash: ").strip()
        jenis = identifikasi_hash(hash_target)
        print(Fore.BLUE + f"[~] Terdeteksi tipe hash: {jenis}")

        if jenis == "UNKNOWN":
            print(Fore.RED + "[!] Tipe hash tidak dikenali.")
            return

        metode = input("[1] Dekripsi Lokal\n[2] Dekripsi via API\n[>] Pilih metode: ").strip()
        if metode == "1":
            path = input("Masukkan path wordlist: ").strip()
            hasil = dekripsi_lokal(hash_target, jenis, path)
        elif metode == "2":
            hasil = dekripsi_api(hash_target)
        else:
            print(Fore.RED + "[!] Metode tidak valid.")
            return

        if hasil:
            hasil_dekripsi.append(f"{hash_target} = {hasil}")

    elif opsi == "2":
        file_hash = input("Path file daftar hash: ").strip()
        if not os.path.exists(file_hash):
            print(Fore.RED + "[!] File tidak ditemukan.")
            return
        wordlist_path = input("Masukkan path wordlist lokal: ").strip()

        with open(file_hash, "r", errors="ignore") as file:
            for line in file:
                hash_target = line.strip()
                jenis = identifikasi_hash(hash_target)
                print(Fore.BLUE + f"[~] {hash_target} | Deteksi: {jenis}")
                hasil = dekripsi_lokal(hash_target, jenis, wordlist_path)
                if not hasil:
                    hasil = dekripsi_api(hash_target)
                if hasil:
                    hasil_dekripsi.append(f"{hash_target} = {hasil}")

    elif opsi == "0":
        return
    else:
        print(Fore.RED + "[!] Pilihan tidak valid.")
        return

    if hasil_dekripsi:
        output_dir = "Hasil_Dekripsi"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join(output_dir, f"hasil_dekripsi_{timestamp}.txt")

        with open(output_file, "w") as out:
            out.write("\n".join(hasil_dekripsi))

        print(Fore.GREEN + f"\n[✓] Semua hasil dekripsi disimpan ke: {output_file}")
    else:
        print(Fore.RED + "\n[X] Tidak ada hash yang berhasil didekripsi.")

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# Analisis Wordlist
def analyze_wordlist():
    clear_screen()
    print(banner)
    print(Fore.GREEN + "[!] Masukan File Wordlist yang akan di Analisis." + Style.RESET_ALL)
    path = input(Fore.YELLOW + "[?] Masukkan path file wordlist: " + Style.RESET_ALL).strip()

    if not os.path.isfile(path):
        print(Fore.RED + "[!] File tidak ditemukan!" + Style.RESET_ALL)
        input(Fore.YELLOW + "[ENTER] untuk kembali..." + Style.RESET_ALL)
        return

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            print(Fore.RED + "[!] File kosong atau tidak valid." + Style.RESET_ALL)
            return

        total_kata = len(lines)
        unik_kata = len(set(lines))
        panjang_kata = [len(kata) for kata in lines]

        min_len = min(panjang_kata)
        max_len = max(panjang_kata)
        avg_len = round(statistics.mean(panjang_kata), 2)

        kata_terpendek = [kata for kata in lines if len(kata) == min_len]
        kata_terpanjang = [kata for kata in lines if len(kata) == max_len]

        freq_counter = Counter(lines)
        top10 = freq_counter.most_common(10)

        panjang_counter = Counter(panjang_kata)

        # Deteksi karakteristik kata
        huruf = sum(1 for kata in lines if kata.isalpha())
        angka = sum(1 for kata in lines if kata.isdigit())
        campuran = sum(1 for kata in lines if kata.isalnum() and not (kata.isalpha() or kata.isdigit()))
        simbol = sum(1 for kata in lines if not kata.isalnum())

        print(Fore.GREEN + "\n[✓] Statistik Wordlist:")
        print(Fore.CYAN + f"  • Total kata           : {total_kata}")
        print(f"  • Kata unik            : {unik_kata}")
        print(f"  • Panjang min/max      : {min_len} / {max_len}")
        print(f"  • Rata-rata panjang    : {avg_len}")
        print(f"  • Kata terpendek       : {kata_terpendek[:3]}{'...' if len(kata_terpendek) > 3 else ''}")
        print(f"  • Kata terpanjang      : {kata_terpanjang[:3]}{'...' if len(kata_terpanjang) > 3 else ''}")

        print(Fore.MAGENTA + "\n[Top 10 Kata Paling Sering Muncul]:")
        for kata, jumlah in top10:
            print(f"  - {kata} : {jumlah}x")

        print(Fore.YELLOW + "\n[Pola Umum Panjang Kata]:")
        for panjang, jumlah in sorted(panjang_counter.items()):
            print(f"  - Panjang {panjang}: {jumlah} kata")

        print(Fore.BLUE + "\n[Karakteristik Kata]:")
        print(f"  • Huruf saja           : {huruf}")
        print(f"  • Angka saja           : {angka}")
        print(f"  • Kombinasi huruf/angka: {campuran}")
        print(f"  • Mengandung simbol    : {simbol}")

    except Exception as e:
        print(Fore.RED + f"[!] Kesalahan saat analisis: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# Sortir Unik Wordlist
def sort_and_unique_wordlist():
    clear_screen()
    print(banner)
    print(Fore.GREEN + "\n=== Sortir & Unikkan Wordlist ===" + Style.RESET_ALL)
    wordlist_path = input(Fore.YELLOW + "[?] Masukkan path file wordlist: " + Style.RESET_ALL).strip()

    if not os.path.isfile(wordlist_path):
        print(Fore.RED + "[!] File tidak ditemukan!" + Style.RESET_ALL)
        return

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()

        cleaned = list(set([line.strip() for line in lines if line.strip() != ""]))

        print(Fore.CYAN + "\n[1] Sortir A–Z")
        print("[2] Sortir Z–A")
        print("[3] Sortir berdasarkan panjang")
        print("[4] Sortir & filter hanya karakter alfanumerik" + Style.RESET_ALL)

        pilihan = input(Fore.YELLOW + "\nPilih metode sortir [1-4]: " + Style.RESET_ALL).strip()

        if pilihan == "1":
            cleaned.sort()
        elif pilihan == "2":
            cleaned.sort(reverse=True)
        elif pilihan == "3":
            cleaned.sort(key=len)
        elif pilihan == "4":
            cleaned = ["".join(filter(str.isalnum, line)) for line in cleaned if line]
            cleaned = sorted(set(cleaned))
        else:
            print(Fore.RED + "[!] Pilihan tidak valid." + Style.RESET_ALL)
            return

        output_dir = "sorted_wordlists"
        os.makedirs(output_dir, exist_ok=True)

        output_name = input(Fore.CYAN + "\nNama file output (cth: unik1.txt): " + Style.RESET_ALL).strip()
        if not output_name.endswith(".txt"):
            output_name += ".txt"

        base_name = os.path.splitext(output_name)[0]
        ext = os.path.splitext(output_name)[1]
        output_path = os.path.join(output_dir, output_name)
        counter = 1

        while os.path.exists(output_path):
            output_name = f"{base_name}_{counter}{ext}"
            output_path = os.path.join(output_dir, output_name)
            counter += 1

        with open(output_path, "w") as outfile:
            for word in cleaned:
                outfile.write(word + "\n")

        print(Fore.GREEN + f"\n[✓] Wordlist berhasil disimpan ke: {output_path}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[ERROR] Terjadi kesalahan: {e}" + Style.RESET_ALL)

    input(Fore.YELLOW + "\n[ENTER] untuk kembali ke menu..." + Style.RESET_ALL)

# ==== Fungsi Utama ====
def main():
    while True:
        try:
            choice = menu()
            if choice == "1":
                generate_targeted_wordlist()
            elif choice == "2":
                brute_force_generator()
            elif choice == "3":
                merge_wordlists()
            elif choice == "4":
                filter_wordlist()
            elif choice == "5":
                remove_duplicates()
            elif choice == "6":
                encrypt_wordlist()
            elif choice == "7":
                dekripsi_wordlist_tool()
            elif choice == "8":
                analyze_wordlist()
            elif choice == "9":
                sort_and_unique_wordlist()
                input(f"{Fore.YELLOW}[ENTER]{Style.RESET_ALL} untuk kembali...")
            elif choice == "0":
                print(f"{Fore.RED}[!] Keluar dari Wordlist-Zen.{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}[ERROR] Pilihan tidak valid!{Style.RESET_ALL}")
        except KeyboardInterrupt:
            signal_handler(None, None)

if __name__ == "__main__":
    main()
