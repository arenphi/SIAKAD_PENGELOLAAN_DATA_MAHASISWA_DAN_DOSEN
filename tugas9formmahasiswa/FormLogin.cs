using System;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace tugas9formmahasiswa
{
    public partial class FormLogin : Form
    {
        public FormLogin()
        {
            InitializeComponent();
            // Pre-fill akun demo untuk kemudahan pengujian
            txtUsername.Text = "admin";
            txtPassword.Text = "admin123";
        }

        // Fungsi helper untuk menghasilkan hash SHA-256 dari string kata sandi
        private static string HitungHashSHA256(string teks)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(teks));
                StringBuilder builder = new StringBuilder();
                foreach (byte b in bytes)
                {
                    builder.Append(b.ToString("x2"));
                }
                return builder.ToString();
            }
        }

        private void BtnLogin_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtUsername.Text) || string.IsNullOrWhiteSpace(txtPassword.Text))
            {
                MessageBox.Show("Username dan Password wajib diisi.", "Validasi Input",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string hashPassword = HitungHashSHA256(txtPassword.Text.Trim());

            try
            {
                using (var conn = Koneksi.Buat())
                {
                    conn.Open();

                    // Menggunakan query berparameter untuk mencegah SQL Injection (Kode 14)
                    string sql = "SELECT COUNT(*) FROM pengguna WHERE username=@u AND password_hash=@p";
                    using (var cmd = new MySqlCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@u", txtUsername.Text.Trim());
                        cmd.Parameters.AddWithValue("@p", hashPassword);

                        int count = Convert.ToInt32(cmd.ExecuteScalar());
                        if (count > 0)
                        {
                            MessageBox.Show("Login berhasil! Selamat datang di Sistem Akademik.", "Informasi",
                                MessageBoxButtons.OK, MessageBoxIcon.Information);
                            this.DialogResult = DialogResult.OK;
                            this.Close();
                        }
                        else
                        {
                            MessageBox.Show("Username atau Password salah.", "Peringatan",
                                MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kesalahan saat menghubungkan ke database:\n" + ex.Message, "Kesalahan",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BtnBatal_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }
    }
}

