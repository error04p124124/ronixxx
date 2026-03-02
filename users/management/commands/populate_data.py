"""
Management command to populate the database with sample data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User
from inventory.models import Category, Component, Supplier, Service
from orders.models import Order, OrderItem
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Создаём группы
        self.create_groups()
        
        # Создаём пользователей
        self.create_users()
        
        # Создаём категории
        self.create_categories()
        
        # Создаём поставщиков
        self.create_suppliers()
        
        # Создаём комплектующие
        self.create_components()
        
        # Создаём услуги
        self.create_services()
        
        # Создаём заявки
        self.create_orders()
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Test users created:'))
        self.stdout.write(self.style.SUCCESS('  Client: client / client123'))
        self.stdout.write(self.style.SUCCESS('  Worker: worker / worker123'))

    def create_groups(self):
        Group.objects.get_or_create(name='Клиенты')
        Group.objects.get_or_create(name='Работники')
        self.stdout.write('✓ Groups created')

    def create_users(self):
        # Клиент
        client, created = User.objects.get_or_create(
            username='client',
            defaults={
                'email': 'client@example.com',
                'first_name': 'Иван',
                'last_name': 'Клиентов',
                'role': 'client',
                'phone': '+7 (999) 111-22-33',
                'address': 'г. Москва, ул. Примерная, д. 10, кв. 5',
            }
        )
        if created:
            client.set_password('client123')
            client.save()
        
        # Работник
        worker, created = User.objects.get_or_create(
            username='worker',
            defaults={
                'email': 'worker@ronix-l.ru',
                'first_name': 'Петр',
                'last_name': 'Работников',
                'role': 'worker',
                'phone': '+7 (999) 222-33-44',
                'address': 'г. Москва, ул. Рабочая, д. 20',
            }
        )
        if created:
            worker.set_password('worker123')
            worker.save()
        
        self.stdout.write('✓ Users created')

    def create_categories(self):
        categories = [
            ('Электронные компоненты', 'Резисторы, конденсаторы, транзисторы'),
            ('Микроконтроллеры', 'Arduino, Raspberry Pi, ESP32'),
            ('Датчики', 'Температурные, давления, движения'),
            ('Дисплеи', 'LCD, OLED, TFT дисплеи'),
            ('Механические детали', 'Винты, гайки, крепежи'),
        ]
        
        for name, desc in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
        
        self.stdout.write('✓ Categories created')

    def create_suppliers(self):
        suppliers = [
            ('ООО "ЭлектроКомпонент"', 'Иванов И.И.', 'info@elektro.ru', '+7 (495) 111-22-33'),
            ('ООО "ТехПоставка"', 'Петров П.П.', 'sales@techpost.ru', '+7 (495) 222-33-44'),
            ('ИП Сидоров С.С.', 'Сидоров С.С.', 'sidorov@mail.ru', '+7 (495) 333-44-55'),
        ]
        
        for name, contact, email, phone in suppliers:
            Supplier.objects.get_or_create(
                name=name,
                defaults={
                    'contact_person': contact,
                    'email': email,
                    'phone': phone,
                    'address': 'г. Москва, ул. Складская, д. 10'
                }
            )
        
        self.stdout.write('✓ Suppliers created')

    def create_components(self):
        categories = {cat.name: cat for cat in Category.objects.all()}
        
        components = [
            ('Резистор 10 кОм', categories['Электронные компоненты'], 'RES-10K', 'Vishay', Decimal('2.50'), 1000, 50),
            ('Конденсатор 100 мкФ', categories['Электронные компоненты'], 'CAP-100uF', 'Panasonic', Decimal('5.00'), 500, 30),
            ('Arduino Uno R3', categories['Микроконтроллеры'], 'ARD-UNO-R3', 'Arduino', Decimal('1200.00'), 15, 5),
            ('Raspberry Pi 4 8GB', categories['Микроконтроллеры'], 'RPI4-8GB', 'Raspberry', Decimal('8500.00'), 8, 3),
            ('ESP32 DevKit', categories['Микроконтроллеры'], 'ESP32-DEV', 'Espressif', Decimal('450.00'), 25, 10),
            ('Датчик температуры DHT22', categories['Датчики'], 'DHT22', 'Asong', Decimal('350.00'), 30, 10),
            ('Ультразвуковой датчик HC-SR04', categories['Датчики'], 'HC-SR04', 'Generic', Decimal('120.00'), 50, 20),
            ('LCD дисплей 16x2', categories['Дисплеи'], 'LCD-16x2', 'Hitachi', Decimal('250.00'), 20, 5),
            ('OLED дисплей 0.96"', categories['Дисплеи'], 'OLED-096', 'SSD1306', Decimal('450.00'), 12, 5),
            ('Винт M3x10мм (100шт)', categories['Механические детали'], 'SCR-M3-10', 'DIN', Decimal('150.00'), 100, 20),
        ]
        
        for name, category, article, manufacturer, price, quantity, min_qty in components:
            Component.objects.get_or_create(
                article_number=article,
                defaults={
                    'name': name,
                    'category': category,
                    'manufacturer': manufacturer,
                    'price': price,
                    'quantity': quantity,
                    'min_quantity': min_qty,
                    'description': f'Описание для {name}'
                }
            )
        
        self.stdout.write('✓ Components created')

    def create_services(self):
        services = [
            # Замена деталей
            ('Замена батареи iPhone', 'replacement', 'Замена аккумулятора на оригинальную или совместимую батарею для iPhone всех моделей', Decimal('1500.00'), 30),
            ('Замена батареи Android', 'replacement', 'Замена аккумулятора для смартфонов на базе Android (Samsung, Xiaomi, Huawei и др.)', Decimal('1200.00'), 30),
            ('Замена экрана iPhone', 'replacement', 'Замена дисплейного модуля iPhone с оригинальной или совместимой матрицей', Decimal('3500.00'), 60),
            ('Замена экрана Samsung', 'replacement', 'Замена дисплея для смартфонов Samsung Galaxy', Decimal('2800.00'), 60),
            ('Замена стекла камеры', 'replacement', 'Замена защитного стекла основной или фронтальной камеры', Decimal('500.00'), 20),
            ('Замена динамика/микрофона', 'replacement', 'Замена разговорного динамика или микрофона в смартфоне', Decimal('800.00'), 40),
            ('Замена разъёма зарядки', 'replacement', 'Замена USB/Lightning разъёма зарядки', Decimal('1000.00'), 45),
            
            # Ремонт
            ('Ремонт материнской платы', 'repair', 'Диагностика и ремонт материнской платы смартфона/планшета (пайка, замена чипов)', Decimal('2500.00'), 120),
            ('Ремонт после попадания влаги', 'repair', 'Чистка, сушка и восстановление устройства после попадания жидкости', Decimal('1800.00'), 90),
            ('Ремонт кнопок управления', 'repair', 'Ремонт или замена физических кнопок (громкость, питание, Home)', Decimal('700.00'), 30),
            ('Ремонт Face ID/Touch ID', 'repair', 'Восстановление работы биометрических датчиков', Decimal('2000.00'), 60),
            ('Ремонт камеры', 'repair', 'Ремонт основной или фронтальной камеры', Decimal('1500.00'), 45),
            
            # Диагностика
            ('Диагностика смартфона', 'diagnostics', 'Полная диагностика смартфона с выявлением всех неисправностей', Decimal('300.00'), 30),
            ('Диагностика планшета', 'diagnostics', 'Комплексная диагностика планшета', Decimal('350.00'), 30),
            ('Диагностика ноутбука', 'diagnostics', 'Полная диагностика ноутбука (железо и ПО)', Decimal('500.00'), 45),
            ('Экспресс-диагностика', 'diagnostics', 'Быстрая проверка основных функций устройства', Decimal('0.00'), 15),
            
            # Обслуживание
            ('Чистка от пыли', 'maintenance', 'Профилактическая чистка устройства от пыли и грязи', Decimal('600.00'), 30),
            ('Замена термопасты', 'maintenance', 'Замена термопасты в ноутбуке/компьютере', Decimal('800.00'), 40),
            ('Профилактика системы охлаждения', 'maintenance', 'Чистка и обслуживание системы охлаждения (вентиляторы, радиаторы)', Decimal('1000.00'), 50),
            
            # Установка
            ('Установка защитного стекла', 'installation', 'Установка защитного стекла на экран (стекло не входит в стоимость)', Decimal('200.00'), 10),
            ('Установка чехла/бампера', 'installation', 'Подбор и установка защитного чехла', Decimal('100.00'), 5),
            ('Прошивка устройства', 'installation', 'Установка или переустановка операционной системы', Decimal('1200.00'), 60),
            ('Разблокировка устройства', 'installation', 'Разблокировка смартфона от оператора или iCloud (при наличии документов)', Decimal('1500.00'), 90),
            
            # Прочее
            ('Восстановление данных', 'other', 'Восстановление удалённых файлов, фото, контактов', Decimal('2000.00'), 120),
            ('Перенос данных', 'other', 'Перенос всех данных со старого устройства на новое', Decimal('500.00'), 30),
            ('Настройка устройства', 'other', 'Первичная настройка нового устройства, установка приложений', Decimal('400.00'), 40),
            ('Прочее', 'other', 'Прочие работы (цена указана за 1 час работы)', Decimal('1000.00'), 60),
        ]
        
        for name, category, description, price, duration in services:
            Service.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'description': description,
                    'price': price,
                    'duration': duration,
                    'is_active': True,
                }
            )
        
        self.stdout.write('✓ Services created')

    def create_orders(self):
        client = User.objects.get(username='client')
        worker = User.objects.get(username='worker')
        
        # Создаём несколько заявок
        order1, created = Order.objects.get_or_create(
            id=1,
            defaults={
                'client': client,
                'order_type': 'service',
                'status': 'new',
                'description': 'Требуется ремонт платы Arduino. Не работает USB порт.',
            }
        )
        
        order2, created = Order.objects.get_or_create(
            id=2,
            defaults={
                'client': client,
                'order_type': 'components',
                'status': 'in_progress',
                'description': 'Необходимы комплектующие для проекта умного дома',
                'assigned_to': worker,
            }
        )
        
        if created:
            # Добавляем позиции в заявку
            arduino = Component.objects.get(article_number='ARD-UNO-R3')
            dht22 = Component.objects.get(article_number='DHT22')
            esp32 = Component.objects.get(article_number='ESP32-DEV')
            
            OrderItem.objects.create(order=order2, component=arduino, quantity=2, price=arduino.price)
            OrderItem.objects.create(order=order2, component=dht22, quantity=3, price=dht22.price)
            OrderItem.objects.create(order=order2, component=esp32, quantity=1, price=esp32.price)
            
            order2.calculate_total()
        
        self.stdout.write('✓ Orders created')
