FROM python:3.10-slim

# установка системных зависимостей + клиента psql
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# рабочая директория
WORKDIR /code

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# код проекта
COPY . .

# команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]