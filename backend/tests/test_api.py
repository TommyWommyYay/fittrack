"""
Basic API tests using pytest and httpx.

Run from the backend directory:
    pytest tests/test_api.py -v

These tests cover the core endpoints and demonstrate testable behaviour.
The test database is separate from the development database.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Use an in-memory SQLite database for tests so production data is not affected
TEST_DATABASE_URL = "sqlite:///./test_fittrack.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


# ── Root ───────────────────────────────────────────────────────────────────────

def test_root_returns_running_message():
    """GET / should return the API running message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "FitTrack API is running"


# ── Registration ───────────────────────────────────────────────────────────────

def test_register_valid_user():
    """A user with valid data should register successfully."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test1234"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "regular"  # Public registration must always produce regular users


def test_register_rejects_short_username():
    """Username shorter than 3 characters should be rejected."""
    response = client.post("/auth/register", json={
        "username": "ab",
        "email": "ab@example.com",
        "password": "Test1234"
    })
    assert response.status_code == 422


def test_register_rejects_weak_password():
    """Password without letters and numbers should be rejected."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password"  # No number
    })
    assert response.status_code == 422


def test_register_rejects_duplicate_email():
    """Registering with an already-used email should return 409."""
    client.post("/auth/register", json={
        "username": "user1",
        "email": "dup@example.com",
        "password": "Test1234"
    })
    response = client.post("/auth/register", json={
        "username": "user2",
        "email": "dup@example.com",
        "password": "Test1234"
    })
    assert response.status_code == 409


def test_register_rejects_invalid_email():
    """Invalid email format should return 422."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "not-an-email",
        "password": "Test1234"
    })
    assert response.status_code == 422


# ── Login ──────────────────────────────────────────────────────────────────────

def _register_and_login(username="testuser", password="Test1234"):
    """Helper: registers a user and returns the login token."""
    client.post("/auth/register", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": password
    })
    response = client.post("/auth/login/json", json={
        "username": username,
        "password": password
    })
    return response


def test_login_valid_credentials():
    """Valid login should return a JWT token."""
    response = _register_and_login()
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_rejects_wrong_password():
    """Wrong password should return 401."""
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test1234"
    })
    response = client.post("/auth/login/json", json={
        "username": "testuser",
        "password": "WrongPass1"
    })
    assert response.status_code == 401


def test_login_rejects_nonexistent_user():
    """Login with a username that does not exist should return 401."""
    response = client.post("/auth/login/json", json={
        "username": "nobody",
        "password": "Test1234"
    })
    assert response.status_code == 401


# ── Protected Endpoints ────────────────────────────────────────────────────────

def test_exercises_requires_authentication():
    """GET /exercises without a token should return 401."""
    response = client.get("/exercises")
    assert response.status_code == 401


def test_authenticated_user_can_view_exercises():
    """A logged-in user should be able to view exercises."""
    login_data = _register_and_login()
    token = login_data.json()["access_token"]
    response = client.get("/exercises", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_regular_user_cannot_delete_workout():
    """DELETE /workouts/{id} by a regular user should return 403."""
    login_data = _register_and_login()
    token = login_data.json()["access_token"]
    # Attempt delete — workout does not need to exist; 403 should be raised first
    response = client.delete("/workouts/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_regular_user_cannot_create_exercise():
    """POST /exercises by a regular user should return 403."""
    login_data = _register_and_login()
    token = login_data.json()["access_token"]
    response = client.post("/exercises", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Push Up",
        "muscle_group": "Chest",
        "difficulty": "Beginner",
        "equipment": "Bodyweight",
        "description": "A basic bodyweight pushing exercise."
    })
    assert response.status_code == 403
