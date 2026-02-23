from django.contrib import admin
from pengaturan.admin import BasePerPageAdmin
from .models import Kategori, Berita


@admin.register(Kategori)
class KategoriAdmin(BasePerPageAdmin):
    list_display = ('nama', 'slug')
    prepopulated_fields = {'slug': ('nama',)}
    list_per_page = 20

@admin.register(Berita)
class BeritaAdmin(BasePerPageAdmin):
    list_display = ('judul', 'kategori', 'penulis', 'tanggal_publikasi')
    search_fields = ('judul', 'konten')
    list_filter = ('kategori', 'tanggal_publikasi')
    prepopulated_fields = {'slug': ('judul',)}
    list_per_page = 20
