<template>
  <div class="hub-view">
    <div class="hub-section-header">
      <h1 class="section-title">APEX Business Intelligence</h1>
      <p class="section-desc">
        Dane pobierane z API (Python → baza danych), wizualizowane w Vue.
        KPI, trendy, raporty, ETL, SLA i alerty w jednym miejscu.
      </p>
    </div>

    <!-- KPI -->
    <section class="kpi-bar">
      <div class="kpi-card" v-for="k in kpis" :key="k.label">
        <span class="kpi-value">{{ k.value }}</span>
        <span class="kpi-label">{{ k.label }}</span>
        <span class="kpi-trend" :class="k.trend === 'up' ? 'up' : 'down'">
          {{ k.trend === 'up' ? '▲' : '▼' }} {{ k.change }}
        </span>
      </div>
    </section>

    <!-- Trendy miesięczne -->
    <section class="section-card">
      <h2>Trend miesięczny</h2>
      <div class="bar-chart">
        <div class="bar-group" v-for="m in trends" :key="m.month">
          <div class="bar-labels">
            <span class="bar-month">{{ m.month }}</span>
            <span class="bar-val">{{ m.transactions }}</span>
          </div>
          <div class="bar-track">
            <div
              class="bar-fill transactions"
              :style="{ width: barPercent(m.transactions, maxTransactions) + '%' }"
            ></div>
          </div>
          <div class="bar-track errors">
            <div
              class="bar-fill errors"
              :style="{ width: barPercent(m.errors, maxErrors) + '%' }"
            ></div>
          </div>
        </div>
        <div class="bar-legend">
          <span><span class="legend-dot trans"></span> Transakcje</span>
          <span><span class="legend-dot err"></span> Błędy</span>
        </div>
      </div>
    </section>

    <!-- Raporty -->
    <section class="section-card">
      <div class="section-row">
        <h2>Ostatnie raporty</h2>
        <span class="badge-api">Dane z /api/reports</span>
      </div>
      <div class="report-list">
        <div v-for="r in reports" :key="r.id" class="report-row">
          <div class="report-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
            </svg>
          </div>
          <div class="report-info">
            <span class="report-name">{{ r.name }}</span>
            <span class="report-meta">{{ r.date }} • {{ r.size }} • {{ r.author }}</span>
          </div>
          <span class="report-status" :class="r.status">{{ r.status === 'ready' ? 'Gotowy' : 'Generowanie...' }}</span>
        </div>
      </div>
    </section>

    <!-- SLA -->
    <section class="section-card">
      <h2>SLA Compliance</h2>
      <table class="sla-table">
        <tr><th>Usługa</th><th>Target</th><th>Actual</th><th>Incydenty</th><th>Status</th></tr>
        <tr v-for="s in sla" :key="s.service">
          <td>{{ s.service }}</td>
          <td>{{ s.sla_target }}%</td>
          <td>{{ s.actual }}%</td>
          <td>{{ s.incidents }}</td>
          <td>
            <span class="sla-status" :class="s.status">
              {{ s.status === 'ok' ? 'OK' : 'Warning' }}
            </span>
          </td>
        </tr>
      </table>
    </section>

    <!-- ETL -->
    <section class="section-card">
      <h2>ETL Performance</h2>
      <table class="etl-table">
        <tr><th>Workflow</th><th>Śr. czas (min)</th><th>Rows</th><th>Success rate</th><th>Status</th></tr>
        <tr v-for="e in etl" :key="e.workflow">
          <td class="cell-mono">{{ e.workflow }}</td>
          <td>{{ e.avg_duration_min }}</td>
          <td>{{ formatNum(e.rows_processed) }}</td>
          <td>{{ e.success_rate }}%</td>
          <td>
            <span class="etl-status" :class="e.status">
              {{ e.status === 'stable' ? '✓ Stable' : '⚠ Degraded' }}
            </span>
          </td>
        </tr>
      </table>
    </section>

    <!-- Alerty -->
    <section class="section-card">
      <div class="section-row">
        <h2>Aktywne alerty</h2>
        <span class="badge-api">Dane z /api/alerts</span>
      </div>
      <div v-if="alerts.length === 0" class="no-alerts">Brak alertów ✓</div>
      <div v-for="a in alerts" :key="a.id" class="alert-row" :class="a.level">
        <span class="alert-level">{{ a.level.toUpperCase() }}</span>
        <span class="alert-source">{{ a.source }}</span>
        <span class="alert-msg">{{ a.message }}</span>
        <span class="alert-time">{{ formatTimeAgo(a.timestamp) }}</span>
      </div>
    </section>

    <!-- Status API -->
    <div class="api-status">
      <span class="api-dot" :class="{ online: apiOk }"></span>
      <span v-if="apiOk">APEX API online (localhost:5100)</span>
      <span v-else>APEX API offline — uruchom: python backend/apex_api.py</span>
      <button v-if="!apiOk" class="btn-retry" @click="fetchAll">Ponów</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = 'http://localhost:5100'
