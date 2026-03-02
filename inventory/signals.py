"""
Сигналы для приложения inventory.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Component
from core.notifications import notify_low_stock


@receiver(post_save, sender=Component)
def check_low_stock(sender, instance, created, **kwargs):
    """
    Проверка низкого остатка при изменении комплектующей.
    Отправляет уведомление если количество <= минимального.
    """
    # Не отправляем уведомление при создании нового товара
    if created:
        return
    
    # Проверяем, достиг ли товар минимального остатка или ниже
    if instance.quantity <= instance.min_quantity:
        # Проверяем, не отправляли ли мы уже уведомление
        # Можно добавить флаг в модель или использовать кеш
        # Пока отправляем всегда при достижении минимума
        notify_low_stock(instance)
