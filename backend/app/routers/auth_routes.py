import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import hash_password, verify_password, create_access_token
from ..dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _authenticate_and_create_token(
    username: str,
    password: str,
    db: Session,
    www_authenticate: bool = False,
) -> dict:
    """
    Shared login logic: look up the user, verify the password, and return the
    Token-shaped dict.  Raises 401 on failure so callers stay clean.

    www_authenticate=True adds the WWW-Authenticate: Bearer header required
    by the OAuth2 spec for the form-encoded /auth/login endpoint.
    """
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        logger.warning("401 — failed login attempt for username=%s", username)
        headers = {"WWW-Authenticate": "Bearer"} if www_authenticate else None
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers=headers,
        )

    token = create_access_token(data={"user_id": user.id, "username": user.username})
    logger.info("User logged in — user_id=%s username=%s", user.id, user.username)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Register a new regular user.
    Public endpoint — no token required.
    Always assigns the 'regular' role regardless of input.
    """
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        logger.warning("409 — registration rejected, username already taken: %s", user_data.username)
        raise HTTPException(status_code=409, detail="Username is already taken.")

    if db.query(models.User).filter(models.User.email == user_data.email).first():
        logger.warning("409 — registration rejected, email already registered: %s", user_data.email)
        raise HTTPException(status_code=409, detail="Email is already registered.")

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="regular"  # Public registration always creates regular users
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info("New user registered — user_id=%s username=%s", new_user.id, new_user.username)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login with username and password (form-encoded).
    Returns a JWT access token plus basic user info.
    Compatible with OAuth2PasswordRequestForm and Swagger UI.
    """
    return _authenticate_and_create_token(
        form_data.username, form_data.password, db, www_authenticate=True
    )


@router.post("/login/json", response_model=schemas.Token)
def login_json(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    JSON-based login endpoint for the React frontend (Axios sends JSON, not form data).
    """
    return _authenticate_and_create_token(credentials.username, credentials.password, db)


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return current_user
