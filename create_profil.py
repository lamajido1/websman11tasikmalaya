
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websman11.settings")
django.setup()

from sekolah.models import Halaman

content = """<div class="row align-items-center mb-5">
    <div class="col-md-4 text-center mb-4 mb-md-0">
        <img src="/static/admin/img/icon-unknown.svg" alt="Building Icon" style="width: 150px; height: 150px;"> 
        <!-- Note: Icon replaced with img tag or keep font awesome if supported in editor -->
        <!-- Since CKEditor might filter <i> tags or they might not render in editor preview, 
             but we allowed 'div' and other tags. Let's try to keep structure. -->
    </div>
    <div class="col-md-8">
        <h3 class="fw-bold text-dark mb-3">Tentang Kami</h3>
        <p class="fs-5 text-secondary lh-lg text-justify">
            SMA Y8199 Tasikmalaya adalah salah satu sekolah menengah atas unggulan yang berlokasi di Tasikmalaya.
            Kami berkomitmen untuk memberikan pendidikan terbaik bagi siswa-siswi kami dengan fasilitas modern dan tenaga pengajar yang profesional.
        </p>
    </div>
</div>

<hr class="my-5">

<div class="row g-4">
    <div class="col-md-6">
        <div class="p-4 bg-light rounded-4 h-100 border border-primary border-opacity-10">
            <h3 class="fw-bold text-primary mb-3">Visi</h3>
            <p class="fs-5 mb-0">"Terwujudnya sekolah yang unggul dalam prestasi, berlandaskan iman dan taqwa."</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="p-4 bg-light rounded-4 h-100 border border-success border-opacity-10">
            <h3 class="fw-bold text-success mb-3">Misi</h3>
            <ul class="list-unstyled fs-5">
                <li class="mb-2 d-flex">Melaksanakan pembelajaran dan bimbingan secara efektif.</li>
                <li class="mb-2 d-flex">Menumbuhkan semangat keunggulan secara intensif.</li>
                <li class="mb-2 d-flex">Mendorong siswa mengenali potensi dirinya.</li>
            </ul>
        </div>
    </div>
</div>"""

# I simplified the HTML slightly to be safer for CKEditor (removed complex i classes if they are not supported, 
# but I'll try to keep them if I can. actually I'll use the original content but wrap it.)

original_content = """<div class="row align-items-center mb-5">
                    <div class="col-md-4 text-center mb-4 mb-md-0">
                        <i class="bi bi-building text-primary" style="font-size: 8rem;"></i>
                    </div>
                    <div class="col-md-8">
                        <h3 class="fw-bold text-dark mb-3">Tentang Kami</h3>
                        <p class="fs-5 text-secondary lh-lg text-justify">
                            SMA Y8199 Tasikmalaya adalah salah satu sekolah menengah atas unggulan yang berlokasi di Tasikmalaya.
                            Kami berkomitmen untuk memberikan pendidikan terbaik bagi siswa-siswi kami dengan fasilitas modern dan tenaga pengajar yang profesional.
                        </p>
                    </div>
                </div>

                <hr class="my-5">

                <div class="row g-4">
                    <div class="col-md-6">
                        <div class="p-4 bg-light rounded-4 h-100 border border-primary border-opacity-10">
                            <h3 class="fw-bold text-primary mb-3"><i class="bi bi-eye-fill me-2"></i>Visi</h3>
                            <p class="fs-5 mb-0">"Terwujudnya sekolah yang unggul dalam prestasi, berlandaskan iman dan taqwa."</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="p-4 bg-light rounded-4 h-100 border border-success border-opacity-10">
                            <h3 class="fw-bold text-success mb-3"><i class="bi bi-bullseye me-2"></i>Misi</h3>
                            <ul class="list-unstyled fs-5">
                                <li class="mb-2 d-flex"><i class="bi bi-check-circle-fill text-success me-2 mt-1"></i> Melaksanakan pembelajaran dan bimbingan secara efektif.</li>
                                <li class="mb-2 d-flex"><i class="bi bi-check-circle-fill text-success me-2 mt-1"></i> Menumbuhkan semangat keunggulan secara intensif.</li>
                                <li class="mb-2 d-flex"><i class="bi bi-check-circle-fill text-success me-2 mt-1"></i> Mendorong siswa mengenali potensi dirinya.</li>
                            </ul>
                        </div>
                    </div>
                </div>"""

Halaman.objects.get_or_create(
    slug='profil-sekolah',
    defaults={
        'judul': 'Profil Sekolah',
        'konten': original_content,
        'aktif': True
    }
)
print("Profil Sekolah page created/verified.")
