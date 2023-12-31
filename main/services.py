from django.core.mail import send_mail

from config import settings
from main.models import Message, Log, SendingSettings
from django.core.cache import cache


def daily_send():
    for item in SendingSettings.objects.filter(frequency='daily'):
        item.status = 'running'
        item.save()
        send_message(item)
        item.status = 'completed'
        item.save()


def weekly_send():
    for item in SendingSettings.objects.filter(frequency='weekly'):
        item.status = 'running'
        item.save()
        send_message(item)
        item.status = 'completed'
        item.save()


def monthly_send():
    for item in SendingSettings.objects.filter(frequency='monthly'):
        item.status = 'running'
        item.save()
        send_message(item)
        item.status = 'completed'
        item.save()


def send_message(message_item: SendingSettings):
    # Получаем список email-адресов клиентов, которым нужно отправить рассылку
    customers_emails = message_item.customers.values_list('email', flat=True)  # noqa(отключить проверку)

    # Отправляем письмо каждому клиенту
    for email in customers_emails:
        message = Message.objects.create(message=message_item)
        try:
            send_mail(
                message_item.subject,  # Тема письма
                message_item.body,  # Тело письма
                settings.EMAIL_HOST_USER,  # От кого отправляем письмо
                [email],  # Кому отправляем письмо
                fail_silently=False,
            )
            status = 'success'
            response = 'Email sent successfully'
        except Exception as e:
            status = 'error'
            response = str(e)
        Log.objects.create(message=message, status=status, response=response)


# run crontab
# python manage.py crontab add

# show current active jobs of this project:
# python manage.py crontab show

# removing all defined jobs is straight forward:
# python manage.py crontab remove

def get_cached_log_data(log):
    if settings.CACHE_ENABLE:
        cache_key = f'log_{log.pk}'
        cached_data = cache.get(cache_key)
        if cached_data is None:
            cached_data = {
                'message': log.message,  # Сообщение для рассылки
                'timestamp': log.timestamp,  # Дата и время последней попытки
                'status': log.status,  # Статус попытки
                'response': log.response,  # Ответ почтового сервера, если он был
            }
            cache.set(cache_key, cached_data, 300)  # Кешируем данные на 5 минут
        return cached_data
    else:
        return {
            'message': log.message,  # Сообщение для рассылки
            'timestamp': log.timestamp,  # Дата и время последней попытки
            'status': log.status,  # Статус попытки
            'response': log.response,  # Ответ почтового сервера, если он был
        }
