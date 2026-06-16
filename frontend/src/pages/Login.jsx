import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import API, { getErrorMessage } from '../api'
import { saveAuth } from '../auth'
import AlertMessage from '../components/AlertMessage'

export default function Login() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!form.username.trim() || !form.password) {
      setError('Username and password are required.')
      return
    }

    setLoading(true)
    try {
      const res = await API.post('/auth/login/json', {
        username: form.username.trim(),
        password: form.password,
      })
      const { access_token, user } = res.data

      // Persist token and user info for subsequent requests
      saveAuth(access_token, user)

      // Redirect based on role
      if (user.role === 'admin') {
        navigate('/admin')
      } else {
        navigate('/dashboard')
      }
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container form-page">
      <div className="form-card">
        <h2>Login to FitTrack</h2>
        <p className="form-subtitle">Enter your credentials to access your account.</p>

        <AlertMessage message={error} type="error" />

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              placeholder="Your username"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Your password"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="test-accounts">
          <h4>Test Accounts</h4>
          <p><strong>Admin:</strong> admin / Admin123</p>
          <p><strong>Regular:</strong> ivan / User1234</p>
        </div>

        <p className="form-footer">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </div>
  )
}
