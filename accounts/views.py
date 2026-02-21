from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model


def login_view(request):
    """
    Страница входа пользователя.
    Отображает форму входа и обрабатывает POST‑запрос.
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт.')
                return redirect('shop:home')  # или другое целевое представление
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """
    Страница регистрации пользователя.
    Отображает форму регистрации и обрабатывает POST‑запрос.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматический вход после регистрации
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Вы вошли в аккаунт.')
            return redirect('shop:home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    """
    Выход пользователя из системы.
    Перенаправляет на главную страницу после выхода.
    """
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('shop:home')

@login_required
def profile_view(request):
    """
    Личная страница пользователя (требует авторизации).
    Здесь можно добавить логику отображения данных профиля.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})
