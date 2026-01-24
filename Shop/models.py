# models.py: Описывает структуру базы данных.
from django.db import models # Импорт модуля для работы с моделями Django.
from django.contrib.auth.models import User # Импорт модели User для связи с пользователями.
from django.utils.text import slugify # Импорт функции slugify для создания slug по названию.
from django.conf import settings

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
