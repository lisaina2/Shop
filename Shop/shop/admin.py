from django.contrib import admin
from .models import Category, Product, CartItem, Order  # Импортируем созданные модели

# Регистрируем модели
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)

