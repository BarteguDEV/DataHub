<template>
  <div class="app">
    <!-- ========== LOGIN ========== -->
    <div v-if="!isLoggedIn" class="login-page">
      <div class="bg-grid"></div>
      <div class="bg-glow"></div>

      <div class="login-card">
        <div class="card-header">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="logo">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
          <div>
            <h1 class="title">Data<span class="accent">Hub</span></h1>
            <p class="subtitle">Vue.js — Proof of Concept</p>
          </div>
        </div>

        <div class="card-body">
          <div class="input-group">
            <label for="user">Użytkownik</label>
            <input
              id="user"
              v-model="username"
              type="text"
              placeholder="np. admin"
              @keyup.enter="handleLogin"
            />
          </div>
          <div class="input-group">
            <label for="pass">Hasło</label>
            <input
              id="pass"
              v-model="password"
              type="password"
              placeholder="••••••••"
              @keyup.enter="handleLogin"
            />
          </div>

          <p v-if="error" class="error-msg">{{ error }}</p>

          <button
            class="btn"
            :disabled="!canLogin"
            @click="handleLogin"
          >
            Zaloguj się
          </button>
        </div>

        <div class="card-footer">
          <span>v0.1.0 POC</span>
          <span>Azure Static Web Apps</span>
        </div>
      </div>
    </div>

    <!-- ========== DASHBOARD ========== -->
    <div v-else class="dashboard">
      <nav class="navbar">
        <div class="nav-brand">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="logo">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
          <span>Data<span class="accent">Hub</span></span>
          <span class="badge">Vue POC</span>
        </div>
        <div class="nav-right">
          <span class="nav-user">{{ user }}</span>
          <button class="btn btn-sm" @click="handleLogout">Wyloguj</button>
        </div>
      </nav>

      <main class="main">
        <div class="welcome">
          <h1>Witaj, <span class="accent">{{ user }}</span></h1>
          <p>Vue.js działa na Azure Static Web Apps. POC zaliczony.</p>
        </div>

        <div class="cards">
          <div class="card">
            <span class="card-icon">⚡</span>
            <h3>Framework</h3>
            <p>Vue 3 + Vite — SPA bez routingu, jeden komponent.</p>
          </div>
          <div class="card">
            <span class="card-icon">☁️</span>
            <h3>Hosting</h3>
            <p>Azure Static Web Apps (Free). CI/CD z GitHub Actions.</p>
          </div>
          <div class="card">
            <span class="card-icon">✅</span>
            <h3>Status</h3>
            <p>Zalogowano: <strong>{{ user }}</strong></p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const username = ref('')
const password = ref('')
const isLoggedIn = ref(false)
const user = ref('')
const error = ref('')

const canLogin = computed(() => username.value.trim().length > 0)

function handleLogin() {
  error.value = ''
  if (!canLogin.value) return

  // POC — każde hasło przechodzi, byle niepuste
  if (!password.value) {
    error.value = 'Wpisz hasło'
    return
  }

  user.value = username.value.trim()
  isLoggedIn.value = true
}

function handleLogout() {
  isLoggedIn.value = false
  user.value = ''
  username.value = ''
  password.value = ''
}
</script>

<style>
/* ===== Reset & Base ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, sans-serif;
  background: #0b0d11;
  color: #e8eaed;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

.app { min-height: 100vh; }

.accent { color: #00c853; }

/* ===== LOGIN PAGE ===== */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: #07090e;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,200,83,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,200,83,0.04) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, black 30%, transparent 70%);
}

.bg-glow {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background: rgba(0,200,83,0.05);
  filter: blur(100px);
  top: -20%;
  right: -10%;
  animation: glow 10s ease-in-out infinite alternate;
}

@keyframes glow {
  0% { transform: translate(0, 0) scale(1); opacity: 0.5; }
  100% { transform: translate(-60px, 40px) scale(1.2); opacity: 1; }
}

.login-card {
  position: relative;
  z-index: 10;
  width: 380px;
  background: rgba(22,24,31,0.85);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 36px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  box-shadow: 0 24px 80px rgba(0,0,0,0.6);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo { color: #00c853; flex-shrink: 0; }

.title {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
}

.subtitle {
  font-size: 11px;
  color: rgba(232,234,237,0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 2px;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 11px;
  font-weight: 600;
  color: rgba(232,234,237,0.5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-group input {
  width: 100%;
  padding: 11px 14px;
  background: rgba(11,13,17,0.8);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  color: #e8eaed;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  outline: none;
  transition: border-color 0.2s;
}

.input-group input::placeholder { color: rgba(232,234,237,0.2); }
.input-group input:focus { border-color: #00c853; box-shadow: 0 0 0 3px rgba(0,200,83,0.1); }

.error-msg {
  font-size: 13px;
  color: #ff5252;
  padding: 8px 12px;
  background: rgba(255,82,82,0.08);
  border-radius: 6px;
  text-align: center;
}

.btn {
  padding: 12px;
  background: #00c853;
  border: none;
  border-radius: 8px;
  color: #000;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0,200,83,0.3);
}

.btn:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-sm { padding: 8px 16px; font-size: 13px; }

.card-footer {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: rgba(232,234,237,0.2);
  padding-top: 8px;
  border-top: 1px solid rgba(255,255,255,0.04);
}

/* ===== DASHBOARD ===== */
.dashboard { min-height: 100vh; display: flex; flex-direction: column; }

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
  background: #0f1117;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
}

.badge {
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 8px;
  background: rgba(0,200,83,0.12);
  color: #00c853;
  border-radius: 100px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.nav-user {
  font-size: 13px;
  font-weight: 500;
  color: rgba(232,234,237,0.7);
}

.main {
  flex: 1;
  max-width: 800px;
  margin: 0 auto;
  padding: 48px 24px;
  width: 100%;
}

.welcome { margin-bottom: 40px; }

.welcome h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}

.welcome p {
  font-size: 14px;
  color: rgba(232,234,237,0.55);
  line-height: 1.6;
}

.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.card {
  background: #16181f;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.2s;
}

.card:hover { transform: translateY(-2px); }

.card-icon { font-size: 24px; }

.card h3 {
  font-size: 15px;
  font-weight: 600;
}

.card p {
  font-size: 13px;
  color: rgba(232,234,237,0.5);
  line-height: 1.6;
}

.card strong { color: #e8eaed; }
</style>
