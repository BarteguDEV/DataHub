<template>
  <header class="app-header">
    <div class="header-left">
      <!-- Przycisk powrotu do hub select -->
      <button
        v-if="showBack"
        class="header-btn back-btn"
        @click="goBack"
        title="Powrót do wyboru huba"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/>
        </svg>
      </button>

      <!-- Breadcrumb / nawigacja -->
      <div class="header-breadcrumb">
        <router-link to="/" class="crumb-home" title="Wybierz hub">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        </router-link>
        <span v-if="hubName" class="crumb-sep">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6"/>
          </svg>
        </span>
        <span v-if="hubName" class="crumb-current">{{ hubName }}</span>
      </div>

      <!-- Szybki przełącznik hubów (zastępuje sidebar) -->
      <div class="hub-switcher" v-if="showBack">
        <button class="hub-switcher-btn" @click.stop="showHubMenu = !showHubMenu" title="Przełącz hub">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
          </svg>
        </button>
        <div v-if="showHubMenu" class="hub-dropdown" @click.stop>
          <router-link
            v-for="h in hubs"
            :key="h.name"
            :to="{ name: h.name }"
            class="hub-dropdown-item"
            :class="{ active: route.name === h.name }"
            @click="showHubMenu = false"
          >
            <span class="hub-dot" :style="{ background: h.color }"></span>
            <span class="hub-label">{{ h.label }}</span>
            <span class="hub-badge" v-if="h.badge">{{ h.badge }}</span>
          </router-link>
        </div>
      </div>
    </div>

    <div class="header-right">
      <!-- Status backendu + wersja -->
      <div class="header-chip backend-indicator" :class="{ online: backendOnline }">
        <span class="chip-dot"></span>
        <span class="chip-label">FastAPI</span>
      </div>
      <div
        v-if="streamlitOnline !== null"
        class="header-chip streamlit-indicator"
        :class="{ online: streamlitOnline }"
        title="Status Streamlit"
      >
        <span class="chip-dot"></span>
        <span class="chip-label">Streamlit</span>
      </div>
      <div class="header-chip version-chip">
        <span class="chip-label">{{ appVersion }}</span>
      </div>

      <!-- Slider szerokości -->
      <div class="width-slider" title="Dopasuj szerokość widoku">
        <svg class="ws-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/>
          <line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/>
        </svg>
        <input
          type="range"
          class="ws-range"
          min="800"
          max="1600"
          step="50"
          :value="contentWidth"
          @input="setWidth(Number($event.target.value))"
        />
        <span class="ws-label">{{ contentWidth }}</span>
      </div>

      <!-- Użytkownik -->
      <div class="header-user">
        <button class="user-btn" @click.stop="showMenu = !showMenu" title="Menu użytkownika">
          <span class="user-avatar-sm">{{ user.initials }}</span>
          <span class="user-info-sm">
            <span class="user-name-sm">{{ user.username }}</span>
            <span class="user-role-sm">{{ user.role }}</span>
          </span>
          <svg
            class="user-chevron"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            :class="{ rotated: showMenu }"
          >
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>

        <!-- Dropdown -->
        <div v-if="showMenu" class="user-dropdown" @click.stop>
          <div class="dropdown-header">
            <div class="dropdown-avatar">{{ user.initials }}</div>
            <div>
              <div class="dropdown-name">{{ user.username }}</div>
              <div class="dropdown-login">Zalogowano: {{ user.loginTime }}</div>
            </div>
          </div>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item about-item" @click.stop="showAbout = true; showMenu = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
            About me
          </button>
          <button class="dropdown-item" @click.stop="handleLogout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Wyloguj
          </button>
        </div>
      </div>
    </div>

    <!-- === ABOUT ME MODAL === -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="showAbout" class="about-overlay" @click.self="showAbout = false">
          <div class="about-card">
            <!-- Avatar banner -->
            <div class="about-banner">
              <div class="about-avatar-wrapper">
                <span class="about-avatar-text">{{ user.initials }}</span>
              </div>
              <div class="about-banner-label">
                <svg class="about-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                </svg>
                <span>{{ user.username }}</span>
              </div>
            </div>

            <div class="about-body">
              <h2 class="about-name">{{ user.username }}</h2>
              <p class="about-role">{{ user.role }}</p>
              <p class="about-desc">DataHub — portal integracyjny. Odpowiedzialny za migrację systemów i rozwój narzędzi wewnętrznych.</p>

              <div class="about-info">
                <div class="about-info-row">
                  <svg class="about-info-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
                  </svg>
                  <span>DataHub Portal</span>
                </div>
                <div class="about-info-row">
                  <svg class="about-info-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z"/><circle cx="12" cy="10" r="3"/>
                  </svg>
                  <span>Bartegu</span>
                </div>
                <div class="about-info-row">
                  <svg class="about-info-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
                  </svg>
                  <span>{{ user.username }}@datahub.local</span>
                </div>
              </div>
            </div>

            <button class="about-close-btn" @click="showAbout = false">Zamknij</button>
          </div>
        </div>
      </transition>
    </Teleport>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'
