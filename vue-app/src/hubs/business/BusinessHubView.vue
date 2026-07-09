<template>
  <div class="hub-view">
    <div class="hub-section-header">
      <h1 class="section-title">Business Hub</h1>
      <p class="section-desc">
        Centrum monitoringu procesów biznesowych. Statusy komunikatów,
        wydajność ETL, SLA i alerty w czasie rzeczywistym.
      </p>
    </div>

    <KpiBar :kpis="kpis" @open="openKpiModal" />

    <MessageBar
      :messages="messages"
      :total="totalMsgs"
      @open="openMsgModal"
    />

    <div class="two-col">
      <DonutChart :segments="donutSegments" :successRate="successRate" />
      <ActivityList :items="activity" @open="openActivityModal" />
    </div>

    <EtlTable :items="etl" @open="openEtlModal" />

    <SlaTable :items="sla" />

    <ModalTeleport v-if="modal.show" :title="modal.title" :body="modal.body" @close="closeModal" />

    <div class="api-status">
      <span class="api-dot" :class="{ online: apiOk }"></span>
      <span>{{ apiOk ? 'API Business Hub online' : 'API niedostępne' }}</span>
      <button v-if="!apiOk" class="btn-retry" @click="fetchAll">Ponów</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import KpiBar from './KpiBar.vue'
import MessageBar from './MessageBar.vue'
import DonutChart from './DonutChart.vue'
import ActivityList from './ActivityList.vue'
import EtlTable from './EtlTable.vue'
import SlaTable from './SlaTable.vue'
import ModalTeleport from './ModalTeleport.vue'

const API_BASE = window.location.origin
const apiOk = ref(false)
const kpis = ref([])
const etl = ref([])
const sla = ref([])
const alerts = ref([])
const activity = ref([])
const messages = ref([])
const modal = reactive({ show: false, title: '', body: '' })

function closeModal() { modal.show = false }

function genSpark() {
  const pts = []
  for (let i = 0; i < 10; i++) pts.push(`${i * 6},${24 - Math.random() * 20}`)
  return pts.join(' ')
}

function generateMessages() {
  const raw = { SENT: { count: 28450, color: '#00c853' }, ACPT: { count: 27120, color: '#00e5ff' }, RJCT: { count: 890, color: '#ff5252' }, INVALID: { count: 340, color: '#ff9100' }, READY: { count: 4120, color: '#536dfe' } }
  const total = Object.values(raw).reduce((s, v) => s + v.count, 0)
  return Object.entries(raw).map(([label, v]) => ({ label, count: v.count, color: v.color, pct: Math.round((v.count / total) * 100) }))
}

const totalMsgs = computed(() => messages.value.reduce((s, m) => s + m.count, 0))
const successRate = computed(() => {
  const sent = messages.value.find(m => m.label === 'SENT')?.count || 1
  const acpt = messages.value.find(m => m.label === 'ACPT')?.count || 0
  return Math.round((acpt / sent) * 100)
})
const donutSegments = computed(() => {
  const total = totalMsgs.value || 1
  const circumference = 2 * Math.PI * 64
  let offset = 0
  return messages.value.map(m => {
    const pct = m.count / total
    const dash = pct * circumference
    const seg = { ...m, dash: `${dash} ${circumference - dash}`, offset: -offset }
    offset += dash
    return seg
  })
})

function formatNum(n) { return Number(n).toLocaleString('pl-PL') }
function formatTimeAgo(ts) {
  const diff = Date.now() - new Date(ts).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m temu`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h temu`
  return `${Math.floor(hrs / 24)}d temu`
}

