# Система управления персоналом
## Авторы
- @MaksimCpp
## Цель
- Реализовать систему, которая поможет компании управлять персоналом.
## Стек технологий
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
## Авторизация и аутентификация
- Авторизация и аутентификация реализована с использованием rerfresh и access токенов
- access token предназначен для доступа к защищенным ресурсам
- rerfresh token предназначен для обновления пары rerfresh и access токенов
- ```POST /api/v1/users``` - регистрация пользователя с автоматическим присвоением ```is_admin = true```
- ```GET /api/v1/users/me``` - получение данных о текущем пользователе
- ```POST /api/v1/auth/token``` - получение пары rerfresh и access токенов и время их жизни
- ```POST /api/v1/auth/refresh``` - обновление пары rerfresh и access токенов
- ```DELETE /api/v1/auth/logout``` - удаление текущей пары токенов
- ```POST /api/v1/employees``` - регистрация сотрудника
- ```GET /api/v1/employees/me``` - получение данных о текущем сотруднике
## Эндпоинты, предназначенные для использования админами
- ```POST /api/v1/departments``` - создение отдела
- ```GET /api/v1/departments``` - получение отделов
- ```POST /api/v1/teams``` - создание команды
- ```GET /api/v1/teams``` - получение команд
- ```GET /api/v1/employees``` - регистрация сотрудника
- ```POST /api/v1/employees/{employee_id}/status``` - обновление статуса сотрудника
- ```POST /api/v1/employees/{employee_id}/team/{team_id}``` - привязать сотрудника к команде
## Инструкция по запуску без Docker
- Клонировать репозиторий ```git clone https://github.com/MaksimCpp/PersonnelManagement.git```
- Создать виртуальное окружение ```python3 -m venv venv```
- Активировать виртуальное окружение ```source venv/bin/activate```
- Скачать зависимости ```pip3 install -r requirements.txt```
- Перейти в каталог src ```cd src```
- Создать файлы config.yaml и .env ```cp config/config.yaml.example config/config.yaml && cp config/.env.example config/.env```
- Заполнить данные в файлах ```config.yaml``` и ```.env```
- Применить миграции ```alembic -c ../alembic.ini upgrade head```
- Запустить приложение ```python3 app.py```
- Перейти на ```http://localhost:8000/docs``` и пользоваться фичами
## Инструкция по запуску через Docker
- Клонировать репозиторий ```git clone https://github.com/MaksimCpp/PersonnelManagement.git```
- Перейти в каталог src ```cd src```
- Создать файлы config.yaml и .env ```cp config/config.yaml.example config/config.yaml && cp config/.env.example config/.env```
- Заполнить данные в файлах ```config.yaml``` и ```.env```
- Запустить приложение ```docker compose -f ../docker-compose.yaml up --build```
- Перейти на ```http://localhost:8000/docs``` и пользоваться фичами
