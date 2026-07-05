/**
 * Auth store — stan autoryzacji z persystencją w sessionStorage.
 * Zbindowany z API Flask (/api/login, /api/logout, /api/me).
 */
import { reactive } from 'vue'
import { loginUser, logoutUser, getMe } from '../api.js'

const STORAGE_KEY = 'datahub_auth'

function loadFromStorage() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (raw) {
      const data = JSON.parse(raw)
      if (data && data.user && data.isAuthenticated) {
        return data
      }
    }
  } catch {
    // ignore
  }
  return null
}

function saveToStorage(user) {
  try {
    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ user, isAuthenticated: true })
    )
  } catch {
    // ignore
  }
}

function clearStorage() {
  try {
    sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
}

const saved = loadFromStorage()

const state = reactive({
  user: saved?.user ?? null,
  isAuthenticated: saved?.isAuthenticated ?? false,
})

export function useAuth() {
  /**
   * Logowanie przez API.
   * Zwraca obiekt odpowiedzi API.
   */
  async function login(username, password) {
    const res = await loginUser(username, password)
    const user = {
      id: res.user.id,
      username: res.user.username,
      role: res.user.role || 'Developer',
      initials: res.user.initials || computeInitials(res.user.username),
      loginTime: new Date().toLocaleTimeString('pl-PL'),
    }
    state.user = user
    state.isAuthenticated = true
    saveToStorage(user)
    return res
  }

  /**
   * Wylogowanie przez API.
   */
  async function logout() {
    try {
      await logoutUser()
    } catch {
      // ignore — i tak czyścimy stan lokalny
    }
    state.user = null
    state.isAuthenticated = false
    clearStorage()
  }

  /**
   * Inicjalizacja przy starcie aplikacji.
   * Sprawdza czy sesja serwerowa jest nadal aktywna.
   * Jeśli nie — czyści stan, ale nie przekierowuje (robi to router guard).
   */
  async function initialize() {
    // Jeśli mamy coś w storage, najpierw sprawdź czy sesja Flask żyje
    if (state.isAuthenticated) {
      try {
        const me = await getMe()
        // Uzupełnij dane jeśli API zwróciło więcej
        if (me.username && state.user) {
          state.user.username = me.username
          state.user.id = me.id
        }
        return
      } catch {
        // Sesja Flask nie żyje — czyścimy stan
        state.user = null
        state.isAuthenticated = false
        clearStorage()
      }
    }
  }

  return {
    state,
    login,
    logout,
    initialize,
  }
}

function computeInitials(username) {
  return username
    .split(/[\s.]+/)
    .map(s => s[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
