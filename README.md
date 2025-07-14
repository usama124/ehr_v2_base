# EHR Management System (FastAPI)

A scalable and modular Electronic Health Record (EHR) system built with **FastAPI**, **SQLAlchemy (async)**, and *
*PostgreSQL**. This app supports user registration, authentication (JWT), role-based access control, and CRUD operations
for doctors, patients, and appointments.

---

## 📦 Features

- JWT-based Authentication
- Role & Permission Management (Doctor, Patient, Receptionist, Admin)
- Doctor & Patient Profile Management
- Appointment Scheduling & Updates
- Medical Record Management for Patients
- Async PostgreSQL with SQLAlchemy
- Alembic for migrations
- Pydantic model validation with role-specific logic
- Swagger & ReDoc for interactive API documentation

---

## 📁 Project Structure

```bash
.
├── alembic/ # Alembic migration setup
│ └── versions/ # Auto-generated migration files
│ └── *.py
│
├── app/
│ ├── core/ # Core configs and utilities
│ │ ├── init.py
│ │ ├── auth.py # JWT, password hashing
│ │ ├── config.py # Settings via pydantic
│ │ ├── database.py # Async DB setup
│ │ ├── dependency.py # Dependency injectors
│ │ ├── enums.py # Role & permission enums
│ │ └── responses.py # Custom API response formatter
│ │
│ ├── crud/ # Business logic layer (services)
│ │ ├── init.py
│ │ ├── appointment.py
│ │ ├── doctor.py
│ │ ├── medical_record.py
│ │ ├── patient.py
│ │ ├── role_perm.py
│ │ └── user.py
│ │
│ ├── models/ # SQLAlchemy database models
│ │ ├── init.py
│ │ ├── appointment.py
│ │ ├── doctor.py
│ │ ├── medical_record.py
│ │ ├── patient.py
│ │ ├── role_permission.py
│ │ └── user.py
│ │
│ ├── routers/ # API routes
│ │ ├── init.py
│ │ ├── appointment.py
│ │ ├── doctor.py
│ │ ├── medical_record.py
│ │ ├── patient.py
│ │ ├── role_permission.py
│ │ ├── user.py
│ │ └── dashboard.py
│ │
│ ├── schema/ # Pydantic schemas
│ │ ├── init.py
│ │ ├── appointment.py
│ │ ├── medical_record.py
│ │ ├── role_permission.py
│ │ └── user.py
│ │
│ └── main.py # FastAPI application entry point
│
├── .env # Environment configuration
├── .env.example # Sample environment config
├── .gitignore # Git ignore rules
├── alembic.ini # Alembic config
├── requirements.txt # Python dependencies
├── seed_initial_data.py # Script to seed roles, permissions, etc.
└── README.md # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ehr-fastapi.git
cd ehr-fastapi
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=4000
DB_NAME=ehr_v2
ALGORITHM=HS256
SECRET_KEY=5e3e18a2-6f1b-438c-9060-5a68e8e437ef
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run Alembic Migrations

```bash
alembic upgrade head
```

### 5.1. Create any new Migration

```bash
alembic revision --autogenerate -m "MIGRATION MESSAGE"
```

### 6. Seed Initial Role Permission Data

```bash
python seed_initial_data.py
```

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

## Auth Flow

POST /auth/register — Register user with role (Doctor, Patient, etc.)

POST /auth/login — Login with email & password to receive JWT

GET /auth/me — Get logged-in user's profile using bearer token

## Permissions System

```bash
require_permission(PermissionsEnum.CAN_EDIT_DOCTOR)
```
