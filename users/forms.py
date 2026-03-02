from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя (без выбора роли)."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'address')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования профиля пользователя."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'address')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserEditFormForManager(forms.ModelForm):
    """Форма редактирования пользователя для управляющих (с возможностью изменения роли)."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'address', 'role', 'is_active')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
            'address': 'Адрес',
            'role': 'Роль',
            'is_active': 'Активен',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'role' and field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
            elif field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
