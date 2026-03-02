from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Категория комплектующих."""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Component(models.Model):
    """Комплектующая деталь."""
    name = models.CharField('Название', max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name='Категория'
    )
    description = models.TextField('Описание', blank=True)
    article_number = models.CharField('Артикул', max_length=100, unique=True)
    manufacturer = models.CharField('Производитель', max_length=200, blank=True)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity = models.PositiveIntegerField('Количество на складе', default=0)
    min_quantity = models.PositiveIntegerField('Минимальное количество', default=5)
    image = models.ImageField('Изображение', upload_to='components/', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Комплектующая'
        verbose_name_plural = 'Комплектующие'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.article_number})"
    
    @property
    def is_low_stock(self):
        """Проверка на низкий остаток."""
        return self.quantity <= self.min_quantity
    
    @property
    def stock_status(self):
        """Статус наличия на складе."""
        if self.quantity == 0:
            return 'Отсутствует'
        elif self.is_low_stock:
            return 'Заканчивается'
        else:
            return 'В наличии'


class Supplier(models.Model):
    """Поставщик комплектующих."""
    name = models.CharField('Название компании', max_length=200)
    contact_person = models.CharField('Контактное лицо', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class StockMovement(models.Model):
    """История движения товаров на складе."""
    
    MOVEMENT_TYPES = [
        ('supply', 'Поставка'),
        ('sale', 'Продажа'),
        ('write_off', 'Списание товара'),
        ('return_supplier', 'Возврат поставщику'),
        ('inventory', 'Инвентаризация'),
        ('transfer', 'Перемещение'),
    ]
    
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name='Комплектующая'
    )
    movement_type = models.CharField('Тип операции', max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField('Количество')
    note = models.TextField('Примечание', blank=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='stock_movements',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField('Дата операции', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Движение товара'
        verbose_name_plural = 'Движения товаров'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_movement_type_display()}: {self.component.name} ({self.quantity} шт.)"


class Service(models.Model):
    """Услуга/работа."""
    
    SERVICE_CATEGORIES = [
        ('repair', 'Ремонт'),
        ('replacement', 'Замена деталей'),
        ('diagnostics', 'Диагностика'),
        ('maintenance', 'Обслуживание'),
        ('installation', 'Установка'),
        ('other', 'Прочее'),
    ]
    
    name = models.CharField('Название услуги', max_length=300)
    category = models.CharField('Категория', max_length=20, choices=SERVICE_CATEGORIES, default='other')
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    duration = models.PositiveIntegerField('Длительность (минуты)', default=30, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} — {self.price} ₽"
