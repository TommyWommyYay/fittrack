/**
 * Simple inline confirmation modal for delete actions.
 * Shown when isOpen is true.
 */
export default function ConfirmDeleteModal({ isOpen, message, onConfirm, onCancel }) {
  if (!isOpen) return null

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>Confirm Delete</h3>
        <p>{message || 'Are you sure you want to delete this record? This action cannot be undone.'}</p>
        <div className="modal-actions">
          <button className="btn btn-danger" onClick={onConfirm}>Yes, Delete</button>
          <button className="btn btn-secondary" onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
  )
}
