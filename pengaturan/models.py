from django.db import models
from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey

class Slider(models.Model):
    judul = models.CharField(max_length=100)
    subjudul = models.CharField(max_length=200, blank=True, null=True)
    gambar = models.ImageField(upload_to='sliders/')
    urutan = models.IntegerField(default=0, help_text="Urutan tampilan slide (angka kecil lebih dulu)")
    aktif = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.gambar:
            try:
                img = Image.open(self.gambar.path)
                if img.height > 1200 or img.width > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size)
                    img.save(self.gambar.path, quality=90, optimize=True)
            except Exception as e:
                pass
    
    def __str__(self):
        return self.judul
        
    class Meta:
        verbose_name_plural = "Slider"
        ordering = ['urutan']
        db_table = 'sekolah_slider'

class Menu(MPTTModel):
    nama = models.CharField(max_length=50)
    url = models.CharField(max_length=200, help_text="Link tujuan (bisa '/profil/' atau 'https://...')")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenu', help_text="Jika ini adalah submenu, pilih menu utamanya")
    aktif = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['nama']

    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = "Menu Navigasi"
        db_table = 'sekolah_menu'

class Pengaturan(models.Model):
    nama_sekolah = models.CharField(max_length=100, default='SMA Y8199 Tasikmalaya')
    slogan = models.CharField(max_length=255, blank=True, null=True, default='Mewujudkan generasi cerdas, berkarakter, dan kompetitif.')
    logo = models.ImageField(upload_to='pengaturan/', blank=True, null=True)
    favicon = models.ImageField(upload_to='pengaturan/', blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    telepon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    copyright = models.CharField(max_length=100, default='© 2026 Copyright SMA Y8199.')
    
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.logo:
            try:
                img = Image.open(self.logo.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.logo.path, quality=90, optimize=True)
            except Exception as e:
                pass
    
    def __str__(self):
        return self.nama_sekolah
        
    class Meta:
        verbose_name_plural = "Pengaturan Website"
        db_table = 'sekolah_pengaturan'

class UpdateAplikasi(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)
    versi = models.CharField(max_length=50, help_text="Versi atau commit ID", blank=True)
    status = models.CharField(max_length=20, choices=[('Sukses', 'Sukses'), ('Gagal', 'Gagal')], default='Sukses')
    log = models.TextField(blank=True, help_text="Log output dari proses sinkronisasi")
    
    def __str__(self):
        return f"Push {self.tanggal.strftime('%d-%m-%Y %H:%M')}"
        
    class Meta:
        verbose_name_plural = "Sinkronisasi ke GitHub"
        db_table = 'sekolah_updateaplikasi'

class KonfigurasiServer(models.Model):
    url_git_remote = models.CharField(
        max_length=255, 
        help_text="URL Repository GitHub (Contoh: https://github.com/username/repo.git)",
        default="origin"
    )
    ssh_public_key = models.TextField(
        blank=True, 
        help_text="Opsional: SSH Public Key jika menggunakan SSH."
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and KonfigurasiServer.objects.exists():
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return "Konfigurasi GitHub"
        
    class Meta:
        verbose_name_plural = "Konfigurasi GitHub"
        db_table = 'sekolah_konfigurasiserver'
