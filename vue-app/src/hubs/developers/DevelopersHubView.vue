<template>
  <div class="hub-view">
    <div class="hub-section-header">
      <h1 class="section-title">Developerzy</h1>
      <p class="section-desc">
        Aplikacja Streamlit z modułami Jira, Confluence, IAM, TeamCity i Informatica.
      </p>
    </div>

    <!-- Streamlit offline → launch card -->
    <template v-if="!streamlitReachable">
      <LaunchCard
        :isAlive="isAlive"
        :lastCheck="lastCheck"
        :modules="modules"
        @open="openStreamlit"
        @check="checkStreamlit"
      />
    </template>

    <!-- Streamlit online → iframe + zwijana karta -->
    <template v-else>
      <StreamlitIframe
        ref="iframeRef"
        :src="streamlitSource"
        :loading="loading"
        :error="iframeError"
        @load="onIframeLoad"
        @error="onIframeError"
        @retry="reloadIframe"
      />

      <CollapseCard :modules="modules" @open="openStreamlit" />

      <div v-if="iframeError" class="embed-status error-bar">
        <span class="status-dot error"></span>
        <span>Streamlit nie odpowiada — spróbuj odświeżyć</span>
        <button class="btn-retry" @click="reloadIframe">Odśwież</button>
      </div>
    </template>

    <div class="embed-footer">
      <span class="footer-ver">DataHub Streamlit | v0.21.0</span>
      <span class="footer-hint">{{ streamlitSource }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StreamlitIframe from './StreamlitIframe.vue'
import LaunchCard from './LaunchCard.vue'
import CollapseCard from './CollapseCard.vue'

const STREAMLIT_LOCAL = '/streamlit/'
const STREAMLIT_EXTERNAL = import.meta.env.VITE_STREAMLIT_URL || ''

const loading = ref(true)
const iframeError = ref(false)
const useExternal = ref(false)
const isAlive = ref(false)
const lastCheck = ref(false)
const iframeRef = ref(null)
const streamlitReachable = ref(true)

const streamlitSource = computed(() =>
  useExternal.value && STREAMLIT_EXTERNAL ? STREAMLIT_EXTERNAL : STREAMLIT_LOCAL
)

function openStreamlit() { window.open('/streamlit/', '_blank') }

function onIframeLoad() { loading.value = false; iframeError.value = false }
function onIframeError() { loading.value = false; iframeError.value = true }

function reloadIframe() {
  if (useExternal.value) useExternal.value = false
  else if (STREAMLIT_EXTERNAL) useExternal.value = true
  loading.value = true; iframeError.value = false
  const iframe = iframeRef.value?.iframeEl
  if (iframe) iframe.src = streamlitSource.value
}

async function checkStreamlit() {
  try {
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 3000)
    const res = await fetch('/streamlit/', { signal: controller.signal })
    isAlive.value = res.ok || res.status === 200
  } catch { isAlive.value = false }
  lastCheck.value = true
}

onMounted(async () => {
  await checkStreamlit()
  streamlitReachable.value = isAlive.value
})

const modules = [
  { name: 'Jira', desc: 'Zadania, sprinty, workflow', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2684ff" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/></svg>' },
  { name: 'Confluence', desc: 'Dokumentacja i wiki', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00b8d9" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>' },
  { name: 'IAM', desc: 'Dostęp, role, MFA', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00c853" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>' },
  { name: 'TeamCity', desc: 'CI/CD, buildy', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ff6b6b" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>' },
  { name: 'Informatica', desc: 'ETL, workflow', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ff6d00" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>' },
]
</script>

<style scoped>
.hub-view { width: 100%; max-width: var(--content-width, 1200px); display: flex; flex-direction: column; gap: 16px; }
.hub-section-header { margin-bottom: 4px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 600px; }
.embed-status { display: flex; align-items: center; gap: 10px; padding: 10px 16px; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; font-size: 13px; color: var(--text-secondary); }
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-dot.error { background: #ff5252; }
.btn-retry { margin-left: auto; padding: 6px 14px; border-radius: 6px; background: var(--bg-hover); border: 1px solid var(--border-color); color: var(--text-secondary); font-size: 12px; cursor: pointer; font-family: 'Inter', sans-serif; transition: all 0.15s; }
.btn-retry:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
.embed-footer { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; font-size: 11px; color: var(--text-muted); }
.footer-hint { font-family: 'JetBrains Mono', monospace; font-size: 10px; opacity: 0.6; }
</style>