from django.contrib.auth.models import User, AbstractUser
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class Category(models.Model):
    name = models.CharField('Название категории', max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название товара', max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField('Дата добавления', default=timezone.now)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Исправляем ссылку на пользователя
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Вместо User
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField(default=0)
    field3 = models.TextField(default='')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    user = settings.AUTH_USER_MODEL
    title = models.CharField(max_length=255, default='Untitled')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, default='')
    field1 = models.CharField(max_length=255, default='')  # или другой тип поля

    def __str__(self):
        return self.name

class UserData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Order(models.Model):
    # Пользователь (может быть null для гостей)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='shop_orders',  # Уникальное имя!
        on_delete=models.SET_NULL,  # изменено с PROTECT на SET_NULL
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    # Личные данные (объединяем first_name/last_name в одно поле name)
    name = models.CharField('Имя и фамилия', max_length=200, default='Не указано')  # новое поле
    email = models.EmailField(default='no-email@example.com')
    phone = models.CharField('Телефон', max_length=20, default='+7 (000) 000-00-00')
    address = models.TextField('Адрес доставки',max_length=255, default='Адрес не указан')

    # Комментарий (сохраняем)
    comment = models.TextField('Комментарий', blank=True)

    # Общая сумма (исправляем null=True → default)
    total_amount = models.DecimalField(
        'Общая сумма',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    # Статус (приводим к стандартному формату)
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    # Дата создания (сохраняем)
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    # Метод оплаты (сохраняем)
    payment_method = models.CharField(
        'Метод оплаты',
        max_length=50,
        blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} от {self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name = 'shop_orderitems'  # Уникальное имя!
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField(
        'Цена на момент покупки',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.quantity} × {self.product.name}'

