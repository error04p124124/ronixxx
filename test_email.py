"""
Скрипт для тестирования отправки email уведомлений.
Запуск: python manage.py shell < test_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ronix_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("ТЕСТИРОВАНИЕ EMAIL УВЕДОМЛЕНИЙ")
print("=" * 60)

# Проверка настроек
print("\n1. Проверка настроек email:")
print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if not settings.EMAIL_HOST_USER:
    print("\n⚠️  ВНИМАНИЕ: EMAIL_HOST_USER не настроен!")
    print("   Настройте переменные окружения в файле .env")
    exit(1)

# Проверка консольного бэкенда
if 'console' in settings.EMAIL_BACKEND.lower():
    print("\n✅ Используется консольный бэкенд - письма будут выведены в консоль")
    print("   Для реальной отправки измените EMAIL_BACKEND в settings.py")
else:
    print("\n✅ Используется SMTP бэкенд - письма будут отправлены по email")

# Запрос email для тестовой отправки
test_email = input("\n2. Введите email для тестовой отправки: ").strip()

if not test_email:
    print("❌ Email не указан, тест отменен")
    exit(1)

print(f"\n3. Отправка тестового письма на {test_email}...")

try:
    send_mail(
        subject='[ТЕСТ] Проверка email уведомлений - ООО НПФ «Роникс-Л»',
        message='Это тестовое письмо для проверки системы email уведомлений.\n\nЕсли вы получили это письмо, значит настройка выполнена успешно!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        fail_silently=False,
    )
    print("✅ Письмо успешно отправлено!")
    print("\nПроверьте почтовый ящик (не забудьте проверить папку Спам)")
    
except Exception as e:
    print(f"❌ Ошибка при отправке письма: {e}")
    print("\nВозможные причины:")
    print("  - Неверный логин или пароль")
    print("  - Для Gmail используйте пароль приложения, а не обычный пароль")
    print("  - Проверьте настройки порта и TLS")
    print("  - Проверьте подключение к интернету")
    print("\nПодробности в EMAIL_SETUP.md")

print("\n" + "=" * 60)
print("ТЕСТ ЗАВЕРШЕН")
print("=" * 60)
