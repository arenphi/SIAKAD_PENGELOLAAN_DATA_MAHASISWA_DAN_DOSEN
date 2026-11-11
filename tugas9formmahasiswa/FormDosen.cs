using System;
using System.Data;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace tugas9formmahasiswa
{
    public partial class FormDosen : Form
    {
        public FormDosen()
        {
            InitializeComponent();
        }

        private void TampilData()
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

                lblTotal.Text = "Total dosen: " + HitungDosen();
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

        private void FormDosen_Load(object sender, EventArgs e)
        {
            TampilData();
        }

        private void BersihkanForm()
        {
            txtNidn.Clear();
            txtNama.Clear();
            txtBidang.Clear();
            txtNidn.ReadOnly = false;
            txtNidn.Focus();
        }

        private void BtnSimpan_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNidn.Text) || string.IsNullOrWhiteSpace(txtNama.Text))
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
                        cmd.Parameters.AddWithValue("@nama", txtNama.Text.Trim());
                        cmd.Parameters.AddWithValue("@bidang", txtBidang.Text.Trim());
                        cmd.ExecuteNonQuery();
                    }
                }

                MessageBox.Show("Data dosen berhasil disimpan.", "Informasi",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                TampilData();
                BersihkanForm();
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
                txtNama.Text = baris.Cells["nama"].Value?.ToString() ?? "";
                txtBidang.Text = baris.Cells["bidang"].Value?.ToString() ?? "";
                txtNidn.ReadOnly = true;
            }
        }

        private void BtnUbah_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNidn.Text))
            {
                MessageBox.Show("Pilih dosen yang akan diubah terlebih dahulu.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (string.IsNullOrWhiteSpace(txtNama.Text))
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
                        cmd.Parameters.AddWithValue("@nama", txtNama.Text.Trim());
                        cmd.Parameters.AddWithValue("@bidang", txtBidang.Text.Trim());
                        cmd.Parameters.AddWithValue("@nidn", txtNidn.Text.Trim());
                        int baris = cmd.ExecuteNonQuery();
                        MessageBox.Show(baris > 0 ? "Data dosen berhasil diubah." : "Data tidak ditemukan.",
                            "Informasi", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                }

                TampilData();
                BersihkanForm();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Gagal mengubah dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnHapus_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNidn.Text))
            {
                MessageBox.Show("Pilih data dosen yang akan dihapus terlebih dahulu.", "Peringatan",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            var jawab = MessageBox.Show("Hapus data dosen " + txtNama.Text + "?", "Konfirmasi Hapus",
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
                TampilData();
                BersihkanForm();
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal menghapus dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnBersih_Click(object sender, EventArgs e)
        {
            BersihkanForm();
        }

        private void TxtCari_TextChanged(object sender, EventArgs e)
        {
            try
            {
                using (var conn = Koneksi.Buat())
                {
                    string sql = "SELECT nidn, nama, bidang FROM dosen " +
                                 "WHERE nidn LIKE @kata OR nama LIKE @kata " +
                                 "ORDER BY nidn";
                    var adapter = new MySqlDataAdapter(sql, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@kata", "%" + txtCari.Text.Trim() + "%");
                    var tabel = new DataTable();
                    adapter.Fill(tabel);
                    dgvDosen.DataSource = tabel;

                    if (string.IsNullOrWhiteSpace(txtCari.Text))
                    {
                        lblTotal.Text = "Total dosen: " + HitungDosen();
                    }
                    else
                    {
                        lblTotal.Text = $"Ditemukan {tabel.Rows.Count} dosen dari total {HitungDosen()}";
                    }
                }
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Gagal mencari data dosen: " + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}

