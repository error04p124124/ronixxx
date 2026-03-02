"""
Модуль для отправки email-уведомлений.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_email_notification(subject, template_name, context, recipient_list):
    """
    Базовая функция для отправки email уведомлений.
    
    Args:
        subject: Тема письма
        template_name: Имя HTML шаблона
        context: Контекст для шаблона
        recipient_list: Список email адресов получателей
    """
    try:
        # Рендерим HTML версию
        html_message = render_to_string(template_name, context)
        # Создаем текстовую версию
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email отправлен: {subject} -> {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки email: {e}")
        return False


def notify_login(user, ip_address, user_agent):
    """
    Уведомление о входе в аккаунт.
    
    Args:
        user: Пользователь
        ip_address: IP-адрес входа
        user_agent: User agent браузера
    """
    if not user.email:
        return False
    
    subject = f"Вход в аккаунт ООО НПФ «Роникс-Л»"
    context = {
        'user': user,
        'ip_address': ip_address,
        'user_agent': user_agent,
    }
    
    return send_email_notification(
        subject=subject,
        template_name='emails/login_notification.html',
        context=context,
        recipient_list=[user.email]
    )


def notify_new_order(order):
    """
    Уведомление всем работникам о новой заявке.
    
    Args:
        order: Объект заявки
    """
    from users.models import User
    
    # Получаем всех работников и админов с email
    workers = User.objects.filter(
        role='worker',
        email__isnull=False
    ).exclude(email='')
    
    superusers = User.objects.filter(
        is_superuser=True,
        email__isnull=False
    ).exclude(email='')
    
    recipients = list(workers.values_list('email', flat=True)) + \
                 list(superusers.values_list('email', flat=True))
    
    if not recipients:
        return False
    
    subject = f"Новая заявка #{order.id} от {order.client.get_full_name()}"
    context = {
        'order': order,
    }
    
    return send_email_notification(
        subject=subject,
        template_name='emails/new_order_notification.html',
        context=context,
        recipient_list=list(set(recipients))  # Убираем дубликаты
    )


def notify_order_assigned(order):
    """
    Уведомление назначенному исполнителю о новой заявке.
    
    Args:
        order: Объект заявки
    """
    if not order.assigned_to or not order.assigned_to.email:
        return False
    
    subject = f"Вы назначены ответственным за заявку #{order.id}"
    context = {
        'order': order,
        'executor': order.assigned_to,
    }
    
    return send_email_notification(
        subject=subject,
        template_name='emails/order_assigned_notification.html',
        context=context,
        recipient_list=[order.assigned_to.email]
    )


def notify_low_stock(component):
    """
    Уведомление всем работникам о низком остатке товара.
    
    Args:
        component: Объект комплектующей
    """
    from users.models import User
    
    # Получаем всех работников и админов с email
    workers = User.objects.filter(
        role='worker',
        email__isnull=False
    ).exclude(email='')
    
    superusers = User.objects.filter(
        is_superuser=True,
        email__isnull=False
    ).exclude(email='')
    
    recipients = list(workers.values_list('email', flat=True)) + \
                 list(superusers.values_list('email', flat=True))
    
    if not recipients:
        return False
    
    subject = f"Низкий остаток: {component.name}"
    context = {
        'component': component,
    }
    
    return send_email_notification(
        subject=subject,
        template_name='emails/low_stock_notification.html',
        context=context,
        recipient_list=list(set(recipients))  # Убираем дубликаты
    )
