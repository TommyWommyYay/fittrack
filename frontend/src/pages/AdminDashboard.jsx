import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import API from '../api'
import { getUser } from '../auth'
import AlertMessage from '../components/AlertMessage'

export default function AdminDashboard() {
  const user = getUser()
  const [stats, setStats] = useState({ users: 0, exercises: 0, workouts: 0 })
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchStats() {
      try {
        const [usersRes, exercisesRes, workoutsRes] = await Promise.all([
          API.get('/users'),
          API.get('/exercises'),
          API.get('/workouts'),
        ])
        setStats({
          users: usersRes.data.length,
          exercises: exercisesRes.data.length,
          workouts: workoutsRes.data.length,
        })
      } catch (err) {
        setError('Could not load admin statistics.')
      }
    }
    fetchStats()
  }, [])

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Admin Dashboard</h1>
        <span className="role-badge role-admin">Admin</span>
      </div>
      <p className="page-subtitle">Welcome back, <strong>{user?.username}</strong>. You have full system access.</p>

      <AlertMessage message={error} type="error" />

      <div className="stats-grid">
        <div className="stat-card stat-blue">
          <span className="stat-number">{stats.users}</span>
          <span className="stat-label">Total Users</span>
        </div>
        <div className="stat-card stat-green">
          <span className="stat-number">{stats.exercises}</span>
          <span className="stat-label">Exercises</span>
        </div>
        <div className="stat-card stat-orange">
          <span className="stat-number">{stats.workouts}</span>
          <span className="stat-label">Total Workouts</span>
        </div>
      </div>

      <h2>Admin Actions</h2>
      <div className="admin-actions-grid">
        <div className="action-card">
          <h3>👥 Users</h3>
          <p>View all registered users and manage their accounts.</p>
          <Link to="/admin/users" className="btn btn-primary">Manage Users</Link>
        </div>
        <div className="action-card">
          <h3>🏋️ Exercises</h3>
          <p>Add, edit and delete exercises from the library.</p>
          <div className="card-actions">
            <Link to="/exercises" className="btn btn-secondary">View Exercises</Link>
            <Link to="/exercises/add" className="btn btn-primary">Add Exercise</Link>
          </div>
        </div>
        <div className="action-card">
          <h3>📋 Workouts</h3>
          <p>View all workout records across all users.</p>
          <div className="card-actions">
            <Link to="/workouts" className="btn btn-secondary">View All Workouts</Link>
            <Link to="/workouts/add" className="btn btn-primary">Add Workout</Link>
          </div>
        </div>
      </div>
    </div>
  )
}
