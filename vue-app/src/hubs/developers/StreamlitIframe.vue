<template>
  <div class="embed-container">
    <div v-if="loading" class="embed-loader">
      <div class="loader-spinner"></div>
      <span>Ładowanie Streamlit…</span>
    </div>
    <iframe
      ref="iframeEl"
      :src="src"
      class="streamlit-iframe"
      :class="{ hidden: loading }"
      frameborder="0"
      sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
      @load="$emit('load')"
      @error="$emit('error')"
    ></iframe>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  src: String,
  loading: Boolean,
  error: Boolean,
})
defineEmits(['load', 'error', 'retry'])

const iframeEl = ref(null)

defineExpose({ iframeEl })
</script>

<style scoped>
.embed-container { flex: 1; min-height: 0; border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden; background: var(--bg-primary); }
.streamlit-iframe { width: 100%; height: 72vh; min-height: 500px; display: block; background: #fff; }
.streamlit-iframe.hidden { display: none; }
.embed-loader { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; padding: 80px 0; color: var(--text-muted); font-size: 14px; }
.loader-spinner { width: 32px; height: 32px; border: 3px solid var(--border-color); border-top-color: #00c853; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>