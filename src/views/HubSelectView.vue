<template>
  <div class="hub-select">
    <!-- Górna sekcja powitalna -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-badge">PORTAL INTEGRACYJNY</div>
        <h1 class="welcome-title">
          Witaj, <span class="text-accent">{{ user.username }}</span>
        </h1>
        <p class="welcome-desc">
          Wybierz jeden z hubów, aby przejść do dedykowanych narzędzi.
          Każdy hub to osobny zestaw funkcjonalności — od narzędzi developerskich,
          przez raportowanie biznesowe, po innowacje AI.
        </p>
      </div>

      <div class="welcome-meta">
        <div class="meta-row">
          <span class="meta-label">Rola</span>
          <span class="meta-value">{{ user.role }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Zalogowano</span>
          <span class="meta-value">{{ user.loginTime }}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Backend API</span>
          <span class="meta-value" :class="{ online: backendOnline }">
            {{ backendOnline ? 'Online' : 'Offline' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Siatka hubów -->
    <div class="hub-grid">
      <!-- DDT -->
      <article class="hub-tile ddt" @click="navigate('DdtHub')">
        <div class="tile-accent"></div>
        <div class="tile-content">
          <div class="tile-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
            </svg>
          </div>
          <h2 class="tile-title">DDT — Developer Dev Tools</h2>
          <p class="tile-desc">
            Integracje z Jira, Confluence, IAM, TeamCity, Informatica PowerCenter
            oraz zestaw narzędzi developerskich uruchamianych przez Streamlit.
          </p>
          <div class="tile-stats">
            <span class="tile-stat">
              <strong>8</strong> modułów
            </span>
            <span class="tile-stat">
              <strong>Streamlit</strong>
            </span>
          </div>
          <div class="tile-footer">
            <span class="tile-action">Przejdź do huba</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
        <div class="tile-glow"></div>
      </article>

      <!-- APEX -->
      <article class="hub-tile apex" @click="navigate('ApexHub')">
        <div class="tile-accent"></div>
        <div class="tile-content">
          <div class="tile-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>
            </svg>
          </div>
          <h2 class="tile-title">APEX — Business Intelligence</h2>
          <p class="tile-desc">
            Dashboardy KPI, raporty codzienne, statystyki systemowe i helicopter view
            na całą organizację. Dane z Oracle i Snowflake.
          </p>
          <div class="tile-stats">
            <span class="tile-stat">
              <strong>24</strong> dashboardy
            </span>
            <span class="tile-stat">
              <strong>Oracle + Snowflake</strong>
            </span>
          </div>
          <div class="tile-footer">
            <span class="tile-action">Przejdź do huba</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
        <div class="tile-glow"></div>
      </article>

      <!-- AI -->
      <article class="hub-tile ai" @click="navigate('AiHub')">
        <div class="tile-accent"></div>
        <div class="tile-content">
          <div class="tile-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          <h2 class="tile-title">AI Innovation Lab</h2>
          <p class="tile-desc">
            Koncepty AI zgodne z regulacjami bankowymi, raporty HTML, eksperymenty
            i rozwiązania do użytku wewnętrznego.
          </p>
          <div class="tile-stats">
            <span class="tile-stat">
              <strong>8</strong> konceptów
            </span>
            <span class="tile-stat">
              <strong>Raporty HTML</strong>
            </span>
          </div>
          <div class="tile-footer">
            <span class="tile-action">Przejdź do huba</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
        <div class="tile-glow"></div>
      </article>
    </div>

    <!-- Dolny pasek statusu -->
    <div class="status-bar">
      <div class="status-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
        </svg>
        <span>Ostatnia aktywność: dziś {{ user.loginTime }}</span>
      </div>
      <div class="status-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        <span>Środowisko: testowe (bankowe)</span>
      </div>
      <div class="status-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
        <span>v0.1.0 POC</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'

const router = useRouter()
const { state } = useAuth()

const DDT_API_PORT = import.meta.env.VITE_DDT_API_PORT || 5000
const backendOnline = ref(false)

const user = state

function navigate(name) {
  router.push({ name })
}

async function checkBackend() {
  try {
    const res = await fetch(`http://localhost:${DDT_API_PORT}/api/health`)
    const data = await res.json()
    backendOnline.value = data.status === 'ok'
  } catch {
    backendOnline.value = false
  }
}

onMounted(checkBackend)
</script>

<style scoped>
.hub-select {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

/* ====================================
   SEKCJA POWITALNA
   ==================================== */

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 32px;
}

.welcome-content {
  flex: 1;
}

.welcome-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  color: var(--accent-primary);
  padding: 4px 14px;
  border-radius: 100px;
  background: rgba(0, 200, 83, 0.1);
  border: 1px solid rgba(0, 200, 83, 0.15);
  margin-bottom: 16px;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.text-accent {
  color: var(--accent-primary);
}

.welcome-desc {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
  max-width: 550px;
}

.welcome-meta {
  flex-shrink: 0;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px 20px;
  min-width: 180px;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
}

.meta-row + .meta-row {
  border-top: 1px solid var(--border-color);
}

.meta-label {
  font-size: 12px;
  color: var(--text-muted);
}

.meta-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.meta-value.online {
  color: #00c853;
}

/* ====================================
   SIATKA HUBÓW
   ==================================== */

.hub-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.hub-tile {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.hub-tile:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
}

/* Akcent koloru na górze kafelka */
.tile-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.hub-tile.ddt .tile-accent { background: linear-gradient(90deg, #00c853, #00e5ff); }
.hub-tile.apex .tile-accent { background: linear-gradient(90deg, #ff9100, #ff3d00); }
.hub-tile.ai .tile-accent { background: linear-gradient(90deg, #536dfe, #d500f9); }

/* Glow na hover */
.tile-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  opacity: 0;
  transition: opacity 0.5s;
  pointer-events: none;
}

.hub-tile.ddt:hover .tile-glow {
  background: radial-gradient(ellipse at 30% 20%, rgba(0, 200, 83, 0.06) 0%, transparent 60%);
  opacity: 1;
}

.hub-tile.apex:hover .tile-glow {
  background: radial-gradient(ellipse at 30% 20%, rgba(255, 145, 0, 0.06) 0%, transparent 60%);
  opacity: 1;
}

.hub-tile.ai:hover .tile-glow {
  background: radial-gradient(ellipse at 30% 20%, rgba(83, 109, 254, 0.06) 0%, transparent 60%);
  opacity: 1;
}

.tile-content {
  position: relative;
  z-index: 2;
  padding: 32px 28px 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.tile-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
}

.hub-tile.ddt .tile-icon { color: #00c853; }
.hub-tile.apex .tile-icon { color: #ff9100; }
.hub-tile.ai .tile-icon { color: #536dfe; }

.tile-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.tile-desc {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
}

.tile-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.tile-stat {
  font-size: 12px;
  color: var(--text-muted);
}

.tile-stat strong {
  color: var(--text-primary);
  font-weight: 600;
}

.tile-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--accent-primary);
  margin-top: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.hub-tile:hover .tile-footer svg {
  transform: translateX(4px);
  transition: transform 0.2s;
}

/* ====================================
   DOLNY PASEK
   ==================================== */

.status-bar {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 14px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
}

.status-item svg {
  opacity: 0.5;
}
</style>
