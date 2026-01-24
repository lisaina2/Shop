from .models import Order, OrderItem
from django.contrib import admin
from .models import Category, Product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    raw_id_fields = ('order', 'product')  # для удобной выборки
