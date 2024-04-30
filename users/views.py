from django.views.generic import CreateView
from django.urls import reverse_lazy
from config import settings
from users.forms import UserRegisterForm
from users.models import User
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views import View

import random
import string


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user_email = form.cleaned_data['email']

        try:
            send_mail(
                subject="Подтверждение регистрации",
                message="Вы успешно зарегистрированы!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
        except Exception as e:
            return print(e)

        form.save()

        return super().form_valid(form)


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        user_email = request.POST.get('email')
        try:
            user = User.objects.get(email=user_email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject='Сброс пароля',
                message=f'Вот твой новый пароль: {new_password}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            return render(request, 'users/password_reset_success.html')
        except User.DoesNotExist:
            return render(request, 'users/password_reset.html',
                          {'error': 'Пользователь с таким адресом электронной почты не существует.'})

