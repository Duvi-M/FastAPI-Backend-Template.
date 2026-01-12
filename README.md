# 🚀 FastAPI Backend Template (Async, JWT, Docker, Alembic)

A production-ready **FastAPI backend template** built with real-world backend engineering practices.

This project demonstrates how to design, build, and run a modern backend API using **FastAPI**, **async SQLAlchemy**, **JWT authentication**, **Docker**, and **Alembic migrations**, with a clean architecture and clear separation of concerns.

---

## Features

- ⚡ **FastAPI** (async-first)
- 🔐 **JWT authentication** (access + refresh tokens)
- 👥 **Role-based access control** (`admin`, `user`)
- 🧩 **Clean architecture** (routers / services / repositories)
- 🗄️ **PostgreSQL** with **SQLAlchemy Async**
- 🔄 **Alembic migrations**
- 🐳 **Docker Compose** for local development
- 🔑 **Secure password hashing (Argon2)**
- 🧪 **Test-ready structure**
- 🤖 **CI-ready** (linting + tests)
- 🌱 **Seed script** for initial admin user

---

## 📂 Project Structure

```text
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   └── tasks.py
│   │       └── router.py
│   ├── core/
│   │   ├── config.py        # Settings / env vars
│   │   └── security.py      # JWT + password hashing
│   ├── db/
│   │   ├── base.py          # SQLAlchemy Base
│   │   └── session.py       # Async DB session
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── repositories/        # DB access layer
│   ├── services/            # Business logic
│   ├── schemas/             # Pydantic schemas
│   └── main.py              # FastAPI app entrypoint
│
├── alembic/
│   ├── versions/            # Migration files
│   ├── env.py
│   └── script.py.mako
│
├── scripts/
│   └── seed_admin.py        # Create initial admin
│
├── tests/                   # Test suite (pytest)
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
``` 

## 🧠 Architecture Overview

This project follows a **layered architecture** commonly used in production-grade backend systems.  
Each layer has a single responsibility and clear boundaries, which makes the codebase easier to understand, test, and scale.

---

### API Layer (Routers)

**Location:** `app/api/v1/endpoints/`

Responsibilities:
- Handle HTTP requests and responses
- Define REST endpoints
- Validate request payloads using Pydantic schemas
- Extract authentication context (current user)
- Delegate all business logic to the service layer

Key principle:
> Routers contain **no business logic**.

---

### Schemas (Pydantic)

**Location:** `app/schemas/`

Responsibilities:
- Define request and response contracts
- Perform data validation and serialization
- Enforce input constraints before data reaches the business layer

Benefits:
- Prevent invalid data from entering the system
- Provide automatic OpenAPI documentation
- Act as a strict boundary between API and domain logic

---

### Services (Business Logic)

**Location:** `app/services/`

Responsibilities:
- Implement business rules
- Authentication and authorization logic
- Role-based access control (admin vs user)
- Ownership checks (e.g. users can only access their own tasks)
- Coordinate repository calls

Key principle:
> Services orchestrate behavior but do not know about HTTP or database internals.

---

### Repositories (Data Access Layer)

**Location:** `app/repositories/`

Responsibilities:
- Encapsulate all database operations
- Perform CRUD operations using SQLAlchemy
- Hide persistence details from services

Benefits:
- Easy to test using mocks
- Easy to replace or refactor database logic
- No business rules inside repositories

---

### Models (SQLAlchemy)

**Location:** `app/models/`

Responsibilities:
- Define database schema using SQLAlchemy ORM
- Represent persisted entities (User, Task, etc.)
- Serve as the source of truth for Alembic migrations

Used by:
- SQLAlchemy Async
- Alembic autogeneration

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fastapi-backend-template.git
cd fastapi-backend-template
```
## 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
## 3.Install Dependencies
```bash
python -m pip install -U pip
pip install -r requirements-dev.txt
```
### 🐳 Database (Docker)

Start PostgreSQL:
```bash
docker compose up -d db
docker compose ps
```
The database is exposed locally, for example:
localhost:5439

### Environment Variables

Create a .env file from the example:
```bash
cp .env.example .env
```
Example .env:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5439/app
JWT_SECRET_KEY=dev-secret
```
### Database Migrations (Alembic)

Check current migration state:
```bash
python -m alembic current
```
Generate migrations:
```bash
python -m alembic revision --autogenerate -m "init tables"
```
Apply migrations:
```bash
python -m alembic upgrade head
```

### Seed Initial Admin User

Create an admin user for the first login:
```bash
python -m scripts.seed_admin
```

Default credentials:

- Email: admin@local.com
- Password: admin123456

### Run the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The API will be available at:
```bash
http://localhost:8001
```

### Authentication Flow
Login (Admin)
```bash
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@local.com&password=admin123456"
```

Response example:
```bash
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

Save the access token:
```bash
TOKEN="PASTE_ACCESS_TOKEN"
```

### User Management (Admin Only)
Create User
```bash
curl -X POST "http://localhost:8001/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user1@local.com",
    "password": "user123456",
    "role": "user"
  }'
```

### Tasks (Authenticated Users)
Login as User
```bash
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user1@local.com&password=user123456"
```
Save the user token:
```bash
USER_TOKEN="PASTE_USER_ACCESS_TOKEN"
```

Create Task
```bash
curl -X POST "http://localhost:8001/api/v1/tasks/" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My first task"}'
```

List My Tasks
```bash
curl -X GET "http://localhost:8001/api/v1/tasks/" \
  -H "Authorization: Bearer $USER_TOKEN"
```
# Testing

Tests are written using pytest and pytest-asyncio.
```bash
Run tests:
```
Recommended coverage:

- Authentication success and failure
- Protected endpoints
- Ownership and permission checks

### Code Quality

Run linters and type checks:
```bash
ruff check 
mypy app/
```

### Future Improvements

- Refresh token rotation
- Pagination utilities
- Rate limiting
- Health check endpoint
- Background tasks
- Coverage reporting in CI

### Purpose of This Project

- This repository is designed to:
- Serve as a real FastAPI backend template
- Demonstrate production-level backend engineering skills
- Be easily extensible for real-world applications
- Act as a portfolio project for backend engineers
