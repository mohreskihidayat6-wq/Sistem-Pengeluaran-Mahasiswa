# Aplikasi Pengelolaan Pengeluaran Mahasiswa

Aplikasi desktop berbasis Python yang dirancang untuk membantu mahasiswa mencatat, mengelola, dan memantau pengeluaran sehari-hari. Aplikasi ini dilengkapi dengan sistem autentikasi pengguna, animasi pada halaman login, serta basis data MySQL yang mendukung penggunaan oleh banyak mahasiswa.

## Deskripsi Proyek

Aplikasi Pengelolaan Pengeluaran Mahasiswa merupakan aplikasi desktop yang dikembangkan untuk memudahkan mahasiswa dalam mengelola keuangan pribadi, khususnya dalam mencatat dan memantau pengeluaran sehari-hari.

Aplikasi ini memungkinkan setiap mahasiswa untuk membuat akun, melakukan login, mencatat transaksi pengeluaran, mengelompokkan pengeluaran berdasarkan kategori, melihat riwayat transaksi, serta memantau total pengeluaran.

Berbeda dengan versi sebelumnya yang hanya dapat digunakan oleh satu mahasiswa, versi terbaru telah dilengkapi dengan sistem multi-user. Setiap mahasiswa dapat memiliki akun sendiri sehingga data pengeluaran dapat dikelola secara terpisah berdasarkan akun yang digunakan.

Proyek ini dikembangkan sebagai proyek praktikum Rekayasa Perangkat Lunak dengan menerapkan arsitektur Model-View-Controller (MVC), basis data relasional MySQL, sistem autentikasi, dan operasi CRUD (Create, Read, Update, Delete).

## Fitur Utama

### 1. Sistem Autentikasi
- Registrasi akun mahasiswa baru.
- Login menggunakan akun yang telah terdaftar.
- Logout untuk mengakhiri sesi pengguna.
- Animasi pada halaman login untuk memberikan tampilan antarmuka yang lebih menarik.
- Setiap mahasiswa dapat menggunakan akun masing-masing.

### 2. Pengelolaan Pengeluaran
- Menambahkan data pengeluaran.
- Melihat daftar pengeluaran.
- Mengubah data pengeluaran.
- Menghapus data pengeluaran.
- Mencatat tanggal, jumlah, dan deskripsi pengeluaran.

### 3. Pengelolaan Kategori
- Mengelola kategori pengeluaran.
- Mengelompokkan pengeluaran berdasarkan kategori, seperti makanan, transportasi, kebutuhan kuliah, dan hiburan.

### 4. Riwayat dan Ringkasan Pengeluaran
- Melihat riwayat transaksi pengeluaran.
- Menampilkan total pengeluaran.
- Memantau pengeluaran berdasarkan data transaksi yang telah dicatat.

### 5. Sistem Multi-User
- Mendukung penggunaan oleh lebih dari satu mahasiswa.
- Setiap mahasiswa memiliki akun tersendiri.
- Data pengeluaran dikelola berdasarkan pengguna yang sedang login.
- Menggunakan MySQL sebagai tempat penyimpanan data secara terpusat.

## Teknologi yang Digunakan

| Teknologi | Keterangan |
|---|---|
| Python | Bahasa pemrograman utama |
| CustomTkinter | Pembuatan antarmuka desktop |
| MySQL | Sistem manajemen basis data |
| Laragon | Server basis data lokal |
| mysql-connector-python | Konektor Python dengan MySQL |
| MVC | Arsitektur aplikasi |
| Visual Studio Code | Editor kode |
| Git | Version control |
| GitHub | Penyimpanan repository proyek |
| Python venv | Lingkungan virtual |

## Struktur Proyek

```text
Modul5/
├── config/
│   └── database.py
├── models/
├── controllers/
├── views/
├── app.py
├── test_model.py
├── requirements.txt
├── .gitignore
└── README.md
```

Struktur folder dan file dapat berkembang mengikuti implementasi aplikasi.

## Struktur Basis Data

Nama basis data: `db_pengeluaran_mahasiswa`

Basis data MySQL digunakan untuk menyimpan informasi akun pengguna, data mahasiswa, kategori, serta transaksi pengeluaran.

| Tabel | Keterangan |
|---|---|
| `users` | Menyimpan informasi akun pengguna yang digunakan untuk proses registrasi dan login. |
| `mahasiswa` | Menyimpan data identitas mahasiswa yang terdaftar. |
| `kategori` | Menyimpan kategori pengeluaran, seperti makanan, transportasi, kebutuhan kuliah, dan hiburan. |
| `pengeluaran` | Menyimpan data transaksi pengeluaran, termasuk tanggal, jumlah, deskripsi, kategori, dan keterkaitan dengan pengguna atau mahasiswa. |

