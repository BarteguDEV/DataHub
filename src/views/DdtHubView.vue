<template>
  <div class="hub-view">
    <div class="hub-section-header">
      <h1 class="section-title">Developer Dev Tools</h1>
      <p class="section-desc">
        Aplikacja Streamlit z modułami Jira, Confluence, IAM, TeamCity i Informatica.
        Kliknij poniżej, aby uruchomić.
      </p>
    </div>

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
          {{ isAlive ? '✓ Serwer Streamlit odpowiada' : '✗ Serwer nie odpowiada — uruchom: streamlit run ddt_streamlit_app.py --server.port 8501' }}
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
  </div>
</template>

<script setup>
import { ref } from 'vue'

const STREAMLIT_PORT = 8501
const streamlitUrl = `http://localhost:${STREAMLIT_PORT}`
const isAlive = ref(false)
const lastCheck = ref(false)

function openStreamlit() {
  window.location.href = streamlitUrl
}

async function checkStreamlit() {
  try {
    const res = await fetch(`http://localhost:${STREAMLIT_PORT}/healthz`, { mode: 'no-cors' })
    // no-cors means we can't read response, but if it doesn't throw, server is up
    isAlive.value = true
  } catch {
    // Try fetching the streamlit page itself
    try {
      const res = await fetch(`http://localhost:${STREAMLIT_PORT}`, { mode: 'no-cors' })
      isAlive.value = true
    } catch {
      isAlive.value = false
    }
  }
  lastCheck.value = true
}

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
  max-width: 900px;
}

.hub-section-header {
  margin-bottom: 28px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.section-desc {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
}

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
