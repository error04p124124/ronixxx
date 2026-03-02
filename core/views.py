from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F
from inventory.models import Component
from orders.models import Order


def home(request):
    """Домашняя страница."""
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    """Панель управления (дашборд)."""
    user = request.user
    
    context = {
        'user': user,
    }
    
    # Статистика для клиента
    if user.is_client:
        context['my_orders'] = Order.objects.filter(client=user).order_by('-created_at')[:5]
        context['total_orders'] = Order.objects.filter(client=user).count()
        context['active_orders'] = Order.objects.filter(
            client=user, 
            status__in=['new', 'in_progress']
        ).count()
    
    # Статистика для работника
    elif user.is_worker or user.is_superuser:
        context['total_orders'] = Order.objects.count()
        context['new_orders'] = Order.objects.filter(status='new').count()
        context['in_progress_orders'] = Order.objects.filter(status='in_progress').count()
        context['completed_orders'] = Order.objects.filter(status='completed').count()
        context['total_components'] = Component.objects.count()
        context['low_stock_items'] = Component.objects.filter(
            quantity__lte=F('min_quantity')
        ).count()
        context['total_revenue'] = Order.objects.filter(
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        context['recent_orders'] = Order.objects.order_by('-created_at')[:5]
        context['assigned_orders'] = Order.objects.filter(
            assigned_to=user
        ).order_by('-created_at')[:5]
    
    return render(request, 'core/dashboard.html', context)


def about(request):
    """О компании."""
    return render(request, 'core/about.html')
