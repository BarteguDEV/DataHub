<template>
  <section class="section-card">
    <div class="card-header">
      <h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>SLA Compliance</h2>
    </div>
    <table class="data-table">
      <thead><tr><th>Usługa</th><th>Target</th><th>Actual</th><th>Incydenty</th><th>Status</th></tr></thead>
      <tbody>
        <tr v-for="s in items" :key="s.service">
          <td>{{ s.service }}</td>
          <td>{{ s.sla_target }}%</td>
          <td>
            <div class="sla-actual-bar"><div class="sla-actual-fill" :class="{ warning: s.actual < s.sla_target, critical: s.actual < s.sla_target - 1 }" :style="{ width: Math.min(s.actual, 100) + '%' }"></div></div>
            <span class="sla-actual-label">{{ s.actual }}%</span>
          </td>
          <td>{{ s.incidents }}</td>
          <td><span class="status-badge" :class="s.status"><span class="status-dot" :class="s.status"></span>{{ s.status === 'ok' ? 'OK' : 'Warning' }}</span></td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
defineProps({ items: Array })
</script>

<style scoped>
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 22px 24px; margin-bottom: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.card-header h2 { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; display: flex; align-items: center; gap: 8px; }
.card-header h2 svg { color: var(--accent-primary); flex-shrink: 0; }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table thead th { text-align: left; padding: 10px 12px; color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; border-bottom: 1px solid var(--border-color); }
.data-table tbody td { padding: 12px 12px; border-bottom: 1px solid var(--border-color); color: var(--text-secondary); }
.data-table tbody tr:last-child td { border: none; }
.data-table tbody tr:hover td { background: var(--bg-hover); }
.sla-actual-bar { width: 80px; height: 6px; background: var(--bg-hover); border-radius: 100px; overflow: hidden; display: inline-block; vertical-align: middle; }
.sla-actual-fill { height: 100%; background: var(--accent-primary); border-radius: 100px; transition: width 0.8s ease; }
.sla-actual-fill.warning { background: #ff9100; }
.sla-actual-fill.critical { background: #ff5252; }
.sla-actual-label { font-size: 11px; font-weight: 600; color: var(--text-primary); margin-left: 8px; vertical-align: middle; }
.status-badge { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 100px; display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; }
.status-badge.ok { background: rgba(0,200,83,0.1); color: #00c853; }
.status-badge.warning { background: rgba(255,145,0,0.1); color: #ff9100; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-dot.ok { background: #00c853; }
.status-dot.warning { background: #ff9100; }
</style>