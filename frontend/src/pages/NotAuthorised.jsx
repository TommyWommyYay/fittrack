import { Link } from 'react-router-dom'
import { isAdmin } from '../auth'

export default function NotAuthorised() {
  const admin = isAdmin()

  return (
    <div className="page-container error-page">
      <div className="error-content">
        <h1>🔒 403</h1>
        <h2>Not Authorised</h2>
        <p>You do not have permission to access this page.</p>
        <Link to={admin ? '/admin' : '/dashboard'} className="btn btn-primary">
          Return to Dashboard
        </Link>
      </div>
    </div>
  )
}