### Pengelolaan Data Multi-User

Setiap pengguna memiliki akun masing-masing yang digunakan untuk mengakses aplikasi. Sistem mengelola data pengeluaran berdasarkan pengguna yang sedang login sehingga setiap mahasiswa dapat mencatat dan melihat pengeluarannya sendiri.
## Persiapan dan Instalasi

### 1. Prasyarat

Pastikan perangkat telah memiliki:

- Python 3.
- Visual Studio Code.
- Laragon dengan MySQL.
- Git.

### 2. Buka Folder Proyek

Buka folder proyek melalui Visual Studio Code, kemudian buka terminal terintegrasi.

### 3. Buat Lingkungan Virtual

Jalankan perintah berikut:

```powershell
py -m venv env
```

Aktifkan lingkungan virtual pada Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

### 4. Instal Pustaka yang Dibutuhkan

Jalankan perintah berikut:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Pastikan seluruh pustaka yang digunakan aplikasi telah tercantum dalam file `requirements.txt`.

### 5. Siapkan Basis Data

1. Buka aplikasi Laragon.
2. Jalankan layanan MySQL.
3. Buka phpMyAdmin atau pengelola basis data lainnya.
4. Buat basis data dengan nama `db_pengeluaran_mahasiswa`.
5. Buat tabel `mahasiswa`, `kategori`, dan `pengeluaran` sesuai struktur basis data proyek.
6. Sesuaikan konfigurasi koneksi database pada file konfigurasi aplikasi.

Pastikan konfigurasi database telah sesuai dengan pengaturan MySQL lokal.

Jangan mengunggah kata sandi database atau informasi rahasia ke repository publik.

### 6. Jalankan Aplikasi

Setelah instalasi pustaka dan konfigurasi database selesai, jalankan aplikasi melalui terminal:

```powershell
python app.py
```

Aplikasi akan dijalankan melalui halaman awal yang menyediakan akses menuju fitur autentikasi pengguna.

## Arsitektur MVC

Aplikasi menerapkan arsitektur Model-View-Controller (MVC) untuk memisahkan pengelolaan data, tampilan antarmuka, dan logika aplikasi.

- **Model:** Mengelola data aplikasi serta komunikasi dengan basis data MySQL.
- **View:** Menampilkan antarmuka aplikasi, termasuk halaman login, registrasi, dan halaman utama menggunakan CustomTkinter.
- **Controller:** Menghubungkan tindakan pengguna dengan proses pada Model dan tampilan pada View, termasuk proses autentikasi dan pengelolaan pengeluaran.

## Version Control dengan Git

Git digunakan untuk mengelola perubahan kode selama proses pengembangan aplikasi, sedangkan GitHub digunakan sebagai tempat penyimpanan repository proyek.

Untuk memeriksa status perubahan:

```bash
git status
```

Untuk menambahkan perubahan:

```bash
git add .
```

Untuk menyimpan perubahan:

```bash
git commit -m "Update fitur aplikasi"
```

Untuk mengunggah perubahan ke GitHub:

```bash
git push origin main
```

Jangan mengunggah folder `env/`, kata sandi, maupun konfigurasi database yang bersifat rahasia.

## Status Pengembangan

Aplikasi telah mengalami pengembangan dari versi awal yang hanya mendukung satu mahasiswa menjadi aplikasi desktop dengan sistem multi-user.

Pengembangan terbaru mencakup:

- Penambahan halaman login.
- Penambahan animasi pada halaman login.
- Penambahan halaman registrasi akun mahasiswa.
- Penambahan fitur logout.
- Penerapan sistem autentikasi pengguna.
- Pengembangan basis data MySQL untuk mendukung banyak akun mahasiswa.
- Pengelolaan data pengeluaran berdasarkan akun mahasiswa yang sedang login.

Pengembangan aplikasi dilakukan secara bertahap dengan menerapkan materi praktikum Rekayasa Perangkat Lunak Modul I–V.

## Pengembang

- **Nama Proyek:** Aplikasi Pengelolaan Pengeluaran Mahasiswa
- **Kelompok:** [6]
- **Anggota:**
- [Moh Reski Hidayat_F5212520091
- Ardhita Amarli Putri_F5212530109
- Dinda Aulia Rizkyanti Putri_F5212530105
- Rifka Anggraini_F5212530115]
- **Program Studi:** Sistem Informasi
- **Fakultas:** Teknik
- **Universitas:** Universitas Tadulako

---

README ini merupakan dokumentasi proyek yang menjelaskan tujuan, fitur, teknologi, struktur basis data, serta petunjuk instalasi dan penggunaan Aplikasi Pengelolaan Pengeluaran Mahasiswa.
