from django.db import models
from PIL import Image

class Galeri(models.Model):
    judul = models.CharField(max_length=150)
    gambar = models.ImageField(upload_to='galeri/', help_text="Sampul Album Utama")
    tanggal = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Kompresi Gambar Otomatis
        if self.gambar:
            try:
                img = Image.open(self.gambar.path)
                if img.height > 1000 or img.width > 1000:
                    output_size = (1000, 1000)
                    img.thumbnail(output_size)
                    img.save(self.gambar.path, quality=85, optimize=True)
            except Exception as e:
                pass

    def __str__(self):
        return self.judul
    
    class Meta:
        verbose_name_plural = "Galeri (Album)"
        db_table = 'sekolah_galeri'

class FotoGaleri(models.Model):
    galeri = models.ForeignKey(Galeri, on_delete=models.CASCADE, related_name='foto_foto')
    gambar = models.ImageField(upload_to='galeri/detail/')
    keterangan = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Kompresi Gambar Otomatis
        if self.gambar:
            try:
                img = Image.open(self.gambar.path)
                if img.height > 1000 or img.width > 1000:
                    output_size = (1000, 1000)
                    img.thumbnail(output_size)
                    img.save(self.gambar.path, quality=85, optimize=True)
            except Exception as e:
                pass

    class Meta:
        verbose_name_plural = "Foto Tambahan"
        db_table = 'sekolah_fotogaleri'
