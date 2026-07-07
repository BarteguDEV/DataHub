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
      </div>
    </div>

    <!-- Siatka hubów -->
    <div class="hub-grid">
      <article
        v-for="hub in hubs"
        :key="hub.name"
        class="hub-tile"
        :class="hub.cls"
        @click="navigate(hub.route)"
      >
        <div class="tile-accent"></div>
        <div class="tile-content">
          <div class="tile-icon" v-html="hub.icon"></div>
          <h2 class="tile-title">{{ hub.title }}</h2>
          <p class="tile-desc">{{ hub.desc }}</p>

          <!-- Lista modułów z autorami i wersjami -->
          <div class="module-list">
            <div
              v-for="mod in hub.modules"
              :key="mod.name"
              class="module-row"
            >
              <span class="module-name">{{ mod.name }}</span>
              <span class="module-meta">
                <span class="module-author" :title="'Autor: ' + mod.author">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  {{ mod.author }}
                </span>
                <span class="module-version">{{ mod.version }}</span>
                <span class="module-status" :class="mod.status">{{ mod.status }}</span>
              </span>
            </div>
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
        <span>Środowisko: testowe</span>
      </div>
      <div class="status-item">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
        <span>{{ appVersion }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'
import { useVersion } from '@/stores/version'

const router = useRouter()
const { state } = useAuth()
const { appVersion, fetchVersion } = useVersion()
const user = state

const hubs = [
  {
    name: 'DDT',
    cls: 'ddt',
    route: 'DdtHub',
    title: 'DDT — Developer Dev Tools',
    desc: 'Integracje z Jira, Confluence, IAM, TeamCity, Informatica PowerCenter oraz zestaw narzędzi developerskich uruchamianych przez Streamlit.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    modules: [
      { name: 'Streamlit POC', author: 'Bartegu', version: 'v0.5.0', status: 'active' },
      { name: 'Jira Integration', author: 'Bartegu', version: 'v2.1.0', status: 'active' },
      { name: 'Confluence Sync', author: 'M. Kowalski', version: 'v1.0.3', status: 'active' },
      { name: 'IAM Tools', author: 'A. Nowak', version: 'v0.8.1', status: 'beta' },
      { name: 'TeamCity Dashboard', author: 'Bartegu', version: 'v1.2.0', status: 'active' },
      { name: 'Informatica PowerCenter', author: 'P. Adamski', version: 'v3.0.0', status: 'active' },
    ],
  },
  {
    name: 'APEX',
    cls: 'apex',
    route: 'ApexHub',
    title: 'APEX — Business Intelligence',
    desc: 'Dashboardy KPI, raporty codzienne, statystyki systemowe i helicopter view na całą organizację. Dane z Oracle i Snowflake.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>',
    modules: [
      { name: 'KPI Dashboard', author: 'M. Kowalski', version: 'v4.2.1', status: 'active' },
      { name: 'Oracle Reports', author: 'P. Adamski', version: 'v2.0.0', status: 'active' },
      { name: 'Snowflake Analytics', author: 'Bartegu', version: 'v1.5.0', status: 'active' },
      { name: 'SLA Monitor', author: 'M. Kowalski', version: 'v1.1.0', status: 'active' },
    ],
  },
  {
    name: 'AI',
    cls: 'ai',
    route: 'AiHub',
    title: 'AI Innovation Lab',
    desc: 'Koncepty AI zgodne z regulacjami bankowymi, raporty HTML, eksperymenty i rozwiązania do użytku wewnętrznego.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>',
    modules: [
      { name: 'SQL Lineage', author: 'Bartegu', version: 'v0.3.0', status: 'alpha' },
      { name: 'Auto Test Generator', author: 'A. Nowak', version: 'v0.2.0', status: 'alpha' },
      { name: 'Data Mapping', author: 'Bartegu', version: 'v0.1.0', status: 'concept' },
    ],
  },
]

onMounted(fetchVersion)

function navigate(name) {
  router.push({ name })
}
</script>

<style scoped>
.hub-select {
  width: 100%;
  max-width: 1100px;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
  gap: 40px;
}

.welcome-content {
  flex: 1;
}

.welcome-badge {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2px;
  color: var(--accent-primary);
  margin-bottom: 12px;
}

.welcome-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

.welcome-desc {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
}

.welcome-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-shrink: 0;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px 20px;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  gap: 32px;
  font-size: 13px;
}

.meta-label {
  color: var(--text-muted);
}

.meta-value {
  font-weight: 600;
  color: var(--text-primary);
}

/* Siatka hubów */
.hub-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.hub-tile {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  transition: all 0.3s ease;
}

.hub-tile:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

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

.tile-content {
  position: relative;
  padding: 28px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
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
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
}

.tile-stats {
  display: flex;
  gap: 16px;
}

.tile-stat {
  font-size: 12px;
  color: var(--text-muted);
}

.tile-stat strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* Lista modułów w karcie */
.module-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 4px 0;
}

.module-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  background: var(--bg-hover);
  transition: background 0.15s;
}

.module-row:hover {
  background: rgba(255, 255, 255, 0.04);
}

.module-name {
  font-weight: 500;
  color: var(--text-primary);
  flex-shrink: 0;
}

.module-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.module-author {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-muted);
  font-size: 11px;
}

.module-author svg {
  opacity: 0.5;
}

.module-version {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 10px;
  color: var(--text-muted);
  padding: 2px 5px;
  border-radius: 4px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
}

.module-status {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 6px;
  border-radius: 4px;
}

.module-status.active {
  background: rgba(0, 200, 83, 0.12);
  color: #00c853;
}

.module-status.beta {
  background: rgba(255, 145, 0, 0.12);
  color: #ff9100;
}

.module-status.alpha {
  background: rgba(83, 109, 254, 0.12);
  color: #536dfe;
}

.module-status.concept {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-muted);
}

.tile-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--accent-primary);
  margin-top: 4px;
}

.hub-tile:hover .tile-footer svg {
  transform: translateX(4px);
  transition: transform 0.2s ease;
}

.tile-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
  background: radial-gradient(ellipse at bottom right, rgba(0,200,83,0.06), transparent 60%);
}

.hub-tile:hover .tile-glow {
  opacity: 1;
}

/* Status bar */
.status-bar {
  display: flex;
  gap: 32px;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
}

.status-item svg {
  color: var(--text-muted);
  flex-shrink: 0;
}
</style>
