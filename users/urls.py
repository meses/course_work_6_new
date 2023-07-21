from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, UserListView, confirm_code, confirmation_succsess, \
    toggle_activity_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/confirm_code/<str:email>/', confirm_code, name='confirm_code'),
    path('register/confirmation_succsess/', confirmation_succsess, name='confirmation_succsess'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('toggle_activity_user/<int:pk>/', toggle_activity_user, name='toggle_activity_user'),
]