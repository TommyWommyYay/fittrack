# FitTrack Backend

FastAPI backend for the FitTrack gym workout tracking system.

## Quick Start

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

## Structure

```
app/
├── main.py          # FastAPI app, CORS, router registration
├── database.py      # SQLAlchemy engine and session
├── models.py        # ORM table definitions
├── schemas.py       # Pydantic request/response models
├── auth.py          # JWT and bcrypt helpers
├── dependencies.py  # get_current_user, get_current_admin_user
├── seed.py          # Database seeding script
└── routers/
    ├── auth_routes.py
    ├── user_routes.py
    ├── exercise_routes.py
    └── workout_routes.py
```
