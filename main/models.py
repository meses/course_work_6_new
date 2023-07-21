from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    """Модель Клиент"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='email', unique=True)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, **NULLABLE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['id']


class SendingSettings(models.Model):
    """Модель Рассылка (настройки)"""
    # выбор частоты отправки ( день, неделя, месяц)
    SEND_FREQUENCY_CHOICES = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    )

    # статус рассылки
    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    )

    subject = models.CharField(max_length=50, verbose_name='Тема рассылки')
    body = models.TextField(verbose_name='Содержание письма')
    frequency = models.CharField(max_length=10, choices=SEND_FREQUENCY_CHOICES,
                                 verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created',
                              verbose_name='Статус рассылки')
    customers = models.ManyToManyField('Customer', verbose_name='Клиенты',
                                       related_name='sendingsettings')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, **NULLABLE)

    def __str__(self):
        return f'{self.subject}, {self.frequency}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['id']


class Message(models.Model):
    """Модель Сообщение для рассылки"""
    message = models.ForeignKey(SendingSettings, verbose_name='Рассылка',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']

    def __str__(self):
        return f'{self.message}'


class Log(models.Model):
    """Модель Логи рассылки"""
    # статус попытки
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('error', 'Ошибка'),
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                                verbose_name='Сообщение для рассылки')
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    response = models.TextField(
        verbose_name='Ответ почтового сервера, если он был', **NULLABLE)

    def __str__(self):
        return f"Время рассылки: {self.timestamp}\n"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
        ordering = ["-timestamp"]
