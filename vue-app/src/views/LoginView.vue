<template>
  <div class="login-page">
    <!-- Tło — gradient + siatka + glow -->
    <div class="bg-gradient"></div>
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>

    <!-- Panel logowania -->
    <div class="login-container">
      <div class="login-card">
        <!-- Logo -->
        <div class="login-logo">
          <div class="logo-mark">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
          </div>
          <div class="logo-text">
            <span class="logo-title">Data<span class="accent">Hub</span></span>
            <span class="logo-sub">Portal integracyjny</span>
          </div>
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
          <span class="footer-env">FastAPI + Vue.js</span>
          <span class="footer-dev">developer: Bartegu</span>
        </div>
      </div>

      <!-- Dekoracyjne statystyki -->
      <div class="login-stats">
        <div class="stat-item">
          <span class="stat-num">3</span>
          <span class="stat-label">Huby</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">12+</span>
          <span class="stat-label">Moduły</span>
        </div>
        <div class="stat-item">
          <span class="stat-num">6</span>
          <span class="stat-label">Integracje</span>
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

const router = useRouter()
const { login } = useAuth()

const { appVersion, fetchVersion } = useVersion()

const username = ref('')
const password = ref('')
const error = ref('')
const loggingIn = ref(false)

onMounted(fetchVersion)

const canLogin = computed(() => username.value.trim().length > 0 && password.value.length > 0)

async function handleLogin() {
  if (!canLogin.value || loggingIn.value) return

  error.value = ''
  loggingIn.value = true

  try {
    await login(username.value.trim(), password.value)
    router.push({ name: 'HubSelect' })
  } catch (e) {
    error.value = e.message
  } finally {
    loggingIn.value = false
  }
}

function particleStyle(i) {
  const size = 2 + Math.random() * 4
  const x = Math.random() * 100
  const y = Math.random() * 100
  const delay = Math.random() * 8
  const duration = 12 + Math.random() * 18
  const opacity = 0.15 + Math.random() * 0.35
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${x}%`,
    top: `${y}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
    opacity,
  }
}
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  overflow: hidden;
}

/* ====================================
   TŁO — RED NOIR
   ==================================== */

.bg-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, #1a0505, #000);
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 60% 60% at 50% 50%, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 60% 60% at 50% 50%, black 30%, transparent 70%);
}

.bg-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 600px;
  height: 600px;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(239, 35, 60, 0.08), transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

/* ====================================
   KARTA LOGOWANIA — GLASSMORPHISM
   ==================================== */

.login-container {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 60px;
}

.login-card {
  width: 400px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.6);
}

/* Logo */
.login-logo {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-mark {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(239, 35, 60, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef233c;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}

.logo-title .accent {
  color: #ef233c;
}

.logo-sub {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.35);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  font-weight: 500;
  margin-top: 2px;
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
  color: #fff;
  margin: 0;
}

.form-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.45);
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
  color: rgba(255, 255, 255, 0.5);
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
  color: rgba(255, 255, 255, 0.25);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  outline: none;
  transition: all 0.2s;
}

.input-wrapper input::placeholder {
  color: rgba(255, 255, 255, 0.2);
}

.input-wrapper input:focus {
  border-color: #ef233c;
  box-shadow: 0 0 0 3px rgba(239, 35, 60, 0.12);
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
  position: relative;
  padding: 14px;
  background: #ef233c;
  border: none;
  border-radius: 10px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 4px;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 0, rgba(255,255,255,0.15), transparent 70%);
  pointer-events: none;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(239, 35, 60, 0.35);
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
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: #fff;
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
  color: rgba(255, 255, 255, 0.2);
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
}

/* Statystyki boczne */
.login-stats {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stat-item {
  text-align: center;
  padding: 24px 32px;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
}

.stat-num {
  display: block;
  font-size: 36px;
  font-weight: 700;
  color: #ef233c;
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 6px;
  display: block;
}
</style>
