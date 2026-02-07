from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail/', views.cart_detail, name='detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]

