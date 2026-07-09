<template>
  <section class="section-card">
    <div class="card-header">
      <h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>ETL Workflows</h2>
      <span class="badge-api">Dane z /api/business/etl</span>
    </div>
    <table class="data-table">
      <thead><tr><th>Workflow</th><th>Śr. czas</th><th>Rekordy</th><th>Success rate</th><th>Status</th><th></th></tr></thead>
      <tbody>
        <tr v-for="e in items" :key="e.workflow" class="clickable-row" @click="$emit('open', e)">
          <td class="cell-mono">{{ e.workflow }}</td>
          <td>{{ e.avg_duration_min }} min</td>
          <td>{{ formatNum(e.rows_processed) }}</td>
          <td>
            <div class="mini-bar"><div class="mini-bar-fill" :style="{ width: e.success_rate + '%' }"></div></div>
            <span class="mini-bar-label">{{ e.success_rate }}%</span>
          </td>
          <td><span class="status-badge" :class="e.status"><span class="status-dot" :class="e.status"></span>{{ e.status === 'stable' ? 'Stable' : 'Degraded' }}</span></td>
          <td><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
defineProps({ items: Array })
defineEmits(['open'])
function formatNum(n) { return Number(n).toLocaleString('pl-PL') }
</script>

<style scoped>
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-header h2 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; display: flex; align-items: center; gap: 8px; }
.card-header h2 svg { color: var(--accent-primary); flex-shrink: 0; }
.badge-api { font-size: 10px; font-weight: 500; color: #536dfe; padding: 3px 10px; border-radius: 100px; background: rgba(83,109,254,0.1); white-space: nowrap; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table thead th { text-align: left; padding: 10px 12px; color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; border-bottom: 1px solid var(--border-color); }
.data-table tbody td { padding: 12px 12px; border-bottom: 1px solid var(--border-color); color: var(--text-secondary); }
.data-table tbody tr:last-child td { border: none; }
.data-table tbody tr:hover td { background: var(--bg-hover); }
.clickable-row { cursor: pointer; }
.clickable-row td:last-child { text-align: right; }
.cell-mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-primary); }
.mini-bar { width: 80px; height: 6px; background: var(--bg-hover); border-radius: 100px; overflow: hidden; display: inline-block; vertical-align: middle; }
.mini-bar-fill { height: 100%; background: linear-gradient(90deg, #00c853, #00e5ff); border-radius: 100px; transition: width 0.8s ease; }
.mini-bar-label { font-size: 11px; font-weight: 600; color: var(--text-primary); margin-left: 8px; vertical-align: middle; }
.status-badge { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 100px; display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; }
.status-badge.stable { background: rgba(0,200,83,0.1); color: #00c853; }
.status-badge.degraded { background: rgba(255,145,0,0.1); color: #ff9100; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-dot.stable { background: #00c853; }
.status-dot.degraded { background: #ff9100; }
</style>