import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import API, { getErrorMessage } from '../api'
import { isAdmin } from '../auth'
import AlertMessage from '../components/AlertMessage'
import ConfirmDeleteModal from '../components/ConfirmDeleteModal'

export default function Workouts() {
  const admin = isAdmin()
  const [workouts, setWorkouts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [deleteTarget, setDeleteTarget] = useState(null)

  useEffect(() => {
    loadWorkouts()
  }, [])

  async function loadWorkouts() {
    try {
      const res = await API.get('/workouts')
      setWorkouts(res.data)
    } catch (err) {
      setError('Could not load workouts.')
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete() {
    try {
      await API.delete(`/workouts/${deleteTarget.id}`)
      setSuccess(`Workout #${deleteTarget.id} deleted successfully.`)
      setDeleteTarget(null)
      loadWorkouts()
    } catch (err) {
      setError(getErrorMessage(err))
      setDeleteTarget(null)
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>{admin ? 'All Workouts' : 'My Workouts'}</h1>
        <Link to="/workouts/add" className="btn btn-primary">+ Add Workout</Link>
      </div>

      <AlertMessage message={error} type="error" />
      <AlertMessage message={success} type="success" />

      {loading ? (
        <p>Loading workouts...</p>
      ) : workouts.length === 0 ? (
        <div className="empty-state">
          <p>No workouts found.</p>
          <Link to="/workouts/add" className="btn btn-primary">Add your first workout</Link>
        </div>
      ) : (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                {admin && <th>User</th>}
                <th>Exercise</th>
                <th>Muscle Group</th>
                <th>Sets</th>
                <th>Reps</th>
                <th>Weight (kg)</th>
                <th>Duration (min)</th>
                <th>Date</th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {workouts.map((w) => (
                <tr key={w.id}>
                  <td>{w.id}</td>
                  {admin && <td>{w.username}</td>}
                  <td><strong>{w.exercise_name}</strong></td>
                  <td>{w.muscle_group}</td>
                  <td>{w.sets}</td>
                  <td>{w.reps}</td>
                  <td>{w.weight}</td>
                  <td>{w.duration_minutes}</td>
                  <td>{w.workout_date}</td>
                  <td className="notes-cell">{w.notes || '—'}</td>
                  <td className="actions-cell">
                    <Link to={`/workouts/edit/${w.id}`} className="btn btn-sm btn-warning">Edit</Link>
                    {admin && (
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => setDeleteTarget(w)}
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <ConfirmDeleteModal
        isOpen={!!deleteTarget}
        message={`Are you sure you want to delete Workout #${deleteTarget?.id}? This cannot be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