const apiOk = ref(false)

const kpis = ref([])
const trends = ref([])
const reports = ref([])
const sla = ref([])
const etl = ref([])
const alerts = ref([])

function formatNum(n) {
  return n.toLocaleString('pl-PL')
}

function formatTimeAgo(ts) {
  const diff = Date.now() - new Date(ts).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m temu`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h temu`
  return `${Math.floor(hrs / 24)}d temu`
}

const maxTransactions = computed(() =>
  Math.max(...trends.value.map(m => m.transactions), 1)
)
const maxErrors = computed(() =>
  Math.max(...trends.value.map(m => m.errors), 1)
)

function barPercent(val, max) {
  return Math.max((val / max) * 100, 2)
}

async function fetchAll() {
  const endpoints = {
    kpi: '/api/kpi',
    trends: '/api/trends',
    reports: '/api/reports',
    sla: '/api/sla',
    etl: '/api/etl',
    alerts: '/api/alerts',
  }

  let anyOk = false

  for (const [key, url] of Object.entries(endpoints)) {
    try {
      const res = await fetch(`${API_BASE}${url}`)
      const json = await res.json()
      if (json.success) {
        anyOk = true
        if (key === 'kpi') {
          const d = json.data
          kpis.value = [
            { value: d.uptime + '%', label: 'Uptime systemu', trend: d.uptime_trend, change: d.uptime_change + '%' },
            { value: d.transactions.toLocaleString(), label: 'Transakcji / dzień', trend: d.transactions_trend, change: d.transactions_change + '%' },
            { value: d.avg_processing_sec + 's', label: 'Śr. czas przetwarzania', trend: d.avg_processing_trend === 'up' ? 'down' : 'up', change: d.avg_processing_change + 's' },
            { value: d.sla + '%', label: 'SLA Procesów ETL', trend: d.sla_trend, change: d.sla_change + '%' },
          ]
        } else {
          const data = json.data
          if (key === 'trends') trends.value = data
          else if (key === 'reports') reports.value = data
          else if (key === 'sla') sla.value = data
          else if (key === 'etl') etl.value = data
          else if (key === 'alerts') alerts.value = data
        }
      }
    } catch {
      // endpoint unavailable
    }
  }

  apiOk.value = anyOk
}

onMounted(fetchAll)
</script>

<style scoped>
.hub-view { max-width: 1100px; }

.hub-section-header { margin-bottom: 28px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 600px; }

