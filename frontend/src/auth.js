/**
 * Auth helpers — store/retrieve the JWT token and user object in localStorage.
 */

export function getToken() {
  return localStorage.getItem('fittrack_token')
}

export function getUser() {
  const user = localStorage.getItem('fittrack_user')
  return user ? JSON.parse(user) : null
}

export function saveAuth(token, user) {
  localStorage.setItem('fittrack_token', token)
  localStorage.setItem('fittrack_user', JSON.stringify(user))
}

export function clearAuth() {
  localStorage.removeItem('fittrack_token')
  localStorage.removeItem('fittrack_user')
}

export function isLoggedIn() {
  return !!getToken()
}

export function isAdmin() {
  const user = getUser()
  return user?.role === 'admin'
}
