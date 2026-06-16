from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import date, datetime
import re


# ─── User Schemas ─────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must include at least one letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must include at least one number.")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None  # Only admin can change role

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) < 3:
                raise ValueError("Username must be at least 3 characters.")
        return v

    @field_validator("role")
    @classmethod
    def role_valid(cls, v):
        if v is not None and v not in ("admin", "regular"):
            raise ValueError("Role must be 'admin' or 'regular'.")
        return v


# ─── Token Schemas ─────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None


# ─── Exercise Schemas ──────────────────────────────────────────────────────────

VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}


class ExerciseCreate(BaseModel):
    name: str
    muscle_group: str
    difficulty: str
    equipment: str
    description: str

    @field_validator("name")
    @classmethod
    def name_required(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Exercise name is required.")
        return v

    @field_validator("muscle_group")
    @classmethod
    def muscle_group_required(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Muscle group is required.")
        return v

    @field_validator("difficulty")
    @classmethod
    def difficulty_valid(cls, v):
        if v not in VALID_DIFFICULTIES:
            raise ValueError("Difficulty must be Beginner, Intermediate, or Advanced.")
        return v

    @field_validator("equipment")
    @classmethod
    def equipment_required(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Equipment is required.")
        return v

    @field_validator("description")
    @classmethod
    def description_min_length(cls, v):
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Description must be at least 10 characters.")
        return v


class ExerciseUpdate(ExerciseCreate):
    pass


class ExerciseResponse(BaseModel):
    id: int
    name: str
    muscle_group: str
    difficulty: str
    equipment: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Workout Schemas ───────────────────────────────────────────────────────────

class WorkoutCreate(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    weight: float
    duration_minutes: int
    workout_date: date
    notes: Optional[str] = None
    user_id: Optional[int] = None  # Admin can specify; regular users cannot

    @field_validator("sets")
    @classmethod
    def sets_positive(cls, v):
        if v <= 0:
            raise ValueError("Sets must be greater than 0.")
        return v

    @field_validator("reps")
    @classmethod
    def reps_positive(cls, v):
        if v <= 0:
            raise ValueError("Reps must be greater than 0.")
        return v

    @field_validator("weight")
    @classmethod
    def weight_non_negative(cls, v):
        if v < 0:
            raise ValueError("Weight cannot be negative.")
        return v

    @field_validator("duration_minutes")
    @classmethod
    def duration_positive(cls, v):
        if v <= 0:
            raise ValueError("Duration must be greater than 0.")
        return v


class WorkoutUpdate(BaseModel):
    exercise_id: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration_minutes: Optional[int] = None
    workout_date: Optional[date] = None
    notes: Optional[str] = None
    user_id: Optional[int] = None  # Admin only

    @field_validator("sets")
    @classmethod
    def sets_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Sets must be greater than 0.")
        return v

    @field_validator("reps")
    @classmethod
    def reps_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Reps must be greater than 0.")
        return v

    @field_validator("weight")
    @classmethod
    def weight_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Weight cannot be negative.")
        return v

    @field_validator("duration_minutes")
    @classmethod
    def duration_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Duration must be greater than 0.")
        return v


class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    sets: int
    reps: int
    weight: float
    duration_minutes: int
    workout_date: date
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    # Joined fields
    username: Optional[str] = None
    exercise_name: Optional[str] = None
    muscle_group: Optional[str] = None

    model_config = {"from_attributes": True}
