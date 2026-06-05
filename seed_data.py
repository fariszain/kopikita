"""
Script untuk membuat data awal (seed data) KopiKita.
Jalankan: python manage.py shell < seed_data.py
"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kopikita.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from core.models import Category, MenuItem, Reservation, ContactMessage, SiteSettings

# Buat superuser admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kopikita.id', 'admin123')
    print('✅ Superuser admin berhasil dibuat (username: admin, password: admin123)')

# Buat SiteSettings
SiteSettings.get_settings()
print('✅ SiteSettings created')

# Buat Kategori
categories_data = [
    {'name': 'Kopi Espresso', 'description': 'Berbagai varian kopi berbasis espresso', 'icon': '☕'},
    {'name': 'Manual Brew', 'description': 'Kopi seduh manual untuk penikmat sejati', 'icon': '🫖'},
    {'name': 'Non-Coffee', 'description': 'Minuman non-kopi yang menyegarkan', 'icon': '🧋'},
    {'name': 'Makanan Ringan', 'description': 'Kudapan pendamping kopi', 'icon': '🥐'},
    {'name': 'Dessert', 'description': 'Hidangan penutup manis', 'icon': '🍰'},
]
for cd in categories_data:
    Category.objects.get_or_create(name=cd['name'], defaults=cd)
print(f'✅ {len(categories_data)} kategori created')

# Buat Menu Items
cat_espresso = Category.objects.get(name='Kopi Espresso')
cat_manual = Category.objects.get(name='Manual Brew')
cat_noncoffee = Category.objects.get(name='Non-Coffee')
cat_snack = Category.objects.get(name='Makanan Ringan')
cat_dessert = Category.objects.get(name='Dessert')

menu_data = [
    {'name': 'Cappuccino', 'description': 'Espresso dengan steamed milk dan foam lembut. Kombinasi sempurna untuk memulai hari.', 'price': 32000, 'category': cat_espresso, 'is_featured': True},
    {'name': 'Caffe Latte', 'description': 'Espresso dengan susu steamed yang creamy. Rasa lembut dan nikmat.', 'price': 30000, 'category': cat_espresso, 'is_featured': True},
    {'name': 'Americano', 'description': 'Espresso dengan air panas. Simpel, kuat, dan autentik.', 'price': 25000, 'category': cat_espresso},
    {'name': 'Espresso', 'description': 'Shot espresso murni dari biji Arabica pilihan Gayo.', 'price': 20000, 'category': cat_espresso},
    {'name': 'Mocha Latte', 'description': 'Espresso dengan cokelat premium dan steamed milk. Perpaduan manis yang sempurna.', 'price': 35000, 'category': cat_espresso, 'is_featured': True},
    {'name': 'V60 Drip', 'description': 'Pour over dengan Hario V60 menggunakan biji single origin pilihan.', 'price': 35000, 'category': cat_manual, 'is_featured': True},
    {'name': 'French Press', 'description': 'Full immersion brewing untuk body kopi yang kaya dan penuh.', 'price': 30000, 'category': cat_manual},
    {'name': 'Matcha Latte', 'description': 'Matcha premium dari Jepang dengan susu segar. Creamy dan menenangkan.', 'price': 32000, 'category': cat_noncoffee, 'is_featured': True},
    {'name': 'Cokelat Panas', 'description': 'Cokelat premium Belgian dengan susu hangat dan whipped cream.', 'price': 30000, 'category': cat_noncoffee},
    {'name': 'Fresh Juice', 'description': 'Jus buah segar pilihan: jeruk, apel, atau mangga.', 'price': 25000, 'category': cat_noncoffee},
    {'name': 'Croissant', 'description': 'Butter croissant renyah berlapis-lapis, dipanggang sempurna setiap hari.', 'price': 22000, 'category': cat_snack, 'is_featured': True},
    {'name': 'Banana Bread', 'description': 'Roti pisang homemade yang lembut dengan taburan walnut.', 'price': 20000, 'category': cat_snack},
    {'name': 'Tiramisu', 'description': 'Tiramisu klasik Italia dengan espresso dan mascarpone cream.', 'price': 35000, 'category': cat_dessert},
    {'name': 'Cheesecake', 'description': 'New York cheesecake creamy dengan saus berry segar.', 'price': 38000, 'category': cat_dessert},
]
for md in menu_data:
    MenuItem.objects.get_or_create(name=md['name'], defaults=md)
print(f'✅ {len(menu_data)} menu items created')

# Sample Reservations
from datetime import date, time
reservations_data = [
    {'name': 'Andi Wirawan', 'email': 'andi@email.com', 'phone': '081234567890', 'date': date(2026, 6, 5), 'time': time(14, 0), 'guests': 4, 'status': 'confirmed'},
    {'name': 'Siti Nurhaliza', 'email': 'siti@email.com', 'phone': '082345678901', 'date': date(2026, 6, 6), 'time': time(19, 30), 'guests': 2, 'status': 'pending'},
    {'name': 'Budi Pratama', 'email': 'budi@email.com', 'phone': '083456789012', 'date': date(2026, 6, 7), 'time': time(10, 0), 'guests': 6, 'status': 'pending'},
]
for rd in reservations_data:
    Reservation.objects.get_or_create(name=rd['name'], date=rd['date'], defaults=rd)
print(f'✅ {len(reservations_data)} reservations created')

# Sample Messages
messages_data = [
    {'name': 'Dewi Lestari', 'email': 'dewi@email.com', 'subject': 'Pertanyaan Menu Vegetarian', 'message': 'Halo, apakah KopiKita menyediakan pilihan makanan vegetarian? Terima kasih.'},
    {'name': 'Riko Firmansyah', 'email': 'riko@email.com', 'subject': 'Booking Event', 'message': 'Saya ingin booking tempat untuk acara ulang tahun sekitar 20 orang. Apakah bisa?'},
]
for md in messages_data:
    ContactMessage.objects.get_or_create(subject=md['subject'], defaults=md)
print(f'✅ {len(messages_data)} messages created')

print('\n🎉 Seed data selesai! Login: admin / admin123')
