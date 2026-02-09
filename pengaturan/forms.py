from django import forms
from django.utils.safestring import mark_safe
from .models import Menu
from sekolah.models import Halaman

class DatalistWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': f'list__{self._name}', 'autocomplete': 'off'})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super().render(name, value, attrs, renderer)
        data_list = f'<datalist id="list__{self._name}">'
        for item in self._list:
            data_list += f'<option value="{item}">'
        data_list += '</datalist>'
        return mark_safe(text_html + data_list)

class MenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Base URLs
        urls = [
            '/',
            '/profil/',
            '/guru/',
            '/berita/',
            '/galeri/',
            '#',
            'https://',
        ]
        
        # Add Halaman URLs
        try:
            halaman_pages = Halaman.objects.filter(aktif=True)
            for page in halaman_pages:
                urls.append(f'/halaman/{page.slug}/')
        except:
            pass
            
        self.fields['url'].widget = DatalistWidget(data_list=urls, name='url_list')

    class Meta:
        model = Menu
        fields = '__all__'