function openKpiModal(k) {
  modal.title = k.label
  modal.body = `<div class="modal-kpi"><div class="modal-kpi-big">${k.current}${k.unit||''}</div><div class="modal-kpi-row"><span class="modal-label">Trend</span><span class="modal-value" style="color:${k.trend==='up'?'var(--accent-primary)':'#ff5252'}">${k.trend==='up'?'▲':'▼'} ${k.change}</span></div><div class="modal-kpi-row"><span class="modal-label">Szczegóły</span><span class="modal-value">Wartość z ostatniej synchronizacji</span></div><div class="modal-kpi-row"><span class="modal-label">Ostatnia aktualizacja</span><span class="modal-value">${new Date().toLocaleString('pl-PL')}</span></div></div>`
  modal.show = true
}
function openMsgModal(m) {
  modal.title = `Status: ${m.label}`
  modal.body = `<div class="modal-msg"><div class="modal-msg-bar" style="background:${m.color};width:100%;height:40px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;color:#000">${m.count.toLocaleString()} (${m.pct}%)</div><div style="margin-top:16px;display:grid;gap:10px"><div class="modal-kpi-row"><span class="modal-label">Status</span><span class="modal-value">${m.label}</span></div><div class="modal-kpi-row"><span class="modal-label">Liczba</span><span class="modal-value">${m.count.toLocaleString()}</span></div><div class="modal-kpi-row"><span class="modal-label">Udział</span><span class="modal-value">${m.pct}%</span></div></div></div>`
  modal.show = true
}
function openActivityModal(a) {
  modal.title = `Alert: ${a.source}`
  modal.body = `<div class="modal-activity"><div class="modal-kpi-row"><span class="modal-label">Źródło</span><span class="modal-value">${a.source}</span></div><div class="modal-kpi-row"><span class="modal-label">Wiadomość</span><span class="modal-value">${a.message}</span></div><div class="modal-kpi-row"><span class="modal-label">Poziom</span><span class="modal-value" style="text-transform:uppercase;color:${a.level==='critical'?'#ff5252':a.level==='warning'?'#ff9100':'#00e5ff'}">${a.level}</span></div><div class="modal-kpi-row"><span class="modal-label">Czas</span><span class="modal-value">${formatTimeAgo(a.timestamp)}</span></div></div>`
  modal.show = true
}
function openEtlModal(e) {
  modal.title = `ETL: ${e.workflow}`
  modal.body = `<div class="modal-etl"><div class="modal-kpi-row"><span class="modal-label">Workflow</span><span class="modal-value cell-mono">${e.workflow}</span></div><div class="modal-kpi-row"><span class="modal-label">Średni czas</span><span class="modal-value">${e.avg_duration_min} min</span></div><div class="modal-kpi-row"><span class="modal-label">Rekordy</span><span class="modal-value">${formatNum(e.rows_processed)}</span></div><div class="modal-kpi-row"><span class="modal-label">Skuteczność</span><span class="modal-value">${e.success_rate}%</span></div><div class="modal-kpi-row"><span class="modal-label">Status</span><span class="modal-value" style="color:${e.status==='stable'?'var(--accent-primary)':'#ff9100'}">${e.status==='stable'?'Stable':'Degraded'}</span></div></div>`
  modal.show = true
}

async function fetchAll() {
  const endpoints = { kpi: '/api/business/kpi', etl: '/api/business/etl', sla: '/api/business/sla', alerts: '/api/business/alerts' }
  let anyOk = false
  for (const [key, url] of Object.entries(endpoints)) {
    try {
      const res = await fetch(url)
      const json = await res.json()
      if (json.success) {
        anyOk = true
        if (key === 'kpi') {
          const d = json.data
          kpis.value = [
            { label: 'Uptime systemu', color: 'green', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>', current: d.uptime + '%', target: parseFloat(d.uptime), unit: '%', trend: d.uptime_trend, change: d.uptime_change + '%', spark: genSpark() },
            { label: 'Transakcji / dzień', color: 'cyan', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>', current: d.transactions.toLocaleString(), target: d.transactions, trend: d.transactions_trend, change: d.transactions_change + '%', spark: genSpark() },
            { label: 'Śr. czas przetwarzania', color: 'orange', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>', current: d.avg_processing_sec + 's', target: d.avg_processing_sec, unit: 's', trend: d.avg_processing_trend === 'up' ? 'down' : 'up', change: d.avg_processing_change + 's', spark: genSpark() },
            { label: 'SLA Procesów ETL', color: 'purple', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>', current: d.sla + '%', target: parseFloat(d.sla), unit: '%', trend: d.sla_trend, change: d.sla_change + '%', spark: genSpark() },
          ]
        } else if (key === 'etl') etl.value = json.data
        else if (key === 'sla') sla.value = json.data
        else if (key === 'alerts') { alerts.value = json.data; activity.value = json.data }
      }
    } catch {}
  }
  apiOk.value = anyOk
  messages.value = generateMessages()
}

onMounted(fetchAll)
</script>

<style scoped>
.hub-view { width: 100%; max-width: var(--content-width, 1100px); animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
.hub-section-header { margin-bottom: 28px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 600px; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
@media (max-width:800px){ .two-col { grid-template-columns: 1fr; } }
.api-status { display: flex; align-items: center; gap: 10px; padding: 12px 20px; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; font-size: 13px; color: var(--text-muted); margin-top: 8px; }
.api-dot { width: 8px; height: 8px; border-radius: 50%; background: #ff5252; }
.api-dot.online { background: #00c853; box-shadow: 0 0 8px rgba(0,200,83,0.4); animation: pulse 2s ease infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.5; } }
.btn-retry { margin-left: auto; padding: 6px 14px; border-radius: 6px; background: var(--bg-hover); border: 1px solid var(--border-color); color: var(--text-secondary); font-size: 12px; cursor: pointer; font-family: 'Inter', sans-serif; transition: border-color 0.15s, color 0.15s; }
.btn-retry:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
</style>