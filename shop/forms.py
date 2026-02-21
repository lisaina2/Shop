<<<<<<< HEAD
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyModel

# Получаем кастомную модель пользователя
CustomUser = get_user_model()

class LoginForm(AuthenticationForm):
    # Используем стандартный AuthenticationForm — он уже содержит поля username/password
    # Можно добавить кастомные метки или виджеты
    username = forms.CharField(label='Логин')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )

class RegisterForm(UserCreationForm):
    # Форма регистрации на основе UserCreationForm
    email = forms.EmailField(label='Email')

    class Meta:
        model = CustomUser  # Используем кастомную модель
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    # Форма для редактирования профиля пользователя
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']  # Укажите нужные поля

class MyForm(forms.ModelForm):
    # Пример формы для другой модели (не пользователя)
    class Meta:
        model = MyModel  # Предположим, MyModel определена в models.py
        fields = ['field1', 'field2']

    def clean_field1(self):
        data = self.cleaned_data['field1']
        # Ваша логика валидации
        return data

class OrderForm(forms.Form):
    # Простая форма (не связана с моделью)
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Телефон')
    address = forms.CharField(widget=forms.Textarea, label='Адрес доставки')
    comment = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Комментарий'
    )
=======
# forms.py: Определяет формы для пользовательского ввода.
from django import forms # Импорт модуля для работы с формами Django.
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=200) # Поле имени.
    email = forms.EmailField() # Поле email.
    phone = forms.CharField(max_length=20) # Поле для телефона.
    address = forms.CharField(widget=forms.Textarea) # Поле адреса (текстовое поле).
    comment = forms.CharField(widget=forms.Textarea, required=False) # Поле для комментария.
>>>>>>> 6c6f88521e4ca81380e7054966a26293059fff48
