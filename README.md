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

## 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

## 3.Install Dependencies

python -m pip install -U pip
pip install -r requirements-dev.txt

### 🐳 Database (Docker)

Start PostgreSQL:
docker compose up -d db
docker compose ps

The database is exposed locally, for example:
localhost:5439

### Environment Variables

Create a .env file from the example:

cp .env.example .env

Example .env:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5439/app
JWT_SECRET_KEY=dev-secret

### Database Migrations (Alembic)

Check current migration state:

python -m alembic current

Generate migrations:

python -m alembic revision --autogenerate -m "init tables"

Apply migrations:

python -m alembic upgrade head



