# 📧 Быстрая настройка Email-уведомлений

## Шаг 1: Получите пароль приложения Gmail

1. Откройте https://myaccount.google.com/
2. Перейдите в **Безопасность**
3. Включите **Двухфакторную аутентификацию** (если не включена)
4. Найдите **Пароли приложений** → Создать
5. Выберите "Почта" и "Другое устройство"
6. Скопируйте сгенерированный пароль (16 символов без пробелов)

## Шаг 2: Создайте файл .env

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=ваш-email@gmail.com
EMAIL_HOST_PASSWORD=пароль-из-16-символов
DEFAULT_FROM_EMAIL=ваш-email@gmail.com
```

**⚠️ Важно:**
- Используйте **пароль приложения**, а не обычный пароль Gmail!
- Замените `ваш-email@gmail.com` на ваш реальный email
- Вставьте пароль без пробелов

## Шаг 3: Проверьте настройку

Запустите тестовый скрипт:

```bash
python test_email.py
```

Или используйте Django shell:

```bash
python manage.py shell
```

И выполните:
```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Тест',
    'Это тестовое письмо',
    settings.DEFAULT_FROM_EMAIL,
    ['ваш-email@gmail.com'],
)
```

## Шаг 4: Для тестирования без отправки

Если хотите видеть письма в консоли вместо отправки, в `ronix_project/settings.py` замените:

```python
# Закомментируйте эту строку:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Раскомментируйте эту:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## ✅ Что будет работать

После настройки автоматически отправляются уведомления:

1. **Вход в аккаунт** → пользователю (IP, время, браузер)
2. **Новая заявка** → всем работникам
3. **Назначение ответственного** → исполнителю
4. **Низкий остаток** → всем работникам

## 📚 Подробная информация

- `EMAIL_NOTIFICATIONS.md` - краткая справка по функциям
- `EMAIL_SETUP.md` - детальная настройка и troubleshooting

## ❓ Проблемы?

**Ошибка аутентификации:**
- Проверьте, что используете **пароль приложения**, а не обычный пароль
- Убедитесь, что двухфакторная аутентификация включена

**Письма не приходят:**
- Проверьте папку **Спам**
- Убедитесь, что у пользователей указаны email в профилях

**Другие проблемы:**
- См. `EMAIL_SETUP.md` раздел "Устранение проблем"
