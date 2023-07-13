from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from main.forms import CustomerForm, SendingSettingsForm, MessageForm
from main.models import Customer, Message, SendingSettings
from main.services import send_message

# Create your views here.
company_name = 'Рассылки'


def index(request):
    return render(request, 'main/index.html')

class CustomerListView(ListView):
    model = Customer
    extra_context = {
        'title': 'Клиенты',
        'company_title': company_name
    }

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('main:customers')

class CustomerDetailView(DetailView):
    model = Customer

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('main:customers')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('main:customer_update', kwargs={'pk': pk})

class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('main:customers')

    def test_func(self):
        return self.request.user.is_superuser  # жесткие требования на удаление (только суперюзер может удалить)

class MessageListView(ListView):
    model = Message
    extra_context = {
        'title': 'Список сообщений'
    }

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:messages')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:messages')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:messages')

    def test_func(self):
        return self.request.user.is_superuser  # жесткие требования на удаление (только суперюзер может удалить)

class SendingSettingsListView(ListView):
    model = SendingSettings
    extra_context = {
        'title': 'Список рассылок'
    }

class SendingSettingsCreateView(CreateView):
    model = SendingSettings
    form_class = SendingSettingsForm
    success_url = reverse_lazy('main:sendingsettings')

    def form_valid(self, form):
        form.instance.status = 'running'
        response = super().form_valid(form)
        send_message(self.object)
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        message_item = self.object
        message_item.status = 'running'
        message_item.save()
        send_message(message_item)
        return response


class SendingSettingsDetailView(DetailView):
        model = SendingSettings


class SendingSettingsUpdateView(UpdateView):
    model = SendingSettings
    form_class = SendingSettingsForm
    success_url = reverse_lazy('main:sendingsettings')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('main:sendingsettings_update', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sendingsettings_count'] = SendingSettings.objects.count()
        return context

class SendingSettingsDeleteView(DeleteView):
    model = SendingSettings
    success_url = reverse_lazy('main:sendingsettings')

    def test_func(self):
        return self.request.user.is_superuser  # жесткие требования на удаление (только суперюзер может удалить)