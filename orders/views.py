from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order, OrderItem, Receipt
from .forms import OrderForm, OrderUpdateForm, OrderItemComponentForm, OrderItemServiceForm, ReceiptForm
from inventory.models import StockMovement


@login_required
def order_list(request):
    """Список заявок."""
    orders = Order.objects.select_related('client', 'assigned_to').all()
    
    # Клиенты видят только свои заявки
    if request.user.is_client:
        orders = orders.filter(client=request.user)
    
    # Фильтр по статусу
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Детальная информация о заявке."""
    order = get_object_or_404(Order, pk=pk)
    
    # Клиенты могут просматривать только свои заявки
    if request.user.is_client and order.client != request.user:
        messages.error(request, 'У вас нет доступа к этой заявке.')
        return redirect('orders:order_list')
    
    items = order.items.select_related('component').all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_create(request):
    """Создание новой заявки."""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.save()
            
            # Отправляем уведомление всем работникам о новой заявке
            from core.notifications import notify_new_order
            notify_new_order(order)
            
            messages.success(request, 'Заявка успешно создана!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm()
    
    return render(request, 'orders/order_form.html', {'form': form})


@login_required
def order_edit(request, pk):
    """Редактирование заявки."""
    # Только работники и администраторы могут редактировать заявки
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к редактированию заявок.')
        return redirect('orders:order_list')
    
    order = get_object_or_404(Order, pk=pk)
    old_assigned_to = order.assigned_to  # Сохраняем старое значение
    
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        
        if form.is_valid():
            order = form.save()
            
            # Проверяем, был ли назначен новый ответственный
            if order.assigned_to and order.assigned_to != old_assigned_to:
                from core.notifications import notify_order_assigned
                notify_order_assigned(order)
            
            messages.success(request, 'Заявка успешно обновлена!')
            return redirect('orders:order_detail', pk=pk)
    else:
        form = OrderUpdateForm(instance=order)
    
    return render(request, 'orders/order_form.html', {'form': form, 'order': order})


@login_required
def order_delete(request, pk):
    """Удаление заявки."""
    # Только администраторы могут удалять заявки
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для удаления заявок.')
        return redirect('orders:order_list')
    
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заявка успешно удалена!')
        return redirect('orders:order_list')
    
    return render(request, 'orders/order_delete.html', {'order': order})


@login_required
def order_add_component(request, pk):
    """Добавление комплектующей в заявку."""
    order = get_object_or_404(Order, pk=pk)
    
    # Проверка прав доступа
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой функции.')
        return redirect('orders:order_detail', pk=pk)
    
    if request.method == 'POST':
        form = OrderItemComponentForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            
            # Уменьшаем количество на складе
            component = item.component
            component.quantity -= item.quantity
            component.save()
            
            # Создаем запись о движении товара (продажа)
            StockMovement.objects.create(
                component=component,
                movement_type='sale',
                quantity=item.quantity,
                note=f'Продажа для заявки #{order.id}',
                user=request.user
            )
            
            item.save()
            order.calculate_total()
            messages.success(request, f'Комплектующая успешно добавлена! На складе осталось: {component.quantity}')
            return redirect('orders:order_detail', pk=pk)
    else:
        form = OrderItemComponentForm()
    
    return render(request, 'orders/order_component_form.html', {'form': form, 'order': order})


@login_required
def order_add_service(request, pk):
    """Добавление услуги в заявку."""
    order = get_object_or_404(Order, pk=pk)
    
    # Проверка прав доступа
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой функции.')
        return redirect('orders:order_detail', pk=pk)
    
    if request.method == 'POST':
        form = OrderItemServiceForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            order.calculate_total()
            messages.success(request, 'Услуга успешно добавлена!')
            return redirect('orders:order_detail', pk=pk)
    else:
        form = OrderItemServiceForm()
    
    return render(request, 'orders/order_service_form.html', {'form': form, 'order': order})


@login_required
def order_complete(request, pk):
    """Отметить заявку как выполненную."""
    order = get_object_or_404(Order, pk=pk)
    
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой функции.')
        return redirect('orders:order_detail', pk=pk)
    
    if request.method == 'POST':
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()
        
        # Создаем чек
        if not hasattr(order, 'receipt'):
            Receipt.objects.create(
                order=order,
                total_amount=order.total_amount
            )
        
        messages.success(request, 'Заявка отмечена как выполненная!')
        return redirect('orders:order_detail', pk=pk)
    
    return render(request, 'orders/order_complete.html', {'order': order})


# Receipts
@login_required
def receipt_list(request):
    """Список чеков."""
    receipts = Receipt.objects.select_related('order', 'order__client').all()
    
    # Клиенты видят только свои чеки
    if request.user.is_client:
        receipts = receipts.filter(order__client=request.user)
    
    return render(request, 'orders/receipt_list.html', {'receipts': receipts})


@login_required
def receipt_detail(request, pk):
    """Детальная информация о чеке."""
    receipt = get_object_or_404(Receipt, pk=pk)
    
    # Клиенты могут просматривать только свои чеки
    if request.user.is_client and receipt.order.client != request.user:
        messages.error(request, 'У вас нет доступа к этому чеку.')
        return redirect('orders:receipt_list')
    
    items = receipt.order.items.select_related('component').all()
    
    context = {
        'receipt': receipt,
        'items': items,
    }
    return render(request, 'orders/receipt_detail.html', context)


@login_required
def receipt_pdf(request, pk):
    """Генерация PDF чека."""
    receipt = get_object_or_404(Receipt, pk=pk)
    
    # Клиенты могут скачивать только свои чеки
    if request.user.is_client and receipt.order.client != request.user:
        messages.error(request, 'У вас нет доступа к этому чеку.')
        return redirect('orders:receipt_list')
    
    # Получаем позиции заявки
    items = receipt.order.items.select_related('component').all()
    
    context = {
        'receipt': receipt,
        'items': items,
    }
    
    # Используем render_to_string для получения чистого HTML без базового шаблона
    html_string = render_to_string('orders/receipt_pdf.html', context)
    return HttpResponse(html_string, content_type='text/html')


@login_required
def order_item_delete(request, order_pk, item_pk):
    """Удаление позиции из заявки."""
    order = get_object_or_404(Order, pk=order_pk)
    item = get_object_or_404(OrderItem, pk=item_pk, order=order)
    
    # Проверка прав доступа
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой функции.')
        return redirect('orders:order_detail', pk=order_pk)
    
    # Проверка, что заявка не завершена
    if order.status == 'completed':
        messages.error(request, 'Нельзя удалять позиции из завершенной заявки.')
        return redirect('orders:order_detail', pk=order_pk)
    
    if request.method == 'POST':
        item_name = item.item_name
        item.delete()  # Удаляем позицию (автоматически вернет комплектующие на склад и создаст запись движения)
        order.calculate_total()  # Пересчитываем сумму заявки
        messages.success(request, f'Позиция "{item_name}" успешно удалена из заявки.')
        return redirect('orders:order_detail', pk=order_pk)
    
    # Если GET-запрос, перенаправляем обратно
    return redirect('orders:order_detail', pk=order_pk)
