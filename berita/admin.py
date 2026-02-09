from django.contrib import admin
from .models import Kategori, Berita

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('nama', 'slug')
    prepopulated_fields = {'slug': ('nama',)}
    list_per_page = 20

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'penulis', 'tanggal_publikasi')
    search_fields = ('judul', 'konten')
    list_filter = ('kategori', 'tanggal_publikasi')
    prepopulated_fields = {'slug': ('judul',)}
    list_per_page = 20
