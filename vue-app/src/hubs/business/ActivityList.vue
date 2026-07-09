<template>
  <section class="section-card activity-card">
    <div class="card-header">
      <h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Ostatnia aktywność</h2>
    </div>
    <div class="activity-list">
      <TransitionGroup name="list">
        <div v-for="a in items" :key="a.id" class="activity-row" @click="$emit('open', a)">
          <span class="activity-dot" :class="a.level"></span>
          <div class="activity-body">
            <span class="activity-msg">{{ a.message }}</span>
            <span class="activity-meta">{{ a.source }} • {{ formatTimeAgo(a.timestamp) }}</span>
          </div>
          <svg class="activity-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </div>
      </TransitionGroup>
    </div>
  </section>
</template>

<script setup>
defineProps({ items: Array })
defineEmits(['open'])

function formatTimeAgo(ts) {
  const diff = Date.now() - new Date(ts).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m temu`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h temu`
  return `${Math.floor(hrs / 24)}d temu`
}
</script>

<style scoped>
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-header h2 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; display: flex; align-items: center; gap: 8px; }
.card-header h2 svg { color: var(--accent-primary); flex-shrink: 0; }
.activity-card { min-height: 260px; }
.activity-list { display: flex; flex-direction: column; }
.activity-row { display: flex; align-items: center; gap: 12px; padding: 10px 8px; border-radius: 8px; cursor: pointer; transition: background 0.15s; border-bottom: 1px solid var(--border-color); }
.activity-row:last-child { border: none; }
.activity-row:hover { background: var(--bg-hover); }
.activity-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 2px; }
.activity-dot.critical { background: #ff5252; animation: pulse 1s ease infinite; }
.activity-dot.warning { background: #ff9100; animation: pulse 2s ease infinite; }
.activity-dot.info { background: #00e5ff; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.activity-body { flex: 1; min-width: 0; }
.activity-msg { font-size: 13px; color: var(--text-primary); display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.activity-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; display: block; }
.activity-chevron { flex-shrink: 0; }
.list-enter-active { transition: all 0.3s ease; }
.list-leave-active { transition: all 0.2s ease; }
.list-enter-from { opacity: 0; transform: translateX(-10px); }
.list-leave-to { opacity: 0; transform: translateX(10px); }
</style>