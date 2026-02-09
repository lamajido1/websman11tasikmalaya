import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, ImageDraw
from sekolah.models import Kategori, Berita, Pengumuman, Guru, Galeri, Slider

class Command(BaseCommand):
    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        paths = {
            'berita': os.path.join(media_root, 'berita'),
            'pengumuman': os.path.join(media_root, 'pengumuman'),
            'guru': os.path.join(media_root, 'guru'),
            'galeri': os.path.join(media_root, 'galeri'),
            'sliders': os.path.join(media_root, 'sliders'),
        }
        for p in paths.values():
            os.makedirs(p, exist_ok=True)

        def make_image(path, size, text, color):
            img = Image.new('RGB', size, color)
            d = ImageDraw.Draw(img)
            d.text((20, 20), text, fill=(255, 255, 255))
            img.save(path, format='JPEG')

        if Kategori.objects.count() == 0:
            k_names = ['Akademik', 'Kegiatan', 'Pengumuman']
            for n in k_names:
                Kategori.objects.create(nama=n)

        kategori_list = list(Kategori.objects.all())

        existing_sliders = Slider.objects.count()
        if existing_sliders < 3:
            for i in range(existing_sliders + 1, 4):
                fname = f'slide_{i}.jpg'
                fpath = os.path.join(paths['sliders'], fname)
                make_image(fpath, (1200, 600), f'Slide {i}', (random.randint(0, 200), 80, 160))
                Slider.objects.create(
                    judul=f'Highlight {i}',
                    subjudul='Informasi unggulan sekolah',
                    gambar=f'sliders/{fname}',
                    urutan=i - 1,
                    aktif=True,
                )

        if Berita.objects.count() == 0:
            for i in range(1, 6):
                fname = f'berita_{i}.jpg'
                fpath = os.path.join(paths['berita'], fname)
                make_image(fpath, (1200, 600), f'Berita {i}', (60, random.randint(0, 200), 120))
                Berita.objects.create(
                    judul=f'Berita Penting {i}',
                    konten='Ini adalah konten berita contoh untuk menampilkan layout dan gaya tampilan di website sekolah. Konten ini hanya dummy.',
                    kategori=random.choice(kategori_list) if kategori_list else None,
                    penulis='Admin',
                    gambar=f'berita/{fname}',
                )

        if Pengumuman.objects.count() == 0:
            titles = ['PPDB Dibuka', 'Ujian Tengah Semester', 'Libur Nasional']
            for t in titles:
                Pengumuman.objects.create(judul=t, isi='Ini adalah pengumuman dummy untuk keperluan tampilan.')

        if Guru.objects.count() == 0:
            guru_data = [
                ('Budi Santoso', 'Matematika'),
                ('Siti Aminah', 'Bahasa Indonesia'),
                ('Andi Kurniawan', 'Fisika'),
                ('Rina Maharani', 'Biologi'),
                ('Dedi Supriatna', 'Kimia'),
            ]
            for i, (nama, mapel) in enumerate(guru_data, start=1):
                fname = f'guru_{i}.jpg'
                fpath = os.path.join(paths['guru'], fname)
                make_image(fpath, (300, 300), nama, (random.randint(0, 200), 120, 60))
                Guru.objects.create(
                    nama=nama,
                    nip=f'12345{i:03d}',
                    mata_pelajaran=mapel,
                    foto=f'guru/{fname}',
                    bio='Profil singkat guru untuk tampilan dummy.',
                )

        if Galeri.objects.count() == 0:
            for i in range(1, 7):
                fname = f'galeri_{i}.jpg'
                fpath = os.path.join(paths['galeri'], fname)
                make_image(fpath, (1024, 768), f'Galeri {i}', (100, 100, random.randint(0, 200)))
                Galeri.objects.create(
                    judul=f'Kegiatan Sekolah {i}',
                    gambar=f'galeri/{fname}',
                )

        self.stdout.write('Dummy data created or already present.')
