from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserEditFormForManager


def register(request):
    """Регистрация нового пользователя (роль по умолчанию - клиент)."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'client'  # Устанавливаем роль клиента по умолчанию
            user.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Ваша роль - Клиент.')
            return redirect('core:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль пользователя."""
    return render(request, 'users/profile.html')


@login_required
def profile_edit(request):
    """Редактирование профиля."""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def user_list(request):
    """Список пользователей (только для работников)."""
    if not request.user.is_worker and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_detail(request, pk):
    """Детальная информация о пользователе."""
    if not request.user.is_worker and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user_obj': user})


@login_required
def user_edit(request, pk):
    """Редактирование пользователя (только для работников)."""
    if not request.user.is_worker and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserEditFormForManager(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно обновлен!')
            return redirect('users:user_detail', pk=pk)
    else:
        form = UserEditFormForManager(instance=user)
    
    return render(request, 'users/user_edit.html', {'form': form, 'user_obj': user})


@login_required
def user_delete(request, pk):
    """Удаление пользователя."""
    if not request.user.is_worker and not request.user.is_superuser:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('core:dashboard')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь успешно удален!')
        return redirect('users:user_list')
    
    return render(request, 'users/user_delete.html', {'user_obj': user})
