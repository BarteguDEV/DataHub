<template>
  <div class="dashboard">
    <nav class="navbar">
      <div class="nav-brand">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
        </svg>
        <span>Data<span class="accent">Hub</span></span>
        <span class="badge">Vue POC</span>
      </div>
      <div class="nav-right">
        <span class="nav-user">{{ user?.username }}</span>
        <button class="btn btn-sm btn-outline" @click="handleLogout">Wyloguj</button>
      </div>
    </nav>

    <main class="main">
      <div class="welcome" v-if="user">
        <h1>Witaj, <span class="accent">{{ user.username }}</span></h1>
        <p>Vue.js + Flask działają razem na Azure App Service.</p>
      </div>
      <div v-else class="welcome">
        <p class="error-msg">Nie udało się pobrać danych użytkownika.</p>
      </div>

      <div class="cards">
        <div class="card">
          <span class="card-icon">⚡</span>
          <h3>Frontend</h3>
          <p>Vue 3 + Vite + Vue Router. SPA serwowana przez Flask.</p>
        </div>
        <div class="card">
          <span class="card-icon">🐍</span>
          <h3>Backend</h3>
          <p>Flask API. Te same endpointy co wersja Jinja2.</p>
        </div>
        <div class="card">
          <span class="card-icon">☁️</span>
          <h3>Hosting</h3>
          <p>Jeden Azure App Service. Vue budowany przed deployem.</p>
        </div>
      </div>

      <div class="info-card" v-if="user">
        <h3>Informacje o sesji</h3>
        <table>
          <tr><td>Użytkownik</td><td>{{ user.username }}</td></tr>
          <tr><td>ID sesji</td><td>{{ user.id }}</td></tr>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMe, logoutUser } from '../api.js'

const router = useRouter()
const user = ref(null)

onMounted(async () => {
  try {
    user.value = await getMe()
  } catch {
    router.push('/')
  }
})

async function handleLogout() {
  try {
    await logoutUser()
  } catch { /* ignore */ }
  router.push('/')
}
</script>

<style scoped>
.dashboard { min-height: 100vh; display: flex; flex-direction: column; }

.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 28px; background: #0f1117;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.nav-brand { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; }
.nav-brand svg { color: #00c853; }

.badge {
  font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
  padding: 2px 8px; background: rgba(0,200,83,0.12); color: #00c853; border-radius: 100px;
}

.nav-right { display: flex; align-items: center; gap: 14px; }
.nav-user { font-size: 13px; font-weight: 500; color: rgba(232,234,237,0.7); }

.main { flex: 1; max-width: 800px; margin: 0 auto; padding: 48px 24px; width: 100%; }

.welcome { margin-bottom: 40px; }
.welcome h1 { font-size: 28px; font-weight: 700; margin-bottom: 8px; }
.welcome p { font-size: 14px; color: rgba(232,234,237,0.55); }

.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 32px; }

.card {
  background: #16181f; border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; padding: 24px; display: flex; flex-direction: column; gap: 10px;
  transition: transform 0.2s;
}

.card:hover { transform: translateY(-2px); }
.card-icon { font-size: 24px; }
.card h3 { font-size: 15px; font-weight: 600; }
.card p { font-size: 13px; color: rgba(232,234,237,0.5); line-height: 1.6; }

.info-card {
  background: #16181f; border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; padding: 24px;
}

.info-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 12px; }

.info-card table { width: 100%; border-collapse: collapse; }
.info-card td { padding: 8px 0; font-size: 13px; border-bottom: 1px solid rgba(255,255,255,0.04); }
.info-card td:first-child { color: rgba(232,234,237,0.5); width: 140px; }
</style>
