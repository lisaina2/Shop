# forms.py: Определяет формы для пользовательского ввода.
from django import forms # Импорт модуля для работы с формами Django.
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=200) # Поле имени.
    email = forms.EmailField() # Поле email.
    phone = forms.CharField(max_length=20) # Поле для телефона.
    address = forms.CharField(widget=forms.Textarea) # Поле адреса (текстовое поле).
    comment = forms.CharField(widget=forms.Textarea, required=False) # Поле для комментария.
