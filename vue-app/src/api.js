const API_BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Błąd serwera')
  return data
}

export function loginUser(username, password) {
  return request('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export function registerUser(username, password) {
  return request('/register', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export function logoutUser() {
  return request('/logout', { method: 'POST' })
}

export function getMe() {
  return request('/me')
}
