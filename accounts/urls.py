from django.urls import path
from . import views

app_name = 'accounts'  # пространство имён (важно для {% url %} в шаблонах)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
