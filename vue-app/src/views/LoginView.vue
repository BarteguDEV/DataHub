<template>
  <div class="login-page">
    <!-- Split layout: 50/50 -->
    <div class="split-layout">
      <!-- LEWY PANEL: Branding + systemy -->
      <div class="left-panel">
        <div class="brand-section">
          <div class="brand-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" class="brand-svg">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
          </div>
          <h1 class="brand-name">Kopa<span class="brand-accent">Nexus</span></h1>
          <p class="brand-tagline">Raportowanie instrumentów pochodnych.</p>
          <p class="brand-systems">Zintegrowane systemy: EMIR_3 / SFTR / WITIP / ARM</p>
        </div>

        <!-- Przełącznik motywu jasny/ciemny -->
        <div class="theme-toggle-wrapper">
          <button class="theme-toggle" @click="theme.toggle()" :title="theme.isDark.value ? 'Tryb jasny' : 'Tryb ciemny'">
            <!-- Sun icon -->
            <svg v-if="!theme.isDark.value" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/>
              <line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
            <!-- Moon icon -->
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
            <span class="theme-toggle-label">{{ theme.isDark.value ? 'Ciemny' : 'Jasny' }}</span>
          </button>
        </div>

        <div class="system-cards">
          <div v-for="sys in systemInfo" :key="sys.id" class="sys-card">
            <div class="sys-card-header">
              <span class="sys-name">{{ sys.label }}</span>
              <span class="sys-status" :class="sys.online ? 'status-online' : 'status-offline'">
                <span class="status-dot"></span>
                {{ sys.online ? 'Online' : 'Offline' }}
              </span>
            </div>
            <div class="sys-card-body">
              <span class="sys-version-label">Wersja systemu</span>
              <span class="sys-version">{{ sys.version }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- PRAWY PANEL: Logowanie -->
      <div class="right-panel">
        <div class="login-card">
          <!-- Dekoracyjny element wizualny -->
          <div class="login-deco">
            <svg width="100%" height="80" viewBox="0 0 320 80" fill="none" xmlns="http://www.w3.org/2000/svg" class="deco-svg">
              <defs>
                <linearGradient id="decoGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="var(--accent-primary)" stop-opacity="0.35"/>
                  <stop offset="50%" stop-color="var(--accent-primary)" stop-opacity="0.12"/>
                  <stop offset="100%" stop-color="var(--accent-primary)" stop-opacity="0"/>
                </linearGradient>
              </defs>
              <!-- Łuki reprezentujące przepływ danych -->
              <path d="M10 65 Q40 10 80 40 Q120 70 160 30 Q200 -10 240 25 Q280 60 310 35" stroke="var(--accent-primary)" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.5"/>
              <path d="M20 70 Q50 25 90 50 Q130 75 170 40 Q210 5 250 35 Q290 65 310 45" stroke="var(--accent-primary)" stroke-width="1" stroke-linecap="round" fill="none" opacity="0.25"/>
              <!-- Kropki na przecięciach -->
              <circle cx="80" cy="40" r="4" fill="var(--accent-primary)" opacity="0.6"/>
              <circle cx="160" cy="30" r="3" fill="var(--accent-primary)" opacity="0.4"/>
              <circle cx="240" cy="25" r="5" fill="var(--accent-primary)" opacity="0.7"/>
              <circle cx="310" cy="35" r="2.5" fill="var(--accent-primary)" opacity="0.3"/>
              <!-- Wypełnienie pod krzywą -->
              <path d="M10 65 Q40 10 80 40 Q120 70 160 30 Q200 -10 240 25 Q280 60 310 35 V80 H10 Z" fill="url(#decoGrad)"/>
            </svg>
          </div>

          <!-- Formularz -->
          <div class="login-form">
            <h1 class="form-title">Witaj w portalu</h1>
            <p class="form-desc">Zaloguj się, aby uzyskać dostęp do hubów</p>

            <div class="input-group">
              <label for="username">Użytkownik</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                </svg>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  placeholder="np. admin"
                  autocomplete="username"
                  @keyup.enter="handleLogin"
                />
              </div>
            </div>

            <div class="input-group">
              <label for="password">Hasło</label>
              <div class="input-wrapper">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  @keyup.enter="handleLogin"
                />
              </div>
            </div>

            <div class="input-group">
              <label for="system">System</label>
              <div class="input-wrapper select-wrapper">
                <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
                <select id="system" v-model="systemId" class="select-input">
                  <option v-for="s in availableSystems" :key="s.id" :value="s.id">
                    {{ s.label }}
                  </option>
                </select>
              </div>
            </div>

            <p v-if="error" class="error-msg">{{ error }}</p>

            <button
              class="login-btn"
              :disabled="!canLogin || loggingIn"
              @click="handleLogin"
            >
              <span v-if="!loggingIn">Zaloguj się</span>
              <span v-else class="btn-loading">
                <span class="spinner"></span>
                Logowanie...
              </span>
            </button>
          </div>

          <!-- Stopka -->
          <div class="login-footer">
            <span class="footer-version">{{ appVersion }}</span>
            <span class="footer-env">FastAPI + Vue.js + Python</span>
            <span class="footer-dev">developer: Bartegu</span>
          </div>
        </div>
      </div>
    </div>

    <!-- === Loading rotator — dolny prawy róg === -->
    <div class="lr-card">
      <div class="lr-loader">
        <p>Ładuję</p>
        <div class="lr-words">
          <span class="lr-word">Nexus</span>
          <span class="lr-word">Raporty</span>
          <span class="lr-word">Baze Danych</span>
          <span class="lr-word">Integracje</span>
          <span class="lr-word">Nexus</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'
import { useVersion } from '@/stores/version'
import { useTheme } from '@/stores/theme'

const router = useRouter()
const { login } = useAuth()
const theme = useTheme()

const { appVersion, fetchVersion } = useVersion()

const username = ref('')
const password = ref('')
const systemId = ref('EMIR_3')
const error = ref('')
const loggingIn = ref(false)

const availableSystems = [
  { id: 'EMIR_3', label: 'EMIR_3' },
  { id: 'WITIP', label: 'WITIP' },
  { id: 'SFTR', label: 'SFTR' },
  { id: 'FATCRS', label: 'FATCRS' },
]

const systemInfo = [
  { id: 'EMIR_3', label: 'EMIR_3', version: '001.002.077', online: true },
  { id: 'SFTR',   label: 'SFTR',   version: '002.001.034', online: true },
  { id: 'WITIP',  label: 'WITIP',  version: '003.000.112', online: true },
  { id: 'ARM',    label: 'ARM',    version: '001.004.056', online: true },
]

onMounted(fetchVersion)

const canLogin = computed(() => username.value.trim().length > 0 && password.value.length > 0)

async function handleLogin() {
  if (!canLogin.value || loggingIn.value) return

  error.value = ''
  loggingIn.value = true

  try {
    await login(username.value.trim(), password.value, systemId.value)
    router.push({ name: 'HubSelect' })
  } catch (e) {
    error.value = e.message
  } finally {
    loggingIn.value = false
  }
}

</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ====================================
   SPLIT LAYOUT — 50/50
   ==================================== */

.split-layout {
  position: relative;
  z-index: 10;
  display: flex;
  width: 100%;
  max-width: 1360px;
  min-height: 100vh;
}

/* LEWY PANEL */
.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 80px 60px 80px 80px;
  gap: 48px;
}

