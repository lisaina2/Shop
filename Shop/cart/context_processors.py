from .models import Cart, CartItem
from django.contrib.auth.models import User

def cart_context(request):
    cart_items = []
    total_price = 0

    # Определяем корзину для авторизованного пользователя или гостя
    if request.user.is_authenticated:
        # Для авторизованных пользователей — берём корзину, привязанную к аккаунту
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            status='active'  # берём только активные корзины
        )
    else:
        # Для гостей создаём «анонимную» корзину (можно использовать session_key)
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            user=None,
            status='active'
        )

    # Получаем все позиции в корзине
    cart_items_qs = CartItem.objects.filter(cart=cart)

    # Собираем данные о товарах и считаем общую сумму
    for item in cart_items_qs:
        item_total = item.product.price * item.quantity
        total_price += item_total
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'item_total': item_total,
            'product_name': item.product.name,  # добавляем название товара для удобства
            'product_price': item.product.price  # цена за единицу
        })

    # Формируем словарь с данными для шаблонов
    return {
        'cart': cart,  # сама модель корзины (можно использовать статус и общую сумму)
        'cart_items': cart_items,  # список позиций в корзине
        'cart_total': total_price,  # общая сумма
        'cart_count': cart_items_qs.count(),  # количество позиций
        'cart_status': cart.status  # статус корзины ('active', 'ordered', 'cancelled')
    }

def cart_processor(request):
    cart = None
    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id, is_active=True).first()

    if cart:
        cart_items_count = cart.get_total_items()  # метод в модели Cart

    return {
        'cart': cart,
        'cart_items_count': cart_items_count,
    }
