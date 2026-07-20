<template>
  <div class="app-root">
    <!-- Globalne tło ambient — wszystkie strony -->
    <div class="bg-grid"></div>
    <div class="bg-ambient">
      <div class="ambient-blob blob-1"></div>
      <div class="ambient-blob blob-2"></div>
      <div class="ambient-blob blob-3"></div>
      <div class="ambient-blob blob-4"></div>
      <div class="ambient-blob blob-5"></div>
    </div>
    <div class="bg-vignette"></div>

    <!-- Zawartość strony (nad tłem) -->
    <div class="app-content">
      <!-- Widok logowania (brak layoutu — pełny ekran) -->
      <template v-if="route.name === 'Login'">
        <router-view />
      </template>

      <!-- Główna aplikacja (header + treść) -->
      <template v-else>
        <div class="app-shell">
          <AppHeader />
          <main class="main-content">
            <router-view v-slot="{ Component, route: r }">
              <transition name="page" mode="out-in">
                <component :is="Component" :key="r.path" />
              </transition>
            </router-view>
          </main>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/stores/auth'
import AppHeader from '@/components/AppHeader.vue'

const route = useRoute()
const { initialize } = useAuth()

onMounted(async () => {
  await initialize()
})
</script>

<style scoped>
.app-root {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

/* Warstwa treści nad tłem */
.app-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

/* Layout po zalogowaniu — brak sidebara */
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
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
