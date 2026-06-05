from django import forms
from .models import MenuItem, Category, Reservation, ContactMessage, SiteSettings


class MenuItemForm(forms.ModelForm):
    """Form untuk menambah/mengedit menu item"""
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'image', 'is_available', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama menu...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Deskripsi menu...',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Contoh: 25000'
            }),
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-input-file'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }


class CategoryForm(forms.ModelForm):
    """Form untuk menambah/mengedit kategori"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama kategori...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Deskripsi kategori...',
                'rows': 3
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '☕'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }


class ReservationForm(forms.ModelForm):
    """Form untuk reservasi (public)"""
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama lengkap Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@contoh.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '08xxxxxxxxxx'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Jumlah tamu',
                'min': 1,
                'max': 20
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Pesan tambahan (opsional)...',
                'rows': 3
            }),
        }


class ReservationAdminForm(forms.ModelForm):
    """Form untuk admin mengedit reservasi"""
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'message', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'guests': forms.NumberInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }


class ContactForm(forms.ModelForm):
    """Form untuk pesan kontak (public)"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nama Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@contoh.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subjek pesan'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Tulis pesan Anda...',
                'rows': 5
            }),
        }


class SiteSettingsForm(forms.ModelForm):
    """Form untuk pengaturan situs"""
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-input'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'about_text': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-input'}),
            'instagram': forms.URLInput(attrs={'class': 'form-input'}),
            'whatsapp': forms.URLInput(attrs={'class': 'form-input'}),
        }
