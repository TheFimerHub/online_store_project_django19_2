from django.urls import path

from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView
from users.forms import UserLoginForm
from users.views import RegisterView, ResetPasswordView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
]
