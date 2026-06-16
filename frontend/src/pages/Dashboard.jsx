import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import API from '../api'
import { getUser } from '../auth'
import AlertMessage from '../components/AlertMessage'

export default function Dashboard() {
  const user = getUser()
  const [workoutCount, setWorkoutCount] = useState(0)
  const [exerciseCount, setExerciseCount] = useState(0)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchStats() {
      try {
        const [workoutsRes, exercisesRes] = await Promise.all([
          API.get('/workouts'),
          API.get('/exercises'),
        ])
        setWorkoutCount(workoutsRes.data.length)
        setExerciseCount(exercisesRes.data.length)
      } catch (err) {
        setError('Could not load dashboard statistics.')
      }
    }
    fetchStats()
  }, [])

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Welcome, {user?.username}!</h1>
        <span className="role-badge role-regular">Regular User</span>
      </div>

      <AlertMessage message={error} type="error" />

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-number">{workoutCount}</span>
          <span className="stat-label">My Workouts</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{exerciseCount}</span>
          <span className="stat-label">Available Exercises</span>
        </div>
      </div>

      <div className="action-buttons">
        <Link to="/exercises" className="btn btn-secondary">View Exercises</Link>
        <Link to="/workouts" className="btn btn-secondary">View My Workouts</Link>
        <Link to="/workouts/add" className="btn btn-primary">Add Workout</Link>
      </div>

      <div className="info-box">
        <h3>Getting Started</h3>
        <ul>
          <li>Browse the exercise library to find exercises you want to track.</li>
          <li>Use <strong>Add Workout</strong> to log a session.</li>
          <li>View and edit your workout history under <strong>My Workouts</strong>.</li>
          <li>Contact an admin if you need an exercise added to the library.</li>
        </ul>
      </div>
    </div>
  )
}
