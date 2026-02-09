from django.urls import path
from . import views

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('profil/', views.profil_sekolah, name='profil'),
    path('guru/', views.daftar_guru, name='guru'),
    path('galeri/', views.galeri_list, name='galeri'),
    path('berita/', views.berita_list, name='berita_list'),
    path('kategori/<slug:slug>/', views.kategori_berita, name='kategori_berita'),
    path('berita/<slug:slug>/', views.berita_detail, name='berita_detail'),
    path('halaman/<slug:slug>/', views.halaman_detail, name='halaman_detail'),
]
