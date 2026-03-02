from django.contrib import admin
from .models import Category, Component, Supplier, StockMovement, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'article_number', 'category', 'price', 'quantity', 'stock_status']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name', 'article_number', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email']
    search_fields = ['name', 'contact_person', 'email']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['component', 'movement_type', 'quantity', 'user', 'created_at']
    list_filter = ['movement_type', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
