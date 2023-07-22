from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.services import generate_code


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    #success_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('users:confirm_code', kwargs={'email': self.object.email})

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            code = generate_code()
            new_user.verify_code = code
            new_user.save()
            send_mail(
                subject='Поздравляем с регистрацией!',
                message=f'Поздравляем! Вы зарегистрировались в магазине на диване. Для завершения регистрации введите этот код: {code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
            my_group = Group.objects.get(name='simple_user')
            new_user.groups.add(my_group)

        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def confirm_code(request, email):
    if request.method == 'POST':
        verify_code = request.POST.get('verify_code')
        user = User.objects.get(email=email)
        if user.verify_code == verify_code:
            user.is_active = True
            user.save()
            return redirect(reverse('users:confirmation_succsess'))
        else:
            raise ValidationError(f'You have used the wrong code!')
    else:
        context = {'title': 'Подтверждение почты'}

    return render(request, 'users/confirm_code.html', context)

class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'
    extra_context = {
        'title': 'Список пользователей сервиса'
    }

def confirmation_succsess(request):
    return render(request, 'users/confirmation_succsess.html')

@login_required
def toggle_activity_user(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()

    return redirect(reverse('users:users_list'))

