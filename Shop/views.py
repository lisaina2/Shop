# views.py: Обрабатывает запросы и возвращает ответы.
from django.shortcuts import render, redirect, get_object_or_404 # Импорт функций для работы с запросами и ответами.
from .models import Product, Category, Order, OrderItem # Импорт моделей.
from .forms import CheckoutForm # Импорт формы.
from django.contrib import messages # Импорт модуля для работы с сообщениями.
from django.core.paginator import Paginator # Импорт класса Paginator для разбиения списка объектов на страницы.
from django.views.generic import CreateView
from .forms import RegisterForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'

def register(request):
    # Логика регистрации пользователя
    return render(request, 'register.html')  # или другой ответ

# Функция для отображения списка продуктов.
def product_list(request, category_slug=None):
    category = None # Инициализация переменной category.
    products = Product.objects.filter(in_stock=True) # Получение списка товаров, которые есть в наличии.
    if category_slug: # Если передан slug категории.
        category = get_object_or_404(Category, slug=category_slug) # Получение объекта Category по slug.
        products = products.filter(category=category) # Фильтрация товаров по категории.

    paginator = Paginator(products, 10)  # Создание объекта Paginator (10 товаров на странице).
    page_number = request.GET.get('page') # Получение номера страницы из GET-параметра.
    page_obj = paginator.get_page(page_number) # Получение объекта Page.

    return render(request, 'shop/product_list.html', {'category': category, 'page_obj': page_obj}) # Рендеринг шаблона.

def product_detail(request, id):
  product = get_object_or_404(Product, id=id) # Получает продукт по id, если не находит то 404
  return render(request, 'shop/product_detail.html', {'product': product}) # Отображает детальную информацию о продукте

def cart(request):
    cart = request.session.get('cart', {})# Получает корзину из сессии или создает пустую
    return render(request, 'shop/cart.html', {'cart': cart}) # Отображает корзину

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id) # Получает продукт по id
    cart = request.session.get('cart', {}) # Получает корзину из сессии
    cart[id] = cart.get(id, 0) + 1 # Увеличивает количество товара в корзине
    request.session['cart'] = cart # Сохраняет корзину в сессии
    messages.success(request, 'Товар добавлен в корзину!') # Выводит сообщение об успехе
    return redirect('product_list') # Или на страницу товара

def checkout(request):
    if request.method == 'POST': # Если это POST запрос
        form = CheckoutForm(request.POST) # Создает форму с данными из POST запроса
        if form.is_valid(): # Если форма валидна
            # Логика создания заказа (Order, OrderItem)
            # Очистка корзины в сессии
            messages.success(request, 'Заказ успешно оформлен!') # Выводит сообщение об успехе
            return redirect('product_list') # Перенаправляет на страницу со списком товаров
    else: # Если это GET запрос
        form = CheckoutForm()  # Создает пустую форму
    return render(request, 'shop/checkout.html', {'form': form}) # Отображает страницу оформления заказа
