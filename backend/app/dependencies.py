import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .auth import decode_access_token
from . import models

logger = logging.getLogger(__name__)

# FastAPI uses this to extract the Bearer token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Decode the JWT, look up the user in the database, and return them.
    Raises 401 if the token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        logger.warning("401 — invalid or expired JWT token presented")
        raise credentials_exception

    user_id: int = payload.get("user_id")
    if user_id is None:
        logger.warning("401 — JWT payload missing user_id claim")
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        logger.warning("401 — JWT references non-existent user_id=%s", user_id)
        raise credentials_exception

    return user


def get_current_admin_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    Extends get_current_user — additionally checks that the user has the admin role.
    Raises 403 if the user is not an admin.
    """
    if current_user.role != "admin":
        logger.warning(
            "403 — user_id=%s username=%s attempted admin-only action",
            current_user.id,
            current_user.username,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return current_user