/* KPI */
.kpi-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; }
.kpi-value { font-size: 26px; font-weight: 700; color: var(--text-primary); }
.kpi-label { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }
.kpi-trend { font-size: 12px; font-weight: 600; margin-top: 6px; display: inline-block; }
.kpi-trend.up { color: #00c853; }
.kpi-trend.down { color: #ff5252; }

/* Section card */
.section-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; margin-bottom: 20px; }
.section-card h2 { font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0 0 16px 0; }
.section-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.section-row h2 { margin: 0; }
.badge-api { font-size: 10px; font-weight: 500; color: #536dfe; padding: 3px 10px; border-radius: 100px; background: rgba(83,109,254,0.1); }

/* Bar chart */
.bar-chart { display: flex; flex-direction: column; gap: 6px; }
.bar-group { display: flex; flex-direction: column; gap: 3px; }
.bar-labels { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); }
.bar-month { font-weight: 600; color: var(--text-secondary); }
.bar-track { height: 8px; background: var(--bg-hover); border-radius: 100px; overflow: hidden; }
.bar-fill.transactions { height: 100%; background: linear-gradient(90deg, #00c853, #00e5ff); border-radius: 100px; transition: width 0.8s ease; }
.bar-fill.errors { height: 100%; background: linear-gradient(90deg, #ff9100, #ff1744); border-radius: 100px; transition: width 0.8s ease; }
.bar-track.errors { margin-top: 2px; }
.bar-legend { display: flex; gap: 20px; font-size: 11px; color: var(--text-muted); margin-top: 8px; }
.legend-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.legend-dot.trans { background: #00c853; }
.legend-dot.err { background: #ff9100; }

/* Reports */
.report-list { }
.report-row { display: flex; align-items: center; gap: 14px; padding: 12px 0; border-bottom: 1px solid var(--border-color); }
.report-row:last-child { border: none; }
.report-icon { color: var(--accent-primary); flex-shrink: 0; }
.report-info { flex: 1; }
.report-name { font-size: 13px; font-weight: 500; color: var(--text-primary); }
.report-meta { font-size: 11px; color: var(--text-muted); margin-top: 2px; display: block; }
.report-status { font-size: 11px; font-weight: 500; padding: 3px 12px; border-radius: 100px; }
.report-status.ready { background: rgba(0,200,83,0.1); color: #00c853; }
.report-status.generating { background: rgba(255,145,0,0.1); color: #ff9100; }

/* Tables */
.sla-table, .etl-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.sla-table th, .etl-table th { text-align: left; padding: 10px 12px; color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid var(--border-color); }
.sla-table td, .etl-table td { padding: 10px 12px; border-bottom: 1px solid var(--border-color); color: var(--text-secondary); }
.sla-table tr:hover td, .etl-table tr:hover td { background: var(--bg-hover); }
.cell-mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; }

.sla-status, .etl-status { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 100px; }
.sla-status.ok, .etl-status.stable { background: rgba(0,200,83,0.1); color: #00c853; }
.sla-status.warning, .etl-status.degraded { background: rgba(255,145,0,0.1); color: #ff9100; }

/* Alerts */
.alert-row { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border-color); font-size: 13px; }
.alert-row:last-child { border: none; }
.alert-level { font-weight: 700; font-size: 10px; letter-spacing: 1px; width: 60px; }
.alert-row.critical .alert-level { color: #ff1744; }
.alert-row.warning .alert-level { color: #ff9100; }
.alert-row.info .alert-level { color: #00e5ff; }
.alert-source { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-muted); width: 100px; }
.alert-msg { flex: 1; color: var(--text-secondary); }
.alert-time { font-size: 11px; color: var(--text-muted); }

.no-alerts { font-size: 14px; color: #00c853; padding: 12px 0; }

/* API Status */
.api-status { display: flex; align-items: center; gap: 10px; padding: 12px 20px; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; font-size: 13px; color: var(--text-muted); margin-top: 8px; }
.api-dot { width: 8px; height: 8px; border-radius: 50%; background: #ff5252; }
.api-dot.online { background: #00c853; }
.btn-retry { margin-left: auto; padding: 6px 14px; border-radius: 6px; background: var(--bg-hover); border: 1px solid var(--border-color); color: var(--text-secondary); font-size: 12px; cursor: pointer; font-family: 'Inter', sans-serif; }
.btn-retry:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
</style>
