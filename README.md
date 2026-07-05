# ✈️ PulseNotify - Flight Price Monitor & Alert System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Celery](https://img.shields.io/badge/Celery-5.x-brightgreen)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

---

## 📖 Overview

PulseNotify is a backend service that continuously monitors flight prices and automatically notifies users whenever a flight price falls below their desired threshold.

The project demonstrates:

- Django REST Framework
- JWT Authentication
- PostgreSQL
- Celery
- Celery Beat
- Redis
- Background Processing
- Docker Compose
- Backend-to-Backend API Communication

The system is inspired by flight price monitoring services like:

- Google Flights
- Skyscanner
- Hopper

---

# ✨ Features

- User Registration
- JWT Authentication
- Flight Price Alerts
- Background Price Monitoring
- Automatic Notifications
- Admin Analytics Dashboard
- Celery Worker
- Celery Beat Scheduler
- PostgreSQL Database
- Redis Message Broker
- Docker Support
- Unit Tests

---

# 🏗 Project Architecture

```text
                    +---------------------+
                    |     REST Client     |
                    |  Postman / Browser  |
                    +----------+----------+
                               |
                               |
                               v
                   +-----------------------+
                   | Django REST Framework |
                   +-----------+-----------+
                               |
         +---------------------+----------------------+
         |                                            |
         |                                            |
         v                                            v
+---------------------+                  +-----------------------+
| PostgreSQL Database |                  | Flight Price Endpoint |
+---------------------+                  +-----------+-----------+
                                                    |
                                                    |
                                                    v
                                           Random Flight Price

                               ^
                               |
                               |
                   +-----------+-----------+
                   |     Celery Worker     |
                   +-----------+-----------+
                               ^
                               |
                               |
                   +-----------+-----------+
                   |      Redis Broker     |
                   +-----------+-----------+
                               ^
                               |
                               |
                    +----------+----------+
                    |     Celery Beat     |
                    +---------------------+
```

---

# 🔄 System Workflow

```text
User Creates Alert
        │
        ▼
Price Alert Stored
        │
        ▼
Celery Beat (Every 60 Seconds)
        │
        ▼
check_prices()
        │
        ▼
GET /api/flights/price/
        │
        ▼
Compare Current Price
        │
        ├──────────────► Above Threshold
        │                     │
        │                     ▼
        │                Do Nothing
        │
        ▼
Below Threshold
        │
        ▼
send_notification.delay()
        │
        ▼
NotificationLog Created
        │
        ▼
Alert Status → TRIGGERED
```

---

# 📁 Project Structure

```text
pulsenotify/

│
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── .env
│
├── pulse/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
└── pulsenotify/
    ├── celery.py
    ├── urls.py
    ├── settings/
    │   ├── base.py
    │   ├── local.py
    │   └── production.py
    ├── asgi.py
    └── wsgi.py
```

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Django | Backend Framework |
| Django REST Framework | REST APIs |
| PostgreSQL | Database |
| Redis | Celery Broker |
| Celery | Background Tasks |
| Celery Beat | Scheduled Jobs |
| Simple JWT | Authentication |
| Docker Compose | Containers |
| Requests | Internal API Calls |

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/PulseNotify.git

cd PulseNotify
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start PostgreSQL & Redis

```bash
docker compose up -d
```

Verify

```bash
docker ps
```

You should see

- PostgreSQL
- Redis

running successfully.

---

# ⚙ Environment Variables

Create a file named

```text
.env
```

Add:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=pulsenotify

DB_USER=postgres

DB_PASSWORD=postgres

DB_HOST=localhost

DB_PORT=5432

DJANGO_SETTINGS_MODULE=pulsenotify.settings.local
```

---

# 📦 Database Migration

```bash
python manage.py makemigrations

python manage.py migrate
```

---

# 👤 Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

---

---

# ▶️ Running the Project

PulseNotify requires **three separate processes** running simultaneously:

1. Django Development Server
2. Celery Worker
3. Celery Beat Scheduler

In addition, PostgreSQL and Redis must be running via Docker.

---

## Step 1 — Start PostgreSQL & Redis

```bash
docker compose up -d
```

Verify the containers are running:

```bash
docker ps
```

Expected output should include:

- PostgreSQL
- Redis

---

## Step 2 — Start Django Server

Open a new terminal.

Navigate to the project directory and activate your virtual environment.

Run:

```bash
python manage.py runserver
```

You should see:

```text
Starting development server at http://127.0.0.1:8000/
```

The REST API is now available at:

```text
http://127.0.0.1:8000/
```

---

## Step 3 — Start Celery Worker

Open **another terminal**.

Activate the same virtual environment.

Run:

```bash
celery -A pulsenotify worker --loglevel=info
```

Expected output:

```text
-------------- celery@DESKTOP v5.x
...
ready.
```

The Celery Worker is responsible for executing background tasks such as:

- Sending notifications
- Processing asynchronous jobs

---

## Step 4 — Start Celery Beat

Open **a third terminal**.

Activate the virtual environment.

Run:

```bash
celery -A pulsenotify beat --loglevel=info
```

Expected output:

```text
Scheduler: Sending due task
check-flight-prices-every-minute
```

Celery Beat automatically schedules the `check_prices` task every **60 seconds**.

---

# 🖥 Terminal Layout

Your development environment should look like this:

```text
Terminal 1
----------------------------------------
python manage.py runserver


Terminal 2
----------------------------------------
celery -A pulsenotify worker --loglevel=info


Terminal 3
----------------------------------------
celery -A pulsenotify beat --loglevel=info
```

---

# ✅ Verify Everything Is Running

You should have:

| Service | Status |
|----------|--------|
| PostgreSQL | Running |
| Redis | Running |
| Django Server | Running |
| Celery Worker | Running |
| Celery Beat | Running |

---

# 🔍 Verifying Background Processing

1. Register a new user.
2. Log in and obtain a JWT access token.
3. Create a new price alert with a high threshold (for example, **9000** for the `DEL-BOM` route).
4. Wait up to **60 seconds**.

You should observe:

- **Celery Beat** logs showing the scheduled `check_prices` task.
- **Celery Worker** logs showing the `send_notification` task being received and completed.
- A new record created in the `NotificationLog` table.
- The corresponding `PriceAlert` status updated to **TRIGGERED**.

This confirms that the complete background job workflow is functioning correctly.

---