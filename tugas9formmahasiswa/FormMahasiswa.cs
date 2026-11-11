using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace tugas9formmahasiswa
{
    public partial class FormMahasiswa : Form
    {
        // Status apakah pengguna mengklik Logout agar Program.cs dapat membuka kembali FormLogin
        public bool IsLogout { get; set; } = false;

        public FormMahasiswa()
        {
            InitializeComponent();
        }

        // Event Form Load: memuat data saat form pertama kali dibuka
        private void FormMahasiswa_Load(object sender, EventArgs e)
        {
            // Tampilkan halaman Data Mahasiswa sebagai halaman default (sesuai modul praktikum)
            TampilkanHalaman("mahasiswa");
            IsiComboProdi();
        }

        #region Sistem Navigasi Halaman (Mainstream Multi-Page Layout)

        private void TampilkanHalaman(string namaHalaman)
        {
            // Sembunyikan seluruh panel halaman
            pnlPageDashboard.Visible = false;
            pnlPageMahasiswa.Visible = false;
            pnlPageDosen.Visible = false;
            pnlPageProdi.Visible = false;

            // Reset warna tombol navigasi sidebar
            Color colorInactive = Color.Transparent;
            Color colorActive = Color.FromArgb(37, 99, 235); // Blue 600

            btnNavDashboard.BackColor = colorInactive;
            btnNavMahasiswa.BackColor = colorInactive;
            btnNavDosen.BackColor = colorInactive;
            btnNavProdi.BackColor = colorInactive;

            switch (namaHalaman.ToLower())
            {
                case "dashboard":
                    pnlPageDashboard.Visible = true;
                    btnNavDashboard.BackColor = colorActive;
                    lblPageTitle.Text = "Dashboard Ringkasan Sistem";
                    lblBreadcrumb.Text = "SIAKAD / Dashboard";
                    MuatStatistikDashboard();
                    break;

                case "mahasiswa":
                    pnlPageMahasiswa.Visible = true;
                    btnNavMahasiswa.BackColor = colorActive;
                    lblPageTitle.Text = "Pengelolaan Data Mahasiswa";
                    lblBreadcrumb.Text = "SIAKAD / Data Mahasiswa";
                    TampilData();
                    break;

                case "dosen":
                    pnlPageDosen.Visible = true;
                    btnNavDosen.BackColor = colorActive;
                    lblPageTitle.Text = "Pengelolaan Data Dosen";
                    lblBreadcrumb.Text = "SIAKAD / Data Dosen";
                    TampilDataDosen();
                    break;

                case "prodi":
                    pnlPageProdi.Visible = true;
                    btnNavProdi.BackColor = colorActive;
                    lblPageTitle.Text = "Daftar Program Studi";
                    lblBreadcrumb.Text = "SIAKAD / Program Studi";
                    TampilDataProdi();
                    break;
            }
        }

        private void BtnNavDashboard_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("dashboard");
        }

        private void BtnNavMahasiswa_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("mahasiswa");
        }

        private void BtnNavDosen_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("dosen");
        }

        private void BtnNavProdi_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("prodi");
        }

        private void BtnQuickMhs_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("mahasiswa");
        }

        private void BtnQuickDosen_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("dosen");
        }

        private void BtnQuickEkspor_Click(object sender, EventArgs e)
        {
            TampilkanHalaman("mahasiswa");
            BtnEkspor_Click(sender, e);
        }

        private void BtnNavLogout_Click(object sender, EventArgs e)
        {
            var tanya = MessageBox.Show(
                "Apakah Anda yakin ingin logout dari sistem?",
                "Konfirmasi Logout",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question);

            if (tanya == DialogResult.Yes)
            {
                this.IsLogout = true;
                this.Close();
            }
        }

        private void MuatStatistikDashboard()
        {
            int totalMhs = HitungMahasiswa();
            int totalDosen = HitungDosen();
            int totalProdi = HitungProdi();

            lblStatMhs.Text = totalMhs + " Data";
            lblStatDosen.Text = totalDosen + " Dosen";
            lblStatProdi.Text = totalProdi + " Prodi";
        }

        #endregion

        #region Modul Praktikum: Pengelolaan Data Mahasiswa (CRUD, Pencarian, Hitung)

        // Method memuat dan menampilkan data ke DataGridView (Kode 5)
        private void TampilData()
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    string sql = "SELECT nim, nama, prodi, angkatan FROM mahasiswa ORDER BY nim";
                    var adapter = new MySqlDataAdapter(sql, conn);
                    var tabel = new DataTable();
                    adapter.Fill(tabel); // Fill membuka dan menutup koneksi otomatis
                    dgvMahasiswa.DataSource = tabel;

                    // Mengatur Header Teks agar lebih rapi
                    if (dgvMahasiswa.Columns["nim"] != null) dgvMahasiswa.Columns["nim"].HeaderText = "NIM";
                    if (dgvMahasiswa.Columns["nama"] != null) dgvMahasiswa.Columns["nama"].HeaderText = "Nama Mahasiswa";
                    if (dgvMahasiswa.Columns["prodi"] != null) dgvMahasiswa.Columns["prodi"].HeaderText = "Program Studi";
                    if (dgvMahasiswa.Columns["angkatan"] != null) dgvMahasiswa.Columns["angkatan"].HeaderText = "Angkatan";
                }

                // Menampilkan jumlah data pada lblTotal (Kode 12 / Langkah 10)
                lblTotal.Text = "Total mahasiswa: " + HitungMahasiswa();
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal memuat data: " + ex.Message, "Kesalahan Koneksi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Method untuk menghitung jumlah total mahasiswa di database (Kode 12)
        private int HitungMahasiswa()
        {
            try
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
            catch
            {
                return 0;
            }
        }

        // Method membaca data program studi dari tabel prodi / mahasiswa (Kode 6 & Latihan 3)
        private void IsiComboProdi()
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "SELECT nama_prodi FROM prodi ORDER BY nama_prodi";
                    using (var cmd = new MySqlCommand(sql, conn))
                    using (var reader = cmd.ExecuteReader())
                    {
                        if (reader.HasRows)
                        {
                            cmbProdi.Items.Clear();
                            while (reader.Read())
                            {
                                cmbProdi.Items.Add(reader.GetString("nama_prodi"));
                            }
                            return;
                        }
                    }
                }
            }
            catch { }

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "SELECT DISTINCT prodi FROM mahasiswa WHERE prodi IS NOT NULL AND prodi != '' ORDER BY prodi";
                    using (var cmd = new MySqlCommand(sql, conn))
                    using (var reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            string item = reader.GetString("prodi");
                            if (!cmbProdi.Items.Contains(item))
                            {
                                cmbProdi.Items.Add(item);
                            }
                        }
                    }
                }
            }
            catch { }
        }

        // Method untuk membersihkan form input mahasiswa
        private void BersihkanForm()
        {
            txtNim.Clear();
            txtNama.Clear();
            txtAngkatan.Clear();
            cmbProdi.SelectedIndex = -1;
            cmbProdi.Text = string.Empty;
            txtNim.ReadOnly = false;
            txtNim.Focus();
        }

        // Event Click tombol Simpan Mahasiswa (Kode 7)
        private void BtnSimpan_Click(object sender, EventArgs e)
        {
            // 1. Validasi input
            if (string.IsNullOrWhiteSpace(txtNim.Text) || string.IsNullOrWhiteSpace(txtNama.Text))
            {
                MessageBox.Show("NIM dan Nama wajib diisi.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (!int.TryParse(txtAngkatan.Text, out int angkatan))
            {
                MessageBox.Show("Angkatan harus berupa angka.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            // 2. Simpan ke database
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "INSERT INTO mahasiswa (nim, nama, prodi, angkatan) VALUES (@nim, @nama, @prodi, @angkatan)";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@nim", txtNim.Text.Trim());
                        cmd.Parameters.AddWithValue("@nama", txtNama.Text.Trim());
                        cmd.Parameters.AddWithValue("@prodi", cmbProdi.Text.Trim());
                        cmd.Parameters.AddWithValue("@angkatan", angkatan);
                        cmd.ExecuteNonQuery();
                    }
                }

                MessageBox.Show("Data berhasil disimpan.", "Informasi",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                TampilData();
                BersihkanForm();
            }
            catch (MySqlException ex) when (ex.Number == 1062) // duplikat primary key
            {
                MessageBox.Show("NIM sudah terdaftar.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal menyimpan: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Event CellClick DataGridView Mahasiswa (Kode 8)
        private void DgvMahasiswa_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0) return; // abaikan klik pada header

            DataGridViewRow baris = dgvMahasiswa.Rows[e.RowIndex];
            if (baris.Cells["nim"].Value != null)
            {
                txtNim.Text = baris.Cells["nim"].Value.ToString();
                txtNama.Text = baris.Cells["nama"].Value?.ToString() ?? "";
                cmbProdi.Text = baris.Cells["prodi"].Value?.ToString() ?? "";
                txtAngkatan.Text = baris.Cells["angkatan"].Value?.ToString() ?? "";
                txtNim.ReadOnly = true; // primary key tidak boleh diubah
            }
        }

        // Event Click tombol Ubah Mahasiswa (Kode 9)
        private void BtnUbah_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNim.Text))
            {
                MessageBox.Show("Pilih data yang akan diubah terlebih dahulu.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (string.IsNullOrWhiteSpace(txtNama.Text))
            {
                MessageBox.Show("Nama wajib diisi.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (!int.TryParse(txtAngkatan.Text, out int angkatan))
            {
                MessageBox.Show("Angkatan harus berupa angka.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "UPDATE mahasiswa SET nama=@nama, prodi=@prodi, angkatan=@angkatan WHERE nim=@nim";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@nama", txtNama.Text.Trim());
                        cmd.Parameters.AddWithValue("@prodi", cmbProdi.Text.Trim());
                        cmd.Parameters.AddWithValue("@angkatan", angkatan);
                        cmd.Parameters.AddWithValue("@nim", txtNim.Text.Trim());
                        int baris = cmd.ExecuteNonQuery();
                        MessageBox.Show(baris > 0 ? "Data berhasil diubah." : "Data tidak ditemukan.",
                            "Informasi", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }

                TampilData();
                BersihkanForm();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Gagal mengubah data: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Event Click tombol Hapus Mahasiswa (Kode 10)
        private void BtnHapus_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNim.Text))
            {
                MessageBox.Show("Pilih data yang akan dihapus terlebih dahulu.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            var jawab = MessageBox.Show(
                "Hapus data " + txtNama.Text + "?", "Konfirmasi Hapus",
                MessageBoxButtons.YesNo, MessageBoxIcon.Question);

            if (jawab != DialogResult.Yes) return;

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "DELETE FROM mahasiswa WHERE nim=@nim";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@nim", txtNim.Text.Trim());
                        cmd.ExecuteNonQuery();
                    }
                }

                MessageBox.Show("Data berhasil dihapus.", "Informasi",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                TampilData();
                BersihkanForm();
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal menghapus: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Event Click tombol Bersih
        private void BtnBersih_Click(object sender, EventArgs e)
        {
            BersihkanForm();
        }

        // Event TextChanged pencarian data dengan LIKE (Kode 11)
        private void TxtCari_TextChanged(object sender, EventArgs e)
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    string sql = "SELECT nim, nama, prodi, angkatan FROM mahasiswa " +
                                 "WHERE nim LIKE @kata OR nama LIKE @kata ORDER BY nim";
                    var adapter = new MySqlDataAdapter(sql, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@kata", "%" + txtCari.Text.Trim() + "%");
                    var tabel = new DataTable();
                    adapter.Fill(tabel);
                    dgvMahasiswa.DataSource = tabel;

                    if (string.IsNullOrWhiteSpace(txtCari.Text))
                    {
                        lblTotal.Text = "Total mahasiswa: " + HitungMahasiswa();
                    }
                    else
                    {
                        lblTotal.Text = $"Ditemukan {tabel.Rows.Count} data dari total {HitungMahasiswa()} mahasiswa";
                    }
                }
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal mencari data: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Fitur Ekspor CSV (Latihan Mandiri 2)
        private void BtnEkspor_Click(object sender, EventArgs e)
        {
            if (dgvMahasiswa.Rows.Count == 0)
            {
                MessageBox.Show("Tidak ada data untuk diekspor.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            using (var sfd = new SaveFileDialog())
            {
                sfd.Filter = "File CSV (*.csv)|*.csv";
                sfd.FileName = "Data_Mahasiswa_" + DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".csv";

                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    try
                    {
                        using (var sw = new StreamWriter(sfd.FileName, false, Encoding.UTF8))
                        {
                            var headerList = new List<string>();
                            foreach (DataGridViewColumn col in dgvMahasiswa.Columns)
                            {
                                headerList.Add($"\"{col.HeaderText}\"");
                            }
                            sw.WriteLine(string.Join(",", headerList));

                            foreach (DataGridViewRow row in dgvMahasiswa.Rows)
                            {
                                var cellList = new List<string>();
                                foreach (DataGridViewCell cell in row.Cells)
                                {
                                    string val = cell.Value != null ? cell.Value.ToString().Replace("\"", "\"\"") : "";
                                    cellList.Add($"\"{val}\"");
                                }
                                sw.WriteLine(string.Join(",", cellList));
                            }
                        }

                        MessageBox.Show("Data berhasil diekspor ke:\n" + sfd.FileName, "Sukses Ekspor",
                            MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Gagal mengekspor file: " + ex.Message, "Kesalahan",
                            MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        #endregion

        #region Modul Latihan Mandiri 1: Pengelolaan Data Dosen (CRUD Dosen)

        private void TampilDataDosen()
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    string sql = "SELECT nidn, nama, bidang FROM dosen ORDER BY nidn";
                    var adapter = new MySqlDataAdapter(sql, conn);
                    var tabel = new DataTable();
                    adapter.Fill(tabel);
                    dgvDosen.DataSource = tabel;

                    if (dgvDosen.Columns["nidn"] != null) dgvDosen.Columns["nidn"].HeaderText = "NIDN";
                    if (dgvDosen.Columns["nama"] != null) dgvDosen.Columns["nama"].HeaderText = "Nama Dosen";
                    if (dgvDosen.Columns["bidang"] != null) dgvDosen.Columns["bidang"].HeaderText = "Bidang Keahlian";
                }

                lblTotalDosen.Text = "Total dosen: " + HitungDosen();
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal memuat data dosen: " + ex.Message, "Kesalahan Koneksi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private int HitungDosen()
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    using (var cmd = new MySqlCommand("SELECT COUNT(*) FROM dosen", conn))
                    {
                        return Convert.ToInt32(cmd.ExecuteScalar());
                    }
                }
            }
            catch
            {
                return 0;
            }
        }

        private void BersihkanFormDosen()
        {
            txtNidn.Clear();
            txtNamaDosen.Clear();
            txtBidang.Clear();
            txtNidn.ReadOnly = false;
            txtNidn.Focus();
        }

        private void BtnSimpanDosen_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNidn.Text) || string.IsNullOrWhiteSpace(txtNamaDosen.Text))
            {
                MessageBox.Show("NIDN dan Nama wajib diisi.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "INSERT INTO dosen (nidn, nama, bidang) VALUES (@nidn, @nama, @bidang)";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@nidn", txtNidn.Text.Trim());
                        cmd.Parameters.AddWithValue("@nama", txtNamaDosen.Text.Trim());
                        cmd.Parameters.AddWithValue("@bidang", txtBidang.Text.Trim());
                        cmd.ExecuteNonQuery();
                    }
                }

                MessageBox.Show("Data dosen berhasil disimpan.", "Informasi",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                TampilDataDosen();
                BersihkanFormDosen();
            }
            catch (MySqlException ex) when (ex.Number == 1062)
            {
                MessageBox.Show("NIDN sudah terdaftar.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal menyimpan dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void DgvDosen_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0) return;

            DataGridViewRow baris = dgvDosen.Rows[e.RowIndex];
            if (baris.Cells["nidn"].Value != null)
            {
                txtNidn.Text = baris.Cells["nidn"].Value.ToString();
                txtNamaDosen.Text = baris.Cells["nama"].Value?.ToString() ?? "";
                txtBidang.Text = baris.Cells["bidang"].Value?.ToString() ?? "";
                txtNidn.ReadOnly = true;
            }
        }

        private void BtnUbahDosen_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNidn.Text))
            {
                MessageBox.Show("Pilih dosen yang akan diubah terlebih dahulu.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (string.IsNullOrWhiteSpace(txtNamaDosen.Text))
            {
                MessageBox.Show("Nama dosen wajib diisi.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "UPDATE dosen SET nama=@nama, bidang=@bidang WHERE nidn=@nidn";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@nama", txtNamaDosen.Text.Trim());
                        cmd.Parameters.AddWithValue("@bidang", txtBidang.Text.Trim());
                        cmd.Parameters.AddWithValue("@nidn", txtNidn.Text.Trim());
                        int baris = cmd.ExecuteNonQuery();
                        MessageBox.Show(baris > 0 ? "Data dosen berhasil diubah." : "Data tidak ditemukan.",
                            "Informasi", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }

                TampilDataDosen();
                BersihkanFormDosen();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Gagal mengubah dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnHapusDosen_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNidn.Text))
            {
                MessageBox.Show("Pilih data dosen yang akan dihapus terlebih dahulu.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            var jawab = MessageBox.Show("Hapus data dosen " + txtNamaDosen.Text + "?", "Konfirmasi Hapus",
                MessageBoxButtons.YesNo, MessageBoxIcon.Question);

            if (jawab != DialogResult.Yes) return;

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    string sql = "DELETE FROM dosen WHERE nidn=@nidn";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@nidn", txtNidn.Text.Trim());
                        cmd.ExecuteNonQuery();
                    }
                }

                MessageBox.Show("Data dosen berhasil dihapus.", "Informasi",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                TampilDataDosen();
                BersihkanFormDosen();
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal menghapus dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnBersihDosen_Click(object sender, EventArgs e)
        {
            BersihkanFormDosen();
        }

        private void TxtCariDosen_TextChanged(object sender, EventArgs e)
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    string sql = "SELECT nidn, nama, bidang FROM dosen " +
                                 "WHERE nidn LIKE @kata OR nama LIKE @kata ORDER BY nidn";
                    var adapter = new MySqlDataAdapter(sql, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@kata", "%" + txtCariDosen.Text.Trim() + "%");
                    var tabel = new DataTable();
                    adapter.Fill(tabel);
                    dgvDosen.DataSource = tabel;

                    if (string.IsNullOrWhiteSpace(txtCariDosen.Text))
                    {
                        lblTotalDosen.Text = "Total dosen: " + HitungDosen();
                    }
                    else
                    {
                        lblTotalDosen.Text = $"Ditemukan {tabel.Rows.Count} dosen dari total {HitungDosen()}";
                    }
                }
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal mencari data dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        #endregion

        #region Modul Latihan Mandiri 3: Daftar Program Studi

        private void TampilDataProdi()
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    string sql = "SELECT kode_prodi, nama_prodi FROM prodi ORDER BY kode_prodi";
                    var adapter = new MySqlDataAdapter(sql, conn);
                    var tabel = new DataTable();
                    adapter.Fill(tabel);
                    dgvProdi.DataSource = tabel;

                    if (dgvProdi.Columns["kode_prodi"] != null) dgvProdi.Columns["kode_prodi"].HeaderText = "Kode Prodi";
                    if (dgvProdi.Columns["nama_prodi"] != null) dgvProdi.Columns["nama_prodi"].HeaderText = "Nama Program Studi";
                }

                lblTotalProdi.Text = "Total program studi terdaftar: " + HitungProdi();
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal memuat data prodi: " + ex.Message, "Kesalahan Koneksi",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private int HitungProdi()
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();
                    using (var cmd = new MySqlCommand("SELECT COUNT(*) FROM prodi", conn))
                    {
                        return Convert.ToInt32(cmd.ExecuteScalar());
                    }
                }
            }
            catch
            {
                return 0;
            }
        }

        private void BtnMuatProdi_Click(object sender, EventArgs e)
        {
            TampilDataProdi();
        }

        #endregion
    }
}
