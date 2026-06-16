# FitTrack — Entity Relationship Diagram

## Entities and Attributes

### users
| Column        | Type     | Constraint               |
|---------------|----------|--------------------------|
| id            | Integer  | PRIMARY KEY, INDEX       |
| username      | String   | UNIQUE, NOT NULL         |
| email         | String   | UNIQUE, NOT NULL         |
| password_hash | String   | NOT NULL                 |
| role          | String   | NOT NULL ('admin'/'regular') |
| created_at    | DateTime | DEFAULT now()            |

### exercises
| Column       | Type     | Constraint                            |
|--------------|----------|---------------------------------------|
| id           | Integer  | PRIMARY KEY, INDEX                    |
| name         | String   | UNIQUE, NOT NULL                      |
| muscle_group | String   | NOT NULL                              |
| difficulty   | String   | NOT NULL (Beginner/Intermediate/Advanced) |
| equipment    | String   | NOT NULL                              |
| description  | Text     | NOT NULL                              |
| created_at   | DateTime | DEFAULT now()                         |

### workouts
| Column           | Type     | Constraint                  |
|------------------|----------|-----------------------------|
| id               | Integer  | PRIMARY KEY, INDEX          |
| user_id          | Integer  | FOREIGN KEY → users.id      |
| exercise_id      | Integer  | FOREIGN KEY → exercises.id  |
| sets             | Integer  | NOT NULL, > 0               |
| reps             | Integer  | NOT NULL, > 0               |
| weight           | Float    | NOT NULL, >= 0              |
| duration_minutes | Integer  | NOT NULL, > 0               |
| workout_date     | Date     | NOT NULL                    |
| notes            | Text     | NULL                        |
| created_at       | DateTime | DEFAULT now()               |
| updated_at       | DateTime | NULL (set on update)        |

## Relationships

```
users ||--o{ workouts : "logs"
exercises ||--o{ workouts : "used in"
```

- **User → Workouts**: One user can have many workouts (one-to-many). Cascade delete.
- **Exercise → Workouts**: One exercise can appear in many workouts (one-to-many). Deletion of an exercise is blocked if workouts reference it.

## Foreign Keys

- `workouts.user_id` references `users.id`
- `workouts.exercise_id` references `exercises.id`