.brand-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.brand-icon {
  margin-bottom: 12px;
}

.brand-svg {
  color: var(--accent-primary);
  width: 52px;
  height: 52px;
}

.brand-name {
  font-size: 56px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -2px;
  line-height: 1;
  margin: 0;
}

.brand-name .brand-accent {
  color: var(--accent-primary);
}

.brand-tagline {
  font-size: 18px;
  color: var(--text-secondary);
  font-weight: 400;
  margin: 6px 0 0 0;
  line-height: 1.4;
}

.brand-systems {
  font-size: 13px;
  color: var(--text-muted);
  margin: 2px 0 0 0;
  letter-spacing: 0.3px;
}

/* Theme toggle — jasny/ciemny */
.theme-toggle-wrapper {
  display: flex;
}

.theme-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  border-radius: 100px;
  padding: 6px 16px 6px 14px;
  cursor: pointer;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}

.theme-toggle:hover {
  background: var(--bg-active);
  border-color: var(--accent-primary);
  opacity: 0.8;
  color: var(--text-primary);
}

.theme-toggle svg {
  flex-shrink: 0;
}

.theme-toggle-label {
  white-space: nowrap;
}

/* System cards */
.system-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.sys-card {
  background: var(--bg-overlay-light);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color 0.2s, background 0.2s;
}

