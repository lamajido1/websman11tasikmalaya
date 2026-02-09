from pengaturan.models import Pengaturan, Menu

def pengaturan_sekolah(request):
    try:
        pengaturan = Pengaturan.objects.first()
    except:
        pengaturan = None
        
    # Ambil semua menu aktif (MPTT akan menangani hierarki di template)
    menu_navigasi = Menu.objects.filter(aktif=True)
    
    return {
        'sekolah': pengaturan,
        'menu_navigasi': menu_navigasi,
    }
