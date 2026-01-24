"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('form/', views.handle_form_submission, name='form_submission'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('profile/', views.profile, name='profile'),

    path('success/', views.success_view, name='success_url'),

    path('admin/', admin.site.urls),

    path('', views.product_list, name='product_list'),

    path('my_view/', views.my_view, name='my_view'),

    path('orders/history/', views.order_history, name='order_history'),

    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_detail, name='cart_detail'),
]
