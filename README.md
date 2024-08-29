# Проект "Управління Чеками"

Цей проект дозволяє керувати чеками через API, побудоване за допомогою FastAPI.

## Встановлення

1. Клонувати репозиторій:
    ```sh
    git clone https://github.com/klaksik/management_receipts
    ```

2. Перейти до папки проекту:
    ```sh
    cd management_receipts
    ```

3. Створити та активувати віртуальне середовище:
    ```sh
    python -m venv venv
    source venv/bin/activate # Для Windows використовуйте venv\Scripts\activate
    ```

4. Встановити залежності:
    ```sh
    pip install -r requirements.txt
    ```

## Запуск застосунку

1. Вказати параметри бази данних в файлі:
    ```sh
    src/database.py
    ```
2. Вказати основні параметри в файлі :
    ```sh
    src/config.py
    ```

2. Запустити застосунок:
    ```sh
    uvicorn src.main:app
    ```

## Тестування

1. Встановіть pytest:
    ```sh
    pip install pytest
    ```

2. Запустіть тести:
    ```sh
    pytest
    ```

## Використання

### Авторизація

- Реєстрація нового користувача та отримання токена:
    ```
    POST /auth/register
    {
        "name": "VSEVOLOD melnyk",
        "username": "newuser",
        "password": "Test1234!"
    }
    ```
  
- Логін користувача та отримання токена:
    ```
    POST /auth/login
    {
        "username": "newuser",
        "password": "Test1234!"
    }
    ```

### Чеки

- Створення нового чеку:
    ```
    POST /receipts/create_receipt (Потребує авторизації)
    {
        "products": [
            {
                "name": "Product1",
                "price": 100.0,
                "quantity": 2
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 500.0
        }
    }
    ```

- Перегляд чеків:
    ```
    GET /receipts/view_receipts (Потребує авторизації)
    ```

- Перегляд чеку за ID:
    ```
    GET /receipts/view_receipts/{receipt_id} (Потребує авторизації)
    ```

- Перегляд чеку клієнта за ID:
    ```
    GET /receipts/customer_receipts/{receipt_id}
    ```

## Структура Проекту

- `src/main.py`: Основний файл для запуску API.
- `src/database.py`: Конфігурація бази даних та створення таблиць.
- `src/auth`: Директрорія для модулів, пов'язаних з авторизацією користувачів (моделі, схеми, маршрути).
- `src/receipts`: Директрорія для модулів, пов'язаних з чеками (моделі, схеми, маршрути, сервіси).
- `tests`: Тести для проєкту.

## Залежності

- `FastAPI`
- `SQLAlchemy`
- `Asyncpg`
- `Pydantic`
- `HTTPX`
- `Pytest`
- `aiobcrypt`
- `PyJWT`
- `starlette`

## Автор

https://www.linkedin.com/in/melnyk-vsevolod/