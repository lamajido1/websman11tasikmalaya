# PANDUAN DEPLOY KE RUMAHWEB VIA GITHUB (AUTO UPDATE)

Panduan ini akan membantu Anda menginstall website di cPanel menggunakan **GitHub**, sehingga ke depannya Anda bisa melakukan update website hanya dengan perintah `git pull` tanpa perlu upload zip berulang-ulang.

## LANGKAH 1: Setup Python App di cPanel

1.  Login ke cPanel RumahWeb/Hosting Anda.
2.  Cari menu **Setup Python App**.
3.  Klik **Create Application**.
4.  Isi form sebagai berikut:
    *   **Python Version**: Pilih **3.11** (Sesuai development kita).
    *   **Application root**: `pythonapp` (Atau nama folder lain yang Anda inginkan, misal `websman11`).
    *   **Application URL**: Pilih domain utama Anda.
    *   **Application startup file**: `passenger_wsgi.py`
    *   **Application Entry point**: `application`
5.  Klik **Create**.

## LANGKAH 2: Hubungkan Terminal cPanel dengan GitHub

1.  Di halaman Setup Python App tadi, salin (copy) perintah untuk masuk ke virtual environment.
    *   Contoh: `source /home/smay8199/virtualenv/pythonapp/3.11/bin/activate && cd /home/smay8199/pythonapp`
2.  Buka menu **Terminal** di cPanel.
3.  Tempel (paste) perintah tadi dan tekan Enter.
    *   Tanda berhasil: Tampilan prompt berubah menjadi `(pythonapp:3.11)[username@server ...]$`.
4.  **Hapus folder kosong yang dibuat otomatis oleh cPanel**:
    *   Saat Python App dibuat, cPanel membuat folder kosong. Kita harus menghapusnya agar bisa di-clone dari GitHub.
    *   Jalankan perintah ini:
        ```bash
        cd ..
        rm -rf pythonapp
        ```
        *(Ganti `pythonapp` dengan nama Application root Anda jika berbeda)*

5.  **Clone dari GitHub**:
    *   Jalankan perintah clone:
        ```bash
        git clone https://github.com/lamajido1/websman11tasikmalaya.git pythonapp
        ```
    *   Jika diminta Username & Password:
        *   **Username**: Username GitHub Anda.
        *   **Password**: **BUKAN password login biasa**, tapi **Personal Access Token**.
        *   *Cara buat Token: Buka GitHub > Settings > Developer Settings > Personal access tokens > Tokens (classic) > Generate new token > Centang "repo" > Copy tokennya.*
        

6.  **Masuk kembali ke folder project**:
    ```bash
    cd pythonapp
    ```

## LANGKAH 3: Install Dependencies

Di dalam Terminal cPanel (pastikan sudah di dalam folder `pythonapp`):

1.  Install library yang dibutuhkan:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## LANGKAH 4: Konfigurasi Database & Settings

1.  Buka **File Manager** cPanel.
2.  Masuk ke folder `pythonapp` -> `websman11`.
3.  Edit file `settings.py`.
4.  Sesuaikan konfigurasi Database (sama seperti panduan manual):
    *   Cari `DATABASES = ...`
    *   Ubah `NAME`, `USER`, `PASSWORD` sesuai database MySQL yang sudah Anda buat di cPanel.
    *   Ubah `HOST` ke `localhost` atau `127.0.0.1`.
5.  Sesuaikan Domain:
    *   Ubah `ALLOWED_HOSTS = ['*']` menjadi `ALLOWED_HOSTS = ['smay8199.sch.id', 'www.smay8199.sch.id']`.
6.  Matikan Debug (Untuk keamanan):
    *   Ubah `DEBUG = True` menjadi `DEBUG = False`.
7.  **Simpan (Save Changes)**.

## LANGKAH 5: Finalisasi (Migrate & Static)

Kembali ke **Terminal** cPanel:

1.  **Migrasi Database** (Membuat tabel-tabel):
    ```bash
    python manage.py migrate
    ```
    > **PENTING:** Perintah ini HANYA membuat **struktur tabel kosong** (seperti rumah tanpa perabot).
    > Data isi (berita, guru, siswa, dll) **TIDAK** ikut otomatis.
    > Untuk mengisi datanya, lihat **LANGKAH 6: Restore Data** di bawah.

2.  **Kumpulkan File Statis** (CSS/JS/Gambar):
    ```bash
    python manage.py collectstatic
    ```
    *   Ketik `yes` jika diminta konfirmasi.

3.  **Buat Akun Admin**:
    ```bash
    python manage.py createsuperuser
    ```

## LANGKAH 6: Restore Data (Opsional)

Jika Anda sudah punya file backup `.sql` dari komputer lokal (hasil fitur Backup Database di Admin):

1.  Upload file `.sql` tersebut ke File Manager cPanel.
2.  Buka menu **PHPMyAdmin** di cPanel.
3.  Pilih database Anda.
4.  Klik menu **Import**.
5.  Pilih file `.sql` tadi, lalu klik **Go/Kirim**.

## LANGKAH 7: Restart Aplikasi

1.  Kembali ke menu **Setup Python App**.
2.  Klik tombol **Restart** pada aplikasi Anda.
3.  Cek website Anda.

---

## CARA UPDATE APLIKASI DI MASA DEPAN

Jika Anda melakukan perubahan di komputer lokal dan sudah di-push ke GitHub (via Admin Panel), cara updatenya di cPanel sangat mudah:

1.  Buka **Terminal** cPanel.
2.  Masuk ke folder project:
    ```bash
    cd pythonapp
    ```
3.  Tarik update terbaru:
    ```bash
    git pull
    ```
4.  Jika ada perubahan database (misal nambah tabel baru), jalankan:
    ```bash
    source ../virtualenv/pythonapp/3.11/bin/activate  # Aktifkan venv dulu jika belum
    python manage.py migrate
    ```
5.  Restart aplikasi di menu **Setup Python App**.
