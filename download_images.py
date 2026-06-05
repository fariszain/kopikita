import os
import sys
import django
import urllib.request
from django.core.files import File
from tempfile import NamedTemporaryFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopikita.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import MenuItem

image_mapping = {
    'Cappuccino': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800&q=80',
    'Caffe Latte': 'https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=800&q=80',
    'Americano': 'https://images.unsplash.com/photo-1551030173-122aabc4489c?w=800&q=80',
    'Espresso': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=800&q=80',
    'Mocha Latte': 'https://images.unsplash.com/photo-1596078841242-12f73caf6fdc?w=800&q=80',
    'V60 Drip': 'https://images.unsplash.com/photo-1495474472205-16270d11a7de?w=800&q=80',
    'French Press': 'https://images.unsplash.com/photo-1544265431-157d609351e3?w=800&q=80',
    'Matcha Latte': 'https://images.unsplash.com/photo-1515823662972-da6a2e4d3002?w=800&q=80',
    'Cokelat Panas': 'https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=800&q=80',
    'Fresh Juice': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=800&q=80',
    'Croissant': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800&q=80',
    'Banana Bread': 'https://images.unsplash.com/photo-1621236166417-380d0d571f30?w=800&q=80',
    'Tiramisu': 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=800&q=80',
    'Cheesecake': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=800&q=80'
}

print("Mulai mengunduh gambar...")

for name, url in image_mapping.items():
    try:
        item = MenuItem.objects.filter(name=name).first()
        if item:
            print(f"Mengunduh gambar untuk {name}...")
            
            # Download the image to a temporary file
            img_temp = NamedTemporaryFile(delete=True)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                img_temp.write(response.read())
            img_temp.flush()
            
            filename = f"{name.replace(' ', '_').lower()}.jpg"
            item.image.save(filename, File(img_temp), save=True)
            print(f"✅ Gambar {name} berhasil disimpan.")
    except Exception as e:
        print(f"❌ Gagal mengunduh gambar untuk {name}: {e}")

print("Selesai!")
