<div align="center">

# Система управления персоналом  
**Современный REST API для управления сотрудниками, отделами и командами**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)


</div>

## Возможности

- Регистрация и авторизация пользователей с **access + refresh токенами**
- Разделение ролей (администратор / обычный пользователь)
- Управление сотрудниками (регистрация, статус, привязка к команде)
- Создание и просмотр отделов и команд (только для админов)
- Получение информации о себе (пользователь / сотрудник)
- Миграции базы данных через Alembic

## 🏗️ Технологии

| Технология       | Назначение                          |
|------------------|-------------------------------------|
| FastAPI          | Основной веб-фреймворк              |
| SQLAlchemy 2.0   | ORM + async поддержка               |
| PostgreSQL       | База данных                         |
| Alembic          | Миграции схемы                      |
| Pydantic         | Валидация и сериализация            |
| Uvicorn          | ASGI-сервер                         |
| Docker           | Контейнеризация                     |

## 📋 Основные эндпоинты

### Аутентификация и пользователи

| Метод   | Путь                        | Описание                              | Кто может |
|---------|-----------------------------|---------------------------------------|-----------|
| `POST`  | `/api/v1/users`             | Регистрация (автоматически is_admin=True) | Все       |
| `GET`   | `/api/v1/users/me`          | Информация о текущем пользователе     | Авторизованный |
| `POST`  | `/api/v1/auth/token`        | Получение access + refresh токенов    | Все       |
| `POST`  | `/api/v1/auth/refresh`      | Обновление токенов                    | С refresh |
| `DELETE`| `/api/v1/auth/logout`       | Удаление текущего токена               | Авторизованный |

### Сотрудники

| Метод   | Путь                                      | Описание                              | Кто может |
|---------|-------------------------------------------|---------------------------------------|-----------|
| `POST`  | `/api/v1/employees`                       | Регистрация сотрудника                | Все |
| `GET`   | `/api/v1/employees/me`                    | Данные текущего сотрудника            | Авторизованный |
| `GET`   | `/api/v1/employees`                       | Список всех сотрудников               | Админ     |
| `POST`  | `/api/v1/employees/{id}/status`           | Изменить статус сотрудника            | Админ     |
| `POST`  | `/api/v1/employees/{id}/team/{team_id}`   | Привязать сотрудника к команде        | Админ     |

### Отделы и команды (только админы)

| Метод   | Путь                        | Описание                  |
|---------|-----------------------------|---------------------------|
| `POST`  | `/api/v1/departments`       | Создать отдел             |
| `GET`   | `/api/v1/departments`       | Получить все отделы       |
| `POST`  | `/api/v1/teams`             | Создать команду           |
| `GET`   | `/api/v1/teams`             | Получить все команды      |

Полная интерактивная документация доступна по адресу:  
→ http://localhost:8000/docs (Swagger UI)  

## 🚀 Быстрый старт

### Вариант 1 — Через Docker

```bash
git clone https://github.com/MaksimCpp/PersonnelManagement.git
cd PersonnelManagement

# Копируем и настраиваем конфиги
cp config/.env.example config/.env
cp config/config.yaml.example config/config.yaml

# Откройте и заполните .env и config.yaml !

docker compose up --build
```

### Вариант 2 — Без Docker

```bash
git clone https://github.com/MaksimCpp/PersonnelManagement.git
cd PersonnelManagement

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

cd src

cp ../config/.env.example ../config/.env
cp ../config/config.yaml.example ../config/config.yaml

# Заполните .env и config.yaml

alembic -c ../alembic.ini upgrade head

python3 app.py
```

Готово! Открывайте → http://localhost:8000/docs
