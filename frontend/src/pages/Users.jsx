import { useState, useEffect } from 'react'
import API, { getErrorMessage } from '../api'
import { getUser } from '../auth'
import AlertMessage from '../components/AlertMessage'
import ConfirmDeleteModal from '../components/ConfirmDeleteModal'

export default function Users() {
  const currentUser = getUser()
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [deleteTarget, setDeleteTarget] = useState(null)

  useEffect(() => {
    loadUsers()
  }, [])

  async function loadUsers() {
    try {
      const res = await API.get('/users')
      setUsers(res.data)
    } catch (err) {
      setError('Could not load users.')
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete() {
    try {
      await API.delete(`/users/${deleteTarget.id}`)
      setSuccess(`User "${deleteTarget.username}" deleted.`)
      setDeleteTarget(null)
      loadUsers()
    } catch (err) {
      setError(getErrorMessage(err))
      setDeleteTarget(null)
    }
  }

  function formatDate(dt) {
    return dt ? new Date(dt).toLocaleDateString() : '—'
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>User Management</h1>
        <span className="stat-label">{users.length} registered users</span>
      </div>

      <AlertMessage message={error} type="error" />
      <AlertMessage message={success} type="success" />

      {loading ? (
        <p>Loading users...</p>
      ) : (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Registered</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className={u.id === currentUser?.id ? 'current-user-row' : ''}>
                  <td>{u.id}</td>
                  <td>
                    <strong>{u.username}</strong>
                    {u.id === currentUser?.id && <span className="you-badge"> (you)</span>}
                  </td>
                  <td>{u.email}</td>
                  <td>
                    <span className={`role-badge ${u.role === 'admin' ? 'role-admin' : 'role-regular'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td>{formatDate(u.created_at)}</td>
                  <td className="actions-cell">
                    {u.id !== currentUser?.id && (
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => setDeleteTarget(u)}
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
        message={`Are you sure you want to delete user "${deleteTarget?.username}"? All their workout records will also be deleted.`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
