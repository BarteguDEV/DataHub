<template>
  <section class="section-card message-card">
    <div class="card-header">
      <h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>Komunikaty — status wysyłki</h2>
      <div class="header-right">
        <span class="header-total">Razem: <strong>{{ total.toLocaleString() }}</strong></span>
        <button class="date-btn" @click="openDatePicker">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
          {{ formattedDate }}
        </button>
        <input ref="dateInput" type="date" class="date-native" :value="selectedDate" @input="onDateChange" />
      </div>
    </div>
    <div class="msg-stats">
      <div v-for="msg in messages" :key="msg.label" class="msg-row" @click="$emit('open', msg)">
        <div class="msg-label">
          <span class="msg-dot" :style="{ background: msg.color }"></span>
          <span class="msg-name">{{ msg.label }}</span>
          <span class="msg-count">{{ msg.count.toLocaleString() }}</span>
        </div>
        <div class="msg-bar-track">
          <div class="msg-bar-fill" :style="{ width: msg.pct + '%', background: msg.color, '--w': msg.pct + '%' }"></div>
        </div>
        <span class="msg-pct">{{ msg.pct }}%</span>
      </div>
    </div>

    <ChartSection :segments="segments" :successRate="successRate" />
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

import ChartSection from './ChartSection.vue'

const props = defineProps({
  messages: Array,
  total: Number,
  segments: Array,
  successRate: Number
})
const emit = defineEmits(['open', 'date-change'])

const dateInput = ref(null)
const selectedDate = ref(new Date().toISOString().slice(0, 10))

const formattedDate = computed(() => {
  const d = new Date(selectedDate.value + 'T00:00:00')
  return d.toLocaleDateString('pl-PL', { weekday: 'short', day: '2-digit', month: '2-digit', year: 'numeric' })
})

function openDatePicker() {
  dateInput.value?.showPicker()
}

function onDateChange(e) {
  selectedDate.value = e.target.value
  emit('date-change', selectedDate.value)
}
</script>

<style scoped>
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; }
.message-card { border-left: 3px solid #536dfe; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-header h2 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; display: flex; align-items: center; gap: 8px; }
.card-header h2 svg { color: var(--accent-primary); flex-shrink: 0; }

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-total {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
}
.header-total strong {
  color: var(--text-primary);
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}

.date-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-hover);
  color: var(--text-secondary);
  font-size: 11px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
  white-space: nowrap;
}
.date-btn:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
  background: var(--bg-surface);
}
.date-btn svg {
  color: var(--accent-primary);
  flex-shrink: 0;
}
.date-native {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

.msg-stats { display: flex; flex-direction: column; gap: 10px; }
.msg-row { display: flex; align-items: center; gap: 12px; padding: 6px 8px; border-radius: 8px; cursor: pointer; transition: background 0.15s; }
.msg-row:hover { background: var(--bg-hover); }
.msg-label { display: flex; align-items: center; gap: 8px; min-width: 140px; }
.msg-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; animation: pulse 2s ease infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.msg-name { font-size: 12px; font-weight: 600; color: var(--text-primary); width: 60px; }
.msg-count { font-size: 12px; font-weight: 500; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; }
.msg-bar-track { flex: 1; height: 10px; background: var(--bg-hover); border-radius: 100px; overflow: hidden; }
.msg-bar-fill { height: 100%; border-radius: 100px; transition: width 1.2s cubic-bezier(0.16,1,0.3,1); animation: barGrow 1.2s cubic-bezier(0.16,1,0.3,1) both; }
@keyframes barGrow { from { width: 0 !important; } to { width: var(--w); } }
.msg-pct { font-size: 11px; font-weight: 600; color: var(--text-muted); min-width: 40px; text-align: right; }
</style>
