using System;
using System.Windows.Forms;

namespace tugas9formmahasiswa
{
    internal static class Program
    {
        /// <summary>
        /// Titik masuk utama aplikasi (Main entry point).
        /// Alur aplikasi: Form Login muncul pertama kali.
        /// Jika login berhasil, Form Utama (FormMahasiswa) dengan multi-page dashboard ditampilkan.
        /// Jika user melakukan Logout, akan kembali ke Form Login.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            while (true)
            {
                using (var formLogin = new FormLogin())
                {
                    if (formLogin.ShowDialog() == DialogResult.OK)
                    {
                        using (var formUtama = new FormMahasiswa())
                        {
                            Application.Run(formUtama);

                            // Jika user mengklik logout di dalam aplikasi, ulangi loop ke FormLogin
                            if (!formUtama.IsLogout)
                            {
                                break;
                            }
                        }
                    }
                    else
                    {
                        // Pengguna menekan Batal atau menutup form login -> keluar dari aplikasi
                        break;
                    }
                }
            }
        }
    }
}
