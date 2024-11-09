import csv
import os
import pwinput
from datetime import datetime, timedelta
from prettytable import PrettyTable

tiket_file = "tiket.csv"
user_file = "user.csv"
seat_file = "seat.csv"

def csv_tiket():
    if not os.path.exists(tiket_file) or os.stat(tiket_file).st_size == 0:
        with open(tiket_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Maskapai Penerbangan", "Tanggal Keberangkatan", "Kota Asal", "Kota Tujuan", "first class", "business class", "economy class", "Gate", "Estimasi Penerbangan"]) 
        menambah_tiket()

def seat_csv():
    if not os.path.exists(seat_file) or os.stat(tiket_file).st_size == 0:
        with open(seat_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Seat", "ID", "Class", "Available" ]) 

def initialize_csv():
    if not os.path.exists(user_file) or os.stat(user_file).st_size == 0:
        with open(user_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['nama', 'password', 'pin', 'saldo', 'role'])
        menambah_user() 

# -------------------------------------------------------
# MENAMBAHKAN AKUN SAMPEL
# -------------------------------------------------------
def menambah_user():
    accounts = [["user1", "password123", "123456", 100000, "user"],
                ["admin", "adminpass", "654321", 500000, "admin"]]
    with open(seat_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(accounts)  

def seat_user():
    accounts = []
    with open(seat_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(accounts)  

def menambah_tiket():
    accounts = []
    with open(user_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(accounts) 

# -------------------------------------------------------
# MENAMBAHKAN AKUN BARU (REGISTRASI)
# -------------------------------------------------------
def akun_telah_ada(nama):
    try:
        with open(user_file, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if row[0] == nama:
                    return True
        return False
    except Exception as e :
        return False

def registrasi():
    print("\n======================== Registrasi ========================")

    while True:
        try:
            nama = input("                       Masukkan Nama: ")
            if not nama:
                print("         Masukan Nama Yang benar. Silakan coba lagi.")
                continue
                
            if akun_telah_ada(nama):
                print("          Registrasi gagal! Nama sudah terdaftar.")
                return
            password = pwinput.pwinput("                    Masukkan Password: ")
            if not password or not password.isalnum():
                print("      Password tidak boleh kosong. Silakan coba lagi.")
                continue
                
            while True:
                pin = pwinput.pwinput("                  Atur PIN (6 digit angka): ")
                if pin.isdigit() and len(pin) == 6:
                    break
                else:
                    print("  PIN harus terdiri dari 6 digit angka. Silakan coba lagi.")
                
            saldo = 0 
            role = "customer"

            # Simpan data ke CSV
            with open(user_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nama, password, pin, saldo, role])
            
            print("                    Registrasi berhasil!")
            break

        except ValueError as e :
            print(f"  Terjadi kesalahan pada input: {e}. Silakan coba lagi.")
        
        except Exception as e :
            print(f" Terjadi kesalahan tidak terduga: {e}. Silahkan coba lagi")
1
# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------

def login():
    print("\n=========================== Login ==========================")
    try :
        nama = input("                       Masukkan nama: ")
        password = pwinput.pwinput("                    Masukkan password: ")

        with open(user_file, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader) 
            for row in csv_reader:
                if row[0] == nama and row[1] == password:
                    print(f"    Login berhasil! Selamat datang, {row[4]} {nama}!!!    ")
                    return nama, row[4], row[2]  
        print("                 Nama atau password salah.")
        return None, None, None
    
    except (ValueError, TypeError) as e :
        print(f"  Terjadi kesalahan pada input: {e}. Silakan coba lagi.")
        return None, None, None

    except Exception as e :
        print(f"                    Akun Tidak Ditemukan.")
        return None, None, None
    
    except KeyboardInterrupt:
        print("\n                Proses login dibatalkan.")

def tambah_kursi(id_penerbangan):
    try:
        jumlah_first_class = 5
        jumlah_business_class = 10
        jumlah_economy_class = 20

        with open(seat_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            for i in range(1, jumlah_first_class + 1):
                seat_id = f"{id_penerbangan}-FC{i}"
                writer.writerow([seat_id, id_penerbangan, "First Class", "Available"])

            for i in range(1, jumlah_business_class + 1):
                seat_id = f"{id_penerbangan}-BC{i}"
                writer.writerow([seat_id, id_penerbangan, "Business Class", "Available"])

            for i in range(1, jumlah_economy_class + 1):
                seat_id = f"{id_penerbangan}-EC{i}"
                writer.writerow([seat_id, id_penerbangan, "Economy Class", "Available"])

        print(f"Tempat duduk untuk penerbangan {id_penerbangan} berhasil ditambahkan.")
    
    except Exception as e:
        print(f"        Terjadi kesalahan saat menambah kursi: {e}")

# -------------------------------------------------------
# CREATE (MENAMBAHKAN TIKET)
# -------------------------------------------------------

def tambah_tiket():
    try:
        while True:
            konfirmasi = input("Apakah Anda yakin ingin menambahkan tiket baru? (YA untuk lanjut, X untuk keluar): ").strip().upper()

            if konfirmasi == "X":
                print("           Keluar dari proses penambahan tiket.")
                return
            
            if konfirmasi != "YA":
                print("Pilihan tidak valid. Silakan pilih 'Y' untuk melanjutkan atau 'X' untuk keluar.")
                continue

            existing_ids = set()
            if os.path.exists(tiket_file) and os.stat(tiket_file).st_size > 0:
                with open(tiket_file, mode='r', newline='') as file:
                    csv_reader = csv.reader(file)
                    header = next(csv_reader, None)  
                    for row in csv_reader:
                        if row:  
                            existing_ids.add(row[0])


            while True:
                ID = input("           Masukkan ID yang ingin ditambahkan: ")
                if not ID.isdigit():
                    print("         ID harus berupa angka! Silakan coba lagi.")
                elif ID in existing_ids:
                    print("        ID sudah ada! Silakan masukkan ID yang unik.")
                else:
                    break
            maskapai_penerbangan = input("             Masukkan Maskapai penerbangan: ").strip()
            while not maskapai_penerbangan:
                print("         Maskapai penerbangan tidak boleh kosong!")
                maskapai_penerbangan = input("              Masukkan Maskapai penerbangan: ").strip()

            while True:
                custom_timestamp = input("     Masukkan tanggal dan jam (YYYY-MM-DD HH:MM:SS): ")
                try:
                    custom_datetime = datetime.strptime(custom_timestamp, '%Y-%m-%d %H:%M:%S')
                    if custom_datetime < datetime.now():
                        print("Tanggal dan waktu tidak boleh di masa lalu! Silakan coba lagi.")
                    else:
                        break
                except ValueError:
                    print("Format waktu tidak valid! Gunakan format YYYY-MM-DD HH:MM:SS.")
            kota_asal = input("                   Masukkan kota asal: ").strip()
            while not kota_asal:
                print("                Kota asal tidak boleh kosong!")
                kota_asal = input("                   Masukkan kota asal: ").strip()
            kota_tujuan = input("                   Masukkan kota tujuan: ").strip()
            while not kota_tujuan:
                print("              Kota tujuan tidak boleh kosong!")
                kota_tujuan = input("                    Masukkan kota tujuan: ").strip()

            while True:
                try:
                    first_class = float(input("             Masukkan harga tiket First class: ").strip())
                    if first_class <= 0:
                        print("           Harga tiket harus lebih besar dari 0!")
                        continue
                    break
                except ValueError:
                    print("           Harga tiket harus berupa angka valid!")

            while True:
                try:
                    business_class = float(input("           Masukkan harga tiket Business Class: ").strip())
                    if business_class <= 0:
                        print("           Harga tiket harus lebih besar dari 0!")
                        continue
                    break
                except ValueError:
                    print("          Harga tiket harus berupa angka valid!")
            
            while True:
                try:
                    economy_class = float(input("            Masukkan harga tiket Economy Class: ").strip())
                    if economy_class <= 0:
                        print("           Harga tiket harus lebih besar dari 0!")
                        continue
                    break
                except ValueError:
                    print("          Harga tiket harus berupa angka valid!")

            gate_tiket = input("                 Masukkan gate penerbangan: ").strip()
            while not gate_tiket:
                print("            Gate penerbangan tidak boleh kosong!")
                gate_tiket = input("                 Masukkan gate penerbangan: ").strip()

            while True:
                estimasi_durasi = input("     Masukkan estimasi durasi perjalanan (jam:menit): ")
                try:
                    jam, menit = map(int, estimasi_durasi.split(":"))
                    if jam < 0 or menit < 0 or menit >= 60:
                        raise ValueError
                    durasi_perjalanan = timedelta(hours=jam, minutes=menit)
                    waktu_kedatangan = custom_datetime + durasi_perjalanan
                    break
                except (ValueError, TypeError):
                    print("Format durasi tidak valid! Pastikan format adalah jam:menit dan menit tidak lebih dari 59.")

            print(f"               Estimasi waktu kedatangan: {waktu_kedatangan}")

            with open(tiket_file, 'a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([ID, maskapai_penerbangan, custom_datetime.strftime('%Y-%m-%d %H:%M:%S'), kota_asal, kota_tujuan, first_class, business_class, economy_class, gate_tiket, waktu_kedatangan.strftime('%Y-%m-%d %H:%M:%S')])
                print("                Tiket berhasil ditambahkan.")

            tambah_kursi(ID)
            break

    except KeyboardInterrupt:
        print("\n            Proses penambahan tiket dibatalkan.")
        return

# -------------------------------------------------------
# READ (MELIHAT TIKET)
# -------------------------------------------------------

def lihat_tiket():
    table = PrettyTable()
    table.field_names = ["ID", "Maskapai Penerbangan", "Tanggal Keberangkatan", "Kota Asal", "Kota Tujuan", "Harga First Class","Harga Business Class", "Harga Economy Class", "Gate", "Estimasi Penerbangan"]

    try:
        with open(tiket_file, mode='r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader, None)  
            for row in csv_reader:
                if len(row) < 10:
                    row += [''] * (10 - len(row))  
                elif len(row) > 10:
                    row = row[:10]  
                table.add_row(row)
        print(table)

    except FileNotFoundError:
        print(f"          File '{tiket_file}' tidak ditemukan.")
    except Exception as e:
        print(f"                 Terjadi kesalahan: {e}")

# -------------------------------------------------------
# UPDATE (MENGUPDATE TIKET)
# -------------------------------------------------------

def update_tiket():
    try:
        while True:
            lihat_tiket()
            konfirmasi = input("Apakah Anda yakin ingin memperbarui tiket? (YA untuk lanjut, X untuk keluar): ").strip().upper()

            
            if konfirmasi == "X":
                print("            Keluar dari proses pembaruan tiket.")
                return
            
            
            if konfirmasi != "YA":
                print("Pilihan tidak valid. Silakan pilih 'Y' untuk melanjutkan atau 'X' untuk keluar.")
                continue

            lihat_tiket()
            while True:
                ID = input("          Masukkan ID tiket yang ingin diperbarui: ").strip()
                if not ID.isdigit():
                    print("         ID harus berupa angka! Silakan coba lagi.")
                    continue

                update_rows = []
                found = False
                with open(tiket_file, mode='r') as file:
                    csv_reader = csv.reader(file)
                    headers = next(csv_reader)
                    for row in csv_reader:
                        if row[0] == ID:
                            found = True
                            print(f"Tiket dengan ID {ID} ditemukan. Silakan masukkan data baru.")

                            maskapai_penerbangan1 = input("            Masukkan Maskapai penerbangan baru: ").strip()
                            while True:
                                                    
                                custom_timestamp = input("Masukkan tanggal dan jam keberangkatan baru (YYYY-MM-DD HH:MM:SS): ")
                                try:
                                    custom_datetime = datetime.strptime(custom_timestamp, '%Y-%m-%d %H:%M:%S')
                                    if custom_datetime < datetime.now():

                                        print("Tanggal dan waktu tidak boleh di masa lalu! Silakan coba lagi.")
                                        continue
                                    break
                                except ValueError:
                                    
                                    print("Format waktu tidak valid! Gunakan format YYYY-MM-DD HH:MM:SS.")
                                        
                            kota_asal = input("                 Masukkan kota asal baru: ").strip()
                            kota_tujuan = input("              Masukkan kota tujuan baru: ").strip()
                            while True:
                                try:

                                    first_class = float(input("                Masukkan harga tiket First class baru: ").strip())
                                    if first_class <= 0:
                                        print("           Harga tiket harus lebih besar dari 0!")
                                        continue
                                    break
                                except ValueError:

                                    print("          Harga tiket harus berupa angka valid!")

                            while True:
                                try:                       
                                    business_class = float(input("             Masukkan harga tiket Business class baru: ").strip())
                                    if business_class <= 0:
                                        print("           Harga tiket harus lebih besar dari 0!")
                                        continue
                                    break
                                except ValueError:
                                    print("           Harga tiket harus berupa angka valid!")
                            
                            while True:
                                try:    
                                    economy_class = float(input("               Masukkan harga tiket Economy class baru: ").strip())
                                    if economy_class <= 0:
                                        print("           Harga tiket harus lebih besar dari 0!")
                                        continue
                                    break
                                except ValueError:
                                    print("           Harga tiket harus berupa angka valid!")

                            gate_tiket = input("               Masukkan gate penerbangan: ").strip()

                            while True:
                                estimasi_durasi = input("       Masukkan estimasi durasi perjalanan (jam:menit): ")
                                try:
                                    jam, menit = map(int, estimasi_durasi.split(":"))
                                    if jam < 0 or menit < 0 or menit >= 60:
                                        raise ValueError

                                    durasi_perjalanan = timedelta(hours=jam, minutes=menit)
                                    waktu_kedatangan = custom_datetime + durasi_perjalanan
                                    break
                                except (ValueError, TypeError):
                                    print("Format durasi tidak valid! Pastikan format adalah jam:menit dan menit tidak lebih dari 59.")
                            print(f"             Estimasi waktu kedatangan: {waktu_kedatangan}")

                            row = [ID, maskapai_penerbangan1, custom_datetime.strftime('%Y-%m-%d %H:%M:%S'), kota_asal, kota_tujuan, first_class, business_class, economy_class, gate_tiket, waktu_kedatangan.strftime('%Y-%m-%d %H:%M:%S')]
                        
                        update_rows.append(row)

                if found:
                    with open(tiket_file, mode='w', newline='') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerow(headers) 
                        csv_writer.writerows(update_rows)
                        print(f"            Tiket dengan ID {ID} berhasil diperbarui.")
                    break 
                else:
                    print(f"Tidak ada tiket dengan ID {ID} yang ditemukan. Silakan coba lagi.")
                    
            break
            
    except KeyboardInterrupt:
        print("\n            Proses pembaruan tiket dibatalkan.")

# -------------------------------------------------------
# DELETE (MENGHAPUS TIKET)
# -------------------------------------------------------

def hapus_tiket():
    try:
        while True:

            konfirmasi = input("Apakah Anda yakin ingin menghapus tiket? (YA untuk lanjut, X untuk keluar): ").strip().upper()
            if konfirmasi == "X":
                print("          Keluar dari proses penghapusan tiket.")
                return

            if konfirmasi != "YA":
                print("Pilihan tidak valid. Silakan pilih 'YA' untuk melanjutkan atau 'X' untuk keluar.")
                continue
            ID = input("         Masukkan ID tiket yang ingin dihapus: ").strip()
            if not ID:
                print(" ID tiket tidak boleh kosong. Silakan masukkan ID yang valid.")
                continue

            update_rows = []
            found = False

            with open(tiket_file, mode='r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) == 0:
                        continue  
                    if row[0] == ID:
                        found = True
                        print(f"          Tiket dengan ID {ID} berhasil dihapus.")
                    else:
                        update_rows.append(row)

            if not found:
                print(f"      Tidak ada tiket dengan ID {ID} yang ditemukan.")
            else:

                with open(tiket_file, mode='w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(update_rows)

    except ValueError as ve:
        print(f"                  Terjadi kesalahan nilai: {ve}")
    except FileNotFoundError:
        print("File tiket.csv tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    except KeyboardInterrupt:
        print("\n      Proses penghapusan tiket dibatalkan oleh pengguna.")
    except Exception as e:
        print(f"                     Terjadi kesalahan: {e}")

# -------------------------------------------------------
# MENU ADMIN
# -------------------------------------------------------

def menu_admin():
    try:
        while True:
            print("\n======================== Menu Admin ========================")
            print("|                     1. Tambah Tiket                      |")
            print("|                     2. Lihat Tiket                       |")
            print("|                     3. Hapus Tiket                       |")
            print("|                     4. Update Tiket                      |")
            print("|                     5. Keluar                            |")
            print("============================================================")
            choice = input("                      Pilih menu (1-5): ")
            if choice == '1':
                tambah_tiket()
            elif choice == '2':
                lihat_tiket()
            elif choice == '3':
                hapus_tiket()
            elif choice == '4':
                update_tiket()
            elif choice == '5':
                print("                   Sampai Jumpa Lagi Admin👋😆")
                main()  
                break
            else:
                print("        Pilihan tidak valid, silahkan coba lagi >-<")
                
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna. Terima kasih telah menggunakan menu admin!")

# -------------------------------------------------------
# BELI TIKET
# -------------------------------------------------------

def pilih_kursi(id_penerbangan, kelas_kursi):
    available_seats = []
    with open(seat_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == id_penerbangan and row[2] == kelas_kursi and row[3] == "Available":
                available_seats.append(row)
    if not available_seats:
        print(f"Tidak ada kursi tersedia di kelas {kelas_kursi} untuk penerbangan ini.")
        return None
    print("                   Kursi yang tersedia:")
    for idx, seat in enumerate(available_seats, start=1):
        print(f"{idx}. {seat[0]}")

    while True:
        try:
            pilihan = int(input("            Pilih nomor kursi yang diinginkan: "))
            if 1 <= pilihan <= len(available_seats):
                return available_seats[pilihan - 1]
            else:
                print("             Nomor kursi tidak valid. Coba lagi.")
        except ValueError:
            print("          Input tidak valid. Masukkan nomor kursi.")

def update_saldo(username, harga_tiket):
    users = []
    with open(user_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append(row)

    for user in users:
        if user[0] == username:
            saldo = float(user[3])
            if saldo >= harga_tiket:
                user[3] = str(saldo - harga_tiket)  
                with open(user_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(users)
                print(f"          Pembelian berhasil. Sisa saldo Anda: {user[3]}")
                return True
            else:
                print("            Saldo tidak cukup untuk pembelian ini.")
                return False
    print("                 Pengguna tidak ditemukan.")
    return False


def beli_tiket(username, pin):
    try:
        with open(user_file, mode='r') as file:
            reader = csv.reader(file)
            users = list(reader)

        for i, user in enumerate(users):
            if user[0] == username:
                print("Sebelum melakukan pembelian, masukkan PIN Anda untuk verifikasi.")
                old_pin = pwinput.pwinput("                    Masukkan PIN Anda: ")

                if old_pin != user[2]:
                    print("   PIN Anda salah. Anda tidak dapat melakukan transaksi.")
                    return
                
                print("             Daftar penerbangan yang tersedia:")
                lihat_tiket()

                id_penerbangan = input("        Masukkan ID penerbangan yang ingin dibeli: ")

                tiket_ditemukan = False
                harga_tiket = 0.0
                kelas_kursi = ""

                with open(tiket_file, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  
                    for row in reader:

                        if len(row) < 8:
                            print("       Data penerbangan tidak lengkap pada baris:", row)
                            continue

                        if row[0] == id_penerbangan:  
                            tiket_ditemukan = True

                            print("============= Pilih kelas kursi yang diinginkan ============")
                            print("|                     1. First Class                       |")
                            print("|                     2. Business Class                    |")
                            print("|                     3. Economy Class                     |")
                            print("============================================================")
                            kelas_pilihan = input("               Masukkan nomor kelas (1/2/3): ")

                            if kelas_pilihan == "1":
                                kelas_kursi = "First Class"
                                harga_tiket = float(row[5])  
                            elif kelas_pilihan == "2":
                                kelas_kursi = "Business Class"
                                harga_tiket = float(row[6])  
                            elif kelas_pilihan == "3":
                                kelas_kursi = "Economy Class"
                                harga_tiket = float(row[7])  
                            else:
                                print("                  Pilihan kelas tidak valid.")
                                return
                            break

                if not tiket_ditemukan:
                    print("             ID penerbangan tidak ditemukan.")
                    return

                kursi_terpilih = pilih_kursi(id_penerbangan, kelas_kursi)
                if not kursi_terpilih:
                    return

                if update_saldo(username, harga_tiket):
                    all_seats = []
                    with open(seat_file, 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if row[0] == kursi_terpilih[0]:
                                row[3] = "Booked"
                            all_seats.append(row)

                    with open(seat_file, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(all_seats)
                    
                    print(f"Tiket berhasil dibeli! Kelas: {kelas_kursi}, Kursi Anda: {kursi_terpilih[0]}")
                    generate_invoice(username, id_penerbangan, harga_tiket)
                else:
                    print("============================================================")
                    print("       Pembelian gagal karena saldo tidak mencukupi.")
    
    except FileNotFoundError:
        print("           File yang diperlukan tidak ditemukan.")
    except KeyboardInterrupt:
        print("\n         Pembelian dibatalkan oleh pengguna.")
    except Exception as e:
        print(f"{e}")

# -------------------------------------------------------
# INVOICE
# -------------------------------------------------------
def generate_invoice(username, id_penerbangan, harga_tiket):
    try:
        maskapai = ""
        kota_asal = ""
        kota_tujuan = ""
        nama = ""
        saldo = 0.0

        with open(tiket_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                
                if len(row) >= 5 and row[0] == id_penerbangan:  
                    maskapai = row[1]
                    kota_asal = row[3]
                    kota_tujuan = row[4]
                    break
            else:
                print("               ID penerbangan tidak ditemukan.")
                return

        with open(user_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                
                if len(row) >= 4 and row[0] == username:
                    nama = row[0]
                    saldo = float(row[3])  
                    break
            else:
                print("                 Pengguna tidak ditemukan.")
                return

        # Menampilkan struk atau karcis
        print("\n========================= KARCIS ===========================")
        print(f"                   Nama Pengguna: {nama}")
        print(f"                      Maskapai  : {maskapai}")
        print(f"                    Kota Asal   : {kota_asal}")
        print(f"                    Kota Tujuan : {kota_tujuan}")
        print(f"                   Harga Tiket  : Rp {harga_tiket:,.2f}")
        print("============================================================")
        print(f"          Saldo Setelah Pembelian: Rp {saldo - harga_tiket:,.2f}")
        print("============================================================")

    except Exception as e:
        print(f"                    Terjadi kesalahan: {e}")

# -------------------------------------------------------
# TOP UP SALDO
# -------------------------------------------------------

def top_up(username):
    try:
        with open("user.csv", mode='r') as file:
            reader = csv.reader(file)
            users = list(reader)

        for i, user in enumerate(users):
            if user[0] == username:
                print(" Sebelum melakukan Top Up, Masukkan PIN untuk Verifikasi.")
                old_pin = pwinput.pwinput("                        Masukkan PIN: ")

                if old_pin != user[2]:
                    print("         PIN salah. Tidak dapat melakukan top-up.")
                    return

                saldo = float(user[3])
                print(f"          Saldo Anda saat ini adalah: {saldo}")

                amount = float(input("Masukkan jumlah yang ingin di top-up (maksimal 10.000.000): "))
                if amount <= 0:
                    print("            Jumlah top-up harus lebih dari 0.")
                    return
                elif amount > 10000000:
                    print("      Jumlah top-up melebihi batas maksimal 10.000.000.")
                    return

                new_saldo = saldo + amount
                if new_saldo > 100000000:
                    print("  Saldo setelah top-up melebihi batas maksimal 100.000.000.")
                    return

                user[3] = str(new_saldo)
                users[i] = user  

                with open("user.csv", mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(users)
                print(f"         Top up berhasil! Saldo baru: {new_saldo}")
                return

        print("                  Pengguna tidak ditemukan.")
        
    except FileNotFoundError:
        print("             File 'user.csv' tidak ditemukan.")
    except ValueError:
        print("               Masukkan jumlah yang valid.")
    except KeyboardInterrupt:
        print("\n           Proses dibatalkan oleh pengguna.")
    except Exception as e:
        print(f"                  Terjadi kesalahan: {e}")

# -------------------------------------------------------
# UBAH IDENTITAS
# -------------------------------------------------------

def ubah_identitas(username):
    try:
        with open("user.csv", mode='r') as file:
            reader = csv.reader(file)
            users = list(reader)

        for i, user in enumerate(users):
            if user[0] == username:
                print(" Sebelum mengubah data, masukkan PIN lama untuk verifikasi.")
                old_pin = pwinput.pwinput("                     Masukkan PIN lama: ")

                if old_pin != user[2]:
                    print("         PIN lama salah. Tidak dapat mengubah data.")
                    return
                
                print("==================== Anda ingin mengubah ===================")
                print("|                        1. Username                       |")
                print("|                        2. Password                       |")
                print("|                        3. PIN                            |")
                print("|                        4. Keluar                         |")
                print("============================================================")
                choice = input("            Pilih opsi untuk diubah (1/2/3/4): ")

                if choice == "1":
                    new_username = input("                Masukkan username baru: ")

                    if any(u[0] == new_username for u in users):
                        print("  Username sudah digunakan. Silakan pilih username lain.")
                        return
                    
                    user[0] = new_username  

                elif choice == "2":
                    new_password = pwinput.pwinput("                 Masukkan password baru: ")
                    user[1] = new_password 

                elif choice == "3":
                    while True:
                        new_pin = pwinput.pwinput("               Masukkan PIN baru (6 angka): ")
                        if len(new_pin) == 6 and new_pin.isdigit():
                            user[2] = new_pin 
                            break
                        else:
                            print("     PIN harus terdiri dari 6 angka. Silakan coba lagi.")
                elif choice == "4":
                    print("                          Keluar")
                    break 
                else:
                    print("                     Opsi tidak valid.")
                    return

                users[i] = user 
                break
        else:
            print("                 Username tidak ditemukan.")
            return

        with open("user.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)

        print("                 Identitas berhasil diubah.")

    except FileNotFoundError:
        print("             File 'user.csv' tidak ditemukan.")
    except Exception as e:
        print(f"                    Terjadi kesalahan: {e}")
    except KeyboardInterrupt:
        print("\n           Proses dibatalkan oleh pengguna.")

# -------------------------------------------------------
# MENU CUSTOMER
# -------------------------------------------------------

def menu_customer(username, pin):
    try:
        while True:

            print("\n======================= Menu Customer ======================")
            print("|                     1. Lihat Tiket                       |")
            print("|                     2. Beli Tiket                        |")
            print("|                     3. Top Up Saldo                      |")
            print("|                     4. Ubah Identitas                    |")
            print("|                     5. Keluar                            |")
            print("============================================================")
            pilihan = input("                      Pilihan Anda: ")
            if pilihan == "1":
                lihat_tiket()
            elif pilihan == "2":
                beli_tiket(username, pin)  
            elif pilihan == "3":
                top_up(username) 
            elif pilihan == "4":
                ubah_identitas(username)
            elif pilihan == "5":
                print("       Terimakasih telah menggunakan layanan kami ^-^")
                break
            else:
                print("          Pilihan tidak valid. Silakan coba lagi.")

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna. Terima kasih sudah menggunakan layanan kami!")

# -------------------------------------------------------
# MENU UTAMA
# -------------------------------------------------------

def main():
    try:
        initialize_csv() 
        csv_tiket()
    except Exception as e:
        print(f"Error saat inisialisasi CSV: {e}")
        return
    
    try:
        while True:
            print("\n    Selamat Datang di Aplikasi Pembelian Tiket Pesawat✈!    ")
            print("========================= Menu Utama =======================")
            print("|                       1. Registrasi                      |")
            print("|                       2. Login                           |")
            print("|                       3. Keluar                          |")
            print("============================================================")
            
            pilihan = input("                       Pilih opsi: ")
            
            if pilihan == "1":
                try:
                    registrasi()
                except Exception as e:
                    print(f"                  Error saat registrasi: {e}")
                    
            elif pilihan == "2":
                try:
                    nama, role, pin = login()
                    if nama:
                        if role == "admin":
                            menu_admin()
                        elif role == "customer":
                            menu_customer(nama, pin) 
                except TypeError:
                    print("         Data login tidak valid. Silakan coba lagi.")
                except Exception as e:
                    print(f"                   Error saat login: {e}")
                    
            elif pilihan == "3":
                print("                    Keluar dari program.")
                break
            else:
                print("                  Pilihan tidak tersedia.")
                
    except KeyboardInterrupt:
        print("\nProgram dihentikan paksa. Terima kasih sudah menggunakan aplikasi ini!")

main()
