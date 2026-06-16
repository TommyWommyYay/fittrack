# FitTrack — API Endpoints Reference

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## Authentication

| Method | Route              | Auth Required | Role  | Description                          |
|--------|--------------------|---------------|-------|--------------------------------------|
| GET    | /                  | No            | —     | Health check — returns API status    |
| POST   | /auth/register     | No            | —     | Register a new regular user          |
| POST   | /auth/login        | No            | —     | Login (form data) — returns JWT      |
| POST   | /auth/login/json   | No            | —     | Login (JSON) — used by React frontend|
| GET    | /auth/me           | Yes           | Any   | Returns current logged-in user       |

---

## Users

| Method | Route            | Auth Required | Role         | Description                              |
|--------|------------------|---------------|--------------|------------------------------------------|
| GET    | /users           | Yes           | Admin        | List all users                           |
| GET    | /users/{id}      | Yes           | Admin or own | Get a specific user                      |
| PUT    | /users/{id}      | Yes           | Admin or own | Update user (role change: admin only)    |
| DELETE | /users/{id}      | Yes           | Admin        | Delete a user (cannot delete last admin) |

---

## Exercises

| Method | Route               | Auth Required | Role  | Description                                    |
|--------|---------------------|---------------|-------|------------------------------------------------|
| GET    | /exercises          | Yes           | Any   | List all exercises                             |
| GET    | /exercises/{id}     | Yes           | Any   | Get a specific exercise                        |
| POST   | /exercises          | Yes           | Admin | Create a new exercise                          |
| PUT    | /exercises/{id}     | Yes           | Admin | Update an exercise                             |
| DELETE | /exercises/{id}     | Yes           | Admin | Delete (blocked if linked to workout records)  |

---

## Workouts

| Method | Route              | Auth Required | Role         | Description                                      |
|--------|--------------------|---------------|--------------|--------------------------------------------------|
| GET    | /workouts          | Yes           | Any          | Admin: all workouts. Regular: own workouts only  |
| GET    | /workouts/{id}     | Yes           | Admin or own | Get a specific workout                           |
| POST   | /workouts          | Yes           | Any          | Create a workout. Regular users own it always    |
| PUT    | /workouts/{id}     | Yes           | Admin or own | Update a workout                                 |
| DELETE | /workouts/{id}     | Yes           | Admin        | Delete a workout — regular users get 403         |

---

## HTTP Status Codes Used

| Code | Meaning                                      |
|------|----------------------------------------------|
| 200  | OK — successful GET or DELETE               |
| 201  | Created — successful POST                   |
| 400  | Bad Request — invalid data or business rule |
| 401  | Unauthorized — missing/invalid token        |
| 403  | Forbidden — insufficient role               |
| 404  | Not Found — record does not exist           |
| 409  | Conflict — duplicate username/email/name    |
| 422  | Unprocessable Entity — validation error     |
