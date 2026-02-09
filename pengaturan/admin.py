from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from mptt.admin import DraggableMPTTAdmin
from .models import Slider, Menu, Pengaturan
from .forms import MenuForm

@admin.register(Pengaturan)
class PengaturanAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identitas Sekolah', {
            'fields': ('nama_sekolah', 'slogan', 'logo', 'favicon', 'copyright'),
            'description': 'Informasi utama yang akan tampil di Header dan Footer website.'
        }),
        ('Kontak & Alamat', {
            'fields': ('alamat', 'telepon', 'email'),
        }),
        ('Sosial Media', {
            'fields': ('facebook', 'instagram', 'twitter', 'youtube'),
            'classes': ('collapse',),
            'description': 'Link sosial media (biarkan kosong jika tidak ada).'
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('judul', 'urutan', 'aktif')
    list_editable = ('urutan', 'aktif')
    ordering = ('urutan',)
    list_per_page = 20

@admin.register(Menu)
class MenuAdmin(DraggableMPTTAdmin):
    form = MenuForm
    list_display = ('tree_actions', 'indented_title', 'url', 'aktif')
    list_display_links = ('indented_title',)
    list_filter = ('aktif',)
    search_fields = ('nama', 'url')
    list_per_page = 20
