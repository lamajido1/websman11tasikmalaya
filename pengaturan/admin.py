from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
import subprocess
import os
import datetime
from django.conf import settings
from mptt.admin import DraggableMPTTAdmin
from .models import Slider, Menu, Pengaturan, KonfigurasiServer, UpdateAplikasi, BackupDatabase
from .forms import MenuForm
from django.db import models


PER_PAGE_OPTIONS = (10, 50, 100)


class BasePerPageAdmin(admin.ModelAdmin):
    per_page_param = 'per_page'

    def changelist_view(self, request, extra_context=None):
        default_per_page = getattr(type(self), 'list_per_page', 20)
        per_page = request.GET.get(self.per_page_param)

        if per_page:
            try:
                per_page_int = int(per_page)
            except (TypeError, ValueError):
                per_page_int = None

            if per_page_int in PER_PAGE_OPTIONS:
                self.list_per_page = per_page_int
            else:
                self.list_per_page = default_per_page
        else:
            self.list_per_page = default_per_page

        extra_context = extra_context or {}
        extra_context.setdefault('current_per_page', self.list_per_page)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(KonfigurasiServer)
class KonfigurasiGitHubAdmin(BasePerPageAdmin):
    list_display = ('url_git_remote', 'status_remote', 'mysqldump_path')
    
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
class PushGitHubAdmin(BasePerPageAdmin):
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
            # Get current branch name
            branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, cwd=os.getcwd())
            current_branch = branch_result.stdout.strip()
            
            if not current_branch:
                current_branch = 'main' # Fallback
                
            log_output.append(f"Pushing to branch: {current_branch}")
            
            # Push ke current branch
            result = subprocess.run(['git', 'push', '-u', 'origin', current_branch], capture_output=True, text=True, cwd=os.getcwd())
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

@admin.register(BackupDatabase)
class BackupDatabaseAdmin(BasePerPageAdmin):
    list_display = ('tanggal', 'status', 'tampil_log')
    readonly_fields = ('tanggal', 'status', 'log', 'file_backup')
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
            # 1. Get Konfigurasi
            config = KonfigurasiServer.objects.first()
            if not config:
                raise Exception("Konfigurasi GitHub belum diatur. Harap atur di menu Konfigurasi GitHub terlebih dahulu.")
                
            mysqldump_path = config.mysqldump_path
            if not os.path.exists(mysqldump_path):
                 # Try fallback default if path doesn't exist
                 fallback = r"C:\laragon82\bin\mysql\mysql-8.4.3-winx64\bin\mysqldump.exe"
                 if os.path.exists(fallback):
                     mysqldump_path = fallback
                 else:
                    raise Exception(f"File mysqldump.exe tidak ditemukan di: {mysqldump_path}")

            # 2. Prepare Backup Path
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            backup_filename = f"backup_smay8199_{timestamp}.sql"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 3. Get DB Settings
            db_settings = settings.DATABASES['default']
            db_user = db_settings['USER']
            db_password = db_settings['PASSWORD']
            db_name = db_settings['NAME']
            db_host = db_settings['HOST']
            
            # 4. Run mysqldump
            log_output.append(f"=== MYSQL DUMP ===")
            log_output.append(f"Target: {backup_path}")
            
            # Construct command
            # Note: Putting password directly in command line can be insecure but easiest for this context.
            # Using --result-file to handle output encoding correctly on Windows
            cmd = [
                mysqldump_path,
                f"--user={db_user}",
                f"--password={db_password}",
                f"--host={db_host}",
                "--result-file=" + backup_path,
                db_name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode != 0:
                log_output.append(f"STDERR: {result.stderr}")
                raise Exception(f"mysqldump error: {result.stderr}")
            else:
                log_output.append("Dump Database Berhasil.")
                
                # Update model with file path (relative to media or just path)
                # Since we are not using MediaStorage for this logic but raw filesystem,
                # we just store relative path if we want to serve it, or we just rely on git push.
                # Here we won't serve it via Django Media URL for security, just keep it on disk.
                
            # 5. Git Push (Add, Commit, Push)
            log_output.append("\n=== GIT PUSH BACKUP ===")
            
            # git add backups/filename.sql
            subprocess.run(['git', 'add', f'backups/{backup_filename}'], check=True, cwd=os.getcwd())
            
            commit_msg = f"Backup Database: {backup_filename}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, cwd=os.getcwd())
            
            # Push
            branch_result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, cwd=os.getcwd())
            current_branch = branch_result.stdout.strip() or 'main'
            
            push_result = subprocess.run(['git', 'push', '-u', 'origin', current_branch], capture_output=True, text=True, cwd=os.getcwd())
            log_output.append(push_result.stdout)
            
            if push_result.returncode != 0:
                log_output.append(f"STDERR: {push_result.stderr}")
                status = 'Gagal' # Dump succes, Push failed
            
        except Exception as e:
            status = 'Gagal'
            log_output.append(f"\nEXCEPTION: {str(e)}")
            messages.error(request, f"Backup Gagal: {str(e)}")
            
        obj.log = "\n".join(log_output)
        obj.status = status
        obj.file_backup.name = f"backups/{backup_filename}" if 'backup_filename' in locals() else None
        super().save_model(request, obj, form, change)
        
        if status == 'Sukses':
            messages.success(request, "Database berhasil di-backup dan di-push ke GitHub!")

@admin.register(Pengaturan)
class PengaturanAdmin(BasePerPageAdmin):
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
class SliderAdmin(BasePerPageAdmin):
    list_display = ('judul', 'urutan', 'aktif')
    list_editable = ('urutan', 'aktif')
    ordering = ('urutan',)
    list_per_page = 20

@admin.register(Menu)
class MenuAdmin(BasePerPageAdmin, DraggableMPTTAdmin):
    form = MenuForm
    list_display = ('tree_actions', 'indented_title', 'url', 'aktif')
    list_display_links = ('indented_title',)
    list_filter = ('aktif',)
    search_fields = ('nama', 'url')
    list_per_page = 20
