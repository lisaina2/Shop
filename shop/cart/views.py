from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required  # если корзина привязана к авторизованному пользователю
def cart_detail(request):
    # Пример: получаем корзину из сессии
    cart = request.session.get('cart', {})

    # Преобразуем данные для передачи в шаблон
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        # Здесь логика получения цены товара (например, из модели Product)
        # Допустим, у вас есть функция get_product_price(product_id)
        price = get_product_price(product_id)  # замените на реальную логику
        item_total = price * quantity
        total_price += item_total
        cart_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'price': price,
            'total': item_total
        })

    # Передаём данные в шаблон
    return render(request, 'cart/detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart:detail')  # перенаправляем на страницу корзины


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, 'Товар удалён из корзины.')
    else:
        messages.error(request, 'Товар не найден в корзине.')

    return redirect('cart:detail')  # перенаправляем обратно на страницу корзины
