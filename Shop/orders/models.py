# shop/orders/models.py
from django.db import models
from django.conf import settings
from shop.models import Product  # предположим, Product лежит в приложении shop


class Order(models.Model):
    status = models.CharField(
        max_length=20,
        choices=[('new', 'Новый'), ('paid', 'Оплачен'), ('shipped', 'Отправлен')],
        default='new',
        verbose_name='Статус'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Сумма заказа'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name = 'orders_orders',  # Другое уникальное имя!
    )
    address = models.TextField(verbose_name='Адрес доставки')
    email = models.EmailField(verbose_name='Email')
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    comment = models.TextField(blank=True, verbose_name='Комментарий', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Заказ #{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за единицу'
    )
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='orders_orderitems')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')


    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'


from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
