<template>
  <div class="hub-view">
    <!-- Header -->
    <div class="hub-section-header">
      <h1 class="section-title">Developer Dev Tools</h1>
      <p class="section-desc">
        Aplikacja Streamlit z modułami Jira, Confluence, IAM, TeamCity i Informatica.
        Wybierz tryb podglądu poniżej.
      </p>
    </div>

    <!-- Przyciski trybu -->
    <div class="mode-toggle">
      <button
        class="mode-btn"
        :class="{ active: mode === 'embed' }"
        @click="mode = 'embed'"
        :disabled="loading"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
        </svg>
        Osadzony (iframe)
      </button>
      <button
        class="mode-btn"
        :class="{ active: mode === 'launch' }"
        @click="mode = 'launch'"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
        Karta uruchamiania
      </button>
    </div>

    <!-- TRYB: Osadzony iframe -->
    <template v-if="mode === 'embed'">
      <!-- Status bar -->
      <div class="embed-status">
        <span class="status-dot" :class="statusClass"></span>
        <span>{{ statusText }}</span>
        <button
          v-if="iframeError"
          class="btn-retry"
          @click="reloadIframe"
        >
          {{ isExternal ? 'Resetuj do lokalnego' : 'Spróbuj zewnętrznego' }}
        </button>
        <a
          :href="streamlitSource"
          target="_blank"
          class="btn-external"
          title="Otwórz w nowej karcie"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
        </a>
      </div>

      <!-- Loader -->
      <div v-if="loading" class="embed-loader">
        <div class="loader-spinner"></div>
        <span>Ładowanie Streamlit…</span>
      </div>

      <!-- Iframe -->
      <div class="embed-container" :class="{ hidden: loading }">
        <iframe
          ref="iframeRef"
          :src="streamlitSource"
          class="streamlit-iframe"
          frameborder="0"
          sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
          @load="onIframeLoad"
          @error="onIframeError"
        ></iframe>
      </div>
    </template>

    <!-- TRYB: Karta uruchamiania (dotychczasowy widok) -->
    <template v-if="mode === 'launch'">
      <div class="streamlit-launch">
        <div class="launch-card">
          <div class="launch-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#00c853" stroke-width="1.5">
              <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
            </svg>
          </div>
          <h2>DDT — Streamlit</h2>
          <p>Pełna aplikacja DDT dostępna jako osobna aplikacja Streamlit.<br>
          Zawiera: Jira, Confluence, IAM, TeamCity, Informatica.<br>
          Dane wyświetlane przez <code>st.write()</code>, <code>st.dataframe()</code>, <code>st.plotly_chart()</code>.</p>

          <div class="launch-actions">
            <button class="btn-launch" @click="openStreamlit">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
              Otwórz DDT Streamlit
            </button>

            <button
              class="btn-check"
              @click="checkStreamlit"
              :class="{ alive: isAlive }"
            >
              <span class="check-dot"></span>
              {{ isAlive ? 'Streamlit online' : 'Sprawdź status' }}
            </button>
          </div>

          <div v-if="lastCheck" class="check-result" :class="{ error: !isAlive }">
            {{ isAlive ? '✓ Serwer Streamlit odpowiada' : '✗ Serwer nie odpowiada — uruchom: streamlit run streamlit_app.py --server.port 8501' }}
          </div>
        </div>

        <div class="module-list">
          <div class="mini-card" v-for="mod in modules" :key="mod.name">
            <div class="mini-icon" v-html="mod.icon"></div>
            <div>
              <div class="mini-name">{{ mod.name }}</div>
              <div class="mini-desc">{{ mod.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Stopka -->
    <div class="embed-footer">
      <span class="footer-ver">DataHub Streamlit | v0.5.0</span>
      <span class="footer-hint">{{ streamlitSource }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ---- Konfiguracja ----
// Jeśli Streamlit proxy nie działa, ustaw zewnętrzny URL (np. Streamlit Community Cloud)
const STREAMLIT_LOCAL = '/streamlit/'
const STREAMLIT_EXTERNAL = import.meta.env.VITE_STREAMLIT_URL || ''

// ---- Stan ----
const mode = ref('embed')           // 'embed' | 'launch'
const loading = ref(true)
const iframeError = ref(false)
const useExternal = ref(false)
const isAlive = ref(false)
const lastCheck = ref(false)
const iframeRef = ref(null)

const streamlitSource = computed(() =>
  useExternal.value && STREAMLIT_EXTERNAL
    ? STREAMLIT_EXTERNAL
    : STREAMLIT_LOCAL
)

const isExternal = computed(() =>
  useExternal.value && !!STREAMLIT_EXTERNAL
)

const statusClass = computed(() => {
  if (loading.value) return 'loading'
  if (iframeError.value) return 'error'
  return 'online'
})

const statusText = computed(() => {
  if (loading.value) return 'Ładowanie Streamlit…'
  if (iframeError.value) return 'Streamlit nie odpowiada — sprawdź czy serwer działa'
  return `Streamlit online${useExternal.value ? ' (zewnętrzny)' : ' (lokalny proxy)'}`
})

// ---- Metody ----

function openStreamlit() {
  window.open('/streamlit/', '_blank')
}

function onIframeLoad() {
  loading.value = false
  iframeError.value = false
}

function onIframeError() {
  loading.value = false
  iframeError.value = true
}

function reloadIframe() {
  if (useExternal.value) {
    useExternal.value = false
  } else if (STREAMLIT_EXTERNAL) {
    useExternal.value = true
  }
  // Wymuszenie przeładowania iframe przez zmianę klucza
  loading.value = true
  iframeError.value = false
  // Force re-render iframe
  const iframe = iframeRef.value
  if (iframe) {
    iframe.src = streamlitSource.value
  }
}

async function checkStreamlit() {
  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 3000)
    const res = await fetch('/streamlit/', { signal: controller.signal })
    clearTimeout(timeout)
    isAlive.value = res.ok || res.status === 200
  } catch {
    isAlive.value = false
  }
  lastCheck.value = true
}

// Auto-check on mount (dla trybu launch)
onMounted(() => {
  checkStreamlit()
})

const modules = [
  { name: 'Jira', desc: 'Zadania, sprinty, workflow', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2684ff" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/></svg>' },
  { name: 'Confluence', desc: 'Dokumentacja i wiki', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00b8d9" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>' },
  { name: 'IAM', desc: 'Dostęp, role, MFA', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00c853" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>' },
  { name: 'TeamCity', desc: 'CI/CD, buildy', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00e5ff" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>' },
  { name: 'Informatica', desc: 'ETL, workflow', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ff6d00" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>' },
]
</script>

<style scoped>
.hub-view {
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Header */
.hub-section-header { margin-bottom: 4px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 600px; }

/* Mode toggle */
.mode-toggle {
  display: flex;
  gap: 8px;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}

.mode-btn:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
}

.mode-btn.active {
  background: rgba(0, 200, 83, 0.08);
  border-color: #00c853;
  color: #00c853;
}

.mode-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Embed status bar */
.embed-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff5252;
  flex-shrink: 0;
}

.status-dot.online {
  background: #00c853;
}

.status-dot.loading {
  background: #ff9100;
  animation: pulse 1.2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.status-dot.error {
  background: #ff5252;
}

.btn-retry {
  margin-left: auto;
  padding: 6px 14px;
  border-radius: 6px;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  transition: all 0.15s;
}

.btn-retry:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.btn-external {
  display: flex;
  align-items: center;
  padding: 6px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
  text-decoration: none;
}

.btn-external:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

/* Loader */
.embed-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 80px 0;
  color: var(--text-muted);
  font-size: 14px;
}

.loader-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color);
  border-top-color: #00c853;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Iframe container */
.embed-container {
  flex: 1;
  min-height: 0;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-primary);
}

.embed-container.hidden {
  display: none;
}

.streamlit-iframe {
  width: 100%;
  height: 70vh;
  min-height: 500px;
  display: block;
  background: #fff;
}

/* Footer */
.embed-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  font-size: 11px;
  color: var(--text-muted);
}

.footer-hint {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  opacity: 0.6;
}

/* ============ TRYB LAUNCH (dotychczasowy widok) ============ */
.streamlit-launch {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.launch-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 32px;
}

.launch-icon {
  margin-bottom: 16px;
}

.launch-card h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.launch-card p {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0 0 20px 0;
}

.launch-card code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  background: var(--bg-hover);
  padding: 2px 6px;
  border-radius: 4px;
  color: #00c853;
}

.launch-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-launch {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: 10px;
  background: linear-gradient(135deg, #00c853, #00e676);
  color: #000;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
}

.btn-launch:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 200, 83, 0.3);
}

.btn-check {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}

.btn-check:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
}

.btn-check.alive {
  border-color: #00c853;
  color: #00c853;
}

.check-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-muted);
}

.btn-check.alive .check-dot {
  background: #00c853;
}

.check-result {
  margin-top: 12px;
  font-size: 13px;
  color: #00c853;
  padding: 10px 16px;
  background: rgba(0, 200, 83, 0.05);
  border: 1px solid rgba(0, 200, 83, 0.15);
  border-radius: 8px;
}

.check-result.error {
  color: #ff5252;
  background: rgba(255, 82, 82, 0.05);
  border-color: rgba(255, 82, 82, 0.15);
}

/* Module list */
.module-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.mini-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
}

.mini-icon {
  flex-shrink: 0;
  display: flex;
}

.mini-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.mini-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}
</style>
