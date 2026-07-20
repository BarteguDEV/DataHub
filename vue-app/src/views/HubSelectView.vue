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
        </div>
        <span class="bottom-text">{{ hub.bottomText }}</span>
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
    title: 'Developers Hub',
    bottomText: 'DEVELOPERS HUB',
    desc: 'Dashboard Streamlit symulujący migrację 5 systemów (Jira, Confluence, IAM, TeamCity, Informatica) z interaktywnymi prognozami i kontrolkami.',
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
    name: 'BUSINESS',
    cls: 'business',
    route: 'BusinessHub',
    title: 'Business Hub',
    bottomText: 'BUSINESS HUB',
    desc: 'KPI, SLA procesów ETL, lista alertów i aktywności w czasie rzeczywistym. Wszystko oparte na symulowanych danych z API — gotowe szkielet pod docelowe integracje.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>',
    modules: [
      { name: 'KPI Dashboard', author: 'Bartegu', version: 'v1.0.0', status: 'active' },
      { name: 'ETL Workflow Monitor', author: 'Bartegu', version: 'v1.0.0', status: 'active' },
      { name: 'SLA Compliance', author: 'Bartegu', version: 'v1.0.0', status: 'active' },
      { name: 'Alerty i aktywność', author: 'Bartegu', version: 'v1.0.0', status: 'active' },
    ],
  },
  {
    name: 'AI',
    cls: 'ai',
    route: 'AiHub',
    title: 'AI Hub',
    bottomText: 'AI HUB',
    desc: '15 raportów AI z analizą SQL, ETL, jakości danych, ryzyka wdrożenia i dokumentacji. Każdy z metryką, ustaleniami i rekomendacjami.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/></svg>',
    modules: [
      { name: 'SQL Performance Advisor', author: 'A. Kowalski', version: 'v2.3.1', status: 'active' },
      { name: 'ETL Dependency Analyzer', author: 'J. Kamiński', version: 'v2.0.2', status: 'active' },
      { name: 'Deployment Risk Analyzer', author: 'A. Wójcik', version: 'v1.2.0', status: 'active' },
      { name: 'Data Quality Analyzer', author: 'Ł. Dąbrowski', version: 'v2.0.0', status: 'active' },
      { name: 'Documentation Generator', author: 'K. Kozłowski', version: 'v2.1.0', status: 'active' },
    ],
  },
  {
    name: 'PLANNING',
    cls: 'planning',
    route: 'PlanningHub',
    title: 'Planning Hub',
    bottomText: 'PLANNING HUB',
    desc: 'Zapisuj tematy ze spotkań, układaj priorytety na liście rankingowej lub w macierzy 2×2. Przeciągaj karty, grupuj, planuj.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    modules: [
      { name: 'Quick-Add Topics', author: 'Bartegu', version: 'v0.1.0', status: 'beta' },
      { name: 'Priority Ranking', author: 'Bartegu', version: 'v0.1.0', status: 'beta' },
      { name: 'Value-Effort Matrix', author: 'Bartegu', version: 'v0.1.0', status: 'beta' },
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
  max-width: var(--content-width, 1100px);
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

/* ──────── KAFELEK HUBU ──────── */
.hub-tile {
  position: relative;
  min-width: 0;
  border-radius: 16px;
  cursor: pointer;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  transition: all 0.5s ease-in-out;
}

.hub-tile:hover {
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* Akcent górny (zachowany, ale overflow nie obcina go — ma własne zaokrąglenie) */
.tile-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 16px 16px 0 0;
  overflow: hidden;
}

.hub-tile.ddt .tile-accent { background: linear-gradient(90deg, #00c853, #00e5ff); }
.hub-tile.business .tile-accent { background: linear-gradient(90deg, #ff9100, #ff3d00); }
.hub-tile.ai .tile-accent { background: linear-gradient(90deg, #536dfe, #d500f9); }
.hub-tile.planning .tile-accent { background: linear-gradient(90deg, #ffd54f, #ff6f00); }

/* ──────── RAMKA ANIMOWANA (WYŁĄCZONA) ──────── */

/* ──────── TEKST NA DOLE (wjeżdża na hover) ──────── */
.bottom-text {
  position: absolute;
  left: 50%;
  bottom: 14px;
  transform: translateX(-50%);
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 8px;
  opacity: 0;
  transition: all 0.5s ease-in-out;
  pointer-events: none;
  white-space: nowrap;
  font-weight: 600;
}

.hub-tile.planning .bottom-text { color: #ffb300; }
.hub-tile.ddt .bottom-text { color: #00c853; }
.hub-tile.business .bottom-text { color: #ff9100; }
.hub-tile.ai .bottom-text { color: #536dfe; }

.hub-tile:hover .bottom-text {
  letter-spacing: 4px;
  opacity: 1;
}

/* ──────── ZAWARTOŚĆ KAFELKA ──────── */
.tile-content {
  position: relative;
  padding: 28px 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.5s ease-in-out;
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

.hub-tile.planning .tile-icon { color: #ffb300; }
.hub-tile.ddt .tile-icon { color: #00c853; }
.hub-tile.business .tile-icon { color: #ff9100; }
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

/* Lista modułów w karcie */
.module-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin: 4px 0;
  max-height: 170px;
  overflow-y: auto;
  padding-right: 4px;
}

.module-list::-webkit-scrollbar {
  width: 4px;
}
.module-list::-webkit-scrollbar-track {
  background: transparent;
}
.module-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 100px;
}
.module-list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
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

.tile-glow {
  display: none;
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
