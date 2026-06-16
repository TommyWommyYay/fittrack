import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user, get_current_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workouts", tags=["Workouts"])


def build_workout_response(workout: models.Workout) -> dict:
    """Build a workout dict that includes joined user and exercise fields."""
    return {
        "id": workout.id,
        "user_id": workout.user_id,
        "exercise_id": workout.exercise_id,
        "sets": workout.sets,
        "reps": workout.reps,
        "weight": workout.weight,
        "duration_minutes": workout.duration_minutes,
        "workout_date": workout.workout_date,
        "notes": workout.notes,
        "created_at": workout.created_at,
        "updated_at": workout.updated_at,
        "username": workout.user.username if workout.user else None,
        "exercise_name": workout.exercise.name if workout.exercise else None,
        "muscle_group": workout.exercise.muscle_group if workout.exercise else None,
    }


@router.get("", response_model=List[schemas.WorkoutResponse])
def get_workouts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Admin sees all workouts.
    Regular users see only their own workouts.
    """
    if current_user.role == "admin":
        workouts = db.query(models.Workout).all()
    else:
        workouts = db.query(models.Workout).filter(
            models.Workout.user_id == current_user.id
        ).all()

    return [build_workout_response(w) for w in workouts]


@router.get("/{workout_id}", response_model=schemas.WorkoutResponse)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Admin can view any workout; regular users can only view their own."""
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        logger.warning("404 — workout not found: workout_id=%s", workout_id)
        raise HTTPException(status_code=404, detail="Workout not found.")

    if current_user.role != "admin" and workout.user_id != current_user.id:
        logger.warning(
            "403 — user_id=%s tried to view workout_id=%s owned by user_id=%s",
            current_user.id, workout_id, workout.user_id,
        )
        raise HTTPException(status_code=403, detail="You do not have permission to view this workout.")

    return build_workout_response(workout)


@router.post("", response_model=schemas.WorkoutResponse, status_code=201)
def create_workout(
    workout_data: schemas.WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Creates a new workout.
    Regular users: backend always uses current_user.id — frontend user_id is ignored.
    Admin: can specify a different user_id; defaults to their own if not provided.
    """
    # Verify the exercise exists
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == workout_data.exercise_id
    ).first()
    if not exercise:
        logger.warning("404 — exercise not found when creating workout: exercise_id=%s", workout_data.exercise_id)
        raise HTTPException(status_code=404, detail="Exercise not found.")

    # Determine who owns this workout
    if current_user.role == "admin":
        target_user_id = workout_data.user_id if workout_data.user_id else current_user.id
        # Verify target user exists
        if not db.query(models.User).filter(models.User.id == target_user_id).first():
            logger.warning("404 — target user not found when creating workout: user_id=%s", target_user_id)
            raise HTTPException(status_code=404, detail="Target user not found.")
    else:
        # Regular users always own their own workouts — ignore any user_id from frontend
        target_user_id = current_user.id

    workout = models.Workout(
        user_id=target_user_id,
        exercise_id=workout_data.exercise_id,
        sets=workout_data.sets,
        reps=workout_data.reps,
        weight=workout_data.weight,
        duration_minutes=workout_data.duration_minutes,
        workout_date=workout_data.workout_date,
        notes=workout_data.notes,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    logger.info("Workout created — workout_id=%s user_id=%s exercise_id=%s",
                workout.id, workout.user_id, workout.exercise_id)
    return build_workout_response(workout)


@router.put("/{workout_id}", response_model=schemas.WorkoutResponse)
def update_workout(
    workout_id: int,
    workout_data: schemas.WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Admin can update any workout.
    Regular users can only update their own workouts.
    """
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        logger.warning("404 — workout not found for update: workout_id=%s", workout_id)
        raise HTTPException(status_code=404, detail="Workout not found.")

    # Ownership check for regular users
    if current_user.role != "admin" and workout.user_id != current_user.id:
        logger.warning(
            "403 — user_id=%s tried to edit workout_id=%s owned by user_id=%s",
            current_user.id, workout_id, workout.user_id,
        )
        raise HTTPException(status_code=403, detail="You do not have permission to edit this workout.")

    # Validate exercise_id if being updated
    if workout_data.exercise_id is not None:
        if not db.query(models.Exercise).filter(
            models.Exercise.id == workout_data.exercise_id
        ).first():
            logger.warning("404 — exercise not found for workout update: exercise_id=%s", workout_data.exercise_id)
            raise HTTPException(status_code=404, detail="Exercise not found.")

    # Admin can reassign workout to another user
    if workout_data.user_id is not None and current_user.role == "admin":
        if not db.query(models.User).filter(models.User.id == workout_data.user_id).first():
            logger.warning("404 — target user not found for workout update: user_id=%s", workout_data.user_id)
            raise HTTPException(status_code=404, detail="Target user not found.")
        workout.user_id = workout_data.user_id

    update_fields = workout_data.model_dump(exclude_unset=True, exclude={"user_id"})
    for field, value in update_fields.items():
        if value is not None:
            setattr(workout, field, value)

    workout.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(workout)
    logger.info("Workout updated — workout_id=%s by user_id=%s", workout_id, current_user.id)
    return build_workout_response(workout)


@router.delete("/{workout_id}", status_code=200)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)  # Admin only
):
    """
    Admin only — regular users receive 403 automatically via get_current_admin_user.
    """
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        logger.warning("404 — workout not found for delete: workout_id=%s", workout_id)
        raise HTTPException(status_code=404, detail="Workout not found.")

    db.delete(workout)
    db.commit()
    logger.info("Workout deleted — workout_id=%s by admin user_id=%s", workout_id, current_user.id)
    return {"message": f"Workout #{workout_id} has been deleted."}
