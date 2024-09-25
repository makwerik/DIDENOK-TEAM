from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PasswordViewSet

# Создаем объект маршрутизатора
router = DefaultRouter()

# Регистрируем ViewSet для паролей по префиксу 'password'.
router.register(r'password', PasswordViewSet, basename='password')

urlpatterns = [
    # Включаем все маршруты, зарегистрированные в маршрутизаторе.
    path('', include(router.urls)),
]