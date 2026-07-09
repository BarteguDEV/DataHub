/**
 * Auth store — JWT + localStorage.
 * Token: localStorage (datahub_token)
 * User data: sessionStorage (datahub_user)
 */
import { reactive } from 'vue'
import { loginUser, logoutUser, getMe, getToken, setToken, clearToken } from '../api.js'

const USER_KEY = 'datahub_user'

function loadUser() {
  try {
    const raw = sessionStorage.getItem(USER_KEY)
    if (raw) {
      const user = JSON.parse(raw)
      if (user && user.username) return user
    }
  } catch {
    // ignore
  }
  return null
}

function saveUser(user) {
  try {
    sessionStorage.setItem(USER_KEY, JSON.stringify(user))
  } catch {
    // ignore
  }
}

function clearUser() {
  try {
    sessionStorage.removeItem(USER_KEY)
  } catch {
    // ignore
  }
}

const savedUser = loadUser()
const hasToken = !!getToken()

const state = reactive({
  user: savedUser,
  isAuthenticated: hasToken && !!savedUser,
})

export function useAuth() {
  async function login(username, password, systemId) {
    const res = await loginUser(username, password, systemId)

    // Zapisz JWT
    setToken(res.access_token)

    // Zapisz usera
    const user = {
      id: res.user.id,
      username: res.user.username,
      role: res.user.role || 'Developer',
      initials: res.user.initials || computeInitials(res.user.username),
      system: res.system || systemId || null,
      loginTime: new Date().toLocaleTimeString('pl-PL'),
    }
    state.user = user
    state.isAuthenticated = true
    saveUser(user)
    return res
  }

  async function logout() {
    try {
      await logoutUser()
    } catch {
      // ignore — i tak czyścimy stan lokalny
    }
    clearToken()
    clearUser()
    state.user = null
    state.isAuthenticated = false
  }

  async function initialize() {
    // Jeśli mamy token, sprawdź czy jest nadal ważny przez /api/me
    if (getToken()) {
      try {
        const me = await getMe()
        const user = {
          id: me.id,
          username: me.username,
          role: me.role || 'Developer',
          initials: me.initials || computeInitials(me.username),
          loginTime: new Date().toLocaleTimeString('pl-PL'),
        }
        state.user = user
        state.isAuthenticated = true
        saveUser(user)
        return
      } catch {
        // Token nieważny — czyścimy wszystko
        clearToken()
        clearUser()
        state.user = null
        state.isAuthenticated = false
      }
    } else {
      state.user = null
      state.isAuthenticated = false
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
