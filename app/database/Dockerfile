# Використовуємо офіційний Python-образ
FROM python:3.11

# Встановлюємо оновлення та ODBC Driver 18 для SQL Server
FROM python:3.11

# Оновлення пакетів і встановлення необхідних залежностей
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg \
    unixodbc \
    unixodbc-dev

# Видалення конфліктуючих пакетів
RUN apt-get remove -y unixodbc unixodbc-dev libodbc2 libodbccr2 libodbcinst2 unixodbc-common \
    && apt-get autoremove -y

# Додавання репозиторіїв для драйвера Microsoft SQL
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Оновлення ODBC перед встановленням драйвера
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev

# Встановлення драйвера ODBC для SQL Server
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Створюємо папку для додатку
WORKDIR /app

# Копіюємо файли
COPY . .

# Встановлюємо залежності (FastAPI, pyodbc тощо)
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт 8000 для FastAPI
EXPOSE 8000

# Запускаємо додаток
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

