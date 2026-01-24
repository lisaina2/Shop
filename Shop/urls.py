from django.urls import path, include
from . import views

urlpatterns = [

    # 1. Главная страница
    path('', views.home_view, name='home'),  # корневой URL ведёт на домашнюю страницу

    path('', views.product_list, name='product_list'),

    # 2. Страница входа
    path('login/', views.login_view, name='login'),

    # 3. Ваша тестовая страница
    path('my_view/', views.my_view, name='my_view'),

    path('register/', RegisterView.as_view(), name='register'),

    path('', include('cart.urls')),
]