.sys-card:hover {
  background: var(--bg-overlay);
  border-color: rgba(0, 200, 83, 0.15);
}

.sys-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sys-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 0.3px;
}

.sys-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sys-status.status-online {
  color: var(--accent-primary);
}

.sys-status.status-offline {
  color: #ff5252;
}

.status-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 6px currentColor;
}

.sys-card-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sys-version-label {
  font-size: 10px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.sys-version {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  letter-spacing: 1px;
}

/* PRAWY PANEL */
.right-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-card {
  width: 400px;
  background: var(--bg-overlay);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 36px 40px 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  box-shadow: var(--card-shadow);
}

/* Dekoracyjny element */
.login-deco {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88px;
  margin-bottom: 4px;
}

.deco-svg {
  max-width: 320px;
  height: 80px;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.form-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: -12px 0 0 0;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  outline: none;
  transition: all 0.2s;
}

.input-wrapper input::placeholder {
  color: var(--text-muted);
}

.input-wrapper input:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.12);
}

.select-wrapper select {
  width: 100%;
  padding: 12px 14px 12px 42px;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  transition: all 0.2s;
}

.select-wrapper::after {
  content: '';
  position: absolute;
  right: 14px;
  width: 10px;
  height: 10px;
  border-right: 2px solid var(--text-muted);
  border-bottom: 2px solid var(--text-muted);
  transform: rotate(45deg);
  pointer-events: none;
  margin-top: -6px;
}

.select-wrapper select:hover {
  border-color: var(--accent-primary);
  opacity: 0.7;
}

.select-wrapper select:focus {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.12);
}

.error-msg {
  font-size: 13px;
  color: #ff5252;
  padding: 8px 12px;
  background: rgba(255, 82, 82, 0.08);
  border-radius: 6px;
  text-align: center;
}

/* Przycisk */
.login-btn {
  padding: 14px;
  background: var(--accent-gradient);
  border: none;
  border-radius: 10px;
  color: #000;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 4px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 200, 83, 0.3);
}

.login-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Footer */
.login-footer {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-muted);
  padding-top: 8px;
  border-top: 1px solid var(--border-color);
}

/* ====================================
   LOADING ROTATOR — dolny prawy róg
   ==================================== */
.lr-card {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 100;
  background: var(--bg-card, #16181f);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  padding: 0.6rem 1.2rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}
.lr-card:hover { opacity: 1; }

.lr-loader {
  color: var(--text-muted, rgba(232,234,237,0.4));
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  box-sizing: content-box;
  height: 22px;
  padding: 6px 8px;
  display: flex;
  border-radius: 8px;
}

.lr-loader p {
  margin: 0;
  line-height: 22px;
}

.lr-words {
  overflow: hidden;
  position: relative;
  height: 22px;
  margin-left: 6px;
}
.lr-words::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    var(--bg-card, #16181f) 10%,
    transparent 30%,
    transparent 70%,
    var(--bg-card, #16181f) 90%
  );
  z-index: 20;
  pointer-events: none;
}

.lr-word {
  display: block;
  height: 22px;
  line-height: 22px;
  padding-left: 4px;
  color: var(--accent-primary);
  animation: lr-spin 4s infinite;
}

@keyframes lr-spin {
  10%  { transform: translateY(-102%); }
  25%  { transform: translateY(-100%); }
  35%  { transform: translateY(-202%); }
  50%  { transform: translateY(-200%); }
  60%  { transform: translateY(-302%); }
  75%  { transform: translateY(-300%); }
  85%  { transform: translateY(-402%); }
  100% { transform: translateY(-400%); }
}

</style>
