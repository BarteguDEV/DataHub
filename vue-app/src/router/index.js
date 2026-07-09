import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: 'Logowanie', guest: true },
  },
  {
    path: '/',
    name: 'HubSelect',
    component: () => import('@/views/HubSelectView.vue'),
    meta: { title: 'Wybierz hub', requiresAuth: true, hub: 'select' },
  },
  {
    path: '/ddt',
    name: 'DdtHub',
    component: () => import('@/views/DdtHubView.vue'),
    meta: { title: 'Developers Hub', requiresAuth: true, hub: 'ddt' },
  },
  {
    path: '/business',
    name: 'BusinessHub',
    component: () => import('@/views/BusinessHubView.vue'),
    meta: { title: 'Business Hub', requiresAuth: true, hub: 'business' },
  },
  {
    path: '/ai',
    name: 'AiHub',
    component: () => import('@/views/AiHubView.vue'),
    meta: { title: 'AI Hub', requiresAuth: true, hub: 'ai' },
  },
  {
    // Wszystko inne → login
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const { state, initialize } = useAuth()

  // Przy każdej nawigacji sprawdź czy sesja żyje (jeśli mamy auth w storage)
  if (!from.name) {
    // Pierwsze wejście do aplikacji — inicjalizacja
    await initialize()
  }

  // Ustaw tytuł strony
  document.title = to.meta?.title
    ? `${to.meta.title} | DataHub`
    : 'DataHub'

  // Auth guard
  if (to.meta.requiresAuth && !state.isAuthenticated) {
    return next({ name: 'Login' })
  }

  // Gość już zalogowany → przekieruj na hub select
  if (to.meta.guest && state.isAuthenticated) {
    return next({ name: 'HubSelect' })
  }

  next()
})

export default router
