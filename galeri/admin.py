from django.contrib import admin
from pengaturan.admin import BasePerPageAdmin
from .models import Galeri, FotoGaleri


class FotoGaleriInline(admin.TabularInline):
    model = FotoGaleri
    extra = 3
    fields = ('gambar', 'keterangan')

@admin.register(Galeri)
class GaleriAdmin(BasePerPageAdmin):
    list_display = ('judul', 'tanggal')
    list_per_page = 20
    inlines = [FotoGaleriInline]
