# Business Management System (BMS)

**Business Management System** — система управления бизнес-процессами для команд и компаний.  
Она позволяет управлять пользователями, командами, задачами, встречами и оценкой работы сотрудников.  

Система построена на **FastAPI**, использует **PostgreSQL** для хранения данных и поддерживает JWT-аутентификацию.

---

## 📌 Основной функционал

### Пользователи
- Регистрация с email и паролем  
- Авторизация / выход (JWT)
- Обновление профиля  
- Удаление аккаунта (без восстановления)  
- Привязка к команде по коду (опционально)  
- Роли:

**user** (обычный пользователь) — может создать команду и стать admin; 
может стать частью команды в роли employee (сотрудник)

**employee** (член команды) — может выполнять задачи, просматривать встречи

**manager** (менеджер команды) — может назначать встречи и задачи сотрудникам; 
оценивает выполненные задачи

**admin** (администратор команды) — управляет командой и ролями

**superadmin** — имеет доступ к панели sqladmin, управление всеми данными

### Команды (Компании)
- Администратор создаёт команду  
- Добавление / удаление пользователей в команде  
- Просмотр состава команды  
- Назначение ролей (менеджер / сотрудник)  

### Задачи
- Создание задач руководителем  
- Назначение исполнителя  
- Описание, дедлайн, статус  
- Изменение / удаление задач  
- Комментарии внутри задачи  
- Статусы: **open** (открыто), **in_progress** (в работе), **done** (выполнено) 

### Оценка задачи
- Руководитель оценивает выполненные задачи (баллы 1–5)  
- Сотрудник видит свои оценки  
- Руководитель видит оценки, которые он поставил
- Вывод средней оценки за период  

### Встречи и Календарь
- Назначение встречи: дата, время, участники  
- Проверка времени на пересечение с другими событиями  
- Просмотр списка встреч пользователя  
- Отмена встречи  
- Календарь задач и встреч: дневной и месячный вид

### Панель администратора
- Используется [sqladmin](https://sqladmin.github.io/)  
- Просмотр и редактирование всех моделей  
- Фильтрация, поиск, сортировка  
- Скрипт в терминале `python -m src.admin.create_superadmin` для создания супер-админа  

### API
- REST API
- Автоматическая OpenAPI документация ([http://localhost:8000/docs](http://localhost:8000/docs) при локальном запуске сервера).
- Асинхронная работа с базой данных

---

## 🧱 Технологический стек

- **Python 3.13**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (async)**
- **Alembic** (миграции базы данных)
- **Docker / Docker Compose**
- **SQLAdmin**
- **JWT (python-jose)**
- **Argon2** (хеширование паролей)

---

## ⚙ Установка и запуск

Клонируйте репозиторий и создайте файл окружения:

```bash
git clone <URL_репозитория>
cd Business_Management_System
cp .env .env
```

Пример .env:

```.env
DB_NAME=business_management_system
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

JWT_SECRET_KEY=c350ea966f6e3b3608458e1a4d20d796

MODE=PROD
```

### 🐳 Через Docker (рекомендованный способ)

Собрать и запустить контейнеры:

```bash
docker compose up --build
```

Перед первым использованием необходимо создать таблицы в базе данных.

```bash
docker compose exec backend alembic upgrade head
или
docker compose run --rm backend alembic upgrade head
```

Для доступа в панель администратора необходимо создать superadmin.

```bash
docker compose exec backend python -m src.admin.create_superadmin
или
docker compose run --rm backend python -m src.admin.create_superadmin
```

При последующих запусках использовать:

```bash
docker compose up
```

### 🐍 Локально без Docker

Создать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Установить зависимости:
```bash
pip install -r requirements.txt
```

Cоздать таблицы в базе данных.

```bash
alembic upgrade head
```

Для доступа в панель администратора необходимо создать superadmin.

```bash
python -m src.admin.create_superadmin
```

Запустить приложение:

```bash
uvicorn src.main:app --reload
```

## 📂 Структура проекта

```
Business_Management_System/
├── src/
│   ├── admin/
│   │   ├── views/
│   │   │   ├── evaluations.py
│   │   │   ├── meetings.py
│   │   │   ├── tasks.py
│   │   │   ├── teams.py
│   │   │   └── users.py
│   │   │   
│   │   ├── admin_app.py
│   │   ├── auth.py
│   │   └── create_admin.py
│   │
│   ├── api/
│   │   ├── core/
│   │   │   ├── dependencies.py
│   │   │   └── decorators.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── calendar.py
│   │   │   ├── evaluations.py
│   │   │   ├── meetings.py
│   │   │   ├── tasks.py
│   │   │   ├── teams.py
│   │   │   └── users.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── migrations/
│   │   ├── versions/
│   │   │   └── migration.py
│   │   │
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── models/
│   │   ├── evaluations.py
│   │   ├── meetings.py
│   │   ├── tasks.py
│   │   ├── teams.py
│   │   └── users.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── calendar.py
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── task.py
│   │   ├── meeting.py
│   │   └── evaluation.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── calendar_service.py
│   │   ├── user_service.py
│   │   ├── team_service.py
│   │   ├── task_service.py
│   │   ├── meeting_service.py
│   │   ├── evaluation_service.py
│   │   ├── exceptions.py
│   │   ├── jwt_manager.py
│   │   ├── security.py
│   │   └── utils.py
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── tests/ 
│   ├── evaluations/
│   │   ├── test_evaluation_routes.py
│   │   └── test_evaluation_service.py
│   │
│   ├── meetings/
│   │   ├── test_meeting_routes.py
│   │   └── test_meeting_service.py
│   │
│   ├── tasks/
│   │   ├── test_task_comments.py
│   │   ├── test_task_comments_routes.py
│   │   ├── test_task_routes.py
│   │   └── test_task_service.py
│   │
│   ├── teams/
│   │   ├── test_team_routes.py
│   │   └── test_team_service.py
│   │
│   ├── users/
│   │   ├── test_team_routes.py
│   │   └── test_team_service.py
│   │
│   └── conftest.py
│
├── .dockerignore
├── .env
├── .test.env
├── .gitignore
├── alembic.ini
├── pytest.ini
├── requirements.txt
```

## Примеры запросов

### Авторизация 

POST /auth/login

```json
{
  "email": "user@example.com",
  "full_name": "Пользователь",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "<jwt_token>",
  "refresh_token": "<jwt_token>",
  "token_type": "bearer"
}
```

### Создание команды

POST /teams

```json
{
  "name": "string"
}
```

Response:

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": "string",
  "created_at": "2026-01-14T08:45:43.148Z"
}
```

### Просмотр задач пользователя

GET /tasks

Response:

```json
[
  {
    "title": "task1",
    "description": "complete the task",
    "deadline": "2026-01-18",
    "id": 0,
    "status": "in_progress",
    "created_at": "2026-01-14T08:48:55.716Z",
    "updated_at": "2026-01-14T08:48:55.716Z",
    "creator_id": 0,
    "team_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  },
  {
    "title": "task2",
    "description": "complete the task",
    "deadline": None,
    "id": 1,
    "status": "open",
    "created_at": "2026-01-13T10:23:51.248Z",
    "updated_at": "2026-01-13T10:23:51.248Z",
    "creator_id": 0,
    "team_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
]
```
