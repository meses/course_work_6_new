from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from main.forms import CustomerForm, SendingSettingsForm, MessageForm
from main.models import Customer, Message, SendingSettings, Log, BlogPost
from main.services import send_message, get_cached_log_data
from config.settings import CACHE_ENABLED
from django.core.cache import cache

# Create your views here.
company_name = 'Рассылки'


def index(request):
    return render(request, 'main/index.html')

class IndexView(ListView):
    def get(self, request, *args, **kwargs):
        sendingsettings_count = SendingSettings.objects.count()  # получаем информацию об общем количестве рассылок
        sendingsettings_count_run = SendingSettings.objects.filter(
            status='running').count()  # получаем информацию об количестве активных рассылок
        unique_customers_count = Customer.objects.annotate(num_sendingsettings=Count('sendingsettings')).filter(
            num_sendingsettings__gt=0).count()  # получаем информацию об уникальных клиентах
        blog_posts = list(BlogPost.objects.filter(is_active=True).order_by('?').values_list('title', flat=True)[
                          :3])  # получаем три случайные публикации
        context = {
            'title': 'Главная',
            'newsletters_count': sendingsettings_count,
            'newsletters_count_run': sendingsettings_count_run,
            'unique_customers_count': unique_customers_count,
            'blog_posts': blog_posts
        }
        return render(request, 'main/index.html', context)

class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    permission_required = 'main.view_customer'
    extra_context = {
        'title': 'Клиенты',
        'company_title': company_name
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id = self.request.user)
        return queryset

class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    permission_required = 'main.add_customer'

    def form_valid(self, form):
        form = CustomerForm(data=self.request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user_id = self.request.user
            customer.save()
        return HttpResponseRedirect(reverse('main:customers'))

class CustomerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Customer
    permission_required = 'main.view_customer'

class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    permission_required = 'main.update_customer'
    success_url = reverse_lazy('main:customers')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('main:customer_update', kwargs={'pk': pk})

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('main:customers')

    def test_func(self):
        return self.request.user.is_superuser  # жесткие требования на удаление (только суперюзер может удалить)

class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    permission_required = 'main.view_message'
    extra_context = {
        'title': 'Список сообщений'
    }

class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'main.add_message'
    success_url = reverse_lazy('main:messages')


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'main.update_message'
    success_url = reverse_lazy('main:messages')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:messages')

    def test_func(self):
        return self.request.user.is_superuser  # жесткие требования на удаление (только суперюзер может удалить)

class SendingSettingsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SendingSettings
    permission_required = 'main.view_sendingsettings'
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id = self.request.user)
        return queryset

class SendingSettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SendingSettings
    form_class = SendingSettingsForm
    permission_required = 'main.add_sendingsettings'
    success_url = reverse_lazy('main:sendingsettings')

    def form_valid(self, form):
        form.instance.status = 'running'
        response = super().form_valid(form)
        send_message(self.object)
        form = SendingSettingsForm(data=self.request.POST)
        if form.is_valid():
            sendingsettings = form.save(commit=False)
            sendingsettings.user_id = self.request.user
            sendingsettings.save()
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        message_item = self.object
        message_item.status = 'running'
        message_item.save()
        send_message(message_item)
        return response


class SendingSettingsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
        model = SendingSettings
        permission_required = 'main.view_sendingsettings'


class SendingSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SendingSettings
    form_class = SendingSettingsForm
    permission_required = 'main.update_sendingsettings'
    success_url = reverse_lazy('main:sendingsettings')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('main:sendingsettings_update', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sendingsettings_count'] = SendingSettings.objects.count()
        return context

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        print(object.user_id)
        print(self.request.user)
        if object.user_id != self.request.user:
            raise Http404("Вы не являетесь владельцем рассылки.")
        return object

class SendingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = SendingSettings
    success_url = reverse_lazy('main:sendingsettings')

    def test_func(self):
        return self.request.user.is_superuser  # жесткие требования на удаление (только суперюзер может удалить)

class LogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Log
    permission_required = 'main.view_log'
    extra_context = {
        'title': 'Список логов'
    }

class LogDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Log
    permission_required = 'main.view_log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['log_data'] = get_cached_log_data(self.object)
        return context

@login_required
def toggle_activity_sendingsettings(request, pk):
    sendingsettings_item = get_object_or_404(SendingSettings, pk=pk)
    if sendingsettings_item.status == 'running':
        sendingsettings_item.status = 'completed'
    else:
        sendingsettings_item.status = 'running'

    sendingsettings_item.save()

    return redirect(reverse('main:sendingsettings'))

class BlogListView(ListView):
    model = BlogPost
    context_object_name = 'blogs'

    def get_queryset(self):
        return BlogPost.objects.filter(is_active=True)  # по положительному признаку публикации

class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()

        return self.object
