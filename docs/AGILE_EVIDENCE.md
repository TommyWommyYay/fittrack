# FitTrack — Agile Evidence

## User Stories

| ID  | User Story                                                                                     | Acceptance Criteria                                                                                           |
|-----|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| US1 | As a new user, I want to register so that I can access the workout tracker.                    | Registration form accepts valid data, rejects duplicates and weak passwords, creates a regular-role account.  |
| US2 | As a user, I want to login so that my workout data is protected.                               | Login returns a JWT token, redirects to role-specific dashboard, invalid credentials show error message.      |
| US3 | As a regular user, I want to view exercises so I can choose the correct one for my workout.    | Exercise list is visible to all logged-in users with name, muscle group, difficulty, equipment, description.  |
| US4 | As a regular user, I want to add a workout so I can track my gym progress.                     | Form validates all fields, workout saved and linked to current user, success message shown.                   |
| US5 | As a regular user, I want to edit my workout so I can correct mistakes.                        | Edit form pre-fills existing values, saves changes, shows success message. Own workouts only.                 |
| US6 | As a regular user, I want protection so I cannot accidentally delete my workouts.              | Delete button absent for regular users; DELETE API returns 403.                                               |
| US7 | As an admin, I want to manage exercises so the exercise list remains accurate.                 | Admin can create, edit and delete exercises. Delete blocked if exercise linked to workouts.                   |
| US8 | As an admin, I want to view all workouts so I can manage system data.                          | Admin workout list shows all users' records with username column.                                             |
| US9 | As an admin, I want to delete workout records so the database remains clean.                   | Delete button visible to admin, confirmation modal shown, success/error message displayed.                    |
| US10| As an admin, I want to view all users so I can see who is registered.                          | User management page shows all users with ID, username, email, role, registration date.                       |

---

## Sprint Plan

### Sprint 1 — Backend Foundation (Week 1–2)
**Goal:** Working API with database and authentication.

| Task                                      | Status |
|-------------------------------------------|--------|
| Set up FastAPI project structure          | Done   |
| Define SQLAlchemy models (User, Exercise, Workout) | Done |
| Configure SQLite database connection      | Done   |
| Implement bcrypt password hashing         | Done   |
| Implement JWT token creation and decoding | Done   |
| Create auth routes (register, login, me)  | Done   |
| Create dependency guards (get_current_user, get_current_admin_user) | Done |
| Write seed script with test data          | Done   |
| Test endpoints via Swagger /docs          | Done   |

### Sprint 2 — Backend CRUD + React Setup (Week 3)
**Goal:** All API routes working; React app skeleton.

| Task                                      | Status |
|-------------------------------------------|--------|
| Exercise CRUD routes                      | Done   |
| Workout CRUD routes with ownership checks | Done   |
| User management routes                    | Done   |
| Error handling and HTTP status codes      | Done   |
| Create Vite React project                 | Done   |
| Set up React Router                       | Done   |
| Create auth helpers (localStorage)        | Done   |
| Create Axios API helper                   | Done   |
| Create ProtectedRoute and AdminRoute      | Done   |

### Sprint 3 — Frontend Pages (Week 4)
**Goal:** All pages built and connected to API.

| Task                                      | Status |
|-------------------------------------------|--------|
| Home, Login, Register pages               | Done   |
| Regular Dashboard                         | Done   |
| Admin Dashboard                           | Done   |
| Exercises page (role-aware)               | Done   |
| Add/Edit Exercise pages (admin only)      | Done   |
| Workouts page (role-aware)                | Done   |
| Add/Edit Workout pages                    | Done   |
| Users page (admin only)                   | Done   |
| Navbar (role-aware)                       | Done   |
| ConfirmDeleteModal component              | Done   |

### Sprint 4 — Testing, Validation and Docs (Week 5)
**Goal:** Polished, tested and documented application.

| Task                                      | Status |
|-------------------------------------------|--------|
| Frontend form validation                  | Done   |
| Backend Pydantic validation               | Done   |
| Success and error alert messages          | Done   |
| Confirm-before-delete modal               | Done   |
| Pytest test file                          | Done   |
| README with run instructions              | Done   |
| ERD documentation                         | Done   |
| API endpoints documentation               | Done   |
| Test plan documentation                   | Done   |
| User manual                               | Done   |

---

## Kanban Board (Final State)

### To Do
*(empty — all tasks completed)*

### In Progress
*(empty)*

### Testing
- Manual test plan execution (fill in Actual Result and Pass/Fail in TEST_PLAN.md)

### Done
- Project structure setup
- Database models and migrations
- Seed data (10 users, 10 exercises, 10 workouts)
- JWT authentication
- Role-based authorisation
- Exercise CRUD (admin only create/update/delete)
- Workout CRUD (admin full, regular own + no delete)
- User management (admin view/delete)
- React frontend with all pages
- Validation (frontend + backend)
- Confirmation modals
- Success/error notifications
- Protected and admin routes
- Responsive CSS
- Documentation suite

---

## Definition of Done

A feature is considered done when:

1. The backend route is implemented and returns correct HTTP status codes.
2. Pydantic validation catches invalid input with clear error messages.
3. Role-based access is enforced on the backend (not just the frontend).
4. The React page correctly calls the API and displays success/error feedback.
5. Confirmation is required before any destructive action.
6. The feature can be demonstrated through the React UI and through Swagger /docs.
7. The feature is covered in the test plan (TEST_PLAN.md).
