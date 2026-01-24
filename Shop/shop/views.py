# Импорты необходимых модулей и классов Django
from django.shortcuts import render, redirect
from .forms import MyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Product
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from .models import MyModel
from django import forms
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.views import generic
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, CartItem
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order, OrderItem
from cart.models import Cart
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')  # укажите путь к вашему шаблону

class RegisterView(CreateView):
    form_class = RegisterForm # Используемая форма для регистрации пользователя
    template_name = 'register.html'
    success_url = '/'

def form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Обработка валидных данных
            return redirect('success_url')
    else:
        form = MyForm()

    # Если форма невалидна, рендерим её с ошибками
    return render(request, 'template.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user()) # Авторизация пользователя
            return redirect('success_page')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def product_list(request):
    products = Product.objects.all() # Получение всех товаров из базы данных
    return render(request, 'shop/product_list.html', {'products': products})

def paginated_view(request):
    objects = MyModel.objects.all()
    paginator = Paginator(objects, 10)  # 10 объектов на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'paginated_template.html', {'page_obj': page_obj})

# Определяем форму, которая будет использоваться для получения данных от пользователя
class MyForm(forms.Form):
    field1 = forms.CharField()
    field2 = forms.IntegerField()
    name = forms.CharField(label="Имя", max_length=100)
    email = forms.EmailField(label="Email")
    pass

# Функция представления, обрабатывающая запросы к странице
def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)  # создаём форму с данными POST
        if form.is_valid():
            # Сохраняем данные в БД — метод save() создаёт объект UserData
            form.save()
            messages.success(request, 'Данные успешно сохранены!')
            return redirect('my_view')  # перенаправляем для очистки формы
        else:
            messages.error(request, 'Пожалуйста, проверьте правильность введённых данных.')
    else:
        form = MyForm()  # пустая форма для GET-запроса
    # Рендерим шаблон 'my_template.html', передавая в него форму
    return render(request, 'my_template.html', {'form': form})


class ProductListView(generic.ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Пагинация по 10 товаров

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по категории
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Поиск по названию
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset.order_by('-created_at')

def user_logout(request):
    logout(request) # Выход пользователя из системы
    return redirect('login')

def profile(request):
    # Здесь логика отображения профиля
    return render(request, 'accounts/profile.html')

@login_required
def handle_form_submission(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в БД
            try:
                # Вариант 1: сохранение через форму
                form.save(user=request.user)

                # ИЛИ Вариант 2: ручное сохранение
                # instance = form.save(commit=False)
                # instance.user = request.user
                # instance.save()

                return redirect('success_url')  # Замените на ваш URL
            except Exception as e:
                form.add_error(None, f'Ошибка сохранения: {str(e)}')
    else:
        form = MyForm()

    return render(
        request,
        'template.html',
        {
            'form': form,
            'title': 'Форма создания записи'
        }
    )

def success_view(request):
    return render(request, 'success.html', {'message': 'Данные успешно сохранены!'})

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.session.get('cart_id'):
        cart_id = request.session['cart_id']
        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart_id,
            product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1
        )
    return redirect('cart_detail')


def cart_detail(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.cartitem_set.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def update_cart_item(request, product_id, quantity):
    cart = get_cart(request)

    if product_id in cart['items']:
        cart['items'][product_id]['quantity'] = quantity

        # Если количество 0 или меньше - удаляем товар
        if quantity <= 0:
            del cart['items'][product_id]

        # Пересчет общей суммы
        cart['total_price'] = sum(
            item['quantity'] * item['price']
            for item in cart['items'].values()
        )

        request.session.modified = True


def remove_from_cart(request, product_id):
    cart = get_cart(request)

    if product_id in cart['items']:
        del cart['items'][product_id]

        # Пересчет общей суммы
        cart['total_price'] = sum(
            item['quantity'] * item['price']
            for item in cart['items'].values()
        )

        request.session.modified = True

# context_processors.py
def cart_context(request):
    cart = get_cart(request)
    return {'cart': cart}

def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user if request.user.is_authenticated else None,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                comment=form.cleaned_data['comment'],
                total_amount=cart.get_total_price()
            )
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['price'])

            cart.clear()
            return redirect('order_success') # Создайте страницу подтверждения заказа
    else:
        form = OrderForm()
    return render(request, 'order/create.html', {'form': form, 'cart': cart})

@login_required # Доступ только для авторизованных
def order_history(request):
    # Только для авторизованных: список заказов пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

@login_required # Доступ только для авторизованных; только свои заказы
def order_detail(request, order_id):
    # Только для авторизованных: детальная информация о конкретном заказе
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})