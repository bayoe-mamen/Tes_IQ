#!/usr/bin/env python3
# TesIQ.py
# Versi: Full (50 soal), shuffle soal, timer 60 menit, validasi input, scoring, threading
# Author: ELANG HYTAM

import shutil
import random
import time
import sys
import threading
import os

def print_tengah(teks):
    # Mengambil ukuran lebar terminal user saat ini
    try:
        lebar_terminal = shutil.get_terminal_size().columns
    except:
        lebar_terminal = 80 # Fallback jika terminal tidak terdeteksi
    print(teks.center(lebar_terminal))

# ==========================================
# FUNGSI: Menampilkan Hasil
# (Dibuat fungsi agar bisa dipanggil oleh Timer jika waktu habis)
# ==========================================
def tampilkan_hasil(nama, umur, waktu_pakai, total_soal, jawaban_user, soal_dipakai, skor, exit_program=False):
    print("\n")
    print_tengah("====================================================================================================")
    if exit_program:
        print_tengah("WAKTU HABIS! TES DIHENTIKAN OTOMATIS")
    else:
        print_tengah("TES BERAKHIR")
    print_tengah("====================================================================================================")
    
    # Hitung Statistik
    persentase = (skor / total_soal) * 100 if total_soal > 0 else 0
    rata = skor / total_soal if total_soal > 0 else 0
    z = (rata - 0.5) / 0.167
    iq_est = 100 + z * 15
    iq_est = max(55, min(145, iq_est)) # Batas aman

    # Tentukan Keterangan
    if iq_est >= 130: ket = "Sangat di atas rata-rata"
    elif iq_est >= 115: ket = "Di atas rata-rata"
    elif iq_est >= 85: ket = "Rata-rata"
    elif iq_est >= 70: ket = "Di bawah rata-rata"
    else: ket = "Sangat rendah"

    # Tampilkan UI
    print(f"\nNama                                         : {nama}")
    print(f"Umur                                         : {umur} tahun")
    print(f"Waktu digunakan                              : {int(waktu_pakai // 60)} menit {int(waktu_pakai % 60)} detik")
    print(f"Total soal terjawab                          : {len(jawaban_user)} / {total_soal}")
    print(f"Total benar                                  : {skor} / {total_soal}")
    print(f"Persentase benar                             : {persentase:.2f}%")
    print(f"Estimasi IQ (mendekati standar internasional): {iq_est:.0f}")
    print(f"Keterangan (perkiraan)                       : {ket}")

    # Rincian jawaban
    print("\nRincian jawaban (Soal ID : Jawaban Anda -> Kunci):")
    for soal in soal_dipakai:
        sid = soal["id"]
        user_jaw = jawaban_user.get(sid, "-")
        kunci = soal.get("kunci", "-")
        print(f"  SoalID {sid}: {user_jaw} -> {kunci}")

    direktori_skrip = os.path.dirname(os.path.abspath(sys.argv[0]))
    nama_file = os.path.join(direktori_skrip, f"hasil_tes_iq_{nama.replace(' ', '_')}.txt")
    
    # Simpan hasil ke file
    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            f.write("====================================================================================================\n")
            f.write("Hasil Tes IQ\n")
            f.write("====================================================================================================\n")
            f.write(f"Nama                                      : {nama}\n")
            f.write(f"Umur                                      : {umur}\n")
            f.write(f"Waktu digunakan                           : {int(waktu_pakai // 60)} menit {int(waktu_pakai % 60)} detik\n")
            f.write(f"Terjawab                                  : {len(jawaban_user)} / {total_soal}\n")
            f.write(f"Benar                                     : {skor} / {total_soal}\n")
            f.write(f"Persentase                                : {persentase:.2f}%\n")
            f.write(f"Estimasi IQ                               : {iq_est:.0f}\n")
            f.write(f"Keterangan                                : {ket}\n")
            f.write("Rincian jawaban (SoalID : Jawaban -> Kunci):\n")
            for soal in soal_dipakai:
                sid = soal["id"]
                user_jaw = jawaban_user.get(sid, "-")
                kunci = soal.get("kunci", "-")
                f.write(f"  SoalID {sid}: {user_jaw} -> {kunci}\n")
        print(f"\nHasil juga disimpan ke file: {nama_file}\n")
    except Exception as e:
        print("Gagal menyimpan hasil ke file:", e, "\n")

    # Jika dipanggil oleh Timer (waktu habis), matikan program paksa
    if exit_program:
        print_tengah("----------------------------------------------------------------------------------------------------")
        print("\nTekan Enter untuk menutup program...")
        os._exit(0)

# ==========================================
# PROGRAM UTAMA
# ==========================================
print_tengah("====================================================================================================")
print_tengah("Tes IQ by ELANG HYTAM (Non Formal)")
print_tengah("====================================================================================================")

