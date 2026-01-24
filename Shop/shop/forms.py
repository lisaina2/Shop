from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyModel
from .models import UserData

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    # Здесь определите поля вашей формы
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class MyForm(forms.ModelForm):
    class Meta:
        model = UserData  # указываем модель, с которой связана форма
        fields = ['name', 'email']  # перечисляем поля модели, которые будут в форме

class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Телефон')
    address = forms.CharField(widget=forms.Textarea, label='Адрес доставки')
    comment = forms.CharField(widget=forms.Textarea, required=False, label='Комментарий')

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2', 'field3']  # Укажите нужные поля

    def clean_field1(self):
        # Дополнительная валидация
        data = self.cleaned_data['field1']
        # Ваша логика валидации
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
