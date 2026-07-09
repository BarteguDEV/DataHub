<template>
  <div class="login-page">
    <!-- Tło animowane — siatka + cząsteczki -->
    <div class="bg-grid"></div>
    <div class="bg-particles">
      <div
        v-for="(style, i) in particles"
        :key="i"
        class="particle"
        :class="{ 'is-star': i % 2 === 0 }"
        :style="style"
      ></div>
    </div>
    <div class="bg-orbs">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
    </div>

    <!-- Panel logowania -->
    <div class="login-container">
      <div class="login-card">
        <!-- Logo -->
        <div class="login-logo">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="logo-icon">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
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

      <!-- Statystyki -->
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
        <div class="stat-item">
          <span class="stat-num">8</span>
          <span class="stat-label">Systemy</span>
        </div>
      </div>
    </div>

    <!-- === Loading rotator — dolny prawy róg === -->
    <div class="lr-card">
      <div class="lr-loader">
        <p>loading</p>
        <div class="lr-words">
          <span class="lr-word">huby</span>
          <span class="lr-word">raporty</span>
          <span class="lr-word">dane</span>
          <span class="lr-word">integracje</span>
          <span class="lr-word">huby</span>
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

// Pre-generowane style cząsteczek — stabilne, nie zmieniają się przy re-renderze
function generateParticleStyle(i) {
  const isStar = i % 2 === 0
  const base = isStar ? 4 : 2
  const extra = Math.random() * (isStar ? 6 : 3)
  const size = base + extra
  const x = Math.random() * 100
  const y = Math.random() * 100
  const delay = Math.random() * 8
  const duration = 5 + Math.random() * 8
  const opacity = isStar ? 0.3 + Math.random() * 0.5 : 0.2 + Math.random() * 0.3
  const driftX = -30 + Math.random() * 60
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${x}%`,
    top: `${y}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
    opacity,
    '--drift-x': `${driftX}px`,
  }
}

const particles = Array.from({ length: 80 }, (_, i) => generateParticleStyle(i))
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #07090e;
  overflow: hidden;
}

/* ====================================
   ANIMOWANE TŁO
   ==================================== */

/* Siatka */
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 200, 83, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 200, 83, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 60% 60% at 50% 50%, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 60% 60% at 50% 50%, black 30%, transparent 70%);
}

/* Cząsteczki i gwiazdy */
.bg-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: #00c853;
  box-shadow: 0 0 4px rgba(0, 200, 83, 0.3);
  animation: float-up linear infinite;
  will-change: transform, opacity;
}

.particle.is-star {
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  clip-path: polygon(
    50% 0%, 61% 35%, 98% 35%, 68% 57%,
    79% 91%, 50% 70%, 21% 91%, 32% 57%,
    2% 35%, 39% 35%
  );
  background: linear-gradient(135deg, #00c853, #69f0ae);
  filter: drop-shadow(0 0 3px rgba(0, 200, 83, 0.5));
  animation-name: float-up-star;
}

.particle.is-star::after {
  content: '';
  position: absolute;
  inset: -50%;
  background: radial-gradient(circle, rgba(0, 200, 83, 0.15), transparent 70%);
  pointer-events: none;
}

@keyframes float-up {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  50% {
    opacity: 1;
  }
  70% {
    opacity: 0.2;
  }
  100% {
    transform: translateY(-100vh) translateX(40px);
    opacity: 0;
  }
}

@keyframes float-up-star {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg) scale(0.6);
    opacity: 0;
  }
  10% {
    opacity: 1;
    transform: translateY(0) translateX(0) rotate(20deg) scale(1);
  }
  40% {
    transform: translateY(-40vh) translateX(var(--drift-x)) rotate(180deg) scale(1.1);
    opacity: 1;
  }
  65% {
    opacity: 0.2;
  }
  100% {
    transform: translateY(-100vh) translateX(var(--drift-x)) rotate(360deg) scale(0.3);
    opacity: 0;
  }
}

/* Kule świetlne */
.bg-orbs {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  animation: orb-move 20s ease-in-out infinite alternate;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: rgba(0, 200, 83, 0.06);
  top: -10%;
  left: -10%;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: rgba(0, 229, 255, 0.05);
  bottom: -10%;
  right: -10%;
  animation-delay: -7s;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: rgba(83, 109, 254, 0.04);
  top: 40%;
  left: 50%;
  animation-delay: -14s;
}

@keyframes orb-move {
  0% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(60px, -40px) scale(1.1); }
  66% { transform: translate(-30px, 50px) scale(0.9); }
  100% { transform: translate(40px, -20px) scale(1.05); }
}

/* ====================================
   KARTA LOGOWANIA
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
  background: rgba(22, 24, 31, 0.8);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
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

.logo-icon {
  color: #00c853;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 22px;
  font-weight: 700;
  color: #e8eaed;
}

.logo-title .accent {
  color: #00c853;
}

.logo-sub {
  font-size: 11px;
  color: rgba(232, 234, 237, 0.4);
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
  color: #e8eaed;
  margin: 0;
}

.form-desc {
  font-size: 13px;
  color: rgba(232, 234, 237, 0.5);
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
  color: rgba(232, 234, 237, 0.6);
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
  color: rgba(232, 234, 237, 0.3);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  background: rgba(11, 13, 17, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: #e8eaed;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  outline: none;
  transition: all 0.2s;
}

.input-wrapper input::placeholder {
  color: rgba(232, 234, 237, 0.25);
}

.input-wrapper input:focus {
  border-color: #00c853;
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.1);
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
  background: linear-gradient(135deg, #00c853, #00e676);
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
  color: rgba(232, 234, 237, 0.2);
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
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
  border: 1px solid rgba(255,255,255,0.06);
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
  color: #00c853;
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

/* ====================================
   STATYSTYKI — flat cards
   ==================================== */
.login-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Kafel z cienkim borderem */
.stat-item {
  background: rgba(22, 24, 31, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 18px 28px;
  text-align: center;
}

.stat-num {
  display: block;
  font-size: 30px;
  font-weight: 700;
  color: #00c853;
  line-height: 1;
}

.stat-label {
  font-size: 11px;
  color: rgba(232, 234, 237, 0.45);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 4px;
  display: block;
}
</style>
