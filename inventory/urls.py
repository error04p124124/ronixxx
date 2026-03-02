from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Price lists (public)
    path('price-list/', views.price_list, name='price_list'),
    path('service-price-list/', views.service_price_list, name='service_price_list'),
    
    # Components
    path('components/', views.component_list, name='component_list'),
    path('components/create/', views.component_create, name='component_create'),
    path('components/<int:pk>/', views.component_detail, name='component_detail'),
    path('components/<int:pk>/edit/', views.component_edit, name='component_edit'),
    path('components/<int:pk>/delete/', views.component_delete, name='component_delete'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    path('suppliers/<int:pk>/create-supply/', views.supplier_create_supply, name='supplier_create_supply'),
    
    # Stock movements
    path('movements/', views.movement_list, name='movement_list'),
    path('movements/create/', views.movement_create, name='movement_create'),
]
