from django.db import models
from django.utils.text import slugify
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField

class Pengumuman(models.Model):
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    tanggal = models.DateField(auto_now_add=True)
    file_lampiran = models.FileField(upload_to='pengumuman/', blank=True, null=True)

    def __str__(self):
        return self.judul
    
    class Meta:
        verbose_name_plural = "Pengumuman"

class Guru(models.Model):
    nama = models.CharField(max_length=150)
    nip = models.CharField(max_length=30, blank=True, null=True)
    mata_pelajaran = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='guru/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Kompresi Gambar Otomatis
        if self.foto:
            try:
                img = Image.open(self.foto.path)
                if img.height > 600 or img.width > 600:
                    output_size = (600, 600)
                    img.thumbnail(output_size)
                    img.save(self.foto.path, quality=85, optimize=True)
            except Exception as e:
                pass

    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = "Guru"

class Halaman(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    konten = RichTextUploadingField()
    aktif = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

    class Meta:
        verbose_name_plural = "Halaman Statis"
