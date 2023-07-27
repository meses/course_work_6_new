from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import index, CustomerListView, MessageListView, SendingSettingsListView, CustomerCreateView, \
    CustomerDetailView, CustomerUpdateView, CustomerDeleteView, SendingSettingsCreateView, SendingSettingsDetailView, \
    SendingSettingsUpdateView, SendingSettingsDeleteView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    LogListView, LogDetailView, toggle_activity_sendingsettings

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/detail/<int:pk>', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/update/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='messages_create'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('sendingsettings/', cache_page(60)(SendingSettingsListView.as_view()), name='sendingsettings'),
    path('sendingsettings/create/', SendingSettingsCreateView.as_view(), name='sendingsettings_create'),
    path('sendingsettings/sendingsettings_details/<int:pk>/', SendingSettingsDetailView.as_view(), name='sendingsettings_detail'),
    path('sendingsettings/update/<int:pk>/', SendingSettingsUpdateView.as_view(), name='sendingsettings_update'),
    path('sendingsettings/delete/<int:pk>/', SendingSettingsDeleteView.as_view(), name='sendingsettings_delete'),
    path('logs/', LogListView.as_view(), name='logs'),
    path('log_details/<int:pk>/', LogDetailView.as_view(), name='log_detail'),
    path('toggle_activity_sendingsettings/<int:pk>/', toggle_activity_sendingsettings, name='toggle_activity_sendingsettings'),

]