import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import API, { getErrorMessage } from '../api'
import { isAdmin } from '../auth'
import AlertMessage from '../components/AlertMessage'
import ConfirmDeleteModal from '../components/ConfirmDeleteModal'

export default function Exercises() {
  const admin = isAdmin()
  const [exercises, setExercises] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [deleteTarget, setDeleteTarget] = useState(null)

  useEffect(() => {
    loadExercises()
  }, [])

  async function loadExercises() {
    try {
      const res = await API.get('/exercises')
      setExercises(res.data)
    } catch (err) {
      setError('Could not load exercises.')
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete() {
    try {
      await API.delete(`/exercises/${deleteTarget.id}`)
      setSuccess(`Exercise "${deleteTarget.name}" deleted successfully.`)
      setDeleteTarget(null)
      loadExercises()
    } catch (err) {
      setError(getErrorMessage(err))
      setDeleteTarget(null)
    }
  }

  const difficultyColour = { Beginner: '#28a745', Intermediate: '#ffc107', Advanced: '#dc3545' }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Exercise Library</h1>
        {admin && <Link to="/exercises/add" className="btn btn-primary">+ Add Exercise</Link>}
      </div>

      <AlertMessage message={error} type="error" />
      <AlertMessage message={success} type="success" />

      {loading ? (
        <p>Loading exercises...</p>
      ) : exercises.length === 0 ? (
        <p>No exercises found.</p>
      ) : (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Muscle Group</th>
                <th>Difficulty</th>
                <th>Equipment</th>
                <th>Description</th>
                {admin && <th>Actions</th>}
              </tr>
            </thead>
            <tbody>
              {exercises.map((ex) => (
                <tr key={ex.id}>
                  <td>{ex.id}</td>
                  <td><strong>{ex.name}</strong></td>
                  <td>{ex.muscle_group}</td>
                  <td>
                    <span
                      className="badge"
                      style={{ backgroundColor: difficultyColour[ex.difficulty] || '#6c757d' }}
                    >
                      {ex.difficulty}
                    </span>
                  </td>
                  <td>{ex.equipment}</td>
                  <td className="description-cell">{ex.description}</td>
                  {admin && (
                    <td className="actions-cell">
                      <Link to={`/exercises/edit/${ex.id}`} className="btn btn-sm btn-warning">Edit</Link>
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => setDeleteTarget(ex)}
                      >
                        Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <ConfirmDeleteModal
        isOpen={!!deleteTarget}
        message={`Are you sure you want to delete "${deleteTarget?.name}"? This cannot be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
