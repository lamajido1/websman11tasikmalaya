# PANDUAN DEPLOY KE RUMAHWEB (CPANEL)

Berikut adalah langkah-langkah untuk memindahkan website ini ke hosting cPanel (RumahWeb):

## 1. Persiapan File
1.  Pastikan semua file sudah tersimpan.
2.  File `passenger_wsgi.py` sudah dibuat (wajib untuk cPanel).
3.  Library `whitenoise` sudah ditambahkan untuk menangani file statis (CSS/JS) secara otomatis.
4.  Compress/Zip seluruh isi folder project `websman11tasikmalaya`, KECUALI folder:
    - `venv`
    - `.git` (jika ada)
    - `__pycache__`
    - `db.sqlite3` (karena kita pakai MySQL/MariaDB)

## 2. Upload ke cPanel
1.  Login ke cPanel RumahWeb.
2.  Buka **File Manager**.
3.  Buat folder baru di root (sejajar dengan public_html), yaitu `pythonapp`.
    *   **PENTING:** Jangan buat di dalam `public_html`! Folder ini harus sejajar dengan `public_html`, `etc`, `logs`, dll.
4.  Upload file zip project ke dalam folder `pythonapp`.
5.  Extract file zip tersebut.

## 3. Setup Python App
1.  Di dashboard cPanel, cari menu **Setup Python App**.
2.  Klik **Create Application**.
3.  Isi form:
    - **Python Version**: Pilih 3.11.
    - **Application root**: `pythonapp` (nama folder tempat upload tadi).
    - **Application URL**: Pilih domain utama Anda (kosongkan path untuk root domain).
    - **Application startup file**: `passenger_wsgi.py`
    - **Application Entry point**: `application`
4.  Klik **Create**.

## 4. Install Dependencies
1.  Setelah aplikasi dibuat, perhatikan bagian atas halaman "Setup Python App".
2.  Ada teks **"Command for entering to virtual environment"**. Di bawahnya ada perintah yang panjang, contohnya seperti ini:
    `source /home/smay8199/virtualenv/pythonapp/3.11/bin/activate && cd /home/smay8199/pythonapp`
3.  **Salin (Copy)** perintah tersebut seluruhnya.
4.  Buka **Terminal** di cPanel (cari menu "Terminal" di kolom pencarian dashboard cPanel).
    *   *Terminal adalah layar hitam tempat mengetik perintah, mirip CMD di Windows.*
5.  **Tempel (Paste)** perintah yang sudah dicopy tadi ke layar Terminal, lalu tekan tombol **Enter** di keyboard.
6.  **Cek perubahannya:**
    *   Sebelumnya tulisan di kiri kursor mungkin seperti: `[smay8199@server ~]$`
    *   Setelah di-Enter, tulisannya akan berubah menjadi ada tanda kurung, contoh: `(pythonapp:3.11)[smay8199@server ...]$`
    *   *Ini tandanya Anda sudah berhasil "masuk" ke lingkungan Python aplikasi Anda.*
7.  Install library:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

    *Jika muncul error "exit code 2" atau gagal install Pillow:*
    Coba install manual satu per satu:
    ```bash
    pip install django pymysql redis whitenoise
    pip install pillow
    ```

## 5. Konfigurasi Database & Environment
1.  Buka **MySQL Database Wizard** di cPanel.
2.  Buat database baru (misal: `smay8199_web`).
3.  Buat user database baru (misal: `smay8199_lamajido`) dan passwordnya.
4.  Berikan hak akses (All Privileges) user ke database tersebut.
5.  Edit file `websman11/settings.py` di File Manager:
    *   Buka File Manager di cPanel, masuk ke folder `pythonapp/websman11`, klik kanan file `settings.py` dan pilih **Edit**.
    *   Cari bagian `DATABASES`: Ganti `NAME`, `USER`, dan `PASSWORD` dengan data database yang baru Anda buat di MySQL Database Wizard cPanel.
    *   Cari `ALLOWED_HOSTS = ['*']`: Ganti menjadi nama domain Anda agar lebih aman.
        *   Contoh: `ALLOWED_HOSTS = ['smay8199.sch.id', 'www.smay8199.sch.id']`
    *   Cari `DEBUG`: Pastikan nilainya `False` agar error coding tidak muncul ke pengunjung.
        *   Cari baris: `DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'`
        *   Ubah menjadi: `DEBUG = False` (atau hapus logikanya dan tulis langsung `DEBUG = False`).

