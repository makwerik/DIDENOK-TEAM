import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Password
from cryptography.fernet import Fernet

# Задаем статический ключ для тестов, чтобы избежать ошибок дешифрования
encryption_key = b'bugqBG7mcs0dmMsLaBkz0WIHQO2K2J65pq9Odft6GTU='


@pytest.fixture()
def api_client():
    """Фикстура для создания api, который будет использоваться в тестах"""
    return APIClient()


@pytest.fixture()
def create_password():
    """Фикстура для создания объекта Password в БД для тестов"""

    def _create_password(service_name, password):
        # Создаём экземпляр Password, шифруем и устанавливаем пароль, сохраняем в БД
        password_instance = Password(service_name=service_name)
        password_instance.set_password(password, encryption_key)
        password_instance.save()
        return password_instance

    return _create_password


@pytest.mark.django_db
def test_create_password_success(api_client):
    """Тест для проверки создания пароля, сохранения в бд в зашифрованном виде"""

    # url для создания пароля
    url = reverse('password-list')
    data = {
        "service_name": "test_service",
        "password": "password"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['status'] == 'Пароль успешно создан/обновлён'
    # Проверяем, что запись с именем 'test_service' была создана в базе данных.
    password_instance = Password.objects.get(service_name='test_service')
    # Проверяем, что пароль хранится в зашифрованном виде.
    # Дешифруем пароль, используя тот же ключ, и проверяем, что он совпадает с исходным.
    decrypted_password = Fernet(encryption_key).decrypt(
        password_instance.encrypted_password.encode('utf-8')).decode('utf-8')
    assert decrypted_password == 'password'


@pytest.mark.django_db
def test_create_password_update_existing(api_client, create_password):
    """Тест для проверки обновления существующего пароля"""
    # Используем фикстуру для создания начальной записи с именем и паролем
    create_password(service_name='test_service', password='initial_password')

    url = reverse('password-list')
    data = {
        "service_name": "test_service",
        "password": "update_password"
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    # Проверка, что пароль обновился
    password_instance = Password.objects.get(service_name='test_service')
    decrypted_password = Fernet(encryption_key).decrypt(
        password_instance.encrypted_password.encode('utf-8')).decode('utf-8')
    assert decrypted_password == 'update_password'


@pytest.mark.django_db
def test_get_password_success(api_client, create_password):
    """Тест для проверки получения пароля"""
    create_password(service_name='test_service', password='initial_password')
    url = reverse('password-get-password')
    response = api_client.get(url, data={"service_name": "test_service"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['service_name'] == "test_service"
    assert response.data['password'] == "initial_password"


@pytest.mark.django_db
def test_get_password_no_service_name(api_client):
    """Проверка, если передали не существующий сервис"""
    url = reverse('password-get-password')
    response = api_client.get(url, data={"service_name": "keklol"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == "Сервис не найден"


@pytest.mark.django_db
def test_search_passwords_success(api_client, create_password):
    """Тест для поиска паролей по части имени сервиса"""
    create_password(service_name='test_service_1', password='password1')
    create_password(service_name='test_service_2', password='password2')
    create_password(service_name='another_service', password='password3')

    url = reverse('password-search', args=['service'])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # Проверяем, что найдены 3 записи с 'service' в имени
    assert len(response.data) == 3


@pytest.mark.django_db
def test_search_passwords_success(api_client, create_password):
    """Тест для поиска паролей по части имени сервиса если они не найдены"""
    create_password(service_name='test_service_1', password='password1')
    create_password(service_name='test_service_2', password='password2')
    create_password(service_name='another_service', password='password3')

    url = reverse('password-search', args=['boss'])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_cript_success(api_client, create_password):
    """Тест для проверки успешного получения зашифрованного пароля по имени сервиса"""
    password_instance = create_password(service_name='test_service', password='test_password')

    url = reverse('password-cript')
    response = api_client.get(url, {'service_name': 'test_service'})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['service_name'] == 'test_service'
    assert response.data['password'] == password_instance.encrypted_password