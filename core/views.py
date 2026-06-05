from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

from .models import Category, MenuItem, Reservation, ContactMessage, SiteSettings
from .forms import (
    MenuItemForm, CategoryForm, ReservationForm,
    ReservationAdminForm, ContactForm, SiteSettingsForm
)


# =====================================================
# PUBLIC VIEWS
# =====================================================

def get_site_settings():
    """Helper untuk mendapatkan pengaturan situs"""
    return SiteSettings.get_settings()


def landing_page(request):
    """Halaman utama (Landing Page)"""
    settings = get_site_settings()
    featured_items = MenuItem.objects.filter(
        is_featured=True, is_available=True
    ).select_related('category')[:6]
    categories = Category.objects.filter(is_active=True)

    context = {
        'settings': settings,
        'featured_items': featured_items,
        'categories': categories,
        'page_title': f'{settings.site_name} - {settings.tagline}',
    }
    return render(request, 'public/landing.html', context)


def menu_page(request):
    """Halaman menu"""
    settings = get_site_settings()
    categories = Category.objects.filter(is_active=True).prefetch_related('menuitem_set')
    active_category = request.GET.get('category', 'all')

    if active_category != 'all':
        menu_items = MenuItem.objects.filter(
            is_available=True, category__id=active_category
        ).select_related('category')
    else:
        menu_items = MenuItem.objects.filter(
            is_available=True
        ).select_related('category')

    context = {
        'settings': settings,
        'categories': categories,
        'menu_items': menu_items,
        'active_category': active_category,
        'page_title': f'Menu - {settings.site_name}',
    }
    return render(request, 'public/menu.html', context)


def about_page(request):
    """Halaman tentang kami"""
    settings = get_site_settings()
    context = {
        'settings': settings,
        'page_title': f'Tentang Kami - {settings.site_name}',
    }
    return render(request, 'public/about.html', context)


def reservation_page(request):
    """Halaman reservasi"""
    settings = get_site_settings()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Reservasi berhasil dikirim! Kami akan menghubungi Anda segera.')
            return redirect('reservation')
    else:
        form = ReservationForm()

    context = {
        'settings': settings,
        'form': form,
        'page_title': f'Reservasi - {settings.site_name}',
    }
    return render(request, 'public/reservation.html', context)


def contact_page(request):
    """Halaman kontak"""
    settings = get_site_settings()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Pesan berhasil dikirim! Terima kasih telah menghubungi kami.')
            return redirect('contact')
    else:
        form = ContactForm()

    context = {
        'settings': settings,
        'form': form,
        'page_title': f'Kontak - {settings.site_name}',
    }
    return render(request, 'public/contact.html', context)


# =====================================================
# DASHBOARD / ADMIN VIEWS
# =====================================================

def dashboard_login(request):
    """Halaman login dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'dashboard/login.html', {
        'page_title': 'Login Dashboard'
    })


def dashboard_logout(request):
    """Logout"""
    logout(request)
    messages.info(request, 'Anda telah keluar dari dashboard.')
    return redirect('landing')


@login_required
def dashboard_index(request):
    """Dashboard utama - overview statistik"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    stats = {
        'total_menu': MenuItem.objects.count(),
        'available_menu': MenuItem.objects.filter(is_available=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_reservations': Reservation.objects.count(),
        'pending_reservations': Reservation.objects.filter(status='pending').count(),
        'confirmed_reservations': Reservation.objects.filter(status='confirmed').count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_messages': ContactMessage.objects.count(),
        'recent_reservations': Reservation.objects.all()[:5],
        'recent_messages': ContactMessage.objects.filter(is_read=False)[:5],
    }

    context = {
        'stats': stats,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)


# --- Menu CRUD ---

@login_required
def menu_list(request):
    """Daftar semua menu items dengan pagination"""
    items = MenuItem.objects.all().select_related('category')
    search = request.GET.get('search', '')
    if search:
        items = items.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    # Set up Pagination (10 items per page)
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,  # We pass the page object as 'items' to keep template loops working
        'total_items': paginator.count,
        'search': search,
        'page_title': 'Kelola Menu',
    }
    return render(request, 'dashboard/menu_list.html', context)


@login_required
def menu_create(request):
    """Tambah menu baru"""
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Menu berhasil ditambahkan!')
            return redirect('menu_list')
    else:
        form = MenuItemForm()

    context = {
        'form': form,
        'page_title': 'Tambah Menu',
        'is_edit': False,
    }
    return render(request, 'dashboard/menu_form.html', context)


