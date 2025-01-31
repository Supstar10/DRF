# Используем официальный образ Python в качестве базового образа
FROM python:3

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install -r /app/requirements.txt --no-cache-dir

# Копируем весь проект в рабочую директорию
COPY . /app

# Запускаем миграции и сервер Django
CMD ["sh", "-c"]