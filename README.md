# FitTrack — Gym Workout Tracking System

A full-stack university assignment project built with React (Vite), FastAPI and SQLite.

---

## Project Description

FitTrack is a web-based gym workout tracking system. Users can log workouts by selecting from an exercise library and recording sets, reps, weight, duration and date. The system has two roles: **admin** (full CRUD access) and **regular** (create, read, update own workouts only).

---

## Features

- User registration and login with JWT authentication
- bcrypt password hashing — no plain-text passwords stored
- Role-based access control (admin and regular)
- Exercise library with difficulty levels and muscle groups
- Workout logging with sets, reps, weight, duration and notes
- Admin dashboard with system-wide statistics
- Regular user dashboard showing personal stats
- Full admin CRUD for exercises and workouts
- Regular users can create, view and edit own workouts only
- Delete confirmation modals
- Success and error notifications
- Responsive interface

---

## Technology Stack

| Layer     | Technology                         |
|-----------|------------------------------------|
| Frontend  | React 18, Vite, React Router, Axios|
| Backend   | Python 3.10+, FastAPI, Uvicorn     |
| Database  | SQLite (fittrack.db)               |
| ORM       | SQLAlchemy                         |
| Auth      | JWT (python-jose), bcrypt (passlib)|
| Validation| Pydantic v2                        |
| Testing   | pytest, httpx                      |

---

## Database Design Summary

Three tables with relationships:

- **users** — stores registered users with hashed passwords and role
- **exercises** — stores the exercise library (admin managed)
- **workouts** — links users to exercises with training data

Foreign keys:
- `workouts.user_id` → `users.id`
- `workouts.exercise_id` → `exercises.id`

See `docs/ERD.md` for full schema details.

---

## User Roles and Permissions

| Action                      | Admin | Regular |
|-----------------------------|-------|---------|
| View exercises              | ✅    | ✅      |
| Add/Edit/Delete exercises   | ✅    | ❌      |
| View all workouts           | ✅    | ❌      |
| View own workouts           | ✅    | ✅      |
| Create workout              | ✅    | ✅      |
| Edit own workout            | ✅    | ✅      |
| Edit any workout            | ✅    | ❌      |
| Delete workout              | ✅    | ❌      |
| View all users              | ✅    | ❌      |
| Delete users                | ✅    | ❌      |

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm

---

### How to Run the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database with test data
python -m app.seed

# Start the server
uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

API documentation: **http://localhost:8000/docs**

---

### How to Run the Frontend

Open a second terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## Test Login Details

| Role    | Username | Password  |
|---------|----------|-----------|
| Admin   | admin    | Admin123  |
| Regular | ivan     | User1234  |

Additional regular user accounts:
- sarah / User1234
- mike / User1234
- emma / User1234

---

## Running Tests

```bash
cd backend
pytest tests/test_api.py -v
```

---

## API Documentation

Full endpoint reference: `docs/API_ENDPOINTS.md`

Interactive Swagger UI: `http://localhost:8000/docs`

---

## Screenshots

*(Add screenshots here for your university report)*

1. Home page
2. Register form
3. Login page
4. Regular user dashboard
5. Admin dashboard
6. Exercise library
7. Add exercise form (admin)
8. My Workouts page
9. Add workout form
10. Admin user list
11. Validation error example
12. Delete confirmation modal
13. Success notification example

---

## Known Limitations

- No email verification on registration
- No password reset functionality
- Single SQLite file (not suitable for multi-user production deployment)
- JWT secret key is hardcoded (should be an environment variable in production)
- No pagination on large data sets

---

## Future Improvements

- Email verification and password reset
- Progress charts and workout statistics over time
- Workout templates and programmes
- Export workouts to CSV
- Environment variable configuration
- Deployment to cloud hosting (e.g. Railway, Heroku)
- Unit tests for all route handlers