@login_required
def menu_edit(request, pk):
    """Edit menu item"""
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Menu berhasil diperbarui!')
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
        'page_title': f'Edit: {item.name}',
        'is_edit': True,
    }
    return render(request, 'dashboard/menu_form.html', context)


@login_required
def menu_delete(request, pk):
    """Hapus menu item"""
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        name = item.name
        item.delete()
        messages.success(request, f'🗑️ Menu "{name}" berhasil dihapus!')
        return redirect('menu_list')

    context = {
        'item': item,
        'page_title': f'Hapus: {item.name}',
    }
    return render(request, 'dashboard/menu_delete.html', context)


# --- Category CRUD ---

@login_required
def category_list(request):
    """Daftar semua kategori"""
    categories = Category.objects.annotate(
        item_count=Count('menuitem')
    )

    context = {
        'categories': categories,
        'page_title': 'Kelola Kategori',
    }
    return render(request, 'dashboard/category_list.html', context)


@login_required
def category_create(request):
    """Tambah kategori baru"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Kategori berhasil ditambahkan!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'page_title': 'Tambah Kategori',
        'is_edit': False,
    }
    return render(request, 'dashboard/category_form.html', context)


@login_required
def category_edit(request, pk):
    """Edit kategori"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Kategori berhasil diperbarui!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
        'page_title': f'Edit: {category.name}',
        'is_edit': True,
    }
    return render(request, 'dashboard/category_form.html', context)


@login_required
def category_delete(request, pk):
    """Hapus kategori"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'🗑️ Kategori "{name}" berhasil dihapus!')
        return redirect('category_list')

    context = {
        'category': category,
        'page_title': f'Hapus: {category.name}',
    }
    return render(request, 'dashboard/category_delete.html', context)


# --- Reservation Management ---

@login_required
def reservation_list(request):
    """Daftar semua reservasi"""
    reservations = Reservation.objects.all()
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        reservations = reservations.filter(status=status_filter)

    # Pagination
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reservations': page_obj,
        'status_filter': status_filter,
        'page_title': 'Kelola Reservasi',
    }
    return render(request, 'dashboard/reservation_list.html', context)


@login_required
def reservation_edit(request, pk):
    """Edit / update status reservasi"""
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationAdminForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Reservasi berhasil diperbarui!')
            return redirect('reservation_list')
    else:
        form = ReservationAdminForm(instance=reservation)

    context = {
        'form': form,
        'reservation': reservation,
        'page_title': f'Edit Reservasi: {reservation.name}',
    }
    return render(request, 'dashboard/reservation_form.html', context)


@login_required
def reservation_delete(request, pk):
    """Hapus reservasi"""
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        name = reservation.name
        reservation.delete()
        messages.success(request, f'🗑️ Reservasi "{name}" berhasil dihapus!')
        return redirect('reservation_list')

    context = {
        'reservation': reservation,
        'page_title': f'Hapus Reservasi: {reservation.name}',
    }
    return render(request, 'dashboard/reservation_delete.html', context)


# --- Contact Messages ---

@login_required
def message_list(request):
    """Daftar semua pesan kontak"""
    contact_messages = ContactMessage.objects.all()
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'unread':
        contact_messages = contact_messages.filter(is_read=False)
    elif filter_type == 'read':
        contact_messages = contact_messages.filter(is_read=True)

    # Pagination
    paginator = Paginator(contact_messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'contact_messages': page_obj,
        'filter_type': filter_type,
        'page_title': 'Pesan Masuk',
    }
    return render(request, 'dashboard/message_list.html', context)


@login_required
def message_detail(request, pk):
    """Detail pesan & tandai sudah dibaca"""
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()

    context = {
        'msg': msg,
        'page_title': f'Pesan: {msg.subject}',
    }
    return render(request, 'dashboard/message_detail.html', context)


@login_required
def message_delete(request, pk):
    """Hapus pesan"""
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, '🗑️ Pesan berhasil dihapus!')
        return redirect('message_list')

    context = {
        'msg': msg,
        'page_title': f'Hapus Pesan: {msg.subject}',
    }
    return render(request, 'dashboard/message_delete.html', context)


# --- Site Settings ---

@login_required
def site_settings(request):
    """Edit pengaturan situs"""
    settings_obj = SiteSettings.get_settings()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Pengaturan situs berhasil diperbarui!')
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings_obj)

    context = {
        'form': form,
        'page_title': 'Pengaturan Situs',
    }
    return render(request, 'dashboard/site_settings.html', context)
