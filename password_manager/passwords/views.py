from rest_framework import status, viewsets
from rest_framework.response import Response

# Импортируем декоратор action для создания дополнительных методов.
from rest_framework.decorators import action

from .models import Password
from .serializers import PasswordSerializer

# Импортируем Fernet для шифрования и дешифрования.
from cryptography.fernet import Fernet

# Генерируем ключ для шифрования и дешифрования.
encryption_key = b'bugqBG7mcs0dmMsLaBkz0WIHQO2K2J65pq9Odft6GTU='


class PasswordViewSet(viewsets.ViewSet):
    """Класс для обработки запросов, связанных с паролями"""

    def create(self, request):
        """Метод для обработки POST запросов на создание или обновления пароля"""

        password = request.data.get('password')
        service_name = request.data.get('service_name')

        if not password:
            return Response({"error": "Пароль не передан"}, status=status.HTTP_400_BAD_REQUEST)
        if not service_name:
            return Response({"error": "Имя сервиса не передано"}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем или создаем запись с указанным именем сервиса.
        password_instance, created = Password.objects.get_or_create(service_name=service_name)
        # Шифруем и сохраняем пароль
        password_instance.set_password(password, encryption_key)
        # Сохраняем в БД
        password_instance.save()

        return Response({"status": "Пароль успешно создан/обновлён"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='get-password')
    def get_password(self, request):
        """
        Метод для обработки GET запросов на получение пароля по имени сервиса.
        """
        service_name = request.query_params.get('service_name')

        if not service_name:
            return Response({"error": "Имя сервиса не передано"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            password_instance = Password.objects.get(service_name=service_name)
            # Дешифруем пароль
            decrypted_password = password_instance.get_password(encryption_key)
            return Response({"service_name": service_name, "password": decrypted_password}, status=status.HTTP_200_OK)
        except Password.DoesNotExist:
            return Response({"error": "Сервис не найден"}, status=status.HTTP_404_NOT_FOUND)

    # Создаем дополнительный метод для поиска паролей.
    @action(detail=False, methods=['get'], url_path='search/(?P<query>[^/.]+)')
    def search(self, request, query=None):
        """Метод для обработки запросов GET на поиск по части имени сервиса."""

        # Ищем все записи, в которых имя сервиса содержит указанный запрос.
        passwords = Password.objects.filter(service_name__icontains=query)
        serializer = PasswordSerializer(passwords, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='cript')
    def cript(self, request):
        service_name = request.query_params.get('service_name')

        if not service_name:
            return Response({"error": "Имя сервиса не передано"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service = Password.objects.get(service_name=service_name)
            return Response({"service_name": service_name, "password": service.encrypted_password},
                            status=status.HTTP_200_OK)
        except Password.DoesNotExist:
            return Response({"error": "Запись с таким именем сервиса не найдена"}, status=status.HTTP_404_NOT_FOUND)
