/**
 * Version store — pobiera wersję aplikacji z /api/health.
 * Pozwala odróżnić starą wersję na Azure od nowej po deploy.
 */
import { ref } from 'vue'

const appVersion = ref('—')
const apiVersion = ref('—')
const loaded = ref(false)

export function useVersion() {
  async function fetchVersion() {
    try {
      const res = await fetch('/api/health')
      const data = await res.json()
      appVersion.value = data.version || '—'
      apiVersion.value = 'ok'
    } catch {
      appVersion.value = '—'
      apiVersion.value = 'offline'
    }
    loaded.value = true
  }

  return {
    appVersion,
    apiVersion,
    loaded,
    fetchVersion,
  }
}
