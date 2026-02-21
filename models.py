# models.py: Описывает структуру базы данных.
from django.utils.text import slugify # Импорт функции slugify для создания slug по названию.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Дополнительные поля для профиля пользователя
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Краткая информация о себе (до 500 символов)"
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        help_text="Дата рождения"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Номер телефона (например, +79991234567)"
    )
    # Пример поля для связи с другими моделями (например, с корзиной пользователя)
    cart = models.OneToOneField(
        'Cart',  # предполагаем, что есть модель Cart
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Мета-информация для модели
    class Meta:
        db_table = 'custom_user'  # имя таблицы в БД
        ordering = ['-created_at']  # сортировка по умолчанию (новые сначала)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Возвращает полное имя пользователя (first_name + last_name)"""
        return f"{self.first_name} {self.last_name}".strip()


class MyModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='my_models'
    )

class Category(models.Model):
    name = models.CharField(max_length=200) # Название категории (текстовое поле).
    slug = models.SlugField(unique=True) # Slug (уникальный идентификатор) для URL.

    def save(self, *args, **kwargs): # Переопределение метода save для автоматического создания slug.
        self.slug = slugify(self.name) # Генерируем slug из названия.
        super().save(*args, **kwargs) # Вызываем родительский метод save.

    def __str__(self): # Метод для отображения объекта Category в виде строки.
        return self.name # Возвращает название категории.

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Связь "многие к одному" с Category.
    name = models.CharField(max_length=200) # Название продукта.
    description = models.TextField() # Описание продукта.
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена продукта.
    image = models.ImageField(upload_to='products/') # Изображение продукта.
    in_stock = models.BooleanField(default=True) # Наличие на складе.
    date_added = models.DateTimeField(auto_now_add=True) # Дата добавления (автоматически).

    def __str__(self): # Метод для отображения объекта Product в виде строки.
        return self.name # Возвращает название продукта.

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'  # опционально
    )

    name = models.CharField(max_length=200)  # Имя покупателя
    email = models.EmailField() # Емейл покупателя
    phone = models.CharField(max_length=20) # Телефон покупателя
    address = models.TextField() # Адрес доставки.
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) # Общая сумма заказа.
    status = models.CharField(max_length=20, default='New') # Статус заказа.
    created_at = models.DateTimeField(auto_now_add=True) # Дата создания заказа.

    def __str__(self):
        return f"Order #{self.id}"  # Возвращает строку с номером заказа


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) # Связь с Order.
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Связь с Product.
    quantity = models.IntegerField() # Количество товара в заказе.
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена товара на момент заказа.

    def __str__(self):
        return f"{self.product.name} in Order #{self.order.id}"  # Возвращает строку c именем товара в заказе
