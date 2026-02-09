from django.contrib import admin
from .models import Pengumuman, Guru, Halaman

@admin.register(Pengumuman)
class PengumumanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal')
    search_fields = ('judul',)
    list_per_page = 20

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'mata_pelajaran')
    search_fields = ('nama', 'nip', 'mata_pelajaran')
    list_per_page = 20

@admin.register(Halaman)
class HalamanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'slug', 'aktif')
    prepopulated_fields = {'slug': ('judul',)}
    list_filter = ('aktif',)
    search_fields = ('judul', 'konten')

# Konfigurasi Header Admin Default
admin.site.site_header = "Administrasi Sekolah"
admin.site.site_title = "Admin Sekolah"
admin.site.index_title = "Selamat Datang di Dashboard Admin"
