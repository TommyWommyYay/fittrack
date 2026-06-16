# FitTrack — User Manual

## Getting Started

### How to Register

1. Open `http://localhost:5173` in your browser.
2. Click **Register** on the home page or navbar.
3. Fill in:
   - **Username** — at least 3 characters, must be unique.
   - **Email** — a valid email address, must be unique.
   - **Password** — at least 8 characters with letters and numbers.
   - **Confirm Password** — must match the password field.
4. Click **Register**.
5. On success you will see a confirmation message and be redirected to the login page.

---

### How to Login

1. Go to `http://localhost:5173/login`.
2. Enter your **Username** and **Password**.
3. Click **Login**.
4. You are redirected to your dashboard:
   - **Admin** users → Admin Dashboard (`/admin`)
   - **Regular** users → Dashboard (`/dashboard`)

**Test accounts:**

| Role    | Username | Password |
| ------- | -------- | -------- |
| Admin   | admin    | Admin123 |
| Regular | ivan     | User1234 |

---

## Regular User Guide

### How to View Exercises

1. Login and click **Exercises** in the navigation bar.
2. The exercise library shows all available exercises with their name, muscle group, difficulty, equipment and description.
3. Regular users can view exercises but cannot add, edit or delete them.

---

### How to Add a Workout

1. Click **Add Workout** in the navigation bar or on the Dashboard.
2. Fill in the form:
   - **Exercise** — select from the dropdown.
   - **Sets** — number of sets performed (must be ≥ 1).
   - **Reps** — repetitions per set (must be ≥ 1).
   - **Weight (kg)** — weight used (0 for bodyweight exercises).
   - **Duration (minutes)** — total session time.
   - **Date** — date of the workout.
   - **Notes** — optional session notes.
3. Click **Add Workout**.
4. You are redirected to your workouts list on success.

---

### How to Edit a Workout

1. Go to **My Workouts** in the navigation bar.
2. Find the workout you want to change and click **Edit**.
3. Modify the fields as needed.
4. Click **Save Changes**.
5. Regular users can only edit their own workouts.

---

### Logout

Click **Logout** in the navigation bar. Your session is cleared and you are redirected to the login page.

---

## Admin Guide

### How to Manage Exercises

1. Login as admin and click **Exercises** in the navigation bar.
2. To **add** an exercise: click **+ Add Exercise**, fill in all fields, click **Save Exercise**.
3. To **edit** an exercise: click **Edit** next to it, make changes, click **Save Changes**.
4. To **delete** an exercise: click **Delete**, confirm in the modal.
   - If the exercise is linked to workout records, deletion is blocked with an error message.

---

### How to Manage Workouts

1. Click **Workouts** — admins see all users' workouts.
2. To **edit** any workout: click **Edit**.
3. To **delete** a workout: click **Delete** and confirm.
4. To **add** a workout for any user: click **Add Workout**, optionally choose a user from the dropdown.

---

### How to Manage Users

1. Click **Users** in the navigation bar.
2. All registered users are listed with their ID, username, email, role and registration date.
3. To delete a user: click **Delete** and confirm. This also deletes their workout records.
4. The last admin account cannot be deleted.
