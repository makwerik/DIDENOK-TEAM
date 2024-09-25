# Password Manager API


## Функционал

- **Создание и обновление паролей:** Создание или обновление зашифрованного пароля для указанного сервиса.
- **Получение пароля:** Получение расшифрованного пароля по имени сервиса. (Это от себя просто сделал)
- **Поиск паролей:** Поиск паролей по части имени сервиса.
- **Получение зашифрованного пароля:** Получение зашифрованного пароля по имени сервиса.

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Склонируйте репозиторий
```bash
   git clone https://github.com/makwerik/DIDENOK-TEAM.git
   cd password_manager
````
2. Постройте и запустите контейнеры с помощью Docker Compose:
````bash
docker-compose up --build
````
3. Выполните миграции и создайте суперпользователя (по умолчанию должен быть makwerik:makwerik):
````bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
````

4. Откройте браузер и перейдите по ссылке [http://localhost:8000/admin](http://localhost:8000/admin), чтобы войти в административную панель.


````
Запрос: POST /api/password/
{
    "service_name": "example_service",
    "password": "example_password"
}

Ответ:
{
    "status": "Пароль успешно создан/обновлён"
}
````

````
Запрос: GET /api/password/get-password/?service_name=example_service
Ответ:
{
    "service_name": "example_service",
    "password": "gAAAAABh..."
}
````


````
Запрос: GET /api/password/search/serv/
Ответ:
[
    {
        "id": 1,
        "service_name": "example_service_1",
        "encrypted_password": "..."
    },
    {
        "id": 2,
        "service_name": "example_service_2",
        "encrypted_password": "..."
    }
]
````


````
Запрос: GET /api/password/cript/?service_name=example_service

Ответ:
{
    "service_name": "example_service",
    "password": "example_password"
}

````

Для запуска тестов:
**docker-compose run web pytest**