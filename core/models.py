from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Kategori menu (Kopi, Non-Kopi, Makanan, dll)"""
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    icon = models.CharField(
        max_length=50, default='☕',
        verbose_name="Icon",
        help_text="Emoji atau icon untuk kategori"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def menu_count(self):
        return self.menuitem_set.filter(is_available=True).count()


class MenuItem(models.Model):
    """Item menu kopi / makanan"""
    name = models.CharField(max_length=200, verbose_name="Nama Menu")
    description = models.TextField(verbose_name="Deskripsi")
    price = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name="Harga (Rp)"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name="Kategori"
    )
    image = models.ImageField(
        upload_to='menu/', blank=True, null=True,
        verbose_name="Gambar"
    )
    is_available = models.BooleanField(default=True, verbose_name="Tersedia")
    is_featured = models.BooleanField(default=False, verbose_name="Menu Unggulan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - Rp {self.price:,.0f}"


class Reservation(models.Model):
    """Reservasi meja di kafe"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu'),
        ('confirmed', 'Dikonfirmasi'),
        ('cancelled', 'Dibatalkan'),
        ('completed', 'Selesai'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nama")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="No. Telepon")
    date = models.DateField(verbose_name="Tanggal")
    time = models.TimeField(verbose_name="Waktu")
    guests = models.PositiveIntegerField(verbose_name="Jumlah Tamu")
    message = models.TextField(blank=True, verbose_name="Pesan Tambahan")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reservasi"
        verbose_name_plural = "Reservasi"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"


class ContactMessage(models.Model):
    """Pesan kontak dari pengunjung"""
    name = models.CharField(max_length=200, verbose_name="Nama")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=300, verbose_name="Subjek")
    message = models.TextField(verbose_name="Pesan")
    is_read = models.BooleanField(default=False, verbose_name="Sudah Dibaca")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pesan Kontak"
        verbose_name_plural = "Pesan Kontak"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"


class SiteSettings(models.Model):
    """Pengaturan situs (singleton)"""
    site_name = models.CharField(max_length=200, default="KopiKita")
    tagline = models.CharField(max_length=500, default="Secangkir Kebahagiaan di Setiap Tegukan")
    about_text = models.TextField(
        default="KopiKita adalah kedai kopi yang menyajikan kopi berkualitas tinggi dari biji pilihan Nusantara."
    )
    address = models.TextField(default="Jl. Kopi Nikmat No. 42, Jakarta Selatan")
    phone = models.CharField(max_length=20, default="+62 812-3456-7890")
    email = models.EmailField(default="hello@kopikita.id")
    opening_hours = models.CharField(max_length=200, default="Setiap Hari, 07:00 - 22:00")
    instagram = models.URLField(blank=True, default="https://instagram.com/kopikita")
    whatsapp = models.URLField(blank=True, default="https://wa.me/6281234567890")

    class Meta:
        verbose_name = "Pengaturan Situs"
        verbose_name_plural = "Pengaturan Situs"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure singleton
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