while True:
    # Inisialisasi Variabel
    nama_pengguna = ""
    umur_pengguna = 0
    mulai_tes_iq = ""
    mulai = ""
    skor_iq = 0
    pakai_lagi = ""
    tutup_program = ""

    # ============================
    # List soal (100 soal)
    # ============================
    soal_list = [
        {
            "id": 1,
            "soal": "Pola: 2, 4, 8, 16, 32, ... Angka berikutnya adalah?",
            "pilihan": ["48", "54", "64", "72", "96"],
            "kunci": "C"
        },
        {
            "id": 2,
            "soal": "Pola: 5, 10, 20, 40, … Angka berikutnya adalah?",
            "pilihan": ["50", "60", "70", "80", "100"],
            "kunci": "D"
        },
        {
            "id": 3,
            "soal": "Pola: 1, 3, 6, 10, 15, …",
            "pilihan": ["18", "20", "21", "24", "28"],
            "kunci": "C"
        },
        {
            "id": 4,
            "soal": "Pola: 7, 14, 28, 56, …",
            "pilihan": ["72", "84", "98", "112", "120"],
            "kunci": "D"
        },
        {
            "id": 5,
            "soal": "Pola: 81, 27, 9, 3, …",
            "pilihan": ["1", "2", "4", "6", "9"],
            "kunci": "A"
        },
        {
            "id": 6,
            "soal": "Pola: 11, 15, 20, 26, 33, …",
            "pilihan": ["40", "41", "42", "43", "44"],
            "kunci": "B"
        },
        {
            "id": 7,
            "soal": "Pola: 4, 9, 16, 25, 36, …",
            "pilihan": ["42", "44", "47", "49", "50"],
            "kunci": "D"
        },
        {
            "id": 8,
            "soal": "Pola: 100, 95, 85, 70, 50, …",
            "pilihan": ["25", "30", "35", "40", "45"],
            "kunci": "A"
        },
        {
            "id": 9,
            "soal": "Pola: 1, 2, 4, 7, 11, 16, …",
            "pilihan": ["20", "21", "22", "23", "24"],
            "kunci": "C"
        },
        {
            "id": 10,
            "soal": "Pola: 12, 6, 3, 1.5, …",
            "pilihan": ["1.0", "0.75", "0.6", "0.5", "0.3"],
            "kunci": "B"
        },
        {
            "id": 11,
            "soal": "Semua burung bisa terbang. Penguin adalah burung. Maka:",
            "pilihan": [
                "Penguin pasti terbang",
                "Penguin mungkin terbang",
                "Penguin tidak bisa terbang",
                "Pernyataan salah",
                "Tidak cukup informasi"
            ],
            "kunci": "A"
        },
        {
            "id": 12,
            "soal": "Semua A adalah B. Semua B adalah C. Maka semua A adalah:",
            "pilihan": ["C", "B", "A", "Tidak ada", "Tidak pasti"],
            "kunci": "A"
        },
        {
            "id": 13,
            "soal": "Tini lebih tua dari Beni. Beni lebih tua dari Rani. Maka:",
            "pilihan": [
                "Rani paling tua",
                "Beni paling tua",
                "Tini paling tua",
                "Rani lebih tua dari Tini",
                "Tidak bisa ditentukan"
            ],
            "kunci": "C"
        },
        {
            "id": 14,
            "soal": "Jika hujan maka jalan basah. Jalan tidak basah. Maka:",
            "pilihan": ["Hujan", "Tidak hujan", "Tetap basah", "Bisa basah", "Tidak pasti"],
            "kunci": "B"
        },
        {
            "id": 15,
            "soal": "3 orang duduk berurutan: A, B, C. B tidak mau di tengah. Urutannya?",
            "pilihan": ["ABC", "ACB", "BAC", "BCA", "CBA"],
            "kunci": "C"
        },
        {
            "id": 16,
            "soal": "Jika semua guru pintar dan Rudi pintar, maka…",
            "pilihan": [
                "Rudi pasti guru",
                "Semua pintar adalah guru",
                "Guru mungkin Rudi",
                "Tidak cukup informasi",
                "Rudi bodoh"
            ],
            "kunci": "D"
        },
        {
            "id": 17,
            "soal": "Andi lebih tinggi dari Budi. Cici lebih pendek dari Budi. Maka:",
            "pilihan": ["Andi tertinggi", "Cici tertinggi", "Budi tertinggi", "Cici terpendek", "Tidak bisa"],
            "kunci": "A"
        },
        {
            "id": 18,
            "soal": "Dalam sebuah kelas hanya ada laki-laki. Dika ada di kelas itu.",
            "pilihan": ["Dika laki-laki", "Dika perempuan", "Dika mungkin perempuan", "Tidak dapat disimpulkan", "Semua salah"],
            "kunci": "A"
        },
        {
            "id": 19,
            "soal": "Jika 5 × X = 45, maka X adalah:",
            "pilihan": ["7", "8", "9", "10", "11"],
            "kunci": "C"
        },
        {
            "id": 20,
            "soal": "Jika 2 jam lalu pukul 6, sekarang pukul:",
            "pilihan": ["7", "8", "9", "10", "12"],
            "kunci": "B"
        },
        {
            "id": 21,
            "soal": "Kucing : Meong = Anjing : …",
            "pilihan": ["Kokok", "Guk", "Ngik", "Ngembek", "Cit-cit"],
            "kunci": "B"
        },
        {
            "id": 22,
            "soal": "Pisang : Kuning = Semangka : …",
            "pilihan": ["Hijau", "Ungu", "Merah", "Oranye", "Biru"],
            "kunci": "A"
        },
        {
            "id": 23,
            "soal": "Mata : Melihat = Telinga : …",
            "pilihan": ["Berjalan", "Tidur", "Mendengar", "Menyentuh", "Bicara"],
            "kunci": "C"
        },
        {
            "id": 24,
            "soal": "Api : Panas = Es : …",
            "pilihan": ["Dingin", "Cair", "Panas", "Putih", "Kental"],
            "kunci": "A"
        },
        {
            "id": 25,
            "soal": "Ikan : Air = Burung : …",
            "pilihan": ["Tanah", "Langit", "Batang", "Air", "Rumah"],
            "kunci": "B"
        },
        {
            "id": 26,
            "soal": "Buku : Membaca = Piring : …",
            "pilihan": ["Melukis", "Memasak", "Makan", "Beli", "Bersih"],
            "kunci": "C"
        },
        {
            "id": 27,
            "soal": "Kayu : Pohon = Daging : …",
            "pilihan": ["Hewan", "Bumbu", "Laut", "Es", "Sayur"],
            "kunci": "A"
        },
        {
            "id": 28,
            "soal": "Malam : Gelap = Siang : …",
            "pilihan": ["Tidur", "Cerah", "Awan", "Matahari", "Lelah"],
            "kunci": "B"
        },
        {
            "id": 29,
            "soal": "Kunci : Gembok = Password : …",
            "pilihan": ["KTP", "Pintu", "Aplikasi", "Keyboard", "WC"],
            "kunci": "C"
        },
        {
            "id": 30,
            "soal": "Dokter : Obat = Chef : …",
            "pilihan": ["TV", "Pisang", "Panci", "Kasur", "Makanan"],
            "kunci": "E"
        },
        {
            "id": 31,
            "soal": "25% dari 200 adalah:",
            "pilihan": ["25", "30", "40", "45", "50"],
            "kunci": "E"
        },
        {
            "id": 32,
            "soal": "12 × 8 =",
            "pilihan": ["80", "84", "90", "96", "100"],
            "kunci": "D"
        },
        {
            "id": 33,
            "soal": "144 ÷ 12 =",
            "pilihan": ["10", "11", "12", "13", "14"],
            "kunci": "C"
        },
        {
            "id": 34,
            "soal": "17 + 28 =",
            "pilihan": ["43", "44", "45", "46", "47"],
            "kunci": "C"
        },
        {
            "id": 35,
            "soal": "100 – 37 =",
            "pilihan": ["62", "63", "64", "65", "66"],
            "kunci": "B"
        },
        {
            "id": 36,
            "soal": "9² =",
            "pilihan": ["72", "81", "90", "99", "121"],
            "kunci": "B"
        },
        {
            "id": 37,
            "soal": "⅓ dari 150 adalah:",
            "pilihan": ["30", "40", "50", "60", "75"],
            "kunci": "C"
        },
        {
            "id": 38,
            "soal": "7 × 9 =",
            "pilihan": ["56", "59", "63", "70", "72"],
            "kunci": "C"
        },
        {
            "id": 39,
            "soal": "60% dari 500 =",
            "pilihan": ["200", "250", "280", "300", "350"],
            "kunci": "D"
        },
        {
            "id": 40,
            "soal": "2.5 + 3.75 =",
            "pilihan": ["5.0", "6.0", "6.25", "6.5", "7.1"],
            "kunci": "C"
        },
        {
            "id": 41,
            "soal": "“Kontras” artinya…",
            "pilihan": ["Mirip", "Berlawanan", "Sebagian", "Menumpuk", "Tersusun"],
            "kunci": "B"
        },
        {
            "id": 42,
            "soal": "Lawan kata “sementara”…",
            "pilihan": ["Singkat", "Tetap", "Biasa", "Jarang", "Ringan"],
            "kunci": "B"
        },
        {
            "id": 43,
            "soal": "Mana huruf yang berbeda pola?",
            "pilihan": ["A", "E", "I", "O", "U"],
            "kunci": "C"
        },
        {
            "id": 44,
            "soal": "Mana yang bukan hewan?",
            "pilihan": ["Zebra", "Panda", "Air", "Ikan", "Kelinci"],
            "kunci": "C"
        },
        {
            "id": 45,
            "soal": "Mana yang termasuk benda cair?",
            "pilihan": ["Batu", "Kayu", "Minyak", "Kertas", "Udara"],
            "kunci": "C"
        },
        {
            "id": 46,
            "soal": "Mana yang termasuk alat komunikasi?",
            "pilihan": ["Gelas", "HP", "Paku", "Tenda", "Roti"],
            "kunci": "B"
        },
        {
            "id": 47,
            "soal": "Manakah yang paling besar?",
            "pilihan": ["Atom", "Sel", "Molekul", "Debu", "Virus"],
            "kunci": "B"
        },
        {
            "id": 48,
            "soal": "Mana yang berhubungan dengan sekolah?",
            "pilihan": ["Kapur", "Kompor", "Ban", "Paku", "Cangkul"],
            "kunci": "A"
        },
        {
            "id": 49,
            "soal": "“Transparan” berarti:",
            "pilihan": ["Gelap", "Terang", "Buram", "Tidak terlihat", "Jernih/tembus pandang"],
            "kunci": "E"
        },
        {
            "id": 50,
            "soal": "Buku : Perpustakaan = Pesawat : …",
            "pilihan": ["Restoran", "Bandara", "Kantor", "Sawah", "Mall"],
            "kunci": "B"
        },
        {
            "id": 51,
            "soal": "Pola: 3, 6, 12, 24, ... Angka berikutnya?",
            "pilihan": ["36", "40", "44", "48", "54"],
            "kunci": "D"
        },
        {
            "id": 52,
            "soal": "Jika 2 ▲ 3 = 11 dan 4 ▲ 2 = 20, maka 3 ▲ 5 = ?",
            "pilihan": ["18", "19", "20", "21", "22"],
            "kunci": "C"
        },
        {
            "id": 53,
            "soal": "Bentuk mana yang berbeda?",
            "pilihan": ["Lingkaran", "Elips", "Persegi", "Oval", "Lingkaran besar"],
            "kunci": "C"
        },
        {
            "id": 54,
            "soal": "Pola huruf: A, C, F, J, O, ... Huruf berikutnya?",
            "pilihan": ["S", "T", "U", "V", "W"],
            "kunci": "C"
        },
        {
            "id": 55,
            "soal": "Mana yang terbesar nilainya?",
            "pilihan": ["1/2", "0.49", "0.5", "50%", "0.48"],
            "kunci": "C"
        },
        {
            "id": 56,
            "soal": "Jika sebuah jam menunjukkan pukul 3:15, sudut jarum jam dan menit adalah?",
            "pilihan": ["0°", "7.5°", "15°", "30°", "90°"],
            "kunci": "B"
        },
        {
            "id": 57,
            "soal": "Urutan: 7, 14, 28, 56, ... Angka berikutnya?",
            "pilihan": ["70", "90", "100", "112", "140"],
            "kunci": "D"
        },
        {
            "id": 58,
            "soal": "Jika 5 kotak = 20, maka 3 kotak = ?",
            "pilihan": ["8", "10", "12", "14", "15"],
            "kunci": "C"
        },
        {
            "id": 59,
            "soal": "Negasi dari pernyataan “Semua orang hadir” adalah?",
            "pilihan": ["Tidak ada yang hadir", "Beberapa tidak hadir", "Semua tidak hadir", "Hanya satu yang hadir", "Banyak yang hadir"],
            "kunci": "B"
        },
        {
            "id": 60,
            "soal": "Urutan: 1, 4, 9, 16, ... Angka berikutnya?",
            "pilihan": ["20", "25", "26", "30", "36"],
            "kunci": "B"
        },
        {
            "id": 61,
            "soal": "Manakah yang tidak termasuk bilangan prima?",
            "pilihan": ["2", "3", "11", "21", "13"],
            "kunci": "D"
        },
        {
            "id": 62,
            "soal": "Jika satu mobil menempuh 60 km dalam 1 jam, maka 150 km ditempuh dalam?",
            "pilihan": ["1 jam", "2 jam", "2.5 jam", "3 jam", "3.5 jam"],
            "kunci": "C"
        },
        {
            "id": 63,
            "soal": "Pola: 11, 22, 33, 44, ... Angka berikutnya?",
            "pilihan": ["45", "48", "50", "55", "66"],
            "kunci": "D"
        },
        {
            "id": 64,
            "soal": "Jika hari ini Kamis, 100 hari lagi adalah hari?",
            "pilihan": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "kunci": "E"
        },
        {
            "id": 65,
            "soal": "Jika 8×8 = 64, maka √64 = ?",
            "pilihan": ["6", "7", "8", "9", "10"],
            "kunci": "C"
        },
        {
            "id": 66,
            "soal": "Pola: 4, 9, 19, 39, ... Angka berikutnya?",
            "pilihan": ["59", "60", "61", "79", "81"],
            "kunci": "D"
        },
        {
            "id": 67,
            "soal": "Berapa sisi bangun decagon?",
            "pilihan": ["8", "9", "10", "11", "12"],
            "kunci": "C"
        },
        {
            "id": 68,
            "soal": "Yang manakah yang bukan hewan mamalia?",
            "pilihan": ["Paus", "Lumba-lumba", "Kelelawar", "Ayam", "Anjing"],
            "kunci": "D"
        },
        {
            "id": 69,
            "soal": "Urutan: 100, 90, 81, 73, ... Angka berikutnya?",
            "pilihan": ["65", "66", "67", "68", "70"],
            "kunci": "B"
        },
    {
            "id": 70,
            "soal": "Pola huruf: Z, X, V, T, ... Huruf berikutnya?",
            "pilihan": ["R", "S", "Q", "O", "P"],
            "kunci": "A"
        },
        {
            "id": 71,
            "soal": "Jika 12 apel dibagi ke 3 orang, tiap orang mendapat?",
            "pilihan": ["2", "3", "4", "5", "6"],
            "kunci": "C"
        },
        {
            "id": 72,
            "soal": "Bentuk mana yang memiliki simetri putar?",
            "pilihan": ["Segitiga Sama Sisi", "Segitiga Siku", "Segitiga Sama Kaki", "Segitiga tumpul", "Tidak ada"],
            "kunci": "A"
        },
        {
            "id": 73,
            "soal": "Pola: 9, 3, 1, 1/3, ... berikutnya?",
            "pilihan": ["1/4", "1/6", "1/9", "1/12", "1/27"],
            "kunci": "C"
        },
        {
            "id": 74,
            "soal": "Jika 1 = A, 2 = B, maka 26 = ?",
            "pilihan": ["X", "Y", "Z", "W", "AA"],
            "kunci": "C"
        },
        {
            "id": 75,
            "soal": "Jika satu kue dibagi 8 sama besar, satu potong bernilai?",
            "pilihan": ["1/4", "1/6", "1/8", "1/10", "1/12"],
            "kunci": "C"
        },
        {
            "id": 76,
            "soal": "Pola: 50, 45, 41, 38, ... berikutnya?",
            "pilihan": ["36", "35", "34", "33", "32"],
            "kunci": "A"
        },
        {
            "id": 77,
            "soal": "Manakah yang bentuknya 3D?",
            "pilihan": ["Segitiga", "Persegi", "Lingkaran", "Kubus", "Trapesium"],
            "kunci": "D"
        },
        {
            "id": 78,
            "soal": "Pola huruf: A, B, D, G, K, ...",
            "pilihan": ["O", "P", "Q", "R", "S"],
            "kunci": "B"
        },
        {
            "id": 79,
            "soal": "Urutan: 2, 3, 5, 8, 12, ...",
            "pilihan": ["15", "16", "17", "18", "19"],
            "kunci": "C"
        },
        {
            "id": 80,
            "soal": "Jika sebuah persegi memiliki sisi 6 cm, kelilingnya?",
            "pilihan": ["12", "18", "24", "30", "36"],
            "kunci": "C"
        },
        {
            "id": 81,
            "soal": "Mana yang bukan warna primer?",
            "pilihan": ["Merah", "Biru", "Kuning", "Hijau", "Semua primer"],
            "kunci": "D"
        },
        {
            "id": 82,
            "soal": "Pola: 1, 3, 7, 15, 31, ...",
            "pilihan": ["48", "50", "55", "60", "63"],
            "kunci": "E"
        },
        {
            "id": 83,
            "soal": "Berapa jumlah sudut dalam segitiga?",
            "pilihan": ["90°", "120°", "180°", "270°", "360°"],
            "kunci": "C"
        },
        {
            "id": 84,
            "soal": "Jika 9 → 81, 6 → 36, maka 12 → ?",
            "pilihan": ["120", "122", "132", "144", "156"],
            "kunci": "D"
        },
        {
            "id": 85,
            "soal": "Urutan: 5, 11, 17, 23, ...",
            "pilihan": ["27", "28", "29", "30", "31"],
            "kunci": "C"
        },
        {
            "id": 86,
            "soal": "Yang manakah yang bukan bilangan genap?",
            "pilihan": ["10", "14", "20", "21", "30"],
            "kunci": "D"
        },
        {
            "id": 87,
            "soal": "Pola: 90, 80, 71, 63, ...",
            "pilihan": ["54", "55", "56", "57", "58"],
            "kunci": "B"
        },
        {
            "id": 88,
            "soal": "Berapa banyak huruf dalam kata 'INTELEGENSI'?",
            "pilihan": ["8", "9", "10", "11", "12"],
            "kunci": "D"
        },
        {
            "id": 89,
            "soal": "Jika jam menunjukkan 12:00, 135 menit kemudian pukul?",
            "pilihan": ["13:35", "14:15", "14:30", "14:45", "15:00"],
            "kunci": "B"
        },
        {
            "id": 90,
            "soal": "Pola huruf: Z, Y, W, T, ...",
            "pilihan": ["R", "Q", "S", "P", "N"],
            "kunci": "D"
        },
        {
            "id": 91,
            "soal": "Jika 3 orang bisa makan 3 kue dalam 3 menit, maka 6 orang makan 6 kue dalam?",
            "pilihan": ["3 menit", "4 menit", "5 menit", "6 menit", "9 menit"],
            "kunci": "A"
        },
        {
            "id": 92,
            "soal": "Berapa banyak bilangan ganjil antara 1–20?",
            "pilihan": ["8", "9", "10", "11", "12"],
            "kunci": "C"
        },
        {
            "id": 93,
            "soal": "Pola: 4, 6, 9, 13, 18, ...",
            "pilihan": ["20", "22", "23", "24", "25"],
            "kunci": "D"
        },
        {
            "id": 94,
            "soal": "Manakah angka yang berbeda?",
            "pilihan": ["8", "12", "16", "20", "25"],
            "kunci": "E"
        },
        {
            "id": 95,
            "soal": "Jika 7 × 7 = 49, maka 49 ÷ 7 = ?",
            "pilihan": ["5", "6", "7", "8", "9"],
            "kunci": "C"
        },
        {
            "id": 96,
            "soal": "Urutan: 21, 18, 14, 9, ...",
            "pilihan": ["4", "5", "6", "7", "8"],
            "kunci": "A"
        },
        {
            "id": 97,
            "soal": "Jika 1 = 1, 2 = 4, 3 = 9, maka 5 = ?",
            "pilihan": ["20", "22", "24", "25", "26"],
            "kunci": "D"
        },
        {
            "id": 98,
            "soal": "Pola huruf: A, E, I, M, Q, ...",
            "pilihan": ["T", "U", "V", "W", "Y"],
            "kunci": "B"
        },
        {
            "id": 99,
            "soal": "Berapa hasil dari 20% dari 250?",
            "pilihan": ["40", "45", "50", "55", "60"],
            "kunci": "C"
        },
        {
            "id": 100,
            "soal": "Urutan: 12, 24, 48, 96, ...",
            "pilihan": ["120", "144", "160", "180", "192"],
            "kunci": "E"
        },
        {
            "id": 101,
            "soal": "Pola: 3, 9, 27, 81, ...\nAngka berikutnya adalah?",
            "pilihan": ["120", "162", "240", "300", "324"],
            "kunci": "B"
        },
        {
            "id": 102,
            "soal": "Pola: 2, 5, 11, 23, 47, ...\nAngka berikutnya adalah?",
            "pilihan": ["70", "80", "94", "100", "120"],
            "kunci": "C"
        },
        {
            "id": 103,
            "soal": "Pola: 10, 7, 4, 1, ...\nAngka berikutnya adalah?",
            "pilihan": ["-1", "-2", "0", "2", "3"],
            "kunci": "C"
        },
        {
            "id": 104,
            "soal": "Pola: 1, 4, 9, 16, 25, ...\nAngka berikutnya adalah?",
            "pilihan": ["30", "35", "36", "40", "49"],
            "kunci": "C"
        },
        {
            "id": 105,
            "soal": "Pola: 2, 3, 5, 8, 12, 17, ...\nAngka berikutnya adalah?",
            "pilihan": ["21", "22", "23", "24", "25"],
            "kunci": "A"
        },
        {
            "id": 106,
            "soal": "Pola: 100, 50, 25, 12.5, ...\nAngka berikutnya adalah?",
            "pilihan": ["6.25", "7", "8.5", "10", "5.5"],
            "kunci": "A"
        },
        {
            "id": 107,
            "soal": "Pola: 4, 7, 14, 28, 56, ...\nAngka berikutnya adalah?",
            "pilihan": ["70", "80", "90", "112", "120"],
            "kunci": "D"
        },
        {
            "id": 108,
            "soal": "Pola: 15, 18, 24, 33, 45, ...\nAngka berikutnya adalah?",
            "pilihan": ["52", "57", "60", "63", "70"],
            "kunci": "B"
        },
        {
            "id": 109,
            "soal": "Pola: 1, 2, 6, 24, 120, ...\nAngka berikutnya adalah?",
            "pilihan": ["240", "300", "720", "840", "960"],
            "kunci": "C"
        },
        {
            "id": 110,
            "soal": "Pola: 90, 85, 75, 60, 40, ...\nAngka berikutnya adalah?",
            "pilihan": ["25", "20", "15", "10", "0"],
            "kunci": "B"
        },
        {
            "id": 111,
            "soal": "Semua benda berbentuk bulat dapat berguling. Bola berbentuk bulat. Maka:",
            "pilihan": ["Bola pasti berguling", "Bola tidak bisa berguling", "Mungkin berguling", "Pernyataan tidak valid", "Tidak ada hubungan"],
            "kunci": "A"
        },
        {
            "id": 112,
            "soal": "Jika A tinggi dari B, dan B tinggi dari C, maka:",
            "pilihan": ["C tertinggi", "A tertinggi", "B tertinggi", "Tidak dapat ditentukan", "Semua sama tinggi"],
            "kunci": "B"
        },
        {
            "id": 113,
            "soal": "Jika lampu mati maka ruangan gelap. Ruangan tidak gelap.",
            "pilihan": ["Lampu mati", "Lampu menyala", "Tetap gelap", "Belum tentu", "Tidak ada hubungan"],
            "kunci": "B"
        },
        {
            "id": 114,
            "soal": "Semua ikan hidup di air. Paus bukan ikan.",
            "pilihan": ["Paus hidup di air", "Paus tidak hidup di air", "Paus pasti ikan", "Ikan bukan paus", "Tidak dapat disimpulkan"],
            "kunci": "A"
        },
        {
            "id": 115,
            "soal": "Jika 3 orang berdiri berurutan A, B, C, dan C tidak mau di tengah.",
            "pilihan": ["ABC", "ACB", "BAC", "BCA", "CAB"],
            "kunci": "E"
        },
        {
            "id": 116,
            "soal": "Semua programmer suka kopi. Joko tidak suka kopi.",
            "pilihan": ["Joko programmer", "Joko bukan programmer", "Joko mungkin programmer", "Tidak tahu", "Semua benar"],
            "kunci": "B"
        },
        {
            "id": 117,
            "soal": "Jika hari ini hujan maka sekolah libur. Sekolah tidak libur.",
            "pilihan": ["Hari ini hujan", "Hari ini tidak hujan", "Tetap libur", "Belum tentu", "Tidak ada hubungan"],
            "kunci": "B"
        },
        {
            "id": 118,
            "soal": "Jika X = benar dan Y = salah, maka pernyataan 'X dan Y' adalah:",
            "pilihan": ["Benar", "Salah", "Tidak pasti", "Campuran", "Tidak ada jawaban"],
            "kunci": "B"
        },
        {
            "id": 119,
            "soal": "Semua kucing berekor. Binatang ini tidak berekor.",
            "pilihan": ["Ini kucing", "Bukan kucing", "Mungkin kucing", "Bisa jadi kucing", "Tidak dapat disimpulkan"],
            "kunci": "B"
        },
        {
            "id": 120,
            "soal": "Semua guru bekerja di sekolah. Tono bekerja di sekolah.",
            "pilihan": ["Tono pasti guru", "Tono bukan guru", "Mungkin guru", "Tidak ada hubungan", "Semua salah"],
            "kunci": "C"
        },
        {
            "id": 121,
            "soal": "Matahari : Siang = Bulan : ...",
            "pilihan": ["Malam", "Gelap", "Awan", "Bumi", "Terang"],
            "kunci": "A"
        },
        {
            "id": 122,
            "soal": "Tangan : Memegang = Kaki : ...",
            "pilihan": ["Melihat", "Melompat", "Berbicara", "Makan", "Mengetik"],
            "kunci": "B"
        },
        {
            "id": 123,
            "soal": "Air : Cair = Batu : ...",
            "pilihan": ["Es", "Cair", "Padat", "Gas", "Minyak"],
            "kunci": "C"
        },
        {
            "id": 124,
            "soal": "Pohon : Daun = Buku : ...",
            "pilihan": ["Huruf", "Sampul", "Kaca", "Meja", "Pena"],
            "kunci": "A"
        },
        {
            "id": 125,
            "soal": "Dokter : Pasien = Mekanik : ...",
            "pilihan": ["Rumah", "Kucing", "Mobil", "TV", "Sepeda"],
            "kunci": "C"
        },
        {
            "id": 126,
            "soal": "Gigi : Mulut = Buku : ...",
            "pilihan": ["Halaman", "Pena", "Tulisan", "Meja", "Gambar"],
            "kunci": "A"
        },
        {
            "id": 127,
            "soal": "Ular : Merayap = Burung : ...",
            "pilihan": ["Lari", "Terbang", "Berenang", "Menggonggong", "Menyala"],
            "kunci": "B"
        },
        {
            "id": 128,
            "soal": "Panas : Api = Dingin : ...",
            "pilihan": ["Es", "Air", "Kabut", "Tanah", "Awan"],
            "kunci": "A"
        },
        {
            "id": 129,
            "soal": "Sarang : Burung = Akuarium : ...",
            "pilihan": ["Kucing", "Ikan", "Harimau", "Lebah", "Burung"],
            "kunci": "B"
        },
        {
            "id": 130,
            "soal": "Kunci : Membuka = Pena : ...",
            "pilihan": ["Menghapus", "Membaca", "Menulis", "Makan", "Memotong"],
            "kunci": "C"
        },
        {
            "id": 131,
            "soal": "15 × 6 =",
            "pilihan": ["80", "85", "90", "95", "100"],
            "kunci": "C"
        },
        {
            "id": 132,
            "soal": "250 ÷ 5 =",
            "pilihan": ["40", "45", "48", "50", "55"],
            "kunci": "D"
        },
        {
            "id": 133,
            "soal": "13 + 19 =",
            "pilihan": ["30", "31", "32", "33", "34"],
            "kunci": "C"
        },
        {
            "id": 134,
            "soal": "90 – 28 =",
            "pilihan": ["60", "61", "62", "63", "65"],
            "kunci": "D"
        },
        {
            "id": 135,
            "soal": "11² =",
            "pilihan": ["100", "110", "121", "130", "140"],
            "kunci": "C"
        },
        {
            "id": 136,
            "soal": "⅕ dari 200 =",
            "pilihan": ["20", "30", "35", "40", "50"],
            "kunci": "A"
        },
        {
            "id": 137,
            "soal": "7 × 12 =",
            "pilihan": ["72", "80", "82", "84", "90"],
            "kunci": "D"
        },
        {
            "id": 138,
            "soal": "64 ÷ 8 =",
            "pilihan": ["6", "7", "8", "9", "10"],
            "kunci": "C"
        },
        {
            "id": 139,
            "soal": "45% dari 200 =",
            "pilihan": ["70", "80", "85", "90", "100"],
            "kunci": "C"
        },
        {
            "id": 140,
            "soal": "6.5 + 4.25 =",
            "pilihan": ["9.0", "10.25", "10.75", "11.0", "12.25"],
            "kunci": "C"
        },
        {
            "id": 141,
            "soal": "\"Cepat\" sinonim dari:",
            "pilihan": ["Lambat", "Kilat", "Berat", "Sedikit", "Sabar"],
            "kunci": "B"
        },
        {
            "id": 142,
            "soal": "Lawan kata \"gelap\" adalah:",
            "pilihan": ["Hitam", "Sedih", "Terang", "Awan", "Malam"],
            "kunci": "C"
        },
        {
            "id": 143,
            "soal": "Mana yang bukan warna?",
            "pilihan": ["Biru", "Kuning", "Tiga", "Merah", "Hijau"],
            "kunci": "C"
        },
        {
            "id": 144,
            "soal": "Mana yang termasuk hewan air?",
            "pilihan": ["Kucing", "Sapi", "Ikan", "Ayam", "Ular"],
            "kunci": "C"
        },
        {
            "id": 145,
            "soal": "\"Transisi\" berarti:",
            "pilihan": ["Perubahan", "Kegelapan", "Hambatan", "Kebisingan", "Menyala"],
            "kunci": "A"
        },
        {
            "id": 146,
            "soal": "Alat untuk menulis adalah:",
            "pilihan": ["Sendok", "Pisau", "Pensil", "Batu", "Lemari"],
            "kunci": "C"
        },
        {
            "id": 147,
            "soal": "Mana yang lebih berat?",
            "pilihan": ["1 kg kapas", "1 kg besi", "Besi 10 gram", "Kapas 5 gram", "Semua sama berat"],
            "kunci": "E"
        },
        {
            "id": 148,
            "soal": "\"Fiksi\" berarti:",
            "pilihan": ["Cerita nyata", "Cerita bohong", "Cerita imajinasi", "Cerita video", "Cerita pendek"],
            "kunci": "C"
        },
        {
            "id": 149,
            "soal": "Mana yang berhubungan dengan teknologi?",
            "pilihan": ["CPU", "Pisang", "Rumput", "Kain", "Kompor kayu"],
            "kunci": "A"
        },
        {
            "id": 150,
            "soal": "Tempat membaca buku adalah:",
            "pilihan": ["Kolam renang", "Toko roti", "Perpustakaan", "Terminal", "Stadion"],
            "kunci": "C"
        },
        {
            "id": 151,
            "soal": "Pola: 7, 14, 28, 56, ...\nAngka berikutnya adalah?",
            "pilihan": ["70", "84", "90", "112", "120"],
            "kunci": "B"
        },
        {
            "id": 152,
            "soal": "Pola: 1, 3, 7, 15, 31, ...\nAngka berikutnya adalah?",
            "pilihan": ["40", "48", "50", "63", "70"],
            "kunci": "D"
        },
        {
            "id": 153,
            "soal": "Pola: 12, 6, 3, 1.5, ...\nAngka berikutnya adalah?",
            "pilihan": ["0.5", "0.75", "1", "2", "3"],
            "kunci": "B"
        },
        {
            "id": 154,
            "soal": "Pola: 5, 12, 24, 41, 63, ...\nAngka berikutnya adalah?",
            "pilihan": ["80", "90", "91", "95", "100"],
            "kunci": "C"
        },
        {
            "id": 155,
            "soal": "Jika semua A adalah B, dan semua B adalah C, maka:",
            "pilihan": ["Semua A adalah C", "Semua C adalah A", "A bukan C", "B bukan C", "Tidak ada hubungan"],
            "kunci": "A"
        },
        {
            "id": 156,
            "soal": "Jika hujan maka jalan basah. Jalan tidak basah.",
            "pilihan": ["Hujan deras", "Hujan kecil", "Tidak hujan", "Tetap basah", "Tidak bisa disimpulkan"],
            "kunci": "C"
        },
        {
            "id": 157,
            "soal": "Pola: 4, 9, 19, 39, 79, ...\nAngka berikutnya adalah?",
            "pilihan": ["100", "120", "150", "159", "160"],
            "kunci": "D"
        },
        {
            "id": 158,
            "soal": "Mana yang bukan bilangan prima?",
            "pilihan": ["11", "13", "17", "21", "29"],
            "kunci": "D"
        },
        {
            "id": 159,
            "soal": "Mana yang paling logis melengkapi pola?\nKucing:Meong = Anjing:...",
            "pilihan": ["Mooo", "Kwek", "Guk", "Hush", "Kriuk"],
            "kunci": "C"
        },
        {
            "id": 160,
            "soal": "Jika 2 = 6, 3 = 12, 4 = 20, 5 = ...",
            "pilihan": ["25", "30", "35", "40", "45"],
            "kunci": "C"
        },
        {
            "id": 161,
            "soal": "Pola: 101, 99, 96, 92, ...\nAngka berikutnya?",
            "pilihan": ["87", "88", "89", "90", "91"],
            "kunci": "A"
        },
        {
            "id": 162,
            "soal": "Jika X lebih besar dari Y, dan Y lebih besar dari Z, maka:",
            "pilihan": ["Z terbesar", "X terbesar", "Y terbesar", "Z lebih besar dari X", "Tidak bisa disimpulkan"],
            "kunci": "B"
        },
        {
            "id": 163,
            "soal": "Pola: 2, 4, 12, 48, ...\nAngka berikutnya?",
            "pilihan": ["96", "120", "144", "192", "200"],
            "kunci": "D"
        },
        {
            "id": 164,
            "soal": "Pola: 50, 45, 35, 20, ...\nAngka berikutnya?",
            "pilihan": ["10", "5", "0", "-5", "-10"],
            "kunci": "C"
        },
        {
            "id": 165,
            "soal": "Segitiga memiliki 3 sisi. Persegi memiliki 4 sisi. Maka lingkaran:",
            "pilihan": ["5 sisi", "3 sisi", "Tidak punya sisi", "Banyak sisi", "Sisi tak terbatas"],
            "kunci": "C"
        },
        {
            "id": 166,
            "soal": "Jika 8 + 2 = 20, 6 + 3 = 18, maka 9 + 1 = ...",
            "pilihan": ["9", "10", "18", "20", "24"],
            "kunci": "C"
        },
        {
            "id": 167,
            "soal": "Pola: 13, 17, 25, 37, 53, ...\nAngka berikutnya?",
            "pilihan": ["65", "70", "73", "80", "85"],
            "kunci": "C"
        },
        {
            "id": 168,
            "soal": "\"Minus\" adalah antonim dari:",
            "pilihan": ["Kurang", "Tambah", "Besar", "Sedikit", "Ganda"],
            "kunci": "B"
        },
        {
            "id": 169,
            "soal": "Mana yang tidak termasuk alat transportasi?",
            "pilihan": ["Kereta", "Pesawat", "Mobil", "Lemari", "Kapal"],
            "kunci": "D"
        },
        {
            "id": 170,
            "soal": "Pola: 1, 4, 8, 13, 19, ...\nBerikutnya adalah?",
            "pilihan": ["24", "25", "26", "27", "28"],
            "kunci": "C"
        },
        {
            "id": 171,
            "soal": "Jika semua burung bisa terbang, dan ayam tidak bisa terbang jauh:",
            "pilihan": ["Ayam adalah burung", "Ayam bukan burung", "Ayam pasti terbang", "Ayam tidak punya sayap", "Tidak dapat disimpulkan"],
            "kunci": "A"
        },
        {
            "id": 172,
            "soal": "Pola: 2, 3, 6, 15, 42, ...\nAngka berikutnya?",
            "pilihan": ["85", "90", "100", "120", "110"],
            "kunci": "C"
        },
        {
            "id": 173,
            "soal": "Pola: 100, 90, 70, 40, ...\nBerikutnya?",
            "pilihan": ["0", "5", "10", "15", "20"],
            "kunci": "C"
        },
        {
            "id": 174,
            "soal": "Jika 3 kotak berisi 15 apel, maka 1 kotak berisi:",
            "pilihan": ["3", "4", "5", "6", "7"],
            "kunci": "C"
        },
        {
            "id": 175,
            "soal": "Pola: 9, 18, 36, 72, ...\nAngka berikutnya?",
            "pilihan": ["90", "120", "144", "150", "200"],
            "kunci": "C"
        },
        {
            "id": 176,
            "soal": "\"Horizontal\" berlawanan dengan:",
            "pilihan": ["Diagonal", "Lurus", "Vertikal", "Kecil", "Dalam"],
            "kunci": "C"
        },
        {
            "id": 177,
            "soal": "Pola: 3, 8, 15, 24, ...\nAngka berikutnya?",
            "pilihan": ["30", "33", "35", "36", "40"],
            "kunci": "B"
        },
        {
            "id": 178,
            "soal": "Semua siswa memakai seragam. Tono tidak memakai seragam.",
            "pilihan": ["Tono siswa", "Tono bukan siswa", "Tono mungkin siswa", "Semua siswa salah", "Tidak dapat disimpulkan"],
            "kunci": "B"
        },
        {
            "id": 179,
            "soal": "Pola: 5, 15, 30, 50, 75, ...",
            "pilihan": ["90", "100", "105", "110", "120"],
            "kunci": "C"
        },
        {
            "id": 180,
            "soal": "Pola: 11, 22, 44, 88, ...",
            "pilihan": ["99", "122", "132", "144", "176"],
            "kunci": "E"
        },
        {
            "id": 181,
            "soal": "Pola: 14, 12, 9, 5, ...",
            "pilihan": ["0", "1", "2", "3", "4"],
            "kunci": "D"
        },
        {
            "id": 182,
            "soal": "Mana yang berbeda?",
            "pilihan": ["Meja", "Kursi", "Lemari", "Kipas", "Ranjang"],
            "kunci": "D"
        },
        {
            "id": 183,
            "soal": "Jika 5 → 25, 6 → 36, 7 → 49, maka 9 → ?",
            "pilihan": ["60", "72", "80", "81", "90"],
            "kunci": "D"
        },
        {
            "id": 184,
            "soal": "Pola: 4, 6, 10, 18, 34, ...",
            "pilihan": ["50", "58", "66", "70", "90"],
            "kunci": "C"
        },
        {
            "id": 185,
            "soal": "Pola: 100, 50, 25, ...",
            "pilihan": ["10", "12.5", "15", "20", "30"],
            "kunci": "B"
        },
        {
            "id": 186,
            "soal": "Jika 8 → 4 → 2 → 1, maka setelah 1 adalah:",
            "pilihan": ["0", "1", "2", "3", "Tidak ada"],
            "kunci": "E"
        },
        {
            "id": 187,
            "soal": "Pola: 17, 20, 26, 35, ...",
            "pilihan": ["45", "48", "50", "52", "55"],
            "kunci": "A"
        },
        {
            "id": 188,
            "soal": "Pola: 3, 5, 9, 17, 33, ...",
            "pilihan": ["50", "55", "57", "60", "65"],
            "kunci": "C"
        },
        {
            "id": 189,
            "soal": "Mana yang merupakan bentuk 3 dimensi?",
            "pilihan": ["Lingkaran", "Kubus", "Segitiga", "Persegi", "Garis"],
            "kunci": "B"
        },
        {
            "id": 190,
            "soal": "Pola: 6, 9, 18, 45, ...",
            "pilihan": ["60", "70", "80", "90", "100"],
            "kunci": "D"
        },
        {
            "id": 191,
            "soal": "Jika 1 → A, 2 → B, 3 → C, maka 26 → ?",
            "pilihan": ["X", "Y", "Z", "AA", "BB"],
            "kunci": "C"
        },
        {
            "id": 192,
            "soal": "Jika 40% dari X = 80, maka X adalah:",
            "pilihan": ["100", "150", "180", "200", "220"],
            "kunci": "D"
        },
        {
            "id": 193,
            "soal": "Pola: 9, 11, 15, 21, 29, ...",
            "pilihan": ["36", "38", "40", "42", "44"],
            "kunci": "C"
        },
        {
            "id": 194,
            "soal": "Pola: 2, 5, 10, 17, 26, ...",
            "pilihan": ["33", "34", "35", "36", "37"],
            "kunci": "A"
        },
        {
            "id": 195,
            "soal": "Mana yang tidak sejenis?",
            "pilihan": ["Pena", "Spidol", "Penggaris", "Krayon", "Pensil"],
            "kunci": "C"
        },
        {
            "id": 196,
            "soal": "Pola: 81, 27, 9, 3, ...",
            "pilihan": ["2", "1", "0", "0.5", "0.25"],
            "kunci": "A"
        },
        {
            "id": 197,
            "soal": "Pola: 20, 24, 33, 49, 74, ...",
            "pilihan": ["100", "105", "110", "115", "120"],
            "kunci": "C"
        },
        {
            "id": 198,
            "soal": "Mana yang sinonim dari 'cepat'?",
            "pilihan": ["Lambat", "Segera", "Damai", "Keras", "Ringan"],
            "kunci": "B"
        },
        {
            "id": 199,
            "soal": "Jika semua burung berkicau, dan hewan ini berkicau:",
            "pilihan": ["Pasti burung", "Belum tentu burung", "Tidak mungkin burung", "Bukan burung", "Tidak ada hubungan"],
            "kunci": "B"
        },
        {
            "id": 200,
            "soal": "Pola: 8, 16, 32, 64, ...",
            "pilihan": ["90", "100", "120", "128", "140"],
            "kunci": "D"
        },
        {
            "id": 201,
            "soal": "Pola huruf: A, C, F, J, O, ... Huruf berikutnya?",
            "pilihan": ["U", "V", "W", "X", "Y"],
            "kunci": "A"
        },
        {
            "id": 202,
            "soal": "Jika 2 → 6, 3 → 12, 4 → 20, maka 5 → ?",
            "pilihan": ["25", "28", "30", "32", "35"],
            "kunci": "C"
        },
        {
            "id": 203,
            "soal": "Urutan angka: 11, 13, 17, 23, 31, ... Angka berikutnya?",
            "pilihan": ["37", "41", "43", "47", "53"],
            "kunci": "B"
        },
        {
            "id": 204,
            "soal": "Jika 'Kucing' → 6 huruf dan 'Harimau' → 7 huruf, maka 'Kanguru' → ?",
            "pilihan": ["5", "6", "7", "8", "9"],
            "kunci": "C"
        },
        {
            "id": 205,
            "soal": "Pola: 9 → 81, 7 → 49, 5 → 25, maka 11 → ?",
            "pilihan": ["99", "100", "110", "121", "140"],
            "kunci": "D"
        },
        {
            "id": 206,
            "soal": "Manakah yang berbeda sendiri?",
            "pilihan": ["Burung", "Kelelawar", "Ayam", "Pinguin", "Paus"],
            "kunci": "E"
        },
        {
            "id": 207,
            "soal": "Jika hari ini Rabu, 100 hari lagi adalah hari apa?",
            "pilihan": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "kunci": "E"
        },
        {
            "id": 208,
            "soal": "Temukan angka yang hilang: 4, 6, 9, 13, 18, ...",
            "pilihan": ["22", "23", "24", "25", "26"],
            "kunci": "C"
        },
        {
            "id": 209,
            "soal": "Pola: 2, 5, 11, 23, 47, ...",
            "pilihan": ["94", "95", "96", "97", "98"],
            "kunci": "B"
        },
        {
            "id": 210,
            "soal": "Manakah yang bukan bilangan prima?",
            "pilihan": ["2", "11", "17", "21", "23"],
            "kunci": "D"
        },
        {
            "id": 211,
            "soal": "Jika 12 → 21, 34 → 43, 56 → 65, maka 89 → ?",
            "pilihan": ["88", "89", "98", "99", "100"],
            "kunci": "C"
        },
        {
            "id": 212,
            "soal": "Pola: 3, 9, 27, 81, ...",
            "pilihan": ["162", "240", "243", "250", "300"],
            "kunci": "C"
        },
        {
            "id": 213,
            "soal": "Jika semua A adalah B, dan semua B adalah C, maka semua A adalah?",
            "pilihan": ["A", "C", "B", "Tidak pasti", "A dan C"],
            "kunci": "B"
        },
        {
            "id": 214,
            "soal": "Temukan yang paling berat: Kertas, Batu, Kapas, Besi, Daun.",
            "pilihan": ["Kertas", "Batu", "Kapas", "Besi", "Daun"],
            "kunci": "D"
        },
        {
            "id": 215,
            "soal": "Jika 1 = 2, 2 = 4, 4 = 16, 5 = ?",
            "pilihan": ["10", "15", "20", "25", "30"],
            "kunci": "D"
        },
        {
            "id": 216,
            "soal": "Pola: 50, 45, 41, 38, 36, ...",
            "pilihan": ["35", "34", "33", "32", "31"],
            "kunci": "A"
        },
        {
            "id": 217,
            "soal": "Apa lanjutan pola bentuk: ▲ ● ▲ ● ▲ ...?",
            "pilihan": ["●", "▲", "●●", "▲▲", "▲●"],
            "kunci": "A"
        },
        {
            "id": 218,
            "soal": "Pola: 7, 10, 15, 22, 31, ...",
            "pilihan": ["40", "41", "42", "43", "44"],
            "kunci": "C"
        },
        {
            "id": 219,
            "soal": "Jika jam menunjukkan pukul 3:15, sudut jarum jam dan menit?",
            "pilihan": ["0°", "7.5°", "12.5°", "15°", "18°"],
            "kunci": "B"
        },
        {
            "id": 220,
            "soal": "Mana yang berbeda: 16, 25, 36, 50, 49?",
            "pilihan": ["16", "25", "36", "50", "49"],
            "kunci": "D"
        },
        {
            "id": 221,
            "soal": "Jika B = 2, E = 5, J = 10, maka P = ?",
            "pilihan": ["14", "15", "16", "17", "18"],
            "kunci": "C"
        },
        {
            "id": 222,
            "soal": "Urutan: 100, 90, 81, 72, ...",
            "pilihan": ["60", "63", "65", "70", "75"],
            "kunci": "C"
        },
        {
            "id": 223,
            "soal": "Manakah yang merupakan sinonim dari 'cepat'?",
            "pilihan": ["Lambat", "Kilap", "Singkat", "Gesit", "Biasa"],
            "kunci": "D"
        },
        {
            "id": 224,
            "soal": "Jika 3 × (2 + 4) = 18, maka 5 × (1 + 3) = ?",
            "pilihan": ["10", "15", "20", "25", "30"],
            "kunci": "C"
        },
        {
            "id": 225,
            "soal": "Pola: 14, 28, 56, 112, ...",
            "pilihan": ["124", "152", "168", "224", "280"],
            "kunci": "D"
        },
        {
            "id": 226,
            "soal": "Jika 6 adalah 3, 9 adalah 4, 12 adalah 5, maka 15 adalah?",
            "pilihan": ["5", "6", "7", "8", "9"],
            "kunci": "B"
        },
        {
            "id": 227,
            "soal": "Pola: 1, 1, 2, 3, 5, 8, 13, ...",
            "pilihan": ["18", "19", "20", "21", "22"],
            "kunci": "D"
        },
        {
            "id": 228,
            "soal": "Manakah kelanjutan pola gambar: ■ ◆ ■ ◆ ■ ...",
            "pilihan": ["■", "◆", "■■", "◆◆", "■◆"],
            "kunci": "B"
        },
        {
            "id": 229,
            "soal": "Jika 4 ayam = 8 telur, maka 7 ayam = ?",
            "pilihan": ["12", "13", "14", "15", "16"],
            "kunci": "C"
        },
        {
            "id": 230,
            "soal": "Pola: 81, 27, 9, 3, ...",
            "pilihan": ["1", "1.5", "2", "3", "4"],
            "kunci": "A"
        },
        {
            "id": 231,
            "soal": "Bilangan ganjil berikutnya setelah 199 adalah?",
            "pilihan": ["200", "201", "202", "203", "205"],
            "kunci": "B"
        },
        {
            "id": 232,
            "soal": "Mana yang bukan hewan mamalia?",
            "pilihan": ["Sapi", "Kucing", "Paus", "Buaya", "Kelelawar"],
            "kunci": "D"
        },
        {
            "id": 233,
            "soal": "Jika 2 orang menyelesaikan tugas dalam 6 jam, berapa jam 3 orang?",
            "pilihan": ["2", "3", "4", "5", "6"],
            "kunci": "C"
        },
        {
            "id": 234,
            "soal": "Pola: 3, 5, 9, 17, 33, ...",
            "pilihan": ["48", "49", "50", "51", "65"],
            "kunci": "B"
        },
        {
            "id": 235,
            "soal": "Bentuk mana yang memiliki sisi paling banyak?",
            "pilihan": ["Segitiga", "Lingkaran", "Persegi", "Segi lima", "Segi enam"],
            "kunci": "E"
        },
        {
            "id": 236,
            "soal": "Jika 10% dari x adalah 5, maka x = ?",
            "pilihan": ["20", "25", "30", "40", "50"],
            "kunci": "E"
        },
        {
            "id": 237,
            "soal": "Urutan: B, D, G, K, P, ...",
            "pilihan": ["Q", "R", "S", "T", "U"],
            "kunci": "D"
        },
        {
            "id": 238,
            "soal": "Pola: 2, 3, 6, 18, ...",
            "pilihan": ["36", "48", "54", "60", "72"],
            "kunci": "C"
        },
        {
            "id": 239,
            "soal": "Manakah kelanjutan pola: 1A, 2B, 3C, 4D, ...",
            "pilihan": ["5A", "5B", "5C", "5D", "5E"],
            "kunci": "E"
        },
        {
            "id": 240,
            "soal": "Jika A = 1, C = 3, F = 6, maka J = ?",
            "pilihan": ["10", "11", "12", "13", "14"],
            "kunci": "A"
        },
        {
            "id": 241,
            "soal": "Pola: 101, 98, 94, 89, 83, ...",
            "pilihan": ["78", "77", "76", "75", "74"],
            "kunci": "A"
        },
        {
            "id": 242,
            "soal": "Mana yang paling ringan?",
            "pilihan": ["Batu", "Besi", "Emas", "Kertas", "Kayu"],
            "kunci": "D"
        },
        {
            "id": 243,
            "soal": "Jika 9 → 4, 25 → 5, 49 → 7, maka 64 → ?",
            "pilihan": ["6", "7", "8", "9", "10"],
            "kunci": "C"
        },
        {
            "id": 244,
            "soal": "Pola: 5, 7, 10, 14, 19, ...",
            "pilihan": ["24", "25", "26", "27", "28"],
            "kunci": "B"
        },
        {
            "id": 245,
            "soal": "Urutan: Z, X, U, Q, ...",
            "pilihan": ["N", "O", "P", "Q", "R"],
            "kunci": "A"
        },
        {
            "id": 246,
            "soal": "Jika 8 × 8 = 64, maka (8 × 8) ÷ 4 = ?",
            "pilihan": ["8", "12", "14", "16", "20"],
            "kunci": "D"
        },
        {
            "id": 247,
            "soal": "Berapa jumlah huruf pada kata 'Teknologi'?",
            "pilihan": ["7", "8", "9", "10", "11"],
            "kunci": "C"
        },
        {
            "id": 248,
            "soal": "Pola: 12, 18, 27, 40.5, ...",
            "pilihan": ["45", "50", "54", "60", "81"],
            "kunci": "D"
        },
        {
            "id": 249,
            "soal": "Jika 100% = 1, 50% = 0.5, 25% = 0.25, maka 12.5% = ?",
            "pilihan": ["0.10", "0.125", "0.15", "0.20", "0.25"],
            "kunci": "B"
        },
        {
            "id": 250,
            "soal": "Manakah kelanjutan pola: ○ △ △ ○ △ △ ○ ...",
            "pilihan": ["○", "△", "△△", "○○", "○△"],
            "kunci": "A"
        },
        {
            "id": 251,
            "soal": "Pola: 7, 14, 21, 28, ... Angka selanjutnya?",
            "pilihan": ["32", "34", "35", "36", "42"],
            "kunci": "C"
        },
        {
            "id": 252,
            "soal": "Jika 3 kotak berisi total 21 bola dan setiap kotak berisi jumlah sama, berapa bola per kotak?",
            "pilihan": ["5", "6", "7", "9", "12"],
            "kunci": "C"
        },
        {
            "id": 253,
            "soal": "Urutan huruf: B, D, G, K, P, ... huruf berikutnya?",
            "pilihan": ["R", "S", "T", "U", "V"],
            "kunci": "C"
        },
        {
            "id": 254,
            "soal": "Pola: 100, 50, 25, 12.5, ...",
            "pilihan": ["10.5", "6.25", "7.25", "8.5", "9.5"],
            "kunci": "B"
        },
        {
            "id": 255,
            "soal": "Jika semua A adalah B. Semua B adalah C. Maka:",
            "pilihan": ["Semua C adalah A", "Semua A adalah C", "Tidak ada hubungan", "Sebagian C bukan A", "A dan C tidak berkaitan"],
            "kunci": "B"
        },
        {
            "id": 256,
            "soal": "Pola: 4 → 16, 5 → 25, 8 → 64, 9 → 81. Maka 6 → ?",
            "pilihan": ["32", "34", "36", "38", "40"],
            "kunci": "C"
        },
        {
            "id": 257,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["apel", "mangga", "pisang", "jeruk", "wortel"],
            "kunci": "E"
        },
        {
            "id": 258,
            "soal": "Pola: 11, 13, 17, 19, 23, ...",
            "pilihan": ["25", "27", "29", "31", "33"],
            "kunci": "C"
        },
        {
            "id": 259,
            "soal": "Jika jam menunjukkan pukul 3:15, sudut antara jarum jam dan menit kira-kira?",
            "pilihan": ["0°", "7.5°", "15°", "30°", "37.5°"],
            "kunci": "E"
        },
        {
            "id": 260,
            "soal": "Pola: 1, 4, 9, 16, 25, ...",
            "pilihan": ["30", "35", "36", "40", "49"],
            "kunci": "C"
        },
        {
            "id": 261,
            "soal": "Jika 2 → 6, 3 → 12, 4 → 20, maka 5 → ?",
            "pilihan": ["25", "30", "35", "40", "45"],
            "kunci": "B"
        },
        {
            "id": 262,
            "soal": "Manakah yang tidak sejenis?",
            "pilihan": ["Senin", "Selasa", "April", "Kamis", "Jumat"],
            "kunci": "C"
        },
        {
            "id": 263,
            "soal": "Pola huruf: A, C, F, J, O, ...",
            "pilihan": ["Q", "R", "S", "T", "U"],
            "kunci": "C"
        },
        {
            "id": 264,
            "soal": "Urutan: 3, 6, 9, 18, 21, 42, 45, ...",
            "pilihan": ["48", "54", "63", "69", "90"],
            "kunci": "A"
        },
        {
            "id": 265,
            "soal": "Mana yang merupakan analogi benar? 'Air : Minum = Bahan bakar : ...'",
            "pilihan": ["Mobil", "Api", "Mesin", "Jalan", "Energi"],
            "kunci": "C"
        },
        {
            "id": 266,
            "soal": "Jika hari ini Rabu, 45 hari lagi hari apa?",
            "pilihan": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "kunci": "E"
        },
        {
            "id": 267,
            "soal": "Bilangan ganjil sebelum 200 yang habis dibagi 5?",
            "pilihan": ["185", "195", "175", "165", "155"],
            "kunci": "B"
        },
        {
            "id": 268,
            "soal": "Jika 8 orang makan 8 kue dalam 8 menit. 4 orang makan 4 kue dalam berapa menit?",
            "pilihan": ["1", "4", "8", "12", "16"],
            "kunci": "C"
        },
        {
            "id": 269,
            "soal": "Pola: 50, 45, 35, 20, ...",
            "pilihan": ["0", "5", "10", "15", "20"],
            "kunci": "C"
        },
        {
            "id": 270,
            "soal": "Manakah yang tidak terkait dengan empat lainnya?",
            "pilihan": ["Segitiga", "Bujur sangkar", "Persegi panjang", "Lingkaran", "Jajar genjang"],
            "kunci": "D"
        },
        {
            "id": 271,
            "soal": "Jika ∆ = 3, □ = 4, ○ = 5. Berapa hasil ∆ + □ × ○?",
            "pilihan": ["23", "27", "20", "32", "28"],
            "kunci": "A"
        },
        {
            "id": 272,
            "soal": "Pola: 2, 5, 11, 23, 47, ...",
            "pilihan": ["94", "95", "97", "99", "101"],
            "kunci": "A"
        },
        {
            "id": 273,
            "soal": "Berapa banyak sisi total dari 7 kubus?",
            "pilihan": ["28", "36", "42", "44", "48"],
            "kunci": "C"
        },
        {
            "id": 274,
            "soal": "Mana yang berbeda?",
            "pilihan": ["Meja", "Kursi", "Lemari", "Pintu", "Buku"],
            "kunci": "E"
        },
        {
            "id": 275,
            "soal": "Jika 15% dari X adalah 45, maka X?",
            "pilihan": ["200", "250", "300", "350", "400"],
            "kunci": "C"
        },
        {
            "id": 276,
            "soal": "Pola: 1, 1, 2, 3, 5, 8, ...",
            "pilihan": ["11", "12", "13", "14", "15"],
            "kunci": "C"
        },
        {
            "id": 277,
            "soal": "1 jam 45 menit = … menit",
            "pilihan": ["95", "100", "105", "110", "115"],
            "kunci": "C"
        },
        {
            "id": 278,
            "soal": "Pola: 9, 18, 20, 40, 42, ...",
            "pilihan": ["82", "84", "86", "88", "90"],
            "kunci": "A"
        },
        {
            "id": 279,
            "soal": "Urutan yang benar?",
            "pilihan": ["batu, kerikil, pasir", "pasir, kerikil, batu", "kerikil, pasir, batu", "batu, pasir, kerikil", "kerikil, batu, pasir"],
            "kunci": "A"
        },
        {
            "id": 280,
            "soal": "Jika 12 → 21, 13 → 31, maka 15 → ?",
            "pilihan": ["50", "51", "15", "55", "52"],
            "kunci": "B"
        },
        {
            "id": 281,
            "soal": "Mana yang merupakan lawan kata 'Optimis'?",
            "pilihan": ["Pesimis", "Realistis", "Netral", "Emosional", "Tegas"],
            "kunci": "A"
        },
        {
            "id": 282,
            "soal": "Berapa jumlah huruf dalam kata 'KONSISTENSI'?",
            "pilihan": ["10", "11", "12", "13", "14"],
            "kunci": "C"
        },
        {
            "id": 283,
            "soal": "Pola: 3, 9, 27, 81, ...",
            "pilihan": ["162", "243", "324", "486", "729"],
            "kunci": "B"
        },
        {
            "id": 284,
            "soal": "Mana yang berbeda?",
            "pilihan": ["Merah", "Kuning", "Hijau", "Biru", "Abu-abu"],
            "kunci": "E"
        },
        {
            "id": 285,
            "soal": "Berapa sisi total pada 12 segitiga?",
            "pilihan": ["24", "30", "36", "48", "60"],
            "kunci": "C"
        },
        {
            "id": 286,
            "soal": "Jika setengah dari angka adalah 12, angkanya?",
            "pilihan": ["20", "22", "24", "26", "28"],
            "kunci": "C"
        },
        {
            "id": 287,
            "soal": "Pola huruf: M, N, P, Q, S, ...",
            "pilihan": ["T", "U", "V", "W", "X"],
            "kunci": "A"
        },
        {
            "id": 288,
            "soal": "Jika 90° adalah sudut siku-siku, maka 45° adalah?",
            "pilihan": ["Lurus", "Tumpul", "Lancip", "Refleks", "Penuh"],
            "kunci": "C"
        },
        {
            "id": 289,
            "soal": "Pola: 15, 30, 27, 54, 51, ...",
            "pilihan": ["100", "102", "103", "105", "108"],
            "kunci": "B"
        },
        {
            "id": 290,
            "soal": "Jumlah bilangan ganjil dari 1–20?",
            "pilihan": ["10", "9", "11", "8", "12"],
            "kunci": "A"
        },
        {
            "id": 291,
            "soal": "Urutan: 8, 4, 4, 2, 2, 1, ...",
            "pilihan": ["1", "0.5", "2", "3", "0"],
            "kunci": "A"
        },
        {
            "id": 292,
            "soal": "Jika 5 = 20, 7 = 42, 9 = 72 maka 11 = ?",
            "pilihan": ["99", "110", "121", "132", "144"],
            "kunci": "D"
        },
        {
            "id": 293,
            "soal": "Manakah sinonim dari 'Stabil'?",
            "pilihan": ["Tetap", "Goyah", "Cepat", "Jatuh", "Aneh"],
            "kunci": "A"
        },
        {
            "id": 294,
            "soal": "Pola: 6, 12, 24, 48, ...",
            "pilihan": ["70", "80", "90", "96", "120"],
            "kunci": "D"
        },
        {
            "id": 295,
            "soal": "Jika X lebih besar dari Y, dan Y lebih besar dari Z. Maka:",
            "pilihan": ["Z terbesar", "X terkecil", "X terbesar", "Y terbesar", "Semua sama"],
            "kunci": "C"
        },
        {
            "id": 296,
            "soal": "Bilangan berikutnya: 4, 11, 25, 46, ...",
            "pilihan": ["65", "67", "70", "74", "78"],
            "kunci": "D"
        },
        {
            "id": 297,
            "soal": "Mana bentuk yang berbeda?",
            "pilihan": ["Kerucut", "Kubus", "Bola", "Balok", "Segitiga"],
            "kunci": "E"
        },
        {
            "id": 298,
            "soal": "Pola: 2, 3, 6, 18, ...",
            "pilihan": ["36", "48", "52", "54", "60"],
            "kunci": "A"
        },
        {
            "id": 299,
            "soal": "Jika 30% dari angka adalah 90, maka angka tersebut?",
            "pilihan": ["200", "250", "270", "300", "330"],
            "kunci": "D"
        },
        {
            "id": 300,
            "soal": "Manakah antonim dari 'Rendah hati'?",
            "pilihan": ["Baik", "Sombong", "Santai", "Bijak", "Tenang"],
            "kunci": "B"
        },
        {
            "id": 301,
            "soal": "Pola: 12, 24, 48, 96, ... Angka berikutnya?",
            "pilihan": ["120", "144", "160", "180", "192"],
            "kunci": "E"
        },
        {
            "id": 302,
            "soal": "Jika A = 1, B = 2, C = 3. Maka nilai kata 'BAD'?",
            "pilihan": ["5", "6", "7", "8", "9"],
            "kunci": "D"
        },
        {
            "id": 303,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Air", "Api", "Tanah", "Angin", "Plastik"],
            "kunci": "E"
        },
        {
            "id": 304,
            "soal": "Pola: 3, 8, 15, 24, ...",
            "pilihan": ["30", "33", "35", "36", "40"],
            "kunci": "C"
        },
        {
            "id": 305,
            "soal": "Urutan huruf: F, I, L, O, ...",
            "pilihan": ["Q", "R", "S", "T", "U"],
            "kunci": "D"
        },
        {
            "id": 306,
            "soal": "Jika 4 kotak berisi 28 apel. Berapa apel dalam 7 kotak?",
            "pilihan": ["40", "42", "46", "49", "50"],
            "kunci": "D"
        },
        {
            "id": 307,
            "soal": "Pola: 101, 98, 94, 89, ...",
            "pilihan": ["84", "83", "82", "80", "79"],
            "kunci": "A"
        },
        {
            "id": 308,
            "soal": "Manakah sinonim dari 'Efisien'?",
            "pilihan": ["Cepat", "Hemat", "Tepat", "Bagus", "Rapi"],
            "kunci": "B"
        },
        {
            "id": 309,
            "soal": "Jika 2 → 8, 3 → 18, 4 → 32, maka 5 → ?",
            "pilihan": ["40", "45", "48", "50", "55"],
            "kunci": "C"
        },
        {
            "id": 310,
            "soal": "Pola: 5, 12, 19, 26, ...",
            "pilihan": ["31", "32", "33", "34", "35"],
            "kunci": "B"
        },
        {
            "id": 311,
            "soal": "Jika 'cepat' berlawanan dengan 'lambat', maka 'kuat' berlawanan dengan?",
            "pilihan": ["Ringan", "Lemah", "Keras", "Berat", "Tinggi"],
            "kunci": "B"
        },
        {
            "id": 312,
            "soal": "Jumlah sisi dari 5 prisma segitiga?",
            "pilihan": ["18", "20", "25", "30", "35"],
            "kunci": "D"
        },
        {
            "id": 313,
            "soal": "Pola huruf: Z, W, T, Q, ...",
            "pilihan": ["N", "O", "P", "M", "L"],
            "kunci": "A"
        },
        {
            "id": 314,
            "soal": "Jika 25% dari X adalah 75, maka X?",
            "pilihan": ["150", "200", "250", "300", "350"],
            "kunci": "D"
        },
        {
            "id": 315,
            "soal": "Pola: 2, 7, 14, 23, 34, ...",
            "pilihan": ["42", "45", "46", "47", "48"],
            "kunci": "C"
        },
        {
            "id": 316,
            "soal": "Manakah yang bukan bilangan prima?",
            "pilihan": ["11", "13", "17", "21", "23"],
            "kunci": "D"
        },
        {
            "id": 317,
            "soal": "Pola: 9, 7, 5, 3, ...",
            "pilihan": ["0", "1", "2", "3", "4"],
            "kunci": "B"
        },
        {
            "id": 318,
            "soal": "Jika 16 → 4, 36 → 6, 49 → 7, maka 81 → ?",
            "pilihan": ["8", "9", "7", "6", "10"],
            "kunci": "A"
        },
        {
            "id": 319,
            "soal": "Urutan angka: 10, 15, 22, 31, ...",
            "pilihan": ["40", "41", "42", "43", "44"],
            "kunci": "A"
        },
        {
            "id": 320,
            "soal": "Manakah yang bukan hewan mamalia?",
            "pilihan": ["Kucing", "Sapi", "Ular", "Paus", "Kelelawar"],
            "kunci": "C"
        },
        {
            "id": 321,
            "soal": "Jika 7 + 3 = 25 dan 4 + 2 = 12, maka 6 + 5 = ?",
            "pilihan": ["30", "33", "40", "45", "50"],
            "kunci": "B"
        },
        {
            "id": 322,
            "soal": "Apa lanjutan dari pola: 100, 95, 90, 85, ...?",
            "pilihan": ["80", "78", "82", "75", "70"],
            "kunci": "A"
        },
        {
            "id": 323,
            "soal": "Pola: 2, 3, 5, 8, 12, 17, ...",
            "pilihan": ["21", "22", "23", "24", "25"],
            "kunci": "B"
        },
        {
            "id": 324,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Perak", "Emas", "Timah", "Perunggu", "Kertas"],
            "kunci": "E"
        },
        {
            "id": 325,
            "soal": "Jika kebalikannya malam adalah siang, maka kebalikannya utara adalah?",
            "pilihan": ["Timur", "Barat", "Selatan", "Tengah", "Bawah"],
            "kunci": "C"
        },
        {
            "id": 326,
            "soal": "Pola bentuk: segitiga, segiempat, segilima, ...",
            "pilihan": ["segienam", "segidelapan", "segitujuh", "lingkaran", "kubus"],
            "kunci": "A"
        },
        {
            "id": 327,
            "soal": "Jika 3 × 5 = 23 dan 4 × 6 = 34, maka 5 × 7 = ?",
            "pilihan": ["40", "41", "42", "43", "44"],
            "kunci": "B"
        },
        {
            "id": 328,
            "soal": "Pola: 4, 9, 16, 25, ...",
            "pilihan": ["30", "31", "32", "35", "36"],
            "kunci": "E"
        },
        {
            "id": 329,
            "soal": "Urutan huruf: H, J, M, Q, ...",
            "pilihan": ["R", "S", "T", "U", "V"],
            "kunci": "D"
        },
        {
            "id": 330,
            "soal": "Jika setengah dari X adalah 45, maka X?",
            "pilihan": ["70", "80", "85", "90", "100"],
            "kunci": "D"
        },
        {
            "id": 331,
            "soal": "Pola: 6, 13, 27, 55, ...",
            "pilihan": ["110", "111", "112", "113", "115"],
            "kunci": "A"
        },
        {
            "id": 332,
            "soal": "Mana yang tidak berhubungan?",
            "pilihan": ["Hidrogen", "Oksigen", "Nitrogen", "Karbon", "Kayu"],
            "kunci": "E"
        },
        {
            "id": 333,
            "soal": "Jika garis panjang 12 dipotong menjadi 3 bagian sama. Panjang tiap bagian?",
            "pilihan": ["2", "3", "4", "5", "6"],
            "kunci": "C"
        },
        {
            "id": 334,
            "soal": "Pola: 3, 5, 9, 17, 33, ...",
            "pilihan": ["48", "49", "57", "65", "66"],
            "kunci": "D"
        },
        {
            "id": 335,
            "soal": "Jika 2 jam = 120 menit, maka 5 jam 30 menit = ... menit",
            "pilihan": ["300", "310", "330", "350", "360"],
            "kunci": "C"
        },
        {
            "id": 336,
            "soal": "Manakah yang merupakan antonim dari 'Teratur'?",
            "pilihan": ["Rapi", "Tertata", "Kacau", "Tersusun", "Baik"],
            "kunci": "C"
        },
        {
            "id": 337,
            "soal": "Urutan angka: 20, 18, 15, 11, ...",
            "pilihan": ["8", "7", "6", "5", "4"],
            "kunci": "A"
        },
        {
            "id": 338,
            "soal": "Jika 8 kotak berisi 64 bola. Berapa bola dalam 3 kotak?",
            "pilihan": ["20", "21", "22", "23", "24"],
            "kunci": "E"
        },
        {
            "id": 339,
            "soal": "Pola: 1, 3, 7, 15, 31, ...",
            "pilihan": ["45", "47", "49", "63", "65"],
            "kunci": "D"
        },
        {
            "id": 340,
            "soal": "Huruf berikutnya: A, E, I, M, Q, ...",
            "pilihan": ["S", "T", "U", "V", "W"],
            "kunci": "D"
        },
        {
            "id": 341,
            "soal": "Jika X = 10, Y = 20. Maka (X + Y) × 2?",
            "pilihan": ["40", "50", "60", "70", "80"],
            "kunci": "E"
        },
        {
            "id": 342,
            "soal": "Pola: 30, 27, 21, 12, ...",
            "pilihan": ["10", "8", "6", "4", "3"],
            "kunci": "C"
        },
        {
            "id": 343,
            "soal": "Manakah yang bukan warna primer?",
            "pilihan": ["Merah", "Biru", "Hijau", "Kuning", "Hitam"],
            "kunci": "E"
        },
        {
            "id": 344,
            "soal": "Jika 6 = 42, 5 = 30, 4 = 20, maka 7 = ?",
            "pilihan": ["48", "49", "50", "52", "56"],
            "kunci": "A"
        },
        {
            "id": 345,
            "soal": "Pola: 8, 11, 17, 26, ...",
            "pilihan": ["34", "35", "36", "37", "38"],
            "kunci": "D"
        },
        {
            "id": 346,
            "soal": "Jika 100% = penuh, maka 50% = ...",
            "pilihan": ["Kosong", "Seperempat", "Setengah", "Tiga per empat", "Penuh"],
            "kunci": "C"
        },
        {
            "id": 347,
            "soal": "Pola: 21, 18, 14, 9, ...",
            "pilihan": ["4", "5", "6", "7", "8"],
            "kunci": "B"
        },
        {
            "id": 348,
            "soal": "Jika √144 = 12, maka √169 = ?",
            "pilihan": ["10", "11", "12", "13", "14"],
            "kunci": "D"
        },
        {
            "id": 349,
            "soal": "Pola: 2, 4, 7, 11, 16, ...",
            "pilihan": ["20", "21", "22", "23", "24"],
            "kunci": "B"
        },
        {
            "id": 350,
            "soal": "Manakah antonim dari 'Tinggi'?",
            "pilihan": ["Lebar", "Dalam", "Rendah", "Kecil", "Kuat"],
            "kunci": "C"
        },
        {
            "id": 351,
            "soal": "Pola: 4, 12, 36, 108, ... Berapa angka selanjutnya?",
            "pilihan": ["216", "324", "432", "648", "1296"],
            "kunci": "B"
        },
        {
            "id": 352,
            "soal": "Jika 'KUCING' = 6 huruf dan 'ULAR' = 4 huruf, maka 'KOMPUTER' = ?",
            "pilihan": ["5", "7", "8", "9", "10"],
            "kunci": "C"
        },
        {
            "id": 353,
            "soal": "Pola: 3 → 9, 4 → 16, 5 → 25, 7 → 49. Lalu 8 → ?",
            "pilihan": ["56", "60", "64", "72", "81"],
            "kunci": "C"
        },
        {
            "id": 354,
            "soal": "Jika hari ini hari Rabu, 100 hari lagi jatuh pada hari?",
            "pilihan": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "kunci": "B"
        },
        {
            "id": 355,
            "soal": "Manakah yang berbeda? 14, 28, 42, 54, 70",
            "pilihan": ["14", "28", "42", "54", "70"],
            "kunci": "D"
        },
        {
            "id": 356,
            "soal": "Pola jam: 2:10 → 4:20 → 8:40 → ...",
            "pilihan": ["10:00", "11:20", "16:80", "16:00", "20:20"],
            "kunci": "D"
        },
        {
            "id": 357,
            "soal": "Segitiga punya 3 sisi, persegi punya 4 sisi. Maka segilima punya?",
            "pilihan": ["3", "4", "5", "6", "7"],
            "kunci": "C"
        },
        {
            "id": 358,
            "soal": "Pola: 11, 13, 17, 19, 23, ...",
            "pilihan": ["25", "27", "29", "31", "33"],
            "kunci": "C"
        },
        {
            "id": 359,
            "soal": "Mana yang paling berat?",
            "pilihan": ["1 kg kapas", "1 kg besi", "1 kg pasir", "Sama berat", "Tidak ada"],
            "kunci": "D"
        },
        {
            "id": 360,
            "soal": "Jika 5 burung di pohon, 2 terbang. Berapa tersisa?",
            "pilihan": ["3", "4", "5", "0", "1"],
            "kunci": "A"
        },
        {
            "id": 361,
            "soal": "Pola: 81, 27, 9, 3, ...",
            "pilihan": ["1", "2", "3", "9", "27"],
            "kunci": "A"
        },
        {
            "id": 362,
            "soal": "Lala lebih tinggi dari Lili, Lili lebih tinggi dari Lolo. Siapa paling pendek?",
            "pilihan": ["Lala", "Lili", "Lolo", "Tidak tahu", "Semua sama"],
            "kunci": "C"
        },
        {
            "id": 363,
            "soal": "Pola: 1, 4, 9, 16, 25, ...",
            "pilihan": ["30", "35", "36", "49", "64"],
            "kunci": "C"
        },
        {
            "id": 364,
            "soal": "Jika 7+7=14, 7×7=49, maka 7² = ?",
            "pilihan": ["7", "14", "21", "49", "56"],
            "kunci": "D"
        },
        {
            "id": 365,
            "soal": "Mana yang berbeda? Kucing, Singa, Anjing, Harimau, Macan",
            "pilihan": ["Kucing", "Singa", "Anjing", "Harimau", "Macan"],
            "kunci": "C"
        },
        {
            "id": 366,
            "soal": "Pola: A=1, B=2, ..., Z=26. Maka J+E = ?",
            "pilihan": ["10", "11", "15", "20", "25"],
            "kunci": "C"
        },
        {
            "id": 367,
            "soal": "Dalam 1 kotak ada 8 apel. 3 dimakan. Berapa sisa?",
            "pilihan": ["3", "4", "5", "6", "8"],
            "kunci": "D"
        },
        {
            "id": 368,
            "soal": "Pola: 10 → 7, 20 → 17, 30 → 27. Maka 50 → ?",
            "pilihan": ["47", "50", "43", "40", "37"],
            "kunci": "A"
        },
        {
            "id": 369,
            "soal": "Andi berlari lebih cepat dari Budi. Budi lebih cepat dari Deni. Siapa paling lambat?",
            "pilihan": ["Andi", "Budi", "Deni", "Tidak tahu", "Semua sama"],
            "kunci": "C"
        },
        {
            "id": 370,
            "soal": "Pola: 100, 90, 72, 48, ...",
            "pilihan": ["44", "36", "24", "12", "8"],
            "kunci": "C"
        },
        {
            "id": 371,
            "soal": "Mana yang terbesar?",
            "pilihan": ["0.9", "0.99", "0.909", "0.9099", "0.999"],
            "kunci": "E"
        },
        {
            "id": 372,
            "soal": "Jika 1 minggu = 7 hari, maka 3 minggu = ?",
            "pilihan": ["10", "14", "17", "21", "24"],
            "kunci": "D"
        },
        {
            "id": 373,
            "soal": "Pola: 2, 5, 10, 17, 26, ...",
            "pilihan": ["35", "36", "37", "38", "39"],
            "kunci": "A"
        },
        {
            "id": 374,
            "soal": "Hewan mana yang tidak bisa terbang?",
            "pilihan": ["Burung Pipit", "Kelelawar", "Ayam", "Merpati", "Elang"],
            "kunci": "C"
        },
        {
            "id": 375,
            "soal": "Pola: 1/2, 1/4, 1/8, 1/16, ...",
            "pilihan": ["1/20", "1/24", "1/28", "1/32", "1/64"],
            "kunci": "D"
        },
        {
            "id": 376,
            "soal": "Jika 2 anak menghabiskan 2 roti dalam 2 jam, maka 4 anak menghabiskan 4 roti dalam?",
            "pilihan": ["2 jam", "4 jam", "1 jam", "3 jam", "Tidak tahu"],
            "kunci": "A"
        },
        {
            "id": 377,
            "soal": "Pola: 7, 14, 21, 28, ...",
            "pilihan": ["30", "32", "35", "36", "40"],
            "kunci": "C"
        },
        {
            "id": 378,
            "soal": "Jika 2 liter air dituangkan ke wadah 1 liter...",
            "pilihan": ["Penuh", "Tumpah", "Setengah", "Kosong", "Menghilang"],
            "kunci": "B"
        },
        {
            "id": 379,
            "soal": "Pola: 5 → 120, 4 → 24, 3 → 6, 2 → 2. Maka 6 → ?",
            "pilihan": ["240", "360", "720", "840", "1200"],
            "kunci": "C"
        },
        {
            "id": 380,
            "soal": "Jika A=1, B=2, Z=26, maka X = ?",
            "pilihan": ["22", "23", "24", "25", "26"],
            "kunci": "D"
        },
        {
            "id": 381,
            "soal": "Pola: 20, 19, 17, 14, ...",
            "pilihan": ["10", "9", "8", "7", "6"],
            "kunci": "C"
        },
        {
            "id": 382,
            "soal": "Ada 3 kotak apel, masing-masing 10. 5 apel busuk dari setiap kotak. Sisa total?",
            "pilihan": ["10", "15", "20", "25", "30"],
            "kunci": "C"
        },
        {
            "id": 383,
            "soal": "Pola: 1 → 3, 2 → 6, 3 → 9, 4 → 12. Maka 6 → ?",
            "pilihan": ["12", "15", "18", "20", "24"],
            "kunci": "C"
        },
        {
            "id": 384,
            "soal": "Siapa yang lahir duluan?",
            "pilihan": ["Kakak", "Adik", "Ayah", "Ibu", "Kakek"],
            "kunci": "E"
        },
        {
            "id": 385,
            "soal": "Pola: 2, 4, 12, 48, ...",
            "pilihan": ["96", "144", "192", "240", "288"],
            "kunci": "C"
        },
        {
            "id": 386,
            "soal": "Pola: 17, 15, 12, 8, ...",
            "pilihan": ["3", "4", "5", "6", "7"],
            "kunci": "D"
        },
        {
            "id": 387,
            "soal": "Mana yang paling besar?",
            "pilihan": ["√16", "√25", "√36", "√49", "√64"],
            "kunci": "E"
        },
        {
            "id": 388,
            "soal": "Jika 10 orang makan 10 roti dalam 10 menit, maka 20 orang makan 20 roti dalam?",
            "pilihan": ["10 menit", "20 menit", "5 menit", "15 menit", "1 jam"],
            "kunci": "A"
        },
        {
            "id": 389,
            "soal": "Pola: 100, 50, 25, 12.5, ...",
            "pilihan": ["6.25", "7.5", "8", "9", "10"],
            "kunci": "A"
        },
        {
            "id": 390,
            "soal": "Mana yang berbeda? 9, 16, 25, 36, 49, 55",
            "pilihan": ["25", "36", "49", "55", "16"],
            "kunci": "D"
        },
        {
            "id": 391,
            "soal": "Pola: 3, 6, 18, 72, ...",
            "pilihan": ["144", "216", "288", "360", "420"],
            "kunci": "C"
        },
        {
            "id": 392,
            "soal": "Mana yang lebih kecil?",
            "pilihan": ["0.2", "0.15", "0.25", "0.3", "0.1"],
            "kunci": "E"
        },
        {
            "id": 393,
            "soal": "Pola: 22, 20, 17, 13, ...",
            "pilihan": ["10", "9", "8", "7", "6"],
            "kunci": "A"
        },
        {
            "id": 394,
            "soal": "Jika semua A adalah B, dan semua B adalah C, maka semua A adalah?",
            "pilihan": ["D", "C", "B", "Tidak tahu", "A"],
            "kunci": "B"
        },
        {
            "id": 395,
            "soal": "Pola: 4, 7, 11, 16, 22, ...",
            "pilihan": ["27", "28", "29", "30", "32"],
            "kunci": "B"
        },
        {
            "id": 396,
            "soal": "Di mana angka 0 berada pada garis angka?",
            "pilihan": ["Kanan", "Kiri", "Tengah", "Atas", "Bawah"],
            "kunci": "C"
        },
        {
            "id": 397,
            "soal": "Pola: 1, 3, 6, 10, 15, ...",
            "pilihan": ["20", "21", "22", "24", "25"],
            "kunci": "B"
        },
        {
            "id": 398,
            "soal": "2 kg kapas dan 1 kg besi, mana yang lebih ringan?",
            "pilihan": ["Kapas", "Besi", "Sama saja", "Tidak ada", "Tergantung wadah"],
            "kunci": "B"
        },
        {
            "id": 399,
            "soal": "Pola: 8, 4, 2, 1, ...",
            "pilihan": ["0", "0.5", "2", "3", "4"],
            "kunci": "B"
        },
        {
            "id": 400,
            "soal": "Berapa jumlah huruf pada kata 'INTELIJENSI'?",
            "pilihan": ["8", "9", "10", "11", "12"],
            "kunci": "E"
        },
        {
            "id": 401,
            "soal": "Urutan: 3, 6, 12, 24, ... Angka berikutnya?",
            "pilihan": ["30", "36", "40", "48", "50"],
            "kunci": "D"
        },
        {
            "id": 402,
            "soal": "Jika 8 = 64, 6 = 36, 3 = 9, maka 9 = ...?",
            "pilihan": ["90", "99", "81", "72", "100"],
            "kunci": "C"
        },
        {
            "id": 403,
            "soal": "Pola huruf: A, C, F, J, O, ... Huruf berikutnya?",
            "pilihan": ["T", "U", "V", "W", "X"],
            "kunci": "B"
        },
        {
            "id": 404,
            "soal": "Jika hari ini Rabu, 100 hari lagi hari apa?",
            "pilihan": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"],
            "kunci": "E"
        },
        {
            "id": 405,
            "soal": "Urutan: 11, 14, 18, 23, 29, ... Angka berikutnya?",
            "pilihan": ["34", "35", "36", "37", "38"],
            "kunci": "C"
        },
        {
            "id": 406,
            "soal": "Berapa banyak sisi pada 5 segitiga?",
            "pilihan": ["10", "12", "15", "18", "20"],
            "kunci": "C"
        },
        {
            "id": 407,
            "soal": "Pola: 4 → 16, 5 → 25, 7 → 49, maka 9 → ...?",
            "pilihan": ["72", "80", "90", "81", "88"],
            "kunci": "D"
        },
        {
            "id": 408,
            "soal": "Jika 2 kucing menangkap 2 tikus dalam 2 menit, maka 10 kucing menangkap 10 tikus dalam ... menit?",
            "pilihan": ["1", "2", "5", "10", "20"],
            "kunci": "B"
        },
        {
            "id": 409,
            "soal": "Urutan: 21, 18, 15, 12, ... Angka berikutnya?",
            "pilihan": ["10", "9", "8", "7", "6"],
            "kunci": "B"
        },
        {
            "id": 410,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Kucing", "Harimau", "Singa", "Macan", "Burung"],
            "kunci": "E"
        },
        {
            "id": 411,
            "soal": "Jika 1 = 3, 2 = 3, 3 = 5, maka 4 = ...?",
            "pilihan": ["3", "4", "5", "6", "7"],
            "kunci": "B"
        },
        {
            "id": 412,
            "soal": "Pola: 50, 45, 41, 38, ... Angka berikutnya?",
            "pilihan": ["35", "34", "33", "32", "31"],
            "kunci": "A"
        },
        {
            "id": 413,
            "soal": "Berapa banyak huruf 'A' dalam kata 'ANAKANAKANAK'?",
            "pilihan": ["3", "4", "5", "6", "7"],
            "kunci": "D"
        },
        {
            "id": 414,
            "soal": "Urutan: 1, 4, 9, 16, ... Angka berikutnya?",
            "pilihan": ["20", "24", "25", "26", "30"],
            "kunci": "C"
        },
        {
            "id": 415,
            "soal": "Jam menunjukkan pukul 3. Jarum pendek dan jarum panjang membentuk sudut ...?",
            "pilihan": ["30°", "45°", "60°", "90°", "120°"],
            "kunci": "D"
        },
        {
            "id": 416,
            "soal": "Jika segitiga memiliki 3 sisi, maka 8 segitiga memiliki ... sisi.",
            "pilihan": ["16", "20", "22", "24", "26"],
            "kunci": "D"
        },
        {
            "id": 417,
            "soal": "Apa kelanjutan pola: RED, RRD, RRRD, ...?",
            "pilihan": ["RRRRD", "RRED", "RRDD", "RRRRED", "RRRRRED"],
            "kunci": "A"
        },
        {
            "id": 418,
            "soal": "Urutan: 2, 5, 11, 23, ... Angka berikutnya?",
            "pilihan": ["45", "47", "50", "55", "60"],
            "kunci": "B"
        },
        {
            "id": 419,
            "soal": "Berapakah setengah dari seperempat dari 100?",
            "pilihan": ["10", "12.5", "20", "25", "50"],
            "kunci": "B"
        },
        {
            "id": 420,
            "soal": "Jika S = 19, maka P = ...?",
            "pilihan": ["13", "14", "15", "16", "17"],
            "kunci": "D"
        },
        {
            "id": 421,
            "soal": "Urutan: 100, 90, 81, 73, ... Angka berikutnya?",
            "pilihan": ["66", "65", "64", "63", "62"],
            "kunci": "A"
        },
        {
            "id": 422,
            "soal": "Pola huruf: Z, X, U, Q, ... Huruf berikutnya?",
            "pilihan": ["N", "O", "P", "Q", "R"],
            "kunci": "A"
        },
        {
            "id": 423,
            "soal": "Urutan: 7, 14, 28, 56, ... Angka berikutnya?",
            "pilihan": ["80", "90", "100", "110", "112"],
            "kunci": "E"
        },
        {
            "id": 424,
            "soal": "Jika semua Burung bisa terbang dan Elang adalah burung, maka:",
            "pilihan": ["Elang tidak terbang", "Elang bisa terbang", "Elang reptil", "Elang ikan", "Elang menyusui"],
            "kunci": "B"
        },
        {
            "id": 425,
            "soal": "Urutan: 12, 15, 21, 30, ... Angka berikutnya?",
            "pilihan": ["37", "40", "42", "45", "48"],
            "kunci": "C"
        },
        {
            "id": 426,
            "soal": "Berapakah jumlah diagonal sisi pada segi enam?",
            "pilihan": ["6", "8", "9", "12", "15"],
            "kunci": "C"
        },
        {
            "id": 427,
            "soal": "Jika 4 jam = 240 menit, maka 7 jam = ... menit?",
            "pilihan": ["300", "360", "400", "420", "450"],
            "kunci": "D"
        },
        {
            "id": 428,
            "soal": "Manakah yang tidak termasuk?",
            "pilihan": ["2", "4", "6", "8", "9"],
            "kunci": "E"
        },
        {
            "id": 429,
            "soal": "Urutan: 40, 35, 31, 28, ... Angka berikutnya?",
            "pilihan": ["24", "25", "26", "27", "28"],
            "kunci": "B"
        },
        {
            "id": 430,
            "soal": "Jika A=1, B=2, Z=26, maka nilai J?",
            "pilihan": ["7", "8", "9", "10", "11"],
            "kunci": "D"
        },
        {
            "id": 431,
            "soal": "Urutan: 5, 8, 12, 17, ... Angka berikutnya?",
            "pilihan": ["21", "22", "23", "24", "25"],
            "kunci": "C"
        },
        {
            "id": 432,
            "soal": "Pola: 2 → 8, 3 → 27, 4 → 64, maka 5 → ...?",
            "pilihan": ["100", "115", "120", "125", "150"],
            "kunci": "D"
        },
        {
            "id": 433,
            "soal": "Mana yang merupakan bilangan prima?",
            "pilihan": ["21", "27", "33", "37", "42"],
            "kunci": "D"
        },
        {
            "id": 434,
            "soal": "Jika 1 hari = 24 jam, maka 2 minggu = ... jam?",
            "pilihan": ["200", "240", "300", "336", "400"],
            "kunci": "D"
        },
        {
            "id": 435,
            "soal": "Urutan: 14, 28, 42, 56, ... Angka berikutnya?",
            "pilihan": ["60", "62", "64", "68", "70"],
            "kunci": "E"
        },
        {
            "id": 436,
            "soal": "Berapa jumlah sudut segi lima?",
            "pilihan": ["360°", "450°", "540°", "720°", "900°"],
            "kunci": "C"
        },
        {
            "id": 437,
            "soal": "Urutan: B, E, H, K, ... Huruf berikutnya?",
            "pilihan": ["M", "N", "O", "P", "Q"],
            "kunci": "B"
        },
        {
            "id": 438,
            "soal": "Jika 20% dari X adalah 50, maka X = ...?",
            "pilihan": ["200", "220", "230", "240", "250"],
            "kunci": "E"
        },
        {
            "id": 439,
            "soal": "Pola: 81, 64, 49, 36, ... Angka berikutnya?",
            "pilihan": ["30", "28", "25", "24", "22"],
            "kunci": "C"
        },
        {
            "id": 440,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Segitiga", "Persegi", "Lingkaran", "Segi Lima", "Segi Enam"],
            "kunci": "C"
        },
        {
            "id": 441,
            "soal": "Urutan: 17, 13, 10, 8, ... Angka berikutnya?",
            "pilihan": ["6", "5", "4", "3", "2"],
            "kunci": "B"
        },
        {
            "id": 442,
            "soal": "Jika 100% = 1, maka 25% = ...?",
            "pilihan": ["0.1", "0.15", "0.20", "0.25", "0.30"],
            "kunci": "D"
        },
        {
            "id": 443,
            "soal": "Pola: 1, 3, 6, 10, ... Angka berikutnya?",
            "pilihan": ["12", "13", "14", "15", "16"],
            "kunci": "D"
        },
        {
            "id": 444,
            "soal": "Jika semua ikan hidup di air dan paus adalah mamalia, maka:",
            "pilihan": ["Paus ikan", "Paus hidup di darat", "Paus hidup di air", "Paus burung", "Paus reptil"],
            "kunci": "C"
        },
        {
            "id": 445,
            "soal": "Urutan: 3, 9, 27, 81, ... Angka berikutnya?",
            "pilihan": ["162", "200", "220", "240", "243"],
            "kunci": "E"
        },
        {
            "id": 446,
            "soal": "Berapakah jumlah huruf pada kata 'MATEMATIKA'?",
            "pilihan": ["8", "9", "10", "11", "12"],
            "kunci": "C"
        },
        {
            "id": 447,
            "soal": "Pola: 5, 10, 20, 40, ... Angka berikutnya?",
            "pilihan": ["60", "70", "80", "90", "100"],
            "kunci": "C"
        },
        {
            "id": 448,
            "soal": "Manakah hasil yang benar dari 3³?",
            "pilihan": ["6", "9", "12", "27", "30"],
            "kunci": "D"
        },
        {
            "id": 449,
            "soal": "Urutan: 90, 81, 73, 66, ... Angka berikutnya?",
            "pilihan": ["60", "59", "58", "57", "56"],
            "kunci": "A"
        },
        {
            "id": 450,
            "soal": "Jika 15 apel dibagi 3 orang sama rata, tiap orang mendapat?",
            "pilihan": ["3", "4", "5", "6", "7"],
            "kunci": "C"
        },
        {
            "id": 451,
            "soal": "Urutan: 6, 11, 17, 24, ... Angka berikutnya?",
            "pilihan": ["28", "30", "32", "33", "35"],
            "kunci": "C"
        },
        {
            "id": 452,
            "soal": "Jika 4 → 3, 6 → 5, 8 → 7, maka 10 → ...?",
            "pilihan": ["8", "7", "9", "10", "6"],
            "kunci": "C"
        },
        {
            "id": 453,
            "soal": "Pola huruf: C, F, J, O, ... Huruf berikutnya?",
            "pilihan": ["R", "S", "T", "U", "V"],
            "kunci": "D"
        },
        {
            "id": 454,
            "soal": "Jika 1 kotak berisi 4 bola, maka 7 kotak berisi ... bola?",
            "pilihan": ["24", "26", "28", "30", "32"],
            "kunci": "C"
        },
        {
            "id": 455,
            "soal": "Urutan: 90, 85, 81, 78, ... Angka berikutnya?",
            "pilihan": ["74", "75", "76", "77", "73"],
            "kunci": "B"
        },
        {
            "id": 456,
            "soal": "Pola: 3 → 27, 2 → 8, 4 → 64, maka 5 → ...?",
            "pilihan": ["100", "110", "115", "120", "125"],
            "kunci": "E"
        },
        {
            "id": 457,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Hati", "Ginjal", "Paru-paru", "Otak", "Meja"],
            "kunci": "E"
        },
        {
            "id": 458,
            "soal": "Urutan: 13, 18, 24, 31, ... Angka berikutnya?",
            "pilihan": ["35", "36", "37", "38", "39"],
            "kunci": "E"
        },
        {
            "id": 459,
            "soal": "Jika 8 × 3 = 24, maka 8 × 0.5 = ...?",
            "pilihan": ["2", "3", "4", "5", "6"],
            "kunci": "C"
        },
        {
            "id": 460,
            "soal": "Urutan: 2, 7, 22, 67, ... Angka berikutnya?",
            "pilihan": ["200", "201", "202", "205", "210"],
            "kunci": "C"
        },
        {
            "id": 461,
            "soal": "Pola huruf: B, D, G, K, ... Huruf berikutnya?",
            "pilihan": ["N", "O", "P", "Q", "R"],
            "kunci": "C"
        },
        {
            "id": 462,
            "soal": "Jika 12 dibagi 4 = 3, maka 48 dibagi 8 = ...?",
            "pilihan": ["4", "5", "6", "7", "8"],
            "kunci": "C"
        },
        {
            "id": 463,
            "soal": "Urutan: 20, 18, 15, 11, ... Angka berikutnya?",
            "pilihan": ["7", "8", "9", "10", "11"],
            "kunci": "B"
        },
        {
            "id": 464,
            "soal": "Manakah yang merupakan bilangan genap?",
            "pilihan": ["11", "13", "15", "17", "18"],
            "kunci": "E"
        },
        {
            "id": 465,
            "soal": "Urutan: 1, 4, 10, 19, ... Angka berikutnya?",
            "pilihan": ["25", "27", "28", "30", "31"],
            "kunci": "E"
        },
        {
            "id": 466,
            "soal": "Jika sebuah jam menunjukkan pukul 12:00, berapa derajat sudut jarum jam dan menit?",
            "pilihan": ["0°", "30°", "45°", "60°", "90°"],
            "kunci": "A"
        },
        {
            "id": 467,
            "soal": "Urutan: 3, 5, 8, 12, 17, ... berikutnya?",
            "pilihan": ["21", "22", "23", "24", "25"],
            "kunci": "C"
        },
        {
            "id": 468,
            "soal": "Jika A = 1, Z = 26, maka R = ...?",
            "pilihan": ["17", "18", "19", "20", "21"],
            "kunci": "B"
        },
        {
            "id": 469,
            "soal": "Pola: 5 → 20, 7 → 42, 9 → 72, maka 11 → ...?",
            "pilihan": ["100", "110", "121", "132", "144"],
            "kunci": "D"
        },
        {
            "id": 470,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Merah", "Biru", "Kuning", "Hijau", "Kucing"],
            "kunci": "E"
        },
        {
            "id": 471,
            "soal": "Urutan: 100, 97, 93, 88, ... Angka berikutnya?",
            "pilihan": ["82", "83", "84", "85", "86"],
            "kunci": "A"
        },
        {
            "id": 472,
            "soal": "Jika 50% dari X adalah 30, maka X = ...?",
            "pilihan": ["50", "55", "60", "65", "70"],
            "kunci": "C"
        },
        {
            "id": 473,
            "soal": "Pola huruf: A, E, I, M, ... Huruf berikutnya?",
            "pilihan": ["O", "P", "Q", "R", "S"],
            "kunci": "C"
        },
        {
            "id": 474,
            "soal": "Manakah yang merupakan bilangan prima?",
            "pilihan": ["21", "25", "31", "35", "39"],
            "kunci": "C"
        },
        {
            "id": 475,
            "soal": "Urutan: 4, 8, 15, 25, ... berikutnya?",
            "pilihan": ["30", "32", "34", "35", "36"],
            "kunci": "E"
        },
        {
            "id": 476,
            "soal": "Jika 9² = 81, maka 11² = ...?",
            "pilihan": ["100", "110", "120", "121", "130"],
            "kunci": "D"
        },
        {
            "id": 477,
            "soal": "Urutan: 8, 16, 32, 64, ... berikutnya?",
            "pilihan": ["100", "110", "120", "128", "140"],
            "kunci": "D"
        },
        {
            "id": 478,
            "soal": "Jika 1 jam = 60 menit, 3 jam 30 menit = ... menit?",
            "pilihan": ["180", "190", "200", "210", "220"],
            "kunci": "D"
        },
        {
            "id": 479,
            "soal": "Manakah yang berbeda?",
            "pilihan": ["Ayam", "Bebek", "Burung", "Ikan", "Kalkun"],
            "kunci": "D"
        },
        {
            "id": 480,
            "soal": "Urutan: 12, 20, 29, 39, ... berikutnya?",
            "pilihan": ["48", "49", "50", "51", "52"],
            "kunci": "C"
        },
        {
            "id": 481,
            "soal": "Jika 3 mobil memiliki total 12 ban, maka 8 mobil memiliki ... ban?",
            "pilihan": ["28", "29", "30", "32", "34"],
            "kunci": "D"
        },
        {
            "id": 482,
            "soal": "Huruf selanjutnya dari pola: Z, W, S, N, ...?",
            "pilihan": ["J", "K", "L", "M", "O"],
            "kunci": "A"
        },
        {
            "id": 483,
            "soal": "Jika 6 × 4 = 24, maka 0.5 × 12 = ...?",
            "pilihan": ["4", "5", "6", "7", "8"],
            "kunci": "C"
        },
        {
            "id": 484,
            "soal": "Urutan: 5, 11, 18, 26, ... berikutnya?",
            "pilihan": ["31", "33", "34", "35", "36"],
            "kunci": "D"
        },
        {
            "id": 485,
            "soal": "Jika 10% dari X adalah 7, maka X = ...?",
            "pilihan": ["60", "65", "68", "70", "75"],
            "kunci": "D"
        },
        {
            "id": 486,
            "soal": "Manakah yang bukan hewan?",
            "pilihan": ["Sapi", "Kambing", "Kuda", "Pohon", "Ayam"],
            "kunci": "D"
        },
        {
            "id": 487,
            "soal": "Urutan: 2, 6, 14, 30, ... berikutnya?",
            "pilihan": ["50", "54", "56", "62", "64"],
            "kunci": "D"
        },
        {
            "id": 488,
            "soal": "Jika 3⁴ = 81, maka 2⁵ = ...?",
            "pilihan": ["16", "20", "24", "30", "32"],
            "kunci": "E"
        },
        {
            "id": 489,
            "soal": "Pola huruf: H, L, Q, W, ...?",
            "pilihan": ["B", "C", "D", "E", "F"],
            "kunci": "A"
        },
        {
            "id": 490,
            "soal": "Jika 12 orang butuh 6 hari, maka 6 orang butuh ... hari?",
            "pilihan": ["6", "8", "10", "12", "18"],
            "kunci": "D"
        },
        {
            "id": 491,
            "soal": "Urutan: 72, 63, 55, 48, ... berikutnya?",
            "pilihan": ["40", "41", "42", "43", "44"],
            "kunci": "C"
        },
        {
            "id": 492,
            "soal": "Manakah hasil yang benar dari 4³?",
            "pilihan": ["16", "32", "48", "64", "96"],
            "kunci": "D"
        },
        {
            "id": 493,
            "soal": "Urutan: 9, 18, 36, 72, ... berikutnya?",
            "pilihan": ["100", "120", "135", "144", "150"],
            "kunci": "D"
        },
        {
            "id": 494,
            "soal": "Jika 7 = Tujuh, 9 = Sembilan, 11 = ...?",
            "pilihan": ["Sebelas", "Dua belas", "Sepuluh", "Lima", "Empat"],
            "kunci": "A"
        },
        {
            "id": 495,
            "soal": "Urutan: 101, 96, 92, 89, ... berikutnya?",
            "pilihan": ["85", "86", "87", "88", "90"],
            "kunci": "A"
        },
        {
            "id": 496,
            "soal": "Pola: 1, 2, 4, 7, 11, ... berikutnya?",
            "pilihan": ["14", "15", "16", "17", "18"],
            "kunci": "C"
        },
        {
            "id": 497,
            "soal": "Jika X = 24 dan Y = X ÷ 3, maka Y = ...?",
            "pilihan": ["6", "7", "8", "9", "10"],
            "kunci": "C"
        },
        {
            "id": 498,
            "soal": "Manakah angka ganjil?",
            "pilihan": ["10", "12", "15", "20", "22"],
            "kunci": "C"
        },
        {
            "id": 499,
            "soal": "Urutan: 3, 12, 48, 192, ... berikutnya?",
            "pilihan": ["300", "600", "700", "768", "800"],
            "kunci": "D"
        },
        {
            "id": 500,
            "soal": "Jika 100% = 1, maka 10% = ...?",
            "pilihan": ["0.1", "0.2", "0.25", "0.5", "0.75"],
            "kunci": "A"
        }
    ]

    # ============================
    # Persiapan pengguna
    # ============================

    # Nama
    print("\nSiapakah nama Anda?")
    nama_pengguna = input("Nama saya, ").strip()
    while nama_pengguna == "":
        print("Nama tidak valid. Silakan masukkan nama yang benar.")
        print("Siapakah nama Anda?")
        nama_pengguna = input("Nama saya, ").strip()

    # Umur (validasi sederhana)
    def input_umur(prompt="Saya berumur "):
        while True:
            try:
                val = input(prompt).strip()
                umur = int(val)
                if umur <= 0 or umur > 120:
                    print("Umur tidak valid. Silakan masukkan umur yang benar (1-120).")
                    continue
                return umur
            except ValueError:
                print("Masukkan angka bulat untuk umur (contoh: 17).")

    print("Halo, " + nama_pengguna + "! Senang bertemu dengan Anda.")
    print("Berapa umur Anda?")
    umur_pengguna = input_umur()

    print("Terima kasih, " + nama_pengguna + ". Umur Anda adalah " + str(umur_pengguna) + " tahun.\n")
    print_tengah("----------------------------------------------------------------------------------------------------")

    # Konfirmasi mulai aplikasi
    print("\nApakah Anda benar-benar ingin memakai program tes IQ?")
    mulai_tes_iq = input("(Ya atau Tidak): ").strip().lower()
    while mulai_tes_iq not in ("ya", "y", "tidak", "t"):
        print("Input tidak valid. Ketik 'ya atau y' untuk mulai atau 'tidak atau t' untuk keluar.")
        print("Apakah Anda benar-benar ingin memakai program tes IQ?")
        mulai_tes_iq = input("(Ya atau Tidak): ").strip().lower()
    
    if mulai_tes_iq in ("tidak", "t"):
        print("Baiklah, sampai jumpa lagi!\n")
        print_tengah("====================================================================================================")
        print("\nTekan apapun untuk menutup program atau terminal...")
        tutup_program = input("Tekan tombol apapun: ")
        sys.exit(0)
    else:
        print("Bagus! Sebelum itu, bacalah beberapa petunjuk pengerjaan di bawah ini.\n")

    # ============================
    # Logika Persiapan Tes
    # ============================
    # Ambil sample soal (Pastikan soal_list tidak kosong)
    jumlah_soal_ambil = min(len(soal_list), 50)
    if jumlah_soal_ambil == 0:
        print("Error: Daftar soal kosong. Mohon isi variabel soal_list.")
        sys.exit(1)
        
    soal_dipakai = random.sample(soal_list, jumlah_soal_ambil)

    # SETTING WAKTU (1 JAM)
    BATAS_WAKTU = 60 * 60  
    
    jawaban_user = {}
    skor = 0
    total_soal = len(soal_dipakai)

    print_tengah("====================================================================================================")
    print(" ")
    print_tengah("Petunjuk Pengerjaan\n")
    print("Anda akan memiliki 60 menit untuk menjawab semua soal.")
    print("Jawaban ketik A/B/C/D/E lalu tekan Enter.")
    print("Jika waktu habis, tes akan otomatis berhenti dan hasil akan dihitung.\n")
    print_tengah("Catatan Penting\n")
    print("Hasil poin IQ yang kelur adalah nilai perkiraan umum. Bukan standar internasional!\n")
    print_tengah("====================================================================================================")

    print("\nMulai tes?")
    mulai = input("(Ya atau Tidak): ").strip().lower()
    while mulai not in ("ya", "y", "tidak", "t"):
        print("Input tidak valid. Ketik 'ya atau y' untuk mulai atau 'tidak atau t' untuk keluar.")
        print("Mulai tes?")
        mulai = input("(Ya atau tidak): ").strip().lower()
    
    if mulai in ("tidak", "t"):
        print("Baiklah, sampai jumpa lagi!\n")
        print_tengah("====================================================================================================")
        print("\nTekan apapun untuk menutup program atau terminal...")
        tutup_program = input("Tekan tombol apapun: ")
        sys.exit(0)

    # ============================
    # START TIMER (THREADING)
    # ============================
    waktu_mulai = time.time()
    tes_selesai = False 

    def monitor_waktu():
        # Fungsi ini berjalan di background
        time.sleep(BATAS_WAKTU)
        # Jika bangun dan tes belum selesai, matikan program dan tampilkan hasil
        if not tes_selesai:
            lama = time.time() - waktu_mulai
            tampilkan_hasil(nama_pengguna, umur_pengguna, lama, total_soal, jawaban_user, soal_dipakai, skor, exit_program=True)
    
    timer_thread = threading.Thread(target=monitor_waktu)
    timer_thread.daemon = True
    timer_thread.start()

    print("\nTes Dimulai! Timer berjalan di latar belakang...\n")

    # ============================
    # LOOP PENGERJAAN SOAL
    # ============================
    for nomor, soal in enumerate(soal_dipakai, start=1):
        # Cek sisa waktu (Visual saja)
        sisa = BATAS_WAKTU - (time.time() - waktu_mulai)
        if sisa <= 0:
            break # Thread timer akan menangani exit-nya

        menit = int(sisa // 60)
        detik = int(sisa % 60)
        print_tengah("----------------------------------------------------------------------------------------------------")
        print_tengah(f"⏱ Sisa waktu: {menit} menit {detik} detik")
        print_tengah("----------------------------------------------------------------------------------------------------")
        print(f"\nSoal ke-{nomor}:")
        print(soal["soal"])
        for i, opsi in enumerate(soal["pilihan"]):
            label = chr(65 + i)
            print(f"  {label}. {opsi}")

        # Input jawaban
        valid = False
        jawaban = ""
        while not valid:
            # Input ini bersifat BLOCKING. Jika waktu habis di sini, Timer Thread yang akan mematikan program.
            jawaban = input("Jawaban Anda (A/B/C/D/E) [ketik 'exit' untuk berhenti]: ").strip().upper()
            
            if jawaban == "EXIT":
                print("Tes dihentikan oleh pengguna.")
                sisa = 0
                break
            if jawaban in ("A", "B", "C", "D", "E"):
                valid = True
            else:
                print("Input tidak valid. Masukkan huruf A, B, C, D, atau E.")

        if sisa <= 0 or jawaban == "EXIT":
            break

        jawaban_user[soal["id"]] = jawaban
        if "kunci" in soal and soal["kunci"].upper() == jawaban:
            skor += 1

        print() # Spasi antar soal

    # ============================
    # SELESAI NORMAL (USER FINISH)
    # ============================
    tes_selesai = True # Beritahu timer untuk tidak mematikan program
    waktu_selesai = time.time()
    lama_pakai = waktu_selesai - waktu_mulai
    if lama_pakai < 0: lama_pakai = 0

    # Tampilkan hasil (Mode normal, tidak exit)
    tampilkan_hasil(nama_pengguna, umur_pengguna, lama_pakai, total_soal, jawaban_user, soal_dipakai, skor, exit_program=False)

    # Konfirmasi Ulang
    print("Apakah anda ingin menggunakan program Tes IQ lagi?")
    pakai_lagi = input("(Ya atau tidak): \n").lower()
    while pakai_lagi not in ("ya", "y", "yes", "tidak", "t", "no", "n"):
        print("Input tidak valid.")
        pakai_lagi = input("(Ya atau tidak): \n").lower()
        
    if pakai_lagi in ("tidak", "t", "no", "n"):
        break

print_tengah("----------------------------------------------------------------------------------------------------")
print("\nTerima kasih telah mengikuti tes IQ kami. Semoga bermanfaat!\n")
print_tengah("====================================================================================================")
print("\nTekan apapun untuk menutup program atau terminal...")
tutup_program = input("Tekan tombol apapun: ")
