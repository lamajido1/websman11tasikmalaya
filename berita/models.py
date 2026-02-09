from django.db import models
from django.utils.text import slugify
from PIL import Image

class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = "Kategori"
        db_table = 'sekolah_kategori'

class Berita(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    konten = models.TextField()
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    penulis = models.CharField(max_length=100)
    tanggal_publikasi = models.DateTimeField(auto_now_add=True)
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)
        
        # Kompresi Gambar Otomatis
        if self.gambar:
            try:
                img = Image.open(self.gambar.path)
                if img.height > 800 or img.width > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size)
                    img.save(self.gambar.path, quality=85, optimize=True)
            except Exception as e:
                pass

    def __str__(self):
        return self.judul
    
    class Meta:
        verbose_name_plural = "Berita"
        db_table = 'sekolah_berita'
