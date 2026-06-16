"""
Seed script — creates all tables and inserts test data.
Run from the backend directory with:
    python -m app.seed
"""
from datetime import date
from .database import engine, SessionLocal, Base
from . import models
from .auth import hash_password


def seed():
    # Create all tables based on SQLAlchemy models
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Skip seeding if data already exists
        if db.query(models.User).count() > 0:
            print("Database already seeded. Skipping.")
            return

        # ── Users ──────────────────────────────────────────────────────────────
        users = [
            models.User(username="admin",   email="admin@fittrack.com",   password_hash=hash_password("Admin123"),  role="admin"),
            models.User(username="ivan",    email="ivan@example.com",     password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="sarah",   email="sarah@example.com",    password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="mike",    email="mike@example.com",     password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="emma",    email="emma@example.com",     password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="james",   email="james@example.com",    password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="olivia",  email="olivia@example.com",   password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="liam",    email="liam@example.com",     password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="sophia",  email="sophia@example.com",   password_hash=hash_password("User1234"),  role="regular"),
            models.User(username="noah",    email="noah@example.com",     password_hash=hash_password("User1234"),  role="regular"),
        ]
        db.add_all(users)
        db.commit()
        print(f"Inserted {len(users)} users.")

        # Re-fetch to get assigned IDs
        admin = db.query(models.User).filter_by(username="admin").first()
        ivan = db.query(models.User).filter_by(username="ivan").first()
        sarah = db.query(models.User).filter_by(username="sarah").first()
        mike = db.query(models.User).filter_by(username="mike").first()
        emma = db.query(models.User).filter_by(username="emma").first()

        # ── Exercises ──────────────────────────────────────────────────────────
        exercises = [
            models.Exercise(name="Bench Press",      muscle_group="Chest",      difficulty="Intermediate", equipment="Barbell",      description="A compound chest exercise performed lying on a bench pressing a barbell upward."),
            models.Exercise(name="Squat",             muscle_group="Legs",       difficulty="Intermediate", equipment="Barbell",      description="A fundamental lower-body compound movement targeting quads, glutes and hamstrings."),
            models.Exercise(name="Deadlift",          muscle_group="Back",       difficulty="Advanced",     equipment="Barbell",      description="A full-body compound lift pulling a loaded barbell from the floor to hip level."),
            models.Exercise(name="Shoulder Press",    muscle_group="Shoulders",  difficulty="Intermediate", equipment="Dumbbells",    description="An overhead pressing movement targeting the deltoids and triceps using dumbbells."),
            models.Exercise(name="Lat Pulldown",      muscle_group="Back",       difficulty="Beginner",     equipment="Machine",      description="A cable machine exercise that targets the latissimus dorsi by pulling a bar down to the chest."),
            models.Exercise(name="Bicep Curl",        muscle_group="Arms",       difficulty="Beginner",     equipment="Dumbbells",    description="An isolation exercise for the biceps performed by curling dumbbells from hip to shoulder level."),
            models.Exercise(name="Tricep Pushdown",   muscle_group="Arms",       difficulty="Beginner",     equipment="Cable Machine",description="A cable machine isolation exercise targeting the triceps by pushing a bar downward."),
            models.Exercise(name="Leg Press",         muscle_group="Legs",       difficulty="Beginner",     equipment="Machine",      description="A machine-based lower-body exercise pressing a weighted platform away using both legs."),
            models.Exercise(name="Plank",             muscle_group="Core",       difficulty="Beginner",     equipment="Bodyweight",   description="An isometric core stability exercise holding the body in a push-up position for time."),
            models.Exercise(name="Treadmill Run",     muscle_group="Cardio",     difficulty="Beginner",     equipment="Treadmill",    description="Cardiovascular exercise performed on a treadmill at varying speeds and inclines."),
        ]
        db.add_all(exercises)
        db.commit()
        print(f"Inserted {len(exercises)} exercises.")

        # Re-fetch exercises to get IDs
        bench  = db.query(models.Exercise).filter_by(name="Bench Press").first()
        squat  = db.query(models.Exercise).filter_by(name="Squat").first()
        dead   = db.query(models.Exercise).filter_by(name="Deadlift").first()
        press  = db.query(models.Exercise).filter_by(name="Shoulder Press").first()
        lat    = db.query(models.Exercise).filter_by(name="Lat Pulldown").first()
        curl   = db.query(models.Exercise).filter_by(name="Bicep Curl").first()
        tri    = db.query(models.Exercise).filter_by(name="Tricep Pushdown").first()
        leg    = db.query(models.Exercise).filter_by(name="Leg Press").first()
        plank  = db.query(models.Exercise).filter_by(name="Plank").first()
        tread  = db.query(models.Exercise).filter_by(name="Treadmill Run").first()

        # ── Workouts ───────────────────────────────────────────────────────────
        workouts = [
            models.Workout(user_id=ivan.id,  exercise_id=bench.id,  sets=4, reps=10, weight=80.0,  duration_minutes=45, workout_date=date(2024, 5, 1),  notes="Good session, chest felt strong."),
            models.Workout(user_id=ivan.id,  exercise_id=squat.id,  sets=5, reps=5,  weight=100.0, duration_minutes=60, workout_date=date(2024, 5, 3),  notes="Hit a new personal best today."),
            models.Workout(user_id=sarah.id, exercise_id=dead.id,   sets=3, reps=5,  weight=90.0,  duration_minutes=50, workout_date=date(2024, 5, 2),  notes="Focused on form."),
            models.Workout(user_id=sarah.id, exercise_id=lat.id,    sets=4, reps=12, weight=50.0,  duration_minutes=40, workout_date=date(2024, 5, 4),  notes="Back day — felt the lats well."),
            models.Workout(user_id=mike.id,  exercise_id=press.id,  sets=3, reps=8,  weight=30.0,  duration_minutes=35, workout_date=date(2024, 5, 5),  notes="Shoulder press superset with lateral raises."),
            models.Workout(user_id=mike.id,  exercise_id=curl.id,   sets=3, reps=15, weight=12.0,  duration_minutes=25, workout_date=date(2024, 5, 6),  notes="Arms feeling pumped."),
            models.Workout(user_id=emma.id,  exercise_id=tread.id,  sets=1, reps=1,  weight=0.0,   duration_minutes=30, workout_date=date(2024, 5, 7),  notes="5km steady pace cardio."),
            models.Workout(user_id=emma.id,  exercise_id=plank.id,  sets=3, reps=1,  weight=0.0,   duration_minutes=15, workout_date=date(2024, 5, 8),  notes="3 x 60 second holds."),
            models.Workout(user_id=admin.id, exercise_id=leg.id,    sets=4, reps=12, weight=120.0, duration_minutes=40, workout_date=date(2024, 5, 9),  notes="Leg day finisher."),
            models.Workout(user_id=admin.id, exercise_id=tri.id,    sets=3, reps=15, weight=20.0,  duration_minutes=20, workout_date=date(2024, 5, 10), notes="Tricep isolation at end of push day."),
        ]
        db.add_all(workouts)
        db.commit()
        print(f"Inserted {len(workouts)} workouts.")

        print("\nSeed complete!")
        print("  Admin login  — username: admin  | password: Admin123")
        print("  Regular user — username: ivan   | password: User1234")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
