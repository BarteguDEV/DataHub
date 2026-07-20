/**
 * Theme store — globalny przełącznik motywu jasny/ciemny.
 * Stan utrzymywany w module (singleton), persistowany w localStorage.
 */
import { ref } from 'vue'

const STORAGE_KEY = 'kopa-nexus-theme-mode'
const isDark = ref(true) // domyślnie ciemny

function loadSaved() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved === 'light') return false
    if (saved === 'dark') return true
  } catch { /* ignore */ }
  return true
}

function apply(mode) {
  const dark = mode === undefined ? isDark.value : mode
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  isDark.value = dark
  try { localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light') } catch { /* ignore */ }
}

// Inicjalizacja przy imporcie
apply(loadSaved())

export function useTheme() {
  function toggle() {
    apply(!isDark.value)
  }

  function setDark(dark) {
    apply(dark)
  }

  return {
    isDark,
    toggle,
    setDark,
  }
}
