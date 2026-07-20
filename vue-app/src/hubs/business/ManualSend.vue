<template>
  <section class="section-card manual-card">
    <div class="card-header">
      <h2>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        Wysyłka Manualna
      </h2>
    </div>
    <div class="manual-grid">
      <button
        v-for="btn in buttons"
        :key="btn.label"
        class="manual-btn"
        :class="btn.cls"
        @click="handleClick(btn.label)"
      >
        <span class="btn-icon" v-html="btn.icon"></span>
        <span class="btn-label">{{ btn.label }}</span>
      </button>
    </div>
    <Transition name="fade">
      <div v-if="flash" class="manual-flash">{{ flash }}</div>
    </Transition>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const flash = ref('')

const buttons = [
  { label: 'Error', cls: 'btn-error', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>' },
  { label: 'Revive', cls: 'btn-revive', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>' },
  { label: 'Wyceny', cls: 'btn-wyceny', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>' },
  { label: 'Zabezpieczenia', cls: 'btn-zabezp', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>' },
]

function handleClick(label) {
  flash.value = `Wysłano: ${label}`
  setTimeout(() => { flash.value = '' }, 2000)
}
</script>

<style scoped>
.section-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 22px 24px;
  margin-bottom: 20px;
}
.manual-card {
  border-left: 3px solid var(--accent-primary);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.card-header h2 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-header h2 svg {
  color: var(--accent-primary);
  flex-shrink: 0;
}

.manual-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.manual-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  padding: 10px 10px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-hover);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
  white-space: nowrap;
}
.manual-btn:hover {
  background: var(--bg-surface);
  border-color: var(--accent-primary);
  color: var(--text-primary);
}
.manual-btn:active {
  transform: scale(0.97);
}
.manual-btn .btn-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
.manual-btn .btn-icon svg {
  display: block;
}
.btn-error:hover { border-color: #ff5252; color: #ff5252; }
.btn-revive:hover { border-color: #00c853; color: #00c853; }
.btn-wyceny:hover { border-color: #ff9100; color: #ff9100; }
.btn-zabezp:hover { border-color: #536dfe; color: #536dfe; }

.manual-flash {
  margin-top: 10px;
  padding: 8px 14px;
  background: rgba(0,200,83,0.1);
  border: 1px solid rgba(0,200,83,0.25);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #00c853;
  text-align: center;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
