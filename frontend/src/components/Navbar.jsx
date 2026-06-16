import { Link, useNavigate } from 'react-router-dom'
import { getUser, clearAuth, isLoggedIn, isAdmin } from '../auth'

export default function Navbar() {
  const navigate = useNavigate()
  const loggedIn = isLoggedIn()
  const admin = isAdmin()
  const user = getUser()

  function handleLogout() {
    clearAuth()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to={loggedIn ? (admin ? '/admin' : '/dashboard') : '/'}>
          FitTrack
        </Link>
      </div>

      <ul className="navbar-links">
        {!loggedIn && (
          <>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}

        {loggedIn && !admin && (
          <>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/exercises">Exercises</Link></li>
            <li><Link to="/workouts">My Workouts</Link></li>
            <li><Link to="/workouts/add">Add Workout</Link></li>
          </>
        )}

        {loggedIn && admin && (
          <>
            <li><Link to="/admin">Admin Dashboard</Link></li>
            <li><Link to="/admin/users">Users</Link></li>
            <li><Link to="/exercises">Exercises</Link></li>
            <li><Link to="/exercises/add">Add Exercise</Link></li>
            <li><Link to="/workouts">Workouts</Link></li>
            <li><Link to="/workouts/add">Add Workout</Link></li>
          </>
        )}

        {loggedIn && (
          <li>
            <button className="btn-link logout-btn" onClick={handleLogout}>
              Logout ({user?.username})
            </button>
          </li>
        )}
      </ul>
    </nav>
  )
}
