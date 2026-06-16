import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Column
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import hash_password
from ..dependencies import get_current_user, get_current_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


def _check_user_field_unique(
    db: Session, column: Column, value: str, exclude_id: int, detail: str
) -> None:
    """
    Raise HTTP 409 if another user already holds the given column value.
    exclude_id prevents the user being updated from conflicting with themselves.
    """
    if db.query(models.User).filter(column == value, models.User.id != exclude_id).first():
        logger.warning("409 — %s", detail)
        raise HTTPException(status_code=409, detail=detail)


@router.get("", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Admin only — returns all registered users."""
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Admin can view any user; regular users can only view their own profile."""
    if current_user.role != "admin" and current_user.id != user_id:
        logger.warning(
            "403 — user_id=%s tried to view user_id=%s", current_user.id, user_id
        )
        raise HTTPException(status_code=403, detail="You do not have permission to view this user.")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning("404 — user not found: user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    update_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Admin can update any user including role.
    Regular users can only update their own username/email — not their role.
    """
    if current_user.role != "admin" and current_user.id != user_id:
        logger.warning(
            "403 — user_id=%s tried to update user_id=%s", current_user.id, user_id
        )
        raise HTTPException(status_code=403, detail="You do not have permission to update this user.")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning("404 — user not found for update: user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="User not found.")

    # Regular users cannot change their own role
    if current_user.role != "admin" and update_data.role is not None:
        logger.warning("403 — user_id=%s attempted to change own role", current_user.id)
        raise HTTPException(status_code=403, detail="You cannot change your own role.")

    if update_data.username is not None:
        _check_user_field_unique(
            db, models.User.username, update_data.username, user_id,
            "Username is already taken."
        )
        user.username = update_data.username

    if update_data.email is not None:
        _check_user_field_unique(
            db, models.User.email, update_data.email, user_id,
            "Email is already registered."
        )
        user.email = update_data.email

    if update_data.role is not None and current_user.role == "admin":
        user.role = update_data.role

    db.commit()
    db.refresh(user)
    logger.info("User updated — user_id=%s by user_id=%s", user_id, current_user.id)
    return user


@router.delete("/{user_id}", status_code=200)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Admin only — deletes a user.
    Prevents deletion if the target is the only admin in the system.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning("404 — user not found for delete: user_id=%s", user_id)
        raise HTTPException(status_code=404, detail="User not found.")

    # Prevent deleting the last admin
    if user.role == "admin":
        admin_count = db.query(models.User).filter(models.User.role == "admin").count()
        if admin_count <= 1:
            logger.warning(
                "400 — delete blocked: user_id=%s is the only admin", user_id
            )
            raise HTTPException(
                status_code=400,
                detail="Cannot delete the only admin account."
            )

    db.delete(user)
    db.commit()
    logger.info("User deleted — user_id=%s username=%s by admin user_id=%s",
                user_id, user.username, current_user.id)
    return {"message": f"User '{user.username}' has been deleted."}
