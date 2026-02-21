from django.urls import path, include
from . import views
from .views import RegisterView
from django.contrib import admin

urlpatterns = [

    Главная страница
    path('', views.home_view, name='home'),  # корневой URL ведёт на домашнюю страницу

    path('products/', views.product_list, name='product_list'),

    path('admin/', admin.site.urls),

    Страница входа
    path('login/', views.login_view, name='login'),

    path('accounts/', include('accounts.urls')),  # подключение

    path('', include('shop.urls')),  # подключаем URL-паттерны из приложения "shop"

    тестовая страница
    path('my_view/', views.my_view, name='my_view'),

    path('register/', RegisterView.as_view(), name='register'),

    path('cart/', include('cart.urls', namespace='cart')),

    path('', include('cart.urls')),
]
