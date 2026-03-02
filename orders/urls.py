from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Orders
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/add-component/', views.order_add_component, name='order_add_component'),
    path('<int:pk>/add-service/', views.order_add_service, name='order_add_service'),
    path('<int:order_pk>/item/<int:item_pk>/delete/', views.order_item_delete, name='order_item_delete'),
    path('<int:pk>/complete/', views.order_complete, name='order_complete'),
    
    # Receipts
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('receipts/<int:pk>/', views.receipt_detail, name='receipt_detail'),
    path('receipts/<int:pk>/pdf/', views.receipt_pdf, name='receipt_pdf'),
]
