# Настройка Email-уведомлений

Система отправляет автоматические email-уведомления для следующих событий:

## Типы уведомлений

1. **Вход в аккаунт** - пользователю приходит уведомление о входе с указанием IP-адреса и браузера
2. **Новая заявка** - всем работникам приходит уведомление о создании новой заявки
3. **Назначение ответственного** - исполнитель получает уведомление с деталями заявки
4. **Низкий остаток товара** - всем работникам приходит уведомление о товаре с низким остатком

## Настройка для Gmail

### 1. Создайте пароль приложения

1. Перейдите в настройки Google Account: https://myaccount.google.com/
2. Включите двухфакторную аутентификацию (если еще не включена)
3. Перейдите в "Безопасность" → "Пароли приложений"
4. Создайте новый пароль для приложения "Почта"
5. Скопируйте сгенерированный пароль (16 символов)

### 2. Настройте переменные окружения

Создайте файл `.env` или добавьте в существующий:

```env
# Email settings для Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

Замените:
- `your-email@gmail.com` - на ваш реальный Gmail адрес
- `your-app-password-here` - на созданный пароль приложения

## Настройка для других почтовых сервисов

### Yandex Mail
```env
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email@yandex.ru
```

### Mail.ru
```env
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@mail.ru
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email@mail.ru
```

### Другие SMTP серверы
```env
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587  # или 465 для SSL
EMAIL_USE_TLS=True  # или False для SSL
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email@example.com
```

## Тестирование в разработке

Для тестирования без реальной отправки писем используйте консольный бэкенд.
В `ronix_project/settings.py` раскомментируйте строку:

```python
# Для разработки - письма выводятся в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Закомментируйте основной бэкенд:

```python
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

## Требования к пользователям

Для получения уведомлений пользователи должны:
- Иметь указанный email адрес в профиле
- Email должен быть действительным

## Логирование

Все отправленные письма логируются. Проверить можно в логах приложения.

## Устранение проблем

### Ошибка аутентификации
- Проверьте правильность email и пароля
- Убедитесь, что включена двухфакторная аутентификация (для Gmail)
- Используйте пароль приложения, а не обычный пароль аккаунта

### Письма не приходят
- Проверьте папку "Спам"
- Убедитесь, что у пользователей указаны email адреса
- Проверьте логи на наличие ошибок

### Таймаут соединения
- Проверьте настройки порта (587 для TLS, 465 для SSL)
- Убедитесь, что EMAIL_USE_TLS соответствует используемому порту
- Проверьте настройки файрвола

## Отключение уведомлений

Чтобы временно отключить отправку уведомлений, используйте консольный бэкенд (см. выше).

Чтобы отключить конкретные типы уведомлений, закомментируйте соответствующие вызовы:
- В `users/signals.py` - уведомления о входе
- В `orders/views.py` (order_create) - уведомления о новых заявках
- В `orders/views.py` (order_edit) - уведомления о назначении
- В `inventory/signals.py` - уведомления о низком остатке
