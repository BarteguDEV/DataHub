/**
 * Width store — globalna kontrola szerokości treści.
 * Slider w headerze ustawia wartość, widoki czytają CSS variable.
 */
import { ref, watch } from 'vue'

const STORAGE_KEY = 'datahub-content-width'

function loadSaved() {
  try {
    return parseInt(localStorage.getItem(STORAGE_KEY) || '', 10) || 1100
  } catch {
    return 1100
  }
}

const contentWidth = ref(loadSaved())

// Zapis do localStorage i aktualizacja CSS Variable przy każdej zmianie
watch(contentWidth, (val) => {
  try {
    localStorage.setItem(STORAGE_KEY, String(val))
  } catch { /* ignore */ }
  document.documentElement.style.setProperty('--content-width', val + 'px')
})

export function useContentWidth() {
  function setWidth(px) {
    contentWidth.value = Math.max(800, Math.min(1900, px))
  }

  return {
    contentWidth,
    setWidth,
  }
}

// Inicjalizacja przy imporcie
document.documentElement.style.setProperty('--content-width', contentWidth.value + 'px')
