import { Navigate } from 'react-router-dom'
import { isLoggedIn, isAdmin } from './auth'

/**
 * Wraps any admin-only route.
 * Redirects to /login if not authenticated, or /not-authorised if not an admin.
 */
export default function AdminRoute({ children }) {
  if (!isLoggedIn()) {
    return <Navigate to="/login" replace />
  }
  if (!isAdmin()) {
    return <Navigate to="/not-authorised" replace />
  }
  return children
}
