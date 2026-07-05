<template>
  <!--
    App.vue — główny orchestrator aplikacji.
    Zarządza auth gatem, layoutem (login vs. main app) i transitionami.
  -->
  <div class="app-root">
    <!-- Widok logowania (brak layoutu — pełny ekran) -->
    <template v-if="route.name === 'Login'">
      <router-view />
    </template>

    <!-- Główna aplikacja (sidebar + header + treść) -->
    <template v-else>
      <div class="app-shell">
        <AppSidebar />
        <div class="app-main">
          <AppHeader />
          <main class="main-content">
            <router-view v-slot="{ Component, route: r }">
              <transition name="page" mode="out-in">
                <component :is="Component" :key="r.path" />
              </transition>
            </router-view>
          </main>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuth } from '@/stores/auth'
import AppSidebar from '@/components/AppSidebar.vue'
import AppHeader from '@/components/AppHeader.vue'

const route = useRoute()
const { state } = useAuth()

// Inicjalizacja — sprawdź czy jest zalogowany (na wypadek odświeżenia)
// W POC brak persistent auth, więc przekierujemy do loginu z router guarda
</script>

<style scoped>
.app-root {
  min-height: 100vh;
  background: var(--bg-primary);
}

/* Layout po zalogowaniu */
.app-shell {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.app-main {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px 40px;
}

/* Transition między stronami */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
