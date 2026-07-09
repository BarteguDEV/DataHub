/**
 * API client — JWT auth.
 * Token przechowywany w localStorage, wysyłany jako Bearer token.
 */
const API_BASE = '/api'

const TOKEN_KEY = 'datahub_token'

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token) {
  try {
    localStorage.setItem(TOKEN_KEY, token)
  } catch {
    // ignore
  }
}

export function clearToken() {
  try {
    localStorage.removeItem(TOKEN_KEY)
  } catch {
    // ignore
  }
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...authHeaders(),
    ...options.headers,
  }
  const res = await fetch(`${API_BASE}${path}`, {
    headers,
    ...options,
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || data.error || 'Błąd serwera')
  return data
}

export function loginUser(username, password, systemId) {
  return request('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password, system: systemId }),
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