import { useVersion } from '@/stores/version'
import { useContentWidth } from '@/stores/width'

const route = useRoute()
const router = useRouter()
const { state, logout } = useAuth()
const { appVersion, fetchVersion } = useVersion()
const { contentWidth, setWidth } = useContentWidth()

const showMenu = ref(false)
const showHubMenu = ref(false)
const backendOnline = ref(false)
const showAbout = ref(false)

// Streamlit status — emitowany z DdtHubView przez zdarzenie lub prosty fetch
const streamlitOnline = ref(null)

onMounted(async () => {
  // Sprawdź czy Streamlit live
  try {
    const ctrl = new AbortController()
    setTimeout(() => ctrl.abort(), 3000)
    const res = await fetch('/streamlit/', { signal: ctrl.signal })
    streamlitOnline.value = res.ok || res.status === 200
  } catch {
    streamlitOnline.value = false
  }
})

const hubs = [
  { name: 'DdtHub', label: 'Developers Hub', color: '#00c853', badge: 'Streamlit' },
  { name: 'BusinessHub', label: 'Business Hub', color: '#ff9100', badge: 'KPI' },
  { name: 'AiHub', label: 'AI Hub', color: '#536dfe', badge: 'New' },
]

const showBack = computed(() => {
  return route.name !== 'HubSelect'
})

const hubName = computed(() => {
  const names = {
    DdtHub: 'Developers Hub',
    BusinessHub: 'Business Hub',
    AiHub: 'AI Hub',
  }
  return names[route.name] || null
})

const user = computed(() => state.user || { initials: '??', username: '—', role: '—', loginTime: '—' })

function goBack() {
  router.push({ name: 'HubSelect' })
}

async function handleLogout() {
  showMenu.value = false
  await logout()
  router.push({ name: 'Login' })
}

onMounted(async () => {
  backendOnline.value = !!state.isAuthenticated
  await fetchVersion()
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})

function closeDropdown(e) {
  if (showMenu.value) showMenu.value = false
  if (showHubMenu.value) showHubMenu.value = false
}

</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 24px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
  z-index: 50;
}

/* Lewa strona */
.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
}

.header-btn:hover {
  background: var(--bg-hover);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.header-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-left: 4px;
}

.crumb-home {
  display: flex;
  align-items: center;
  color: var(--text-muted);
  transition: color 0.15s;
}

.crumb-home:hover {
  color: var(--accent-primary);
}

.crumb-sep {
  display: flex;
  align-items: center;
  color: var(--border-color);
}

.crumb-current {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

/* Prawa strona */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
}

.chip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ff5252;
  transition: background 0.3s;
}

.backend-indicator.online .chip-dot {
  background: #00c853;
}
.streamlit-indicator .chip-dot {
  background: #ff5252;
}
.streamlit-indicator.online .chip-dot {
  background: #00e5ff;
}

.version-chip {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 10px;
}

