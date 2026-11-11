# Sistem Informasi Akademik (Pengelolaan Data Mahasiswa & Dosen)

Aplikasi desktop modern untuk pengelolaan data akademik civitas kampus (Mahasiswa, Dosen, dan Program Studi) berbasis **C# Windows Forms (.NET Framework 4.7.2)** dan **MySQL**, dirancang menggunakan arsitektur **Pola Repositori (Repository Pattern)** dan antarmuka **Multi-Page Sidebar** yang elegan.

---

## 🌟 Fitur Utama

1. **Sistem Autentikasi Pengguna (Login Form)**
   - Validasi kredensial pengguna menggunakan *parameterized query* (anti SQL Injection).
   - Pengamanan kata sandi menggunakan enkripsi satu arah **SHA-256 Hash**.
   - Otomatis redirect kembali ke login jika pengguna melakukan *Logout*.

2. **Antarmuka Modern Multi-Page (Single-Form Sidebar)**
   - Navigasi bilah samping (*Slate Navy & Indigo Accent*) tanpa popup modal bertumpuk.
   - **📊 Dashboard Page:** Metrik ringkasan data *real-time* (Total Mahasiswa, Total Dosen, Total Prodi), *quick actions*, dan status sistem.
   - **🎓 Data Mahasiswa:** CRUD lengkap data mahasiswa, validasi NIM unik (Error code `1062`), pencarian langsung (*live search*), dan tombol **📥 Ekspor CSV**.
   - **👨‍🏫 Data Dosen:** CRUD mandiri untuk tenaga pengajar (NIDN, Nama, Bidang Keahlian) dan filter pencarian.
   - **🏛️ Program Studi:** Tabel referensi kode dan nama program studi dari database.

3. **Keandalan & Best Practices Arsitektur**
   - **Pola Repositori (`MahasiswaRepository.cs`):** Pemisahan tegas antara lapisan UI (*Presentation Layer*) dan lapisan akses data (*Data Access Layer*).
   - **Konfigurasi Terpusat (`App.config` & `Koneksi.cs`):** Pengelolaan *connection string* modular.
   - **Manajemen Sumber Daya Aman:** Pemanfaatan konstruksi `using` untuk mencegah kebocoran koneksi (*connection leak*).

---

## 🛠️ Teknologi & Prasyarat

- **Bahasa Pemrograman:** C# (.NET Framework 4.7.2)
- **GUI Framework:** Windows Forms (WinForms)
- **Database Driver:** `MySql.Data` v9.2.0 (NuGet)
- **Database Server:** MySQL 8.0+ / MariaDB 10.4+ (XAMPP Stack)
- **IDE:** Microsoft Visual Studio 2022

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Kloning Repositori
```bash
git clone https://github.com/arenphi/tugas9formmahasiswa.git
cd tugas9formmahasiswa
```

### 2. Konfigurasi Basis Data
1. Jalankan modul **MySQL** pada panel kontrol XAMPP.
2. Impor berkas [`db_akademik.sql`](./db_akademik.sql) ke MySQL:
   ```bash
   mysql -u root < db_akademik.sql
   ```
   *Skrip ini akan membuat database `db_akademik`, tabel `mahasiswa`, `dosen`, `prodi`, `pengguna`, serta menyuntikkan data sampel.*

### 3. Kompilasi & Jalankan Aplikasi
1. Buka solusi `tugas9formmahasiswa.slnx` atau proyek `tugas9formmahasiswa/tugas9formmahasiswa.csproj` di Visual Studio.
2. Tekan **F5** atau **Start**.
3. Atau jalankan langsung berkas hasil kompilasi:
   ```powershell
   .\tugas9formmahasiswa\bin\Debug\tugas9formmahasiswa.exe
   ```

### 4. Kredensial Masuk Baku (Default Login)
- **Username:** `admin`
- **Password:** `admin123`

---

## 📁 Struktur Direktori Proyek

```
tugas9formmahasiswa/
├── tugas9formmahasiswa/
│   ├── App.config                # Konfigurasi connection string basis data
│   ├── FormLogin.cs              # Antarmuka dialog autentikasi login (SHA-256)
│   ├── FormMahasiswa.cs          # Formulir utama multi-page sidebar
│   ├── FormDosen.cs              # Modul CRUD Dosen terpisah
│   ├── Koneksi.cs                # Factory koneksi terpusat MySQL
│   ├── MahasiswaRepository.cs    # Repositori data mahasiswa (DAL)
│   └── Program.cs                # Titik masuk aplikasi (Startup flow)
├── db_akademik.sql               # Skrip DDL & DML skema database
├── Laporan_Praktikum_Data_Mahasiswa_Revisi.docx # Dokumen laporan akademik lengkap
└── README.md                     # Dokumentasi repositori
```

---

## 📄 Dokumentasi Akademik

Laporan praktikum akademik lengkap (5 Bab standar akademik, tabel pengujian, pseudocode, analisis kinerja, dan pembuktian teoretis) disertakan dalam format Microsoft Word:
- [`Laporan_Praktikum_Data_Mahasiswa_Revisi.docx`](./Laporan_Praktikum_Data_Mahasiswa_Revisi.docx)
