from django.db import models
from django.conf import settings
from shop.models import Product
from django.conf import settings

class Cart(models.Model):
    """
    Модель корзины покупок.
    Хранит информацию о корзине пользователя (или гостя),
    её статусе и времени создания.
    """

    # Связь с пользователем (может быть пустой для гостей)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # При удалении пользователя удаляются и его корзины
        null=True,                   # В БД может быть NULL
        blank=True,                 # В формах можно не заполнять
        verbose_name='Пользователь'
    )

    # Дата и время создания корзины
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,         # Устанавливается при создании
        editable=False              # Нельзя редактировать вручную
    )

    # Возможные статусы корзины
    STATUS_CHOICES = [
        ('active', 'Активна'),      # Корзина открыта, товары добавляются
        ('ordered', 'Оформлена'), # Заказ оформлен, идёт обработка
        ('cancelled', 'Отменена'), # Корзина отменена
    ]

    # Поле статуса с выбором из вариантов
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',            # Статус по умолчанию
        help_text='Выберите статус корзины'
    )

    # Общая сумма товаров в корзине (если нужно)
    total_amount = models.DecimalField(
        'Общая сумма',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='Сумма всех товаров в корзине'
    )

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-created_at']
        db_table = 'cart'

    def __str__(self):
        user_info = self.user.username if self.user else 'Гость'
        return f'Корзина #{self.id} ({user_info})'

    def save(self, *args, **kwargs):
        # Здесь можно добавить логику (например, пересчёт суммы)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product_name = models.CharField(max_length=200, verbose_name='Название товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

