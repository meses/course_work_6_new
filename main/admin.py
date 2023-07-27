from django.contrib import admin

from main.models import Customer, SendingSettings, Message, Log, BlogPost


# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'description')
    list_filter = ('name', 'email', 'description')


@admin.register(SendingSettings)
class SendingSettingsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'frequency', 'status')
    list_filter = ('frequency', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('message', 'timestamp', 'status', 'response')
    list_filter = ('message', 'timestamp', 'status', 'response')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'pub_date', 'is_active')
    list_filter = ('title', 'views', 'pub_date', 'is_active')