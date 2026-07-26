# 1. Используем официальный легковесный образ Python
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Устанавливаем системные зависимости (если понадобятся для сборки некоторых пакетов)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Копируем файл зависимостей отдельно (для кэширования слоев Docker)
COPY requirements.txt .

# 5. Обновляем pip и устанавливаем зависимости проекта
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь исходный код проекта в контейнер
COPY . .

# 7. Добавляем корневую директорию в PYTHONPATH, чтобы Python видел модуль 'src'
ENV PYTHONPATH=/app

# 8. Команда по умолчанию для запуска тестов при старте контейнера
CMD ["pytest", "-v", "--alluredir=allure-results"]
