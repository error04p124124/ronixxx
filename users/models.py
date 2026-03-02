from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Расширенная модель пользователя."""
    
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('worker', 'Работник сервисного центра'),
    ]
    
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    @property
    def is_client(self):
        return self.role == 'client'
    
    @property
    def is_worker(self):
        return self.role == 'worker'


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    """Автоматически присваивает пользователя к нужной группе при создании."""
    if created:
        group_name = None
        if instance.role == 'client':
            group_name = 'Клиенты'
        elif instance.role == 'worker':
            group_name = 'Работники'
        
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
