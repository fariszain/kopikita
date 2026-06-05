# ☕ KopiKita - Coffee Shop Web Application

Aplikasi web untuk manajemen kedai kopi **KopiKita**, dibangun menggunakan **Django** (Python).

## 📋 Deskripsi

KopiKita adalah aplikasi web lengkap untuk mengelola kedai kopi yang terdiri dari:

- **Halaman Publik** — Landing page, halaman menu, tentang kami, reservasi, dan kontak
- **Dashboard Admin** — Panel admin untuk mengelola menu, kategori, reservasi, dan pesan kontak

## 🧰 Teknologi

| Teknologi     | Keterangan                     |
| ------------- | ------------------------------ |
| **Framework** | Django 6.0 (Python)            |
| **Database**  | SQLite3                        |
| **Frontend**  | HTML5, Vanilla CSS, JavaScript |
| **Font**      | Google Fonts (Inter, Playfair) |

## 📁 Struktur Folder

```
kopikita/
├── kopikita/            # Konfigurasi Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Aplikasi utama
│   ├── models.py        # Model: Category, MenuItem, Reservation, etc.
│   ├── views.py         # Views untuk public & dashboard
│   ├── forms.py         # Form classes
│   ├── urls.py          # URL routing
│   └── admin.py         # Django admin registration
├── templates/
│   ├── public/          # Template halaman publik
│   │   ├── base.html
│   │   ├── landing.html
│   │   ├── menu.html
│   │   ├── about.html
│   │   ├── reservation.html
│   │   └── contact.html
│   └── dashboard/       # Template dashboard admin
│       ├── base.html
│       ├── login.html
│       ├── index.html
│       ├── menu_list.html
│       ├── menu_form.html
│       └── ... (CRUD templates)
├── static/
│   ├── css/
│   │   ├── style.css      # CSS halaman publik
│   │   └── dashboard.css  # CSS dashboard admin
│   └── js/
│       └── main.js        # JavaScript
├── media/                 # Upload gambar menu
├── manage.py
├── requirements.txt
├── seed_data.py           # Script data awal
└── README.md
```

## 🚀 Instalasi & Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/username/kopikita.git
cd kopikita
```

### 2. Buat Virtual Environment (Opsional)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Migrasi Database

```bash
python manage.py makemigrations core
python manage.py migrate
```

### 5. Buat Data Awal (Seed)

```bash
python seed_data.py
```

Ini akan membuat:
- Akun admin (username: `admin`, password: `admin123`)
- 5 kategori menu
- 14 menu items
- 3 reservasi contoh
- 2 pesan kontak contoh

### 6. Jalankan Server

```bash
python manage.py runserver
```

Buka di browser: **http://127.0.0.1:8000/**

## 🔑 Login Dashboard

- URL: `http://127.0.0.1:8000/dashboard/login/`
- Username: `admin`
- Password: `admin123`

## ✅ Fitur Utama

### Halaman Publik (Tanpa Login)
- ✅ **Landing Page** — Hero section, menu unggulan, kategori, keunggulan
- ✅ **Halaman Menu** — Daftar menu dengan filter kategori
- ✅ **Halaman Tentang** — Cerita, nilai, dan tim KopiKita
- ✅ **Halaman Reservasi** — Form booking meja
- ✅ **Halaman Kontak** — Form kirim pesan

### Dashboard Admin (Wajib Login)
- ✅ **Dashboard Overview** — Statistik, aksi cepat, data terbaru
- ✅ **CRUD Menu Items** — Tambah, lihat, edit, hapus menu
- ✅ **CRUD Kategori** — Tambah, lihat, edit, hapus kategori
- ✅ **Kelola Reservasi** — Lihat, edit status, hapus reservasi
- ✅ **Kelola Pesan** — Baca, tandai, hapus pesan kontak
- ✅ **Pengaturan Situs** — Edit informasi website

## 📸 Screenshots

### Landing Page
Halaman utama dengan desain modern dark theme, hero section animasi, menu unggulan, dan call-to-action.

### Dashboard Admin
Panel admin dengan sidebar navigasi, statistik real-time, dan tabel data yang responsif.

## 👤 Dibuat Oleh

**[Nama Anda]** — Proyek Perangkat Lunak, 2026
