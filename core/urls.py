from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.landing_page, name='landing'),
    path('menu/', views.menu_page, name='menu'),
    path('tentang/', views.about_page, name='about'),
    path('reservasi/', views.reservation_page, name='reservation'),
    path('kontak/', views.contact_page, name='contact'),

    # Dashboard Auth
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),

    # Dashboard Home
    path('dashboard/', views.dashboard_index, name='dashboard'),

    # Menu CRUD
    path('dashboard/menu/', views.menu_list, name='menu_list'),
    path('dashboard/menu/tambah/', views.menu_create, name='menu_create'),
    path('dashboard/menu/<int:pk>/edit/', views.menu_edit, name='menu_edit'),
    path('dashboard/menu/<int:pk>/hapus/', views.menu_delete, name='menu_delete'),

    # Category CRUD
    path('dashboard/kategori/', views.category_list, name='category_list'),
    path('dashboard/kategori/tambah/', views.category_create, name='category_create'),
    path('dashboard/kategori/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('dashboard/kategori/<int:pk>/hapus/', views.category_delete, name='category_delete'),

    # Reservation Management
    path('dashboard/reservasi/', views.reservation_list, name='reservation_list'),
    path('dashboard/reservasi/<int:pk>/edit/', views.reservation_edit, name='reservation_edit'),
    path('dashboard/reservasi/<int:pk>/hapus/', views.reservation_delete, name='reservation_delete'),

    # Contact Messages
    path('dashboard/pesan/', views.message_list, name='message_list'),
    path('dashboard/pesan/<int:pk>/', views.message_detail, name='message_detail'),
    path('dashboard/pesan/<int:pk>/hapus/', views.message_delete, name='message_delete'),

    # Site Settings
    path('dashboard/pengaturan/', views.site_settings, name='site_settings'),
]
