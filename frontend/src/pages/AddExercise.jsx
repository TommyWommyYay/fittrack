import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import API, { getErrorMessage } from '../api'
import AlertMessage from '../components/AlertMessage'

export default function AddExercise() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '',
    muscle_group: '',
    difficulty: '',
    equipment: '',
    description: '',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function validate() {
    if (!form.name.trim()) return 'Exercise name is required.'
    if (!form.muscle_group.trim()) return 'Muscle group is required.'
    if (!form.difficulty) return 'Please select a difficulty level.'
    if (!form.equipment.trim()) return 'Equipment is required.'
    if (form.description.trim().length < 10) return 'Description must be at least 10 characters.'
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
    try {
      await API.post('/exercises', form)
      setSuccess('Exercise added successfully!')
      setTimeout(() => navigate('/exercises'), 1000)
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
          <h2>Add New Exercise</h2>
          <Link to="/exercises" className="btn btn-secondary">← Back</Link>
        </div>

        <AlertMessage message={error} type="error" />
        <AlertMessage message={success} type="success" />

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Exercise Name *</label>
            <input
              type="text"
              name="name"
              placeholder="e.g. Bench Press"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Muscle Group *</label>
            <input
              type="text"
              name="muscle_group"
              placeholder="e.g. Chest, Back, Legs"
              value={form.muscle_group}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Difficulty *</label>
            <select name="difficulty" value={form.difficulty} onChange={handleChange} required>
              <option value="">-- Select Difficulty --</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>

          <div className="form-group">
            <label>Equipment *</label>
            <input
              type="text"
              name="equipment"
              placeholder="e.g. Barbell, Dumbbells, Bodyweight"
              value={form.equipment}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Description * (min. 10 characters)</label>
            <textarea
              name="description"
              placeholder="Describe the exercise technique and muscles targeted."
              value={form.description}
              onChange={handleChange}
              rows={4}
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving...' : 'Save Exercise'}
            </button>
            <Link to="/exercises" className="btn btn-secondary">Cancel</Link>
          </div>
        </form>
      </div>
    </div>
  )
}
