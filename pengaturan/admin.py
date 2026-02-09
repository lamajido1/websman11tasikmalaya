from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
import subprocess
import os
from mptt.admin import DraggableMPTTAdmin
from .models import Slider, Menu, Pengaturan, KonfigurasiServer, UpdateAplikasi
from .forms import MenuForm

@admin.register(KonfigurasiServer)
class KonfigurasiGitHubAdmin(admin.ModelAdmin):
    list_display = ('url_git_remote', 'status_remote')
    
    def status_remote(self, obj):
        try:
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, cwd=os.getcwd())
            if obj.url_git_remote in result.stdout:
                return "Terhubung"
            return "Belum Terhubung / URL Beda"
        except:
            return "Error Git"
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if obj.url_git_remote:
            try:
                # Cek apakah remote origin sudah ada
                remotes = subprocess.run(['git', 'remote'], capture_output=True, text=True, cwd=os.getcwd()).stdout
                
                if 'origin' in remotes:
                    subprocess.run(['git', 'remote', 'set-url', 'origin', obj.url_git_remote], check=True, cwd=os.getcwd())
                else:
                    subprocess.run(['git', 'remote', 'add', 'origin', obj.url_git_remote], check=True, cwd=os.getcwd())
                    
                messages.success(request, f"Git Remote berhasil diatur ke: {obj.url_git_remote}")
            except Exception as e:
                messages.error(request, f"Gagal mengatur Git Remote: {e}")

@admin.register(UpdateAplikasi)
class PushGitHubAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'status', 'versi', 'tampil_log')
    readonly_fields = ('tanggal', 'status', 'versi', 'log')
    list_per_page = 10
    
    def tampil_log(self, obj):
        return (obj.log[:100] + '...') if len(obj.log) > 100 else obj.log
    tampil_log.short_description = 'Log Output'

    def has_add_permission(self, request):
        return True
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def save_model(self, request, obj, form, change):
        log_output = []
        status = 'Sukses'
        
        try:
            log_output.append("=== GIT STATUS ===")
            result = subprocess.run(['git', 'status'], capture_output=True, text=True, cwd=os.getcwd())
            log_output.append(result.stdout)

            log_output.append("\n=== GIT ADD ===")
            result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True, cwd=os.getcwd())
            log_output.append(result.stdout)
            
            log_output.append("\n=== GIT COMMIT ===")
            commit_msg = f"Auto-save from Admin Panel: {obj.tanggal}"
            result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True, cwd=os.getcwd())
            log_output.append(result.stdout)
            
            log_output.append("\n=== GIT PUSH ===")
            # Push ke branch main
            result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True, cwd=os.getcwd())
            log_output.append(result.stdout)
            if result.stderr:
                log_output.append(f"STDERR: {result.stderr}")
                if "error" in result.stderr.lower() or "fatal" in result.stderr.lower():
                     # Note: git push outputs info to stderr too, so only mark failed if return code is non-zero
                     if result.returncode != 0:
                        status = 'Gagal'

        except Exception as e:
            status = 'Gagal'
            log_output.append(f"\nEXCEPTION: {str(e)}")
            messages.error(request, f"Push Gagal: {str(e)}")
            
        obj.log = "\n".join(log_output)
        obj.status = status
        obj.versi = "Latest Push"
        super().save_model(request, obj, form, change)
        
        if status == 'Sukses':
            messages.success(request, "Kode berhasil di-push ke GitHub!")
        else:
            messages.error(request, "Terjadi kesalahan saat push ke GitHub. Cek log detail.")

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
