"""
Сигналы для приложения users.
"""
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from core.notifications import notify_login


@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    """
    Отправка уведомления при входе пользователя.
    """
    # Получаем IP-адрес
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', 'Неизвестно')
    
    # Получаем User Agent
    user_agent = request.META.get('HTTP_USER_AGENT', 'Неизвестно')
    
    # Отправляем уведомление
    notify_login(user, ip_address, user_agent)
