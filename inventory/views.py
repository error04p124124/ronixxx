from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Component, Category, Supplier, StockMovement, Service
from .forms import ComponentForm, CategoryForm, SupplierForm, StockMovementForm


@login_required
def component_list(request):
    """Список комплектующих."""
    # Только работники и администраторы имеют доступ к инвентарю
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к инвентарю. Используйте прайс-лист для просмотра товаров.')
        return redirect('inventory:price_list')
    
    components = Component.objects.select_related('category').all()
    
    # Поиск
    search = request.GET.get('search', '')
    if search:
        components = components.filter(
            Q(name__icontains=search) |
            Q(article_number__icontains=search) |
            Q(manufacturer__icontains=search)
        )
    
    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        components = components.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'components': components,
        'categories': categories,
        'search': search,
    }
    return render(request, 'inventory/component_list.html', context)


@login_required
def component_detail(request, pk):
    """Детальная информация о комплектующей."""
    # Только работники и администраторы имеют доступ к инвентарю
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к инвентарю.')
        return redirect('inventory:price_list')
    
    component = get_object_or_404(Component, pk=pk)
    movements = component.movements.all()[:10]
    
    return render(request, 'inventory/component_detail.html', {
        'component': component,
        'movements': movements,
    })


@login_required
def component_create(request):
    """Создание новой комплектующей."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:component_list')
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комплектующая успешно добавлена!')
            return redirect('inventory:component_list')
    else:
        form = ComponentForm()
    
    return render(request, 'inventory/component_form.html', {'form': form})


@login_required
def component_edit(request, pk):
    """Редактирование комплектующей."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:component_list')
    
    component = get_object_or_404(Component, pk=pk)
    
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES, instance=component)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комплектующая успешно обновлена!')
            return redirect('inventory:component_detail', pk=pk)
    else:
        form = ComponentForm(instance=component)
    
    return render(request, 'inventory/component_form.html', {'form': form, 'component': component})


