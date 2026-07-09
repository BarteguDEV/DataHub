<template>
  <section class="section-card message-card">
    <div class="card-header">
      <h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>Komunikaty — status wysyłki</h2>
      <span class="badge-api">ostatnie 24h</span>
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
    <div class="msg-footer">
      <span>Razem: <strong>{{ total.toLocaleString() }}</strong></span>
      <span class="msg-footer-success"><span class="pulse-dot"></span>System działa poprawnie</span>
    </div>
  </section>
</template>

<script setup>
defineProps({ messages: Array, total: Number })
defineEmits(['open'])
</script>

<style scoped>
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; }
.message-card { border-left: 3px solid #536dfe; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-header h2 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; display: flex; align-items: center; gap: 8px; }
.card-header h2 svg { color: var(--accent-primary); flex-shrink: 0; }
.badge-api { font-size: 10px; font-weight: 500; color: #536dfe; padding: 3px 10px; border-radius: 100px; background: rgba(83,109,254,0.1); white-space: nowrap; }
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
.msg-footer { display: flex; justify-content: space-between; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border-color); font-size: 12px; color: var(--text-muted); }
.msg-footer-success { display: flex; align-items: center; gap: 6px; color: #00c853; }
.pulse-dot { width: 6px; height: 6px; border-radius: 50%; background: #00c853; animation: pulse 1.5s ease infinite; }
</style>