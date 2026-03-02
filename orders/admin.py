from django.contrib import admin
from .models import Order, OrderItem, Receipt


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['component', 'service', 'quantity', 'price']
    readonly_fields = []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'order_type', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'order_type', 'created_at']
    search_fields = ['client__username', 'client__first_name', 'client__last_name', 'description']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'order', 'total_amount', 'issue_date']
    search_fields = ['receipt_number', 'order__id']
    readonly_fields = ['issue_date']
