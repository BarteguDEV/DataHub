<template>
  <div class="login-page">
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>

    <div class="login-card">
      <div class="card-header">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="logo">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
        </svg>
        <div>
          <h1 class="title">Data<span class="accent">Hub</span></h1>
          <p class="subtitle">Rejestracja</p>
        </div>
      </div>

      <div class="card-body">
        <div class="input-group">
          <label for="user">Użytkownik</label>
          <input id="user" v-model="username" type="text" placeholder="np. admin" @keyup.enter="register" />
        </div>
        <div class="input-group">
          <label for="pass">Hasło</label>
          <input id="pass" v-model="password" type="password" placeholder="••••••••" @keyup.enter="confirm" />
        </div>
        <div class="input-group">
          <label for="confirm">Potwierdź hasło</label>
          <input id="confirm" v-model="confirmPass" type="password" placeholder="••••••••" @keyup.enter="register" />
        </div>

        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>

        <button class="btn" :disabled="!username.trim() || loading" @click="register">
          {{ loading ? 'Rejestracja...' : 'Utwórz konto' }}
        </button>

        <p class="register-link">
          Masz już konto?
          <router-link to="/">Zaloguj się</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { registerUser } from '../api.js'

const username = ref('')
const password = ref('')
const confirmPass = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function register() {
  error.value = ''
  success.value = ''
  if (!username.value.trim() || !password.value) {
    error.value = 'Uzupełnij wszystkie pola'
    return
  }
  if (password.value !== confirmPass.value) {
    error.value = 'Hasła nie są zgodne'
    return
  }
  loading.value = true
  try {
    await registerUser(username.value, password.value)
    success.value = 'Konto utworzone! Możesz się zalogować.'
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden; background: #07090e;
}

.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,200,83,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,200,83,0.04) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, black 30%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, black 30%, transparent 70%);
}

.bg-glow {
  position: absolute; width: 500px; height: 500px; border-radius: 50%;
  background: rgba(0,200,83,0.05); filter: blur(100px);
  top: -20%; right: -10%;
  animation: glow 10s ease-in-out infinite alternate;
}

@keyframes glow {
  0% { transform: translate(0,0) scale(1); opacity: 0.5; }
  100% { transform: translate(-60px,40px) scale(1.2); opacity: 1; }
}

.login-card {
  position: relative; z-index: 10; width: 380px;
  background: rgba(22,24,31,0.85); backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.08); border-radius: 16px;
  padding: 36px; display: flex; flex-direction: column; gap: 28px;
  box-shadow: 0 24px 80px rgba(0,0,0,0.6);
}

.card-header { display: flex; align-items: center; gap: 14px; }
.logo { color: #00c853; flex-shrink: 0; }
.title { font-size: 22px; font-weight: 700; }
.subtitle { font-size: 11px; color: rgba(232,234,237,0.4); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }
.card-body { display: flex; flex-direction: column; gap: 16px; }

.success-msg {
  font-size: 13px; color: #00c853; padding: 8px 12px;
  background: rgba(0,200,83,0.08); border-radius: 6px; text-align: center;
}

.register-link { font-size: 13px; color: rgba(232,234,237,0.4); text-align: center; }
.register-link a { color: #00c853; text-decoration: none; font-weight: 600; }
</style>
