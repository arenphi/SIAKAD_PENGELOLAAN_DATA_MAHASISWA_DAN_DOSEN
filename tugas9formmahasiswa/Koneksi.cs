using System;
using System.Configuration;
using MySql.Data.MySqlClient;

namespace tugas9formmahasiswa
{
    public static class Koneksi
    {
        // Connection string dapat diambil dari App.config atau fallback ke default
        private static readonly string ConnStr =
            ConfigurationManager.ConnectionStrings["DbAkademik"] != null
                ? ConfigurationManager.ConnectionStrings["DbAkademik"].ConnectionString
                : "Server=localhost;Port=3306;Database=db_akademik;Uid=root;Pwd=;";

        public static MySqlConnection Buat()
        {
            return new MySqlConnection(ConnStr);
        }
    }
}

