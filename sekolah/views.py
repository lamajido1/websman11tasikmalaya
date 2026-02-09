from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from berita.models import Berita, Kategori
from galeri.models import Galeri
from pengaturan.models import Slider
from .models import Pengumuman, Guru, Halaman

@cache_page(60)
def beranda(request):
    slider_list = Slider.objects.filter(aktif=True).order_by('urutan')
    berita_terbaru = Berita.objects.order_by('-tanggal_publikasi')[:3]
    pengumuman_terbaru = Pengumuman.objects.order_by('-tanggal')[:3]
    galeri_terbaru = Galeri.objects.order_by('-tanggal')[:4]
    
    context = {
        'slider_list': slider_list,
        'berita_list': berita_terbaru,
        'pengumuman_list': pengumuman_terbaru,
        'galeri_list': galeri_terbaru,
    }
    return render(request, 'sekolah/beranda.html', context)

def profil_sekolah(request):
    profil = Halaman.objects.filter(slug='profil-sekolah', aktif=True).first()
    return render(request, 'sekolah/profil.html', {'profil': profil})

def daftar_guru(request):
    guru_list = Guru.objects.all()
    return render(request, 'sekolah/guru.html', {'guru_list': guru_list})

@cache_page(60)
def berita_list(request):
    berita = Berita.objects.all().order_by('-tanggal_publikasi')
    return render(request, 'sekolah/berita_list.html', {'berita_list': berita})

def kategori_berita(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug)
    berita = Berita.objects.filter(kategori=kategori).order_by('-tanggal_publikasi')
    return render(request, 'sekolah/berita_list.html', {
        'berita_list': berita,
        'kategori': kategori
    })

def berita_detail(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    return render(request, 'sekolah/berita_detail.html', {'berita': berita})

def galeri_list(request):
    galeri = Galeri.objects.all().order_by('-tanggal')
    return render(request, 'sekolah/galeri.html', {'galeri_list': galeri})

def halaman_detail(request, slug):
    halaman = get_object_or_404(Halaman, slug=slug, aktif=True)
    return render(request, 'sekolah/halaman_detail.html', {'halaman': halaman})