6.  **Konfigurasi HTTPS (PENTING)**:
    Agar website aman dan bisa login admin via HTTPS, tambahkan baris berikut di bagian paling bawah file `settings.py`:
    ```python
    # Konfigurasi HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://smay8199.sch.id', 'https://www.smay8199.sch.id']
    ```
    *Ganti domain sesuai nama domain Anda.*

## 6. Finalisasi
1.  Kembali ke Terminal cPanel (pastikan venv aktif).
2.  Jalankan migrasi database:
    ```bash
    python manage.py migrate
    ```
    
    *Jika muncul error `Access denied for user ... to database ...`*:
    *   Cek kembali file `settings.py` Anda.
    *   Pastikan `USER` dan `PASSWORD` database sudah BENAR sesuai yang Anda buat di MySQL Database Wizard.
    *   Pastikan User tersebut sudah ditambahkan ke Database (Add User to Database) dan dicentang **ALL PRIVILEGES**.

3.  Kumpulkan file statis:
    ```bash
    python manage.py collectstatic
    ```
    *   Jika muncul pertanyaan `Type 'yes' to continue, or 'no' to cancel:`, ketik **yes** lalu tekan **Enter**.

4.  Buat Superuser (Akun Admin):
    Agar bisa login ke halaman admin (`/admin`), buat akun superuser:
    ```bash
    python manage.py createsuperuser
    ```
    *   Masukkan username, email (boleh kosong), dan password.
    *   *Catatan: Saat mengetik password, layar memang tidak menampilkan karakter (silent), tetap ketik saja lalu Enter.*

5.  Restart aplikasi Python di menu **Setup Python App** (klik tombol Restart).

## 7. Cek Website
Buka domain Anda. Website seharusnya sudah aktif.

## 8. Troubleshooting (Masalah Umum)

### A. Muncul Halaman "Index of /"
Jika saat mengakses website yang muncul adalah daftar file (seperti `cgi-bin`, `pythonapp`, dll), ini berarti aplikasi Python belum "mengambil alih" domain utama.
**Penyebab:**
1.  Folder `pythonapp` mungkin berada **di dalam** `public_html` (seharusnya di luar/sejajar).
2.  File `.htaccess` di dalam `public_html` hilang atau salah konfigurasi.

**Solusi:**
1.  **Cek Lokasi Folder Project**:
    *   Buka File Manager cPanel.
    *   Jika folder `pythonapp` ada di dalam `public_html`, **Pindahkan (Move)** folder tersebut keluar (ke `/home/smay8199/pythonapp`).
    *   Pastikan `public_html` bersih dari folder project Anda.

2.  **Buat/Edit File `.htaccess`**:
    *   Di dalam folder `public_html`, buat file baru bernama `.htaccess` (gunakan titik di awal).
    *   Isi dengan kode berikut (sesuaikan path jika berbeda):
        ```apache
        # Force HTTPS
        RewriteEngine On
        RewriteCond %{HTTPS} off
        RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

        # DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION BEGIN
        PassengerAppRoot "/home/smay8199/pythonapp"
        PassengerBaseURI "/"
        PassengerPython "/home/smay8199/virtualenv/pythonapp/3.11/bin/python"
        # DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION END
        ```
    *   *Catatan:* Bagian `PassengerPython` harus sesuai dengan path virtual environment Anda (bisa dicek di menu Setup Python App).

3.  **Restart App**:
    *   Kembali ke menu **Setup Python App**, klik icon **Restart** pada aplikasi Anda.

### B. Error Database (Access Denied)
(Lihat langkah 6.2 di atas)

### C. Error 503 Service Unavailable
Error ini menandakan aplikasi Python **gagal berjalan/crash** saat baru dimulai.
**Cara Mengatasinya:**

1.  **Cek Error Log**:
    *   Buka File Manager, masuk ke folder `pythonapp`.
    *   Cari file bernama `stderr.log` (jika tidak ada, cek di folder root atau `public_html`).
    *   Klik kanan -> **View**. Lihat pesan error di baris paling bawah.

2.  **Cek Script Manual via Terminal**:
    *   Buka Terminal cPanel (pastikan venv aktif).
    *   Jalankan perintah ini untuk melihat apakah ada error coding:
        ```bash
        python manage.py check
        ```
    *   Jika muncul error, perbaiki sesuai pesan errornya.

