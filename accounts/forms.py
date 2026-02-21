from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']  # ТОЛЬКО username и email!

    def __init__(self, *args, **kwargs):
        # Извлекаем instance из kwargs, если он передан; иначе — None
        self.instance = kwargs.pop('instance', None)
        # Вызываем родительский __init__ с оставшимися аргументами
        super().__init__(*args, **kwargs)