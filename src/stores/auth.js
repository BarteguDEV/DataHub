/**
 * Auth store — prosty stan autoryzacji na potrzeby POC.
 * Stan zapisywany w sessionStorage, dzięki czemu:
 *   - przeżywa przeładowania strony (np. powrót ze Streamlit do portalu)
 *   - ginie po zamknięciu karty (login wymagany przy nowej sesji)
 *
 * W docelowej wersji zastąpiony integracją z IAM/SSO.
 */
import { reactive } from 'vue'

const STORAGE_KEY = 'portal_auth'

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
    // ignore (private mode, quota exceeded, etc.)
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
  function login(username, role) {
    const user = {
      username,
      role,
      initials: username
        .split(/[\s.]+/)
        .map(s => s[0])
        .join('')
        .toUpperCase()
        .slice(0, 2),
      loginTime: new Date().toLocaleTimeString('pl-PL'),
    }
    state.user = user
    state.isAuthenticated = true
    saveToStorage(user)
  }

  function logout() {
    state.user = null
    state.isAuthenticated = false
    clearStorage()
  }

  return {
    state,
    login,
    logout,
  }
}
