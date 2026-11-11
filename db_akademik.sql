-- ========================================================
-- Database: db_akademik
-- Modul Praktikum: Koneksi dan Pengelolaan Database (C# WinForms + MySQL)
-- ========================================================

CREATE DATABASE IF NOT EXISTS db_akademik;
USE db_akademik;

-- 1. Tabel Utama: mahasiswa (Praktikum Bagian I)
CREATE TABLE IF NOT EXISTS mahasiswa (
    nim VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    prodi VARCHAR(50),
    angkatan INT
);

-- Data Awal mahasiswa (Kode 1)
INSERT INTO mahasiswa (nim, nama, prodi, angkatan) VALUES
('2025001', 'Andi Pratama', 'Teknik Informatika', 2025),
('2025002', 'Siti Aisyah', 'Sistem Informasi', 2025),
('2024010', 'Budi Santoso', 'Teknik Industri', 2024)
ON DUPLICATE KEY UPDATE nama=VALUES(nama), prodi=VALUES(prodi), angkatan=VALUES(angkatan);

-- 2. Tabel Tambahan: dosen (Latihan Mandiri 1)
CREATE TABLE IF NOT EXISTS dosen (
    nidn VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    bidang VARCHAR(100)
);

INSERT INTO dosen (nidn, nama, bidang) VALUES
('0412018001', 'Dr. Muhamad Fatchan, S.Kom., M.Kom.', 'Pemrograman Visual & Kecerdasan Buatan'),
('0415088502', 'Ir. Hendra Wijaya, M.T.', 'Jaringan Komputer & Basis Data')
ON DUPLICATE KEY UPDATE nama=VALUES(nama), bidang=VALUES(bidang);

-- 3. Tabel Tambahan: prodi (Latihan Mandiri 3)
CREATE TABLE IF NOT EXISTS prodi (
    kode_prodi VARCHAR(10) PRIMARY KEY,
    nama_prodi VARCHAR(100) NOT NULL
);

INSERT INTO prodi (kode_prodi, nama_prodi) VALUES
('TIF', 'Teknik Informatika'),
('SIF', 'Sistem Informasi'),
('TIN', 'Teknik Industri'),
('TEL', 'Teknik Elektro'),
('MIF', 'Manajemen Informatika')
ON DUPLICATE KEY UPDATE nama_prodi=VALUES(nama_prodi);

-- 4. Tabel Tambahan: pengguna (Latihan Mandiri 4 - Form Login & Hash Password)
CREATE TABLE IF NOT EXISTS pengguna (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(100)
);

-- Kata sandi default: admin123 (contoh hash SHA256: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9)
INSERT INTO pengguna (username, password_hash, nama_lengkap) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrator Sistem')
ON DUPLICATE KEY UPDATE nama_lengkap=VALUES(nama_lengkap);
