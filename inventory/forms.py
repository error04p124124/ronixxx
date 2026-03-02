from django import forms
from .models import Category, Component, Supplier, StockMovement


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'category', 'description', 'article_number', 
                  'manufacturer', 'price', 'quantity', 'min_quantity', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'article_number': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['component', 'movement_type', 'quantity', 'note']
        widgets = {
            'component': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SupplyOrderItemForm(forms.Form):
    """Форма для одной позиции в заказе поставки."""
    component = forms.ModelChoiceField(
        queryset=Component.objects.all(),
        label='Комплектующая',
        widget=forms.Select(attrs={'class': 'form-select component-select'}),
        required=False
    )
    quantity = forms.IntegerField(
        label='Количество',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control quantity-input'}),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        component = cleaned_data.get('component')
        quantity = cleaned_data.get('quantity')
        
        # Если указан компонент, то количество обязательно
        if component and not quantity:
            raise forms.ValidationError('Укажите количество для выбранной комплектующей')
        
        # Если указано количество, то компонент обязателен
        if quantity and not component:
            raise forms.ValidationError('Выберите комплектующую для указанного количества')
        
        return cleaned_data
