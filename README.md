# 🛫 PulseNotify — Flight Price Monitor & Alert System

> **Airtribe EventHub Project 4**
> A Django-based backend application that monitors flight prices and sends real-time alerts when prices drop, powered by PostgreSQL, Redis, and Celery.

---

## 📑 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Settings Architecture](#-settings-architecture)
- [Docker Services](#-docker-services)
- [Running the Server](#-running-the-server)
- [API & Authentication](#-api--authentication)
- [Key Design Decisions](#-key-design-decisions)
- [Changelog](#-changelog)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Django 5.2 |
| **REST API** | Django REST Framework 3.17 |
| **Authentication** | SimpleJWT (JSON Web Tokens) |
| **Database** | PostgreSQL 16 (via Docker) |
| **Cache / Rate Limiting** | Redis 7 (via Docker) |
| **DB Adapter** | psycopg2-binary |
| **Env Management** | django-environ |
| **Containerization** | Docker Compose |

---

## 📁 Project Structure

```
airtribe_eventhub_project_4/
├── config/                     # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                 # ASGI entry point (settings → config.settings.local)
│   ├── wsgi.py                 # WSGI entry point (settings → config.settings.local)
│   ├── urls.py                 # Root URL configuration
│   └── settings/               # Split settings (environment-aware)
│       ├── __init__.py
│       ├── base.py             # Shared settings (DB, apps, middleware, env loading)
│       ├── local.py            # Development overrides (DEBUG=True)
│       └── production.py       # Production overrides (DEBUG=False)
│
├── pulse/                      # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
│
├── docker-compose.yml          # PostgreSQL 16 + Redis 7 containers
├── manage.py                   # Django management CLI (uses config.settings.local)
├── requirements.txt            # Python dependencies (pip freeze)
├── .env                        # Environment variables (git-ignored)
├── .gitignore                  # Git exclusions
├── Interview_Questions.md      # Interview prep Q&A
└── README.md                   # ← You are here
```

---

## ✅ Prerequisites

- **Python** 3.10+
- **Docker Desktop** (for PostgreSQL & Redis containers)
- **pip** (Python package manager)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/IonMors/Airtribe_EventHub_Project_4.git
cd Airtribe_EventHub_Project_4
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file in the **project root** with the following variables:

```env
SECRET_KEY='your-django-secret-key-here'
DEBUG=True

POSTGRES_DB=pulsenotify
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5434

REDIS_HOST=localhost
REDIS_PORT=6379

DJANGO_SETTINGS_MODULE=config.settings.local
```

> **Note:** The `.env` file is git-ignored for security. Each developer must create their own.

### 5. Start Docker services

```bash
docker-compose up -d
```

This spins up:
- **PostgreSQL 16** on port `5434` (mapped to container's internal `5432`)
- **Redis 7** on port `6379`

### 6. Run database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Environment Variables

All secrets and environment-specific values are managed via `django-environ` and loaded from a `.env` file at the project root.

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | *(required)* |
| `DEBUG` | Debug mode toggle | `True` |
| `POSTGRES_DB` | Database name | `pulsenotify` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5434` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `DJANGO_SETTINGS_MODULE` | Active settings module | `config.settings.local` |

---

## ⚙ Settings Architecture

The original monolithic `settings.py` has been **split into environment-specific modules** following Django best practices:

```
config/settings/
├── __init__.py          # Makes this a Python package
├── base.py              # Shared settings (all environments)
├── local.py             # Development: inherits base + DEBUG=True
└── production.py        # Production:  inherits base + DEBUG=False
```

### How it works

- **`base.py`** contains all shared configuration: installed apps, middleware, database connections (PostgreSQL), templates, password validators, i18n, and static files. It reads secrets from the `.env` file using `django-environ`.
- **`local.py`** imports everything from `base.py` and sets `DEBUG = True`.
- **`production.py`** imports everything from `base.py` and sets `DEBUG = False`.
- **`manage.py`**, **`wsgi.py`**, and **`asgi.py`** all default to `config.settings.local`.

### Switching environments

```bash
# Development (default)
DJANGO_SETTINGS_MODULE=config.settings.local python manage.py runserver

# Production
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py runserver
```

---

## 🐳 Docker Services

The `docker-compose.yml` provisions two infrastructure services:

### PostgreSQL 16

| Property | Value |
|---|---|
| Image | `postgres:16` |
| Container name | `pulsenotify_postgres` |
| Host port | `5434` |
| Internal port | `5432` |
| Database | `pulsenotify` |
| User / Password | `postgres` / `postgres` |
| Persistent volume | `postgres_data` |

> **Port note:** Host port is `5434` (not the default `5432`) to avoid conflicts with any locally installed PostgreSQL instance.

### Redis 7

| Property | Value |
|---|---|
| Image | `redis:7-alpine` |
| Container name | `pulsenotify_redis` |
| Host port | `6379` |

### Useful commands

```bash
# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker logs pulsenotify_postgres
docker logs pulsenotify_redis

# Connect to PostgreSQL inside the container
docker exec -it pulsenotify_postgres psql -U postgres -d pulsenotify
```

---

## 🏃 Running the Server

```bash
# Make sure Docker services are running
docker-compose up -d

# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```

---

## 🔑 API & Authentication

| Package | Purpose |
|---|---|
| `djangorestframework` | REST API framework for serializers, viewsets, and routers |
| `djangorestframework-simplejwt` | JWT-based authentication (access + refresh tokens) |

Registered in `INSTALLED_APPS`:
- `rest_framework`
- `rest_framework_simplejwt`

---

## 💡 Key Design Decisions

| Decision | Rationale |
|---|---|
| **PostgreSQL over SQLite** | Production-grade: concurrent users, advanced indexing, transactions, and scalability |
| **Redis** | In-memory cache for flight prices and rate limiting to prevent API abuse |
| **Split settings** | Isolates dev/prod configs; prevents deploying debug mode to production |
| **Environment variables** | Keeps secrets out of source code; 12-factor app compliant |
| **`psycopg2-binary`** | PostgreSQL adapter enabling Django ↔ PostgreSQL communication |
| **Docker Compose** | Reproducible infrastructure; one command to spin up all services |
| **Port 5434** | Avoids conflict with locally installed PostgreSQL on the default 5432 |

---

## 📝 Changelog

### June 2026

- **Settings refactor** — Split monolithic `settings.py` into `base.py`, `local.py`, and `production.py` under `config/settings/`
- **Docker infrastructure** — Added `docker-compose.yml` with PostgreSQL 16 and Redis 7 containers
- **Environment management** — Added `django-environ` for `.env`-based configuration; all secrets externalized
- **Database migration** — Switched from SQLite to PostgreSQL via Docker container
- **Authentication** — Integrated `djangorestframework-simplejwt` for JWT auth
- **Port conflict resolution** — Changed Postgres host port to `5434` to avoid collision with local Windows Postgres
- **Updated `manage.py`, `wsgi.py`, `asgi.py`** — All entry points now reference `config.settings.local`
- **Updated `.gitignore`** — Added rules for `.env`, `db.sqlite3`, and local draft files
- **Interview Q&A** — Added `Interview_Questions.md` with 13 system design & architecture questions
- **GitHub mirror** — Pushed repository to [GitHub](https://github.com/IonMors/Airtribe_EventHub_Project_4.git)

---

## 📄 License

This project is part of the Airtribe curriculum.
