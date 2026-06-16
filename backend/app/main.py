from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth_routes, user_routes, exercise_routes, workout_routes
from .logging_config import setup_logging
from .seed import seed

# Configure logging before anything else runs
setup_logging()

# Create all database tables on startup if they do not already exist
Base.metadata.create_all(bind=engine)

# Auto-seed the database on startup; seed() itself skips if data already
# exists, but a failure here (e.g. transient DB issue) must not crash the app
try:
    seed()
except Exception as exc:
    print(f"Seeding skipped due to error: {exc}")

app = FastAPI(
    title="FitTrack API",
    description="Gym workout tracking REST API built with FastAPI and SQLite.",
    version="1.0.0"
)

# CORS — allow the Vite dev server and deployed frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_origins=[
        "https://your-frontend-name.onrender.com",  # TODO: replace with actual Render frontend URL after deploying frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route groups
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(exercise_routes.router)
app.include_router(workout_routes.router)


@app.get("/", tags=["Root"])
def root():
    """Health-check endpoint."""
    return {"message": "FitTrack API is running"}
