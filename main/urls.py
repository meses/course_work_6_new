from django.urls import path

from main.apps import MainConfig
from main.views import index, CustomerListView, MessageListView, SendingSettingsListView, CustomerCreateView, \
    CustomerDetailView, CustomerUpdateView, CustomerDeleteView, SendingSettingsCreateView, SendingSettingsDetailView, \
    SendingSettingsUpdateView, SendingSettingsDeleteView, MessageCreateView, MessageUpdateView, MessageDeleteView

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
    path('sendingsettings/', SendingSettingsListView.as_view(), name='sendingsettings'),
    path('sendingsettings/create/', SendingSettingsCreateView.as_view(), name='sendingsettings_create'),
    path('sendingsettings/sendingsettings_details/<int:pk>/', SendingSettingsDetailView.as_view(), name='sendingsettings_detail'),
    path('sendingsettings/update/<int:pk>/', SendingSettingsUpdateView.as_view(), name='sendingsettings_update'),
    path('sendingsettings/delete/<int:pk>/', SendingSettingsDeleteView.as_view(), name='sendingsettings_delete'),

]