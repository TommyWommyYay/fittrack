import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user, get_current_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exercises", tags=["Exercises"])


def _check_exercise_name_unique(db: Session, name: str, exclude_id: Optional[int] = None) -> None:
    """
    Raise HTTP 409 if an exercise with the given name already exists.
    Pass exclude_id when updating so the exercise being edited is not flagged
    against itself.
    """
    query = db.query(models.Exercise).filter(models.Exercise.name == name)
    if exclude_id is not None:
        query = query.filter(models.Exercise.id != exclude_id)
    if query.first():
        logger.warning("409 — exercise name already exists: '%s'", name)
        raise HTTPException(status_code=409, detail="Exercise name already exists.")


@router.get("", response_model=List[schemas.ExerciseResponse])
def get_exercises(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """All authenticated users can view all exercises."""
    return db.query(models.Exercise).all()


@router.get("/{exercise_id}", response_model=schemas.ExerciseResponse)
def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """All authenticated users can view a single exercise."""
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        logger.warning("404 — exercise not found: exercise_id=%s", exercise_id)
        raise HTTPException(status_code=404, detail="Exercise not found.")
    return exercise


@router.post("", response_model=schemas.ExerciseResponse, status_code=201)
def create_exercise(
    exercise_data: schemas.ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Admin only — creates a new exercise."""
    _check_exercise_name_unique(db, exercise_data.name)

    exercise = models.Exercise(**exercise_data.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    logger.info("Exercise created — exercise_id=%s name='%s' by user_id=%s",
                exercise.id, exercise.name, current_user.id)
    return exercise


@router.put("/{exercise_id}", response_model=schemas.ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_data: schemas.ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Admin only — updates an existing exercise."""
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        logger.warning("404 — exercise not found for update: exercise_id=%s", exercise_id)
        raise HTTPException(status_code=404, detail="Exercise not found.")

    # Only check uniqueness if the name is actually changing
    if exercise_data.name != exercise.name:
        _check_exercise_name_unique(db, exercise_data.name, exclude_id=exercise_id)

    for field, value in exercise_data.model_dump().items():
        setattr(exercise, field, value)

    db.commit()
    db.refresh(exercise)
    logger.info("Exercise updated — exercise_id=%s by user_id=%s", exercise_id, current_user.id)
    return exercise


@router.delete("/{exercise_id}", status_code=200)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Admin only — deletes an exercise.
    Prevents deletion if the exercise is linked to existing workout records.
    """
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        logger.warning("404 — exercise not found for delete: exercise_id=%s", exercise_id)
        raise HTTPException(status_code=404, detail="Exercise not found.")

    # Prevent deletion if workouts reference this exercise
    linked_workouts = db.query(models.Workout).filter(
        models.Workout.exercise_id == exercise_id
    ).count()

    if linked_workouts > 0:
        logger.warning(
            "400 — delete blocked for exercise_id=%s ('%s'): linked to %s workout(s)",
            exercise_id, exercise.name, linked_workouts,
        )
        raise HTTPException(
            status_code=400,
            detail="This exercise cannot be deleted because it is linked to existing workout records."
        )

    db.delete(exercise)
    db.commit()
    logger.info("Exercise deleted — exercise_id=%s name='%s' by user_id=%s",
                exercise_id, exercise.name, current_user.id)
    return {"message": f"Exercise '{exercise.name}' has been deleted."}