@login_required
def component_delete(request, pk):
    """Удаление комплектующей."""
    if not (request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:component_list')
    
    component = get_object_or_404(Component, pk=pk)
    
    if request.method == 'POST':
        component.delete()
        messages.success(request, 'Комплектующая успешно удалена!')
        return redirect('inventory:component_list')
    
    return render(request, 'inventory/component_delete.html', {'component': component})


# Categories
@login_required
@login_required
def category_list(request):
    """Список категорий."""
    # Только работники и администраторы имеют доступ к категориям
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Создание категории."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:category_list')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'inventory/category_form.html', {'form': form})


@login_required
def category_edit(request, pk):
    """Редактирование категории."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:category_list')
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена!')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'inventory/category_form.html', {'form': form, 'category': category})


@login_required
def category_delete(request, pk):
    """Удаление категории."""
    if not (request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:category_list')
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена!')
        return redirect('inventory:category_list')
    
    return render(request, 'inventory/category_delete.html', {'category': category})


# Suppliers
@login_required
def supplier_list(request):
    """Список поставщиков."""
    # Только работники и администраторы имеют доступ к поставщикам
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})


@login_required
def supplier_detail(request, pk):
    """Детальная информация о поставщике."""
    # Только работники и администраторы имеют доступ к поставщикам
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'inventory/supplier_detail.html', {'supplier': supplier})


@login_required
def supplier_create(request):
    """Создание поставщика."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:supplier_list')
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поставщик успешно добавлен!')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'inventory/supplier_form.html', {'form': form})


@login_required
def supplier_edit(request, pk):
    """Редактирование поставщика."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:supplier_list')
    
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поставщик успешно обновлен!')
            return redirect('inventory:supplier_detail', pk=pk)
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'inventory/supplier_form.html', {'form': form, 'supplier': supplier})


@login_required
def supplier_delete(request, pk):
    """Удаление поставщика."""
    if not (request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:supplier_list')
    
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Поставщик успешно удален!')
        return redirect('inventory:supplier_list')
    
    return render(request, 'inventory/supplier_delete.html', {'supplier': supplier})


@login_required
def supplier_create_supply(request, pk):
    """Создание заказа поставки от поставщика."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('inventory:supplier_list')
    
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        note = request.POST.get('note', '')
        items_added = 0
        
        # Обрабатываем все отправленные строки формы
        i = 0
        while True:
            component_id = request.POST.get(f'component_{i}')
            quantity_str = request.POST.get(f'quantity_{i}')
            
            # Если нет больше данных, выходим из цикла
            if component_id is None:
                break
            
            if component_id and quantity_str:
                try:
                    component = Component.objects.get(pk=component_id)
                    quantity = int(quantity_str)
                    
                    if quantity > 0:
                        # Создаем запись о поставке
                        StockMovement.objects.create(
                            component=component,
                            movement_type='supply',
                            quantity=quantity,
                            note=f"Поставка от {supplier.name}. {note}".strip(),
                            user=request.user
                        )
                        
                        # Увеличиваем количество на складе
                        component.quantity += quantity
                        component.save()
                        
                        items_added += 1
                except (Component.DoesNotExist, ValueError):
                    pass
            
            i += 1
        
        if items_added > 0:
            messages.success(request, f'Поставка успешно оформлена! Добавлено позиций: {items_added}')
            return redirect('inventory:supplier_detail', pk=pk)
        else:
            messages.warning(request, 'Не было добавлено ни одной позиции.')
    
    # Получаем все комплектующие для выпадающего списка
    components = Component.objects.select_related('category').order_by('name')
    
    context = {
        'supplier': supplier,
        'components': components,
    }
    
    return render(request, 'inventory/supplier_create_supply.html', context)


# Stock Movements
@login_required
def movement_list(request):
    """Список движений товаров."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    movements = StockMovement.objects.select_related('component', 'user').all()
    return render(request, 'inventory/movement_list.html', {'movements': movements})


@login_required
def movement_create(request):
    """Создание движения товара."""
    if not (request.user.is_worker or request.user.is_superuser):
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.user = request.user
            
            # Обновляем количество в зависимости от типа операции
            component = movement.component
            if movement.movement_type == 'supply':
                # Поставка - увеличивает остаток
                component.quantity += movement.quantity
            elif movement.movement_type == 'write_off':
                # Списание товара - уменьшает остаток
                if component.quantity < movement.quantity:
                    messages.error(request, 'Недостаточно товара на складе для списания!')
                    return render(request, 'inventory/movement_form.html', {'form': form})
                component.quantity -= movement.quantity
            elif movement.movement_type == 'return_supplier':
                # Возврат поставщику - уменьшает остаток
                if component.quantity < movement.quantity:
                    messages.error(request, 'Недостаточно товара на складе для возврата!')
                    return render(request, 'inventory/movement_form.html', {'form': form})
                component.quantity -= movement.quantity
            elif movement.movement_type == 'inventory':
                # Инвентаризация - устанавливает новое количество
                # В поле quantity записывается разница
                component.quantity += movement.quantity  # может быть отрицательным
            elif movement.movement_type == 'transfer':
                # Перемещение - только регистрирует операцию, не меняет общий остаток
                pass
            
            component.save()
            movement.save()
            
            messages.success(request, 'Операция успешно выполнена!')
            return redirect('inventory:movement_list')
    else:
        form = StockMovementForm()
    
    return render(request, 'inventory/movement_form.html', {'form': form})


def price_list(request):
    """Прайс-лист комплектующих (доступен всем)."""
    components = Component.objects.select_related('category').filter(quantity__gt=0).order_by('category__name', 'name')
    
    # Поиск
    search = request.GET.get('search', '')
    if search:
        components = components.filter(
            Q(name__icontains=search) |
            Q(article_number__icontains=search) |
            Q(manufacturer__icontains=search)
        )
    
    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        components = components.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'components': components,
        'categories': categories,
        'search': search,
    }
    return render(request, 'inventory/price_list.html', context)


def service_price_list(request):
    """Прайс-лист услуг (доступен всем)."""
    services = Service.objects.filter(is_active=True).order_by('category', 'name')
    
    # Поиск
    search = request.GET.get('search', '')
    if search:
        services = services.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Фильтр по категории
    category = request.GET.get('category')
    if category:
        services = services.filter(category=category)
    
    # Получаем список уникальных категорий
    categories = Service.SERVICE_CATEGORIES
    
    context = {
        'services': services,
        'categories': categories,
        'search': search,
        'selected_category': category,
    }
    return render(request, 'inventory/service_price_list.html', context)
