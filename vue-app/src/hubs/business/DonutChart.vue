<template>
  <section class="section-card chart-card">
    <div class="card-header">
      <h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>Rozkład komunikatów</h2>
    </div>
    <div class="donut-wrap">
      <svg width="200" height="200" viewBox="0 0 160 160" class="donut-svg">
        <circle cx="80" cy="80" r="64" fill="none" stroke="var(--bg-hover)" stroke-width="20"/>
        <circle v-for="(s, i) in segments" :key="i" cx="80" cy="80" r="64" fill="none" :stroke="s.color" stroke-width="20" :stroke-dasharray="s.dash" :stroke-dashoffset="s.offset" :style="{ transform: 'rotate(-90deg)', transformOrigin: '80px 80px', transition: 'stroke-dashoffset 1.2s ease' }"/>
        <text x="80" y="74" text-anchor="middle" fill="var(--text-primary)" font-size="24" font-weight="700">{{ successRate }}%</text>
        <text x="80" y="94" text-anchor="middle" fill="var(--text-muted)" font-size="11">dostarczone</text>
      </svg>
      <div class="donut-legend">
        <div v-for="s in segments" :key="s.label" class="legend-item">
          <span class="legend-swatch" :style="{ background: s.color }"></span>
          <span class="legend-label">{{ s.label }}</span>
          <span class="legend-val">{{ s.count.toLocaleString() }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({ segments: Array, successRate: Number })
</script>

<style scoped>
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-header h2 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; display: flex; align-items: center; gap: 8px; }
.card-header h2 svg { color: var(--accent-primary); flex-shrink: 0; }
.chart-card { display: flex; flex-direction: column; min-height: 260px; }
.donut-wrap { display: flex; align-items: center; justify-content: center; gap: 32px; flex: 1; padding: 8px 0; }
.donut-svg { flex-shrink: 0; display: block; }
.donut-legend { display: flex; flex-direction: column; gap: 12px; }
.legend-item { display: flex; align-items: center; gap: 10px; font-size: 13px; }
.legend-swatch { width: 12px; height: 12px; border-radius: 4px; flex-shrink: 0; }
.legend-label { color: var(--text-secondary); min-width: 70px; font-weight: 500; }
.legend-val { color: var(--text-primary); font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
</style>