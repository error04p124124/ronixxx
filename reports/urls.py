from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='home'),
    path('inventory/', views.inventory_report, name='inventory'),
    path('inventory/pdf/', views.inventory_report_pdf, name='inventory_pdf'),
    path('inventory/pdf-improved/', views.inventory_report_pdf_improved, name='inventory_pdf_improved'),
    path('inventory/excel/', views.inventory_report_excel, name='inventory_excel'),
    path('inventory/word/', views.inventory_report_word, name='inventory_word'),
    path('orders/', views.orders_report, name='orders'),
    path('orders/pdf/', views.orders_report_pdf, name='orders_pdf'),
    path('orders/pdf-improved/', views.orders_report_pdf_improved, name='orders_pdf_improved'),
    path('orders/excel/', views.orders_report_excel, name='orders_excel'),
    path('orders/word/', views.orders_report_word, name='orders_word'),
    path('financial/', views.financial_report, name='financial'),
    path('financial/pdf/', views.financial_report_pdf, name='financial_pdf'),
]
