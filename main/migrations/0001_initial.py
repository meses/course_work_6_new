# Generated by Django 4.2.3 on 2023-07-12 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SendingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50, verbose_name='Тема рассылки')),
                ('body', models.TextField(verbose_name='Содержание письма')),
                ('frequency', models.CharField(choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')], max_length=10, verbose_name='Периодичность рассылки')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('running', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=10, verbose_name='Статус рассылки')),
                ('customers', models.ManyToManyField(related_name='sendingsettings', to='main.customer', verbose_name='Клиенты')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sendingsettings', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')),
                ('status', models.CharField(choices=[('success', 'Успешно'), ('error', 'Ошибка')], max_length=20, verbose_name='Статус попытки')),
                ('response', models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера, если он был')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.message', verbose_name='Сообщение для рассылки')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
                'ordering': ['-timestamp'],
            },
        ),
    ]