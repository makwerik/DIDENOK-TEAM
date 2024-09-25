from django.db import models

# Fernet из библиотеки cryptography для шифрования и дешифрования данных.
from cryptography.fernet import Fernet

encryption_key = b'bugqBG7mcs0dmMsLaBkz0WIHQO2K2J65pq9Odft6GTU='


class Password(models.Model):
    """Модель для паролей"""
    service_name = models.CharField(max_length=300, unique=True)  # Хранение имени сервера
    encrypted_password = models.TextField()  # Хранение зашифрованного пароля

    def set_password(self, password, key):
        """
            Метод для шифрования и установки пароля
            password: str,
            key: bytes
        """
        #  Объект для шифрования с использованием ключа
        cipher_suite = Fernet(key)

        # Шифруем пароль и сохраняем его в зашифрованном виде.
        self.encrypted_password = cipher_suite.encrypt(password.encode('utf-8')).decode('utf-8')

    def get_password(self, key):
        """
            Метод для дешифрования и получения пароля
            key: bytes
        """
        # Объект для дешеврования с использованием ключа
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(self.encrypted_password.encode('utf-8')).decode('utf-8')

    def __str__(self):
        return self.service_name
