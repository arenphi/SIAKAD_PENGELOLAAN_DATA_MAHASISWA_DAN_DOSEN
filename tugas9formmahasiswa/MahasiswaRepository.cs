using System;
using System.Data;
using MySql.Data.MySqlClient;

namespace tugas9formmahasiswa
{
    // Model entity untuk Mahasiswa
    public class Mahasiswa
    {
        public string Nim { get; set; }
        public string Nama { get; set; }
        public string Prodi { get; set; }
        public int Angkatan { get; set; }
    }

    // Class Repository (Latihan Mandiri 5) untuk memisahkan logika akses database dari antarmuka
    public class MahasiswaRepository
    {
        public DataTable GetAll()
        {
            using (var conn = Koneksi.Buat())
            {
                string sql = "SELECT nim, nama, prodi, angkatan FROM mahasiswa ORDER BY nim";
                var adapter = new MySqlDataAdapter(sql, conn);
                var tabel = new DataTable();
                adapter.Fill(tabel);
                return tabel;
            }
        }

        public void Tambah(Mahasiswa m)
        {
            using (var conn = Koneksi.Buat())
            {
                conn.Open();
                string sql = "INSERT INTO mahasiswa (nim, nama, prodi, angkatan) VALUES (@nim, @nama, @prodi, @angkatan)";
                using (var cmd = new MySqlCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@nim", m.Nim);
                    cmd.Parameters.AddWithValue("@nama", m.Nama);
                    cmd.Parameters.AddWithValue("@prodi", m.Prodi);
                    cmd.Parameters.AddWithValue("@angkatan", m.Angkatan);
                    cmd.ExecuteNonQuery();
                }
            }
        }

        public int Ubah(Mahasiswa m)
        {
            using (var conn = Koneksi.Buat())
            {
                conn.Open();
                string sql = "UPDATE mahasiswa SET nama=@nama, prodi=@prodi, angkatan=@angkatan WHERE nim=@nim";
                using (var cmd = new MySqlCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@nama", m.Nama);
                    cmd.Parameters.AddWithValue("@prodi", m.Prodi);
                    cmd.Parameters.AddWithValue("@angkatan", m.Angkatan);
                    cmd.Parameters.AddWithValue("@nim", m.Nim);
                    return cmd.ExecuteNonQuery();
                }
            }
        }

        public int Hapus(string nim)
        {
            using (var conn = Koneksi.Buat())
            {
                conn.Open();
                string sql = "DELETE FROM mahasiswa WHERE nim=@nim";
                using (var cmd = new MySqlCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@nim", nim);
                    return cmd.ExecuteNonQuery();
                }
            }
        }

        public DataTable Cari(string kataKunci)
        {
            using (var conn = Koneksi.Buat())
            {
                string sql = "SELECT nim, nama, prodi, angkatan FROM mahasiswa WHERE nim LIKE @kata OR nama LIKE @kata ORDER BY nim";
                var adapter = new MySqlDataAdapter(sql, conn);
                adapter.SelectCommand.Parameters.AddWithValue("@kata", "%" + kataKunci + "%");
                var tabel = new DataTable();
                adapter.Fill(tabel);
                return tabel;
            }
        }

        public int HitungTotal()
        {
            using (var conn = Koneksi.Buat())
            {
                conn.Open();
                using (var cmd = new MySqlCommand("SELECT COUNT(*) FROM mahasiswa", conn))
                {
                    return Convert.ToInt32(cmd.ExecuteScalar());
                }
            }
        }
    }
}

