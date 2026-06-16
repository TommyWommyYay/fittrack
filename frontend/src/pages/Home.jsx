import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="page-container">
      <div className="hero">
        <h1>FitTrack</h1>
        <p className="hero-subtitle">
          FitTrack is a web-based gym workout tracking system that allows users to record
          exercises, sets, reps, weight, duration and workout dates.
        </p>
        <p>
          Register a free account to start logging your workouts, or login if you already
          have an account. Admins can manage the exercise library and all user records.
        </p>
        <div className="hero-actions">
          <Link to="/login" className="btn btn-primary">Login</Link>
          <Link to="/register" className="btn btn-secondary">Register</Link>
        </div>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <h3>📋 Log Workouts</h3>
          <p>Record sets, reps, weight, duration and dates for every session.</p>
        </div>
        <div className="feature-card">
          <h3>🏋️ Exercise Library</h3>
          <p>Browse a curated library of exercises with difficulty and muscle group info.</p>
        </div>
        <div className="feature-card">
          <h3>🔒 Secure Accounts</h3>
          <p>JWT authentication keeps your data private and secure.</p>
        </div>
        <div className="feature-card">
          <h3>👤 Role-Based Access</h3>
          <p>Admins manage all data; regular users manage their own workouts.</p>
        </div>
      </div>
    </div>
  )
}
