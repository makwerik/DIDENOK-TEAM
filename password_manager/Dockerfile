# Указываем базовый образ Python
FROM python:3.11.4

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Открываем порт для доступа к серверу Django
EXPOSE 8000

# Выполняем миграции и запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
