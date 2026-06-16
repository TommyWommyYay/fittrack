import { Navigate } from 'react-router-dom'
import { isLoggedIn } from './auth'

/**
 * Wraps any route that requires the user to be logged in.
 * Redirects to /login if no token is found in localStorage.
 */
export default function ProtectedRoute({ children }) {
  if (!isLoggedIn()) {
    return <Navigate to="/login" replace />
  }
  return children
}
