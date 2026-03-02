from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    """Заявка на обслуживание или заказ комплектующих."""
    
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('service', 'Обслуживание'),
        ('components', 'Заказ комплектующих'),
    ]
    
    client = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент'
    )
    order_type = models.CharField('Тип заявки', max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    description = models.TextField('Описание')
    assigned_to = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders',
        verbose_name='Ответственный',
        limit_choices_to={'role': 'worker'}
    )
    total_amount = models.DecimalField(
        'Сумма',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    completed_at = models.DateTimeField('Дата выполнения', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка #{self.id} от {self.client.get_full_name() or self.client.username}"
    
    def calculate_total(self):
        """Подсчет общей суммы заявки."""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save()
        return total
    
    def delete(self, *args, **kwargs):
        """При удалении заявки возвращаем все комплектующие на склад."""
        from inventory.models import StockMovement
        
        for item in self.items.all():
            if item.component:
                item.component.quantity += item.quantity
                item.component.save()
                
                # Создаем запись о движении (возврат на склад)
                StockMovement.objects.create(
                    component=item.component,
                    movement_type='supply',
                    quantity=item.quantity,
                    note=f'Возврат при удалении заявки #{self.id}',
                    user=None
                )
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """При изменении статуса на 'отменена' возвращаем комплектующие на склад."""
        from inventory.models import StockMovement
        
        if self.pk:  # Если заявка уже существует
            old_order = Order.objects.filter(pk=self.pk).first()
            if old_order and old_order.status != 'cancelled' and self.status == 'cancelled':
                # Заявка была отменена - возвращаем комплектующие
                for item in self.items.all():
                    if item.component:
                        item.component.quantity += item.quantity
                        item.component.save()
                        
                        # Создаем запись о движении (возврат на склад)
                        StockMovement.objects.create(
                            component=item.component,
                            movement_type='supply',
                            quantity=item.quantity,
                            note=f'Возврат при отмене заявки #{self.id}',
                            user=None
                        )
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Позиция в заявке."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заявка'
    )
    component = models.ForeignKey(
        'inventory.Component',
        on_delete=models.CASCADE,
        verbose_name='Комплектующая',
        null=True,
        blank=True
    )
    service = models.ForeignKey(
        'inventory.Service',
        on_delete=models.CASCADE,
        verbose_name='Услуга',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField(
        'Цена за единицу',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    class Meta:
        verbose_name = 'Позиция заявки'
        verbose_name_plural = 'Позиции заявки'
    
    def __str__(self):
        if self.component:
            return f"{self.component.name} x {self.quantity}"
        elif self.service:
            return f"{self.service.name} x {self.quantity}"
        return f"Позиция #{self.id}"
    
    @property
    def subtotal(self):
        """Подытог по позиции."""
        return self.price * self.quantity
    
    @property
    def item_name(self):
        """Название позиции."""
        if self.component:
            return self.component.name
        elif self.service:
            return self.service.name
        return "Неизвестная позиция"
    
    def save(self, *args, **kwargs):
        # Автоматически устанавливаем цену
        if not self.price:
            if self.component:
                # Для комплектующих - цена + 20% наценка
                base_price = self.component.price
                markup = base_price * Decimal('0.20')
                self.price = base_price + markup
            elif self.service:
                # Для услуг - цена из прайс-листа
                self.price = self.service.price
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """При удалении позиции возвращаем комплектующие на склад."""
        from inventory.models import StockMovement
        
        if self.component:
            self.component.quantity += self.quantity
            self.component.save()
            
            # Создаем запись о движении (возврат на склад)
            StockMovement.objects.create(
                component=self.component,
                movement_type='supply',
                quantity=self.quantity,
                note=f'Возврат при удалении позиции из заявки #{self.order.id}',
                user=None
            )
        super().delete(*args, **kwargs)


class Receipt(models.Model):
    """Чек об оказанных услугах."""
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='receipt',
        verbose_name='Заявка'
    )
    receipt_number = models.CharField('Номер чека', max_length=50, unique=True)
    issue_date = models.DateTimeField('Дата выдачи', auto_now_add=True)
    total_amount = models.DecimalField(
        'Общая сумма',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    notes = models.TextField('Примечания', blank=True)
    
    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Чек #{self.receipt_number}"
    
    def save(self, *args, **kwargs):
        # Генерируем номер чека
        if not self.receipt_number:
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            count = Receipt.objects.filter(receipt_number__startswith=date_str).count() + 1
            self.receipt_number = f"{date_str}-{count:04d}"
        
        # Автоматически устанавливаем сумму из заявки
        if not self.total_amount:
            self.total_amount = self.order.total_amount
        
        super().save(*args, **kwargs)
