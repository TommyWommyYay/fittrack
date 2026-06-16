import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import API, { getErrorMessage } from '../api'
import { isAdmin } from '../auth'
import AlertMessage from '../components/AlertMessage'

export default function AddWorkout() {
  const navigate = useNavigate()
  const admin = isAdmin()
  const [exercises, setExercises] = useState([])
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({
    exercise_id: '',
    sets: '',
    reps: '',
    weight: '',
    duration_minutes: '',
    workout_date: '',
    notes: '',
    user_id: '',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    async function loadData() {
      try {
        const exercisesRes = await API.get('/exercises')
        setExercises(exercisesRes.data)
        if (admin) {
          const usersRes = await API.get('/users')
          setUsers(usersRes.data)
        }
      } catch (err) {
        setError('Could not load form data.')
      }
    }
    loadData()
  }, [admin])

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function validate() {
    if (!form.exercise_id) return 'Please select an exercise.'
    if (!form.sets || Number(form.sets) <= 0) return 'Sets must be greater than 0.'
    if (!form.reps || Number(form.reps) <= 0) return 'Reps must be greater than 0.'
    if (form.weight === '' || Number(form.weight) < 0) return 'Weight must be 0 or greater.'
    if (!form.duration_minutes || Number(form.duration_minutes) <= 0) return 'Duration must be greater than 0.'
    if (!form.workout_date) return 'Workout date is required.'
    return null
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')

    const validationError = validate()
    if (validationError) {
      setError(validationError)
      return
    }

    setLoading(true)
    const payload = {
      exercise_id: Number(form.exercise_id),
      sets: Number(form.sets),
      reps: Number(form.reps),
      weight: parseFloat(form.weight),
      duration_minutes: Number(form.duration_minutes),
      workout_date: form.workout_date,
      notes: form.notes || null,
    }
    // Admin can optionally assign to another user
    if (admin && form.user_id) {
      payload.user_id = Number(form.user_id)
    }

    try {
      await API.post('/workouts', payload)
      setSuccess('Workout added successfully!')
      setTimeout(() => navigate('/workouts'), 1000)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container form-page">
      <div className="form-card">
        <div className="page-header">
          <h2>Add Workout</h2>
          <Link to="/workouts" className="btn btn-secondary">← Back</Link>
        </div>

        <AlertMessage message={error} type="error" />
        <AlertMessage message={success} type="success" />

        <form onSubmit={handleSubmit}>
          {admin && (
            <div className="form-group">
              <label>Assign to User (optional — defaults to you)</label>
              <select name="user_id" value={form.user_id} onChange={handleChange}>
                <option value="">-- My workout --</option>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>{u.username} ({u.role})</option>
                ))}
              </select>
            </div>
          )}

          <div className="form-group">
            <label>Exercise *</label>
            <select name="exercise_id" value={form.exercise_id} onChange={handleChange} required>
              <option value="">-- Select Exercise --</option>
              {exercises.map((ex) => (
                <option key={ex.id} value={ex.id}>
                  {ex.name} — {ex.muscle_group} ({ex.difficulty})
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Sets *</label>
              <input
                type="number"
                name="sets"
                min="1"
                placeholder="e.g. 3"
                value={form.sets}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Reps *</label>
              <input
                type="number"
                name="reps"
                min="1"
                placeholder="e.g. 10"
                value={form.reps}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Weight (kg) *</label>
              <input
                type="number"
                name="weight"
                min="0"
                step="0.5"
                placeholder="e.g. 60 (use 0 for bodyweight)"
                value={form.weight}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Duration (minutes) *</label>
              <input
                type="number"
                name="duration_minutes"
                min="1"
                placeholder="e.g. 45"
                value={form.duration_minutes}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Workout Date *</label>
            <input
              type="date"
              name="workout_date"
              value={form.workout_date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Notes (optional)</label>
            <textarea
              name="notes"
              placeholder="Any notes about this workout session..."
              value={form.notes}
              onChange={handleChange}
              rows={3}
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving...' : 'Add Workout'}
            </button>
            <Link to="/workouts" className="btn btn-secondary">Cancel</Link>
          </div>
        </form>
      </div>
    </div>
  )
}
