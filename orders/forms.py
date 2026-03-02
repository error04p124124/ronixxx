from django import forms
from .models import Order, OrderItem, Receipt
from users.models import User
from inventory.models import Service


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type', 'description']
        widgets = {
            'order_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'assigned_to', 'description']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'status': 'Статус',
            'assigned_to': 'Ответственный',
            'description': 'Описание',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только работников в списке ответственных
        self.fields['assigned_to'].queryset = User.objects.filter(
            role='worker'
        ).order_by('last_name', 'first_name')
        self.fields['assigned_to'].required = False
        self.fields['assigned_to'].empty_label = "Не назначен"


class OrderItemComponentForm(forms.ModelForm):
    """Форма для добавления комплектующей в заявку."""
    class Meta:
        model = OrderItem
        fields = ['component', 'quantity', 'price']
        widgets = {
            'component': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        }
        labels = {
            'component': 'Комплектующая',
            'quantity': 'Количество',
            'price': 'Цена за единицу (с наценкой 20%)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        component = cleaned_data.get('component')
        quantity = cleaned_data.get('quantity')
        
        if component and quantity:
            if component.quantity < quantity:
                raise forms.ValidationError(
                    f'Недостаточно комплектующих на складе. '
                    f'Доступно: {component.quantity}, запрошено: {quantity}'
                )
        
        return cleaned_data


class OrderItemServiceForm(forms.ModelForm):
    """Форма для добавления услуги в заявку."""
    class Meta:
        model = OrderItem
        fields = ['service', 'quantity', 'price']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        }
        labels = {
            'service': 'Услуга',
            'quantity': 'Количество',
            'price': 'Цена за единицу',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только активные услуги
        self.fields['service'].queryset = Service.objects.filter(is_active=True).order_by('category', 'name')
        self.fields['price'].required = False


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
