# FitTrack — Test Plan

## Manual Test Cases

Tests can be performed via the React UI or directly through FastAPI Swagger at `http://localhost:8000/docs`.

| Test ID | Feature                          | Test Data                                                          | Expected Result                                          | Actual Result | Pass/Fail |
|---------|----------------------------------|--------------------------------------------------------------------|----------------------------------------------------------|---------------|-----------|
| T01     | Register valid user              | username: testuser, email: test@test.com, password: Test1234       | 201 Created, role: regular                               |               |           |
| T02     | Reject duplicate email           | Register again with same email                                     | 409 Conflict — "Email is already registered."            |               |           |
| T03     | Reject duplicate username        | Register again with same username                                  | 409 Conflict — "Username is already taken."              |               |           |
| T04     | Reject short password            | password: pass1                                                    | 422 — "Password must be at least 8 characters."          |               |           |
| T05     | Reject password no number        | password: password                                                 | 422 — "Password must include at least one number."       |               |           |
| T06     | Reject invalid email             | email: notanemail                                                  | 422 — invalid email format                               |               |           |
| T07     | Login valid user                 | username: ivan, password: User1234                                 | 200 OK, returns JWT token and user object                |               |           |
| T08     | Reject wrong password            | username: ivan, password: wrongpass                                | 401 — "Incorrect username or password."                  |               |           |
| T09     | Regular user views exercises     | Login as ivan, GET /exercises                                      | 200 OK, list of exercises returned                       |               |           |
| T10     | Regular user creates workout     | Login as ivan, POST /workouts with valid data                      | 201 Created, workout linked to ivan's user_id            |               |           |
| T11     | Regular user edits own workout   | Login as ivan, PUT /workouts/{own_id}                              | 200 OK, workout updated                                  |               |           |
| T12     | Regular user cannot delete       | Login as ivan, DELETE /workouts/{id}                               | 403 Forbidden                                            |               |           |
| T13     | Regular user cannot add exercise | Login as ivan, POST /exercises                                     | 403 Forbidden                                            |               |           |
| T14     | Regular user cannot access admin | Navigate to /admin as ivan                                         | Redirect to /not-authorised                              |               |           |
| T15     | Admin views all users            | Login as admin, GET /users                                         | 200 OK, all 10 users returned                            |               |           |
| T16     | Admin creates exercise           | Login as admin, POST /exercises with valid data                    | 201 Created, exercise saved                              |               |           |
| T17     | Admin edits exercise             | Login as admin, PUT /exercises/{id}                                | 200 OK, exercise updated                                 |               |           |
| T18     | Admin deletes exercise (no links)| Create new exercise, DELETE /exercises/{new_id}                   | 200 OK, exercise deleted                                 |               |           |
| T19     | Block delete linked exercise     | DELETE /exercises/1 (linked to workouts)                           | 400 — "Exercise is linked to existing workout records."  |               |           |
| T20     | Admin deletes workout            | Login as admin, DELETE /workouts/{id}                              | 200 OK, workout deleted                                  |               |           |
| T21     | Invalid sets value rejected      | POST /workouts with sets: 0                                        | 422 — "Sets must be greater than 0."                     |               |           |
| T22     | Negative weight rejected         | POST /workouts with weight: -5                                     | 422 — "Weight cannot be negative."                       |               |           |
| T23     | Exercise required on workout     | POST /workouts without exercise_id                                 | 422 validation error                                     |               |           |
| T24     | Logout clears session            | Click Logout                                                       | Token removed from localStorage, redirect to /login      |               |           |
| T25     | Unauthenticated access blocked   | GET /exercises without token                                       | 401 Unauthorized                                         |               |           |

## Automated Tests

Run from `backend/` directory:

```bash
pytest tests/test_api.py -v
```

Automated tests cover:
- Root endpoint health check
- User registration (valid and invalid cases)
- Login (valid and wrong password)
- Protected endpoint requiring authentication
- Role-based access control (regular user blocked from admin endpoints)
