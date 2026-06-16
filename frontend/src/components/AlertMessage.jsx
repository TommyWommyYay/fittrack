/**
 * Reusable alert banner.
 * type: 'success' | 'error' | 'warning' | 'info'
 */
export default function AlertMessage({ message, type = 'info' }) {
  if (!message) return null

  const colours = {
    success: '#d4edda',
    error: '#f8d7da',
    warning: '#fff3cd',
    info: '#d1ecf1',
  }
  const borders = {
    success: '#28a745',
    error: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8',
  }

  return (
    <div
      style={{
        padding: '12px 16px',
        borderLeft: `4px solid ${borders[type] || borders.info}`,
        backgroundColor: colours[type] || colours.info,
        borderRadius: '4px',
        marginBottom: '16px',
        fontSize: '0.95rem',
      }}
    >
      {message}
    </div>
  )
}