3.  **Pastikan `passenger_wsgi.py` Benar (HAPUS SEMUA KODE LAMA)**:
    *   Error `wsgi = imp.load_source` atau `RecursionError` terjadi karena Anda **menumpuk** kode saya dengan kode bawaan cPanel.
    *   **SOLUSI:** Hapus **SELURUH** isi file `passenger_wsgi.py` yang ada di cPanel. File harus **BENAR-BENAR BERSIH** sebelum diisi kode baru.
    *   Lalu copas kode ini saja:
        ```python
        import os
        import sys
        
        # Tambahkan folder project ke path
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Arahkan ke settings project
        os.environ['DJANGO_SETTINGS_MODULE'] = 'websman11.settings'
        
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        ```

### D. Error "lswsgi_wrapper: ... File atau direktori tidak ditemukan"
Error ini sering terjadi karena path di file `.htaccess` salah atau Virtual Environment rusak.

**LANGKAH 1: Cek File `.htaccess` (Paling Sering Salah Disini)**
1.  Buka File Manager, masuk ke folder `public_html`.
2.  Edit file `.htaccess`.
3.  Perhatikan baris `PassengerAppRoot` dan `PassengerPython`.
4.  **PASTIKAN ADA TANDA GARIS MIRING (/) DI AWAL PATH!**
    *   SALAH: `home/smay8199/pythonapp`
    *   BENAR: `/home/smay8199/pythonapp`
    *   SALAH: `home/smay8199/virtualenv/pythonapp/3.11/bin/python`
    *   BENAR: `/home/smay8199/virtualenv/pythonapp/3.11/bin/python`
5.  Jika kurang tanda `/` di depan `home`, tambahkan manual lalu Save.

**LANGKAH 2: Recreate App (Jika Langkah 1 Tidak Mempan)**
Jika path sudah benar tapi masih error, berarti Virtual Environment rusak.
1.  **Hapus Aplikasi di cPanel**:
    *   Buka menu **Setup Python App**.
    *   Klik icon **Tempat Sampah (Delete)** di sebelah kanan aplikasi Anda.
    *   Konfirmasi penghapusan (Tenang, ini **TIDAK MENGHAPUS** file coding/project Anda, hanya menghapus konfigurasi sistem).

2.  **Buat Ulang Aplikasi**:
    *   Klik **Create Application**.
    *   **Python Version**: 3.11.
    *   **Application root**: `pythonapp` (folder project Anda yang sudah ada).
    *   **Application URL**: Domain Anda.
    *   **Application startup file**: `passenger_wsgi.py`.
    *   **Application Entry point**: `application`.
    *   Klik **Create**.

3.  **Install Ulang Dependencies (PENTING: TUTUP TERMINAL LAMA)**:
    *   **Tutup** jendela Terminal cPanel yang sedang terbuka saat ini (klik tanda X atau ketik `exit`).
    *   **Buka Terminal Baru**. *Ini wajib dilakukan agar terminal melupakan path error yang lama.*
    *   Copy perintah `source ...` dari halaman Setup Python App yang baru.
    *   Paste perintah `source ...` ke Terminal baru, lalu Enter.
    *   Jalankan:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Cek Website**:
    *   Refresh domain Anda. Seharusnya sekarang sudah benar-benar normal.

## 9. Perawatan (Maintenance) agar Inode Tidak Penuh

### A. Setup Cron Job (Pembersih Otomatis)
Agar session login yang sudah kadaluarsa tidak menumpuk di database, buat jadwal pembersihan otomatis:
1.  Di Dashboard cPanel, cari menu **Cron Jobs**.
2.  Di bagian **Add New Cron Job**:
    *   **Common Settings**: Pilih **Once Per Week** (Seminggu Sekali).
    *   **Command**: Masukkan perintah berikut (satu baris):
        `/home/smay8199/virtualenv/pythonapp/3.11/bin/python /home/smay8199/pythonapp/manage.py clearsessions`
3.  Klik **Add New Cron Job**.

### B. Pembersihan Manual (Opsional)
Jika Inode tiba-tiba penuh, jalankan perintah ini di Terminal cPanel:
```bash
# Hapus cache installer library
pip cache purge

# Cek folder mana yang paling banyak filenya
find . -maxdepth 2 -not -path '*/.*' -type d -print0 | xargs -0 -n 1 du --inode -s | sort -rn | head -5
```