.chip-label {
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* User */
.header-user {
  position: relative;
  display: flex;
  align-items: center;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 10px 6px 6px;
  border-radius: 8px;
  background: none;
  border: 1px solid transparent;
  color: inherit;
  font: inherit;
  cursor: pointer;
  transition: background 0.15s;
}

.user-btn:hover {
  background: var(--bg-hover);
  border-color: var(--border-color);
}

.user-avatar-sm {
  width: 30px;
  height: 30px;
  border-radius: 7px;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #000;
  flex-shrink: 0;
}

.user-info-sm {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.user-name-sm {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-role-sm {
  font-size: 11px;
  color: var(--text-muted);
}

.user-chevron {
  color: var(--text-muted);
  transition: transform 0.2s;
}

.user-chevron.rotated {
  transform: rotate(180deg);
}

/* Dropdown */
.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 240px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  z-index: 200;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.dropdown-avatar {
  width: 38px;
  height: 38px;
  border-radius: 9px;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #000;
  flex-shrink: 0;
}

.dropdown-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.dropdown-login {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.dropdown-divider {
  height: 1px;
  background: var(--border-color);
  margin: 0 16px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}

.dropdown-item:hover {
  background: var(--bg-hover);
  color: #ff5252;
}

/* Transitions */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Hub switcher — zastępuje sidebar */
.hub-switcher {
  position: relative;
  margin-left: 8px;
}

.hub-switcher-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
}

.hub-switcher-btn:hover {
  background: var(--bg-hover);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.hub-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 200px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  z-index: 200;
  padding: 6px;
}

.hub-dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s;
}

.hub-dropdown-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.hub-dropdown-item.active {
  background: var(--bg-hover);
  color: var(--accent-primary);
}

.hub-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.hub-label {
  flex: 1;
}

.hub-badge {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 6px;
  border-radius: 4px;
  background: var(--bg-hover);
  color: var(--text-muted);
}

/* ────────── Szerokość (slider) ────────── */
.width-slider {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 4px;
}

.ws-icon {
  color: var(--text-muted);
  flex-shrink: 0;
  opacity: 0.6;
}

.ws-range {
  -webkit-appearance: none;
  appearance: none;
  width: 72px;
  height: 4px;
  border-radius: 100px;
  background: var(--border-color);
  outline: none;
  cursor: pointer;
  transition: background 0.15s;
}

.ws-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #536dfe;
  border: 2px solid var(--bg-card);
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}

.ws-range::-webkit-slider-thumb:hover {
  transform: scale(1.25);
  box-shadow: 0 0 0 4px rgba(83, 109, 254, 0.2);
}

.ws-range::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #536dfe;
  border: 2px solid var(--bg-card);
  cursor: pointer;
}

.ws-range:hover {
  background: rgba(255, 255, 255, 0.12);
}

.ws-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
  min-width: 28px;
  text-align: right;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

/* ────────── About item w dropdownie ────────── */
.about-item {
  transition: all 0.15s;
}
.about-item:hover {
  background: var(--bg-hover);
  color: var(--accent-primary) !important;
}

/* ────────── ABOUT ME MODAL ────────── */
.about-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.about-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

.about-banner {
  height: 120px;
  background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(0,229,255,0.1));
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 16px 20px;
}

.about-avatar-wrapper {
  position: absolute;
  bottom: -32px;
  left: 20px;
  width: 64px;
  height: 64px;
  border-radius: 14px;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid var(--bg-card);
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}

.about-avatar-text {
  font-size: 20px;
  font-weight: 700;
  color: #000;
}

.about-banner-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 600;
  margin-left: 0;
}
.about-icon {
  color: var(--accent-primary);
}

.about-body {
  padding: 48px 20px 20px;
}

.about-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.about-role {
  font-size: 12px;
  font-weight: 600;
  color: var(--accent-primary);
  margin: 4px 0 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.about-desc {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0 0 16px;
}

.about-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.about-info-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  padding: 6px 0;
  border-bottom: 1px solid var(--border-color);
}
.about-info-row:last-child { border: none; }

.about-info-icon {
  color: var(--text-muted);
  flex-shrink: 0;
}

.about-close-btn {
  width: calc(100% - 40px);
  margin: 0 20px 16px;
  padding: 10px;
  border-radius: 8px;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}
.about-close-btn:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

/* Modal transitions */
.modal-enter-active { transition: opacity 0.2s ease; }
.modal-leave-active { transition: opacity 0.15s ease; }
.modal-enter-from,
.modal-leave-to { opacity: 0; }
.modal-enter-active .about-card { animation: modalIn 0.25s ease; }
.modal-leave-active .about-card { animation: modalOut 0.15s ease; }
@keyframes modalIn {
  from { transform: scale(0.95) translateY(10px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes modalOut {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(0.95); opacity: 0; }
}
</style>
