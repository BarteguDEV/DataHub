<template>
  <div class="hub-view">
    <!-- Header -->
    <div class="hub-section-header">
      <h1 class="section-title">Business Hub</h1>
      <p class="section-desc">
        Centrum monitoringu procesów biznesowych. Statusy komunikatów,
        wydajność ETL, SLA i alerty w czasie rzeczywistym.
      </p>
    </div>

    <!-- === KPI CARDS === -->
    <section class="kpi-bar">
      <article
        v-for="(k, i) in kpis"
        :key="k.label"
        class="kpi-card"
        :style="{ '--i': i }"
        @click="openKpiModal(k)"
      >
        <div class="kpi-icon-wrapper" :class="k.color">
          <span class="kpi-icon" v-html="k.icon"></span>
        </div>
        <div class="kpi-body">
          <span class="kpi-value">{{ k.current }}</span>
          <span class="kpi-label">{{ k.label }}</span>
          <span class="kpi-trend" :class="k.trend">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
              <polyline :points="k.trend === 'up' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"/>
            </svg>
            {{ k.change }}
          </span>
        </div>
        <!-- mini spark -->
        <div class="kpi-spark">
          <svg width="60" height="28" viewBox="0 0 60 28">
            <polyline
              :points="k.spark"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              class="spark-line"
              :class="k.color"
            />
          </svg>
        </div>
      </article>
    </section>

    <!-- === KOMUNIKATY — STATUS BAR === -->
    <section class="section-card message-card">
      <div class="card-header">
        <h2>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          Komunikaty — status wysyłki
        </h2>
        <span class="badge-api">ostatnie 24h</span>
      </div>
      <div class="msg-stats">
        <div
          v-for="msg in messages"
          :key="msg.label"
          class="msg-row"
          @click="openMsgModal(msg)"
        >
          <div class="msg-label">
            <span class="msg-dot" :style="{ background: msg.color }"></span>
            <span class="msg-name">{{ msg.label }}</span>
            <span class="msg-count">{{ msg.count.toLocaleString() }}</span>
          </div>
          <div class="msg-bar-track">
            <div
              class="msg-bar-fill"
              :style="{ width: msg.pct + '%', background: msg.color, '--w': msg.pct + '%' }"
            ></div>
          </div>
          <span class="msg-pct">{{ msg.pct }}%</span>
        </div>
      </div>
      <!-- mini podsumowanie -->
      <div class="msg-footer">
        <span>Razem: <strong>{{ totalMsgs.toLocaleString() }}</strong></span>
        <span class="msg-footer-success">
          <span class="pulse-dot"></span>
          System działa poprawnie
        </span>
      </div>
    </section>

    <!-- === WYKRES + AKTYWNOŚĆ (2 kolumny) === -->
    <div class="two-col">
      <!-- Donut chart -->
      <section class="section-card chart-card">
        <div class="card-header">
          <h2>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/>
            </svg>
            Rozkład komunikatów
          </h2>
        </div>
        <div class="donut-wrap">
          <svg width="200" height="200" viewBox="0 0 160 160" class="donut-svg">
            <circle cx="80" cy="80" r="64" fill="none" stroke="var(--bg-hover)" stroke-width="20"/>
            <circle
              v-for="(s, i) in donutSegments"
              :key="i"
              cx="80" cy="80" r="64"
              fill="none"
              :stroke="s.color"
              stroke-width="20"
              :stroke-dasharray="s.dash"
              :stroke-dashoffset="s.offset"
              :style="{ transform: 'rotate(-90deg)', transformOrigin: '80px 80px', transition: 'stroke-dashoffset 1.2s ease' }"
            />
            <text x="80" y="74" text-anchor="middle" fill="var(--text-primary)" font-size="24" font-weight="700">{{ successRate }}%</text>
            <text x="80" y="94" text-anchor="middle" fill="var(--text-muted)" font-size="11">dostarczone</text>
          </svg>
          <div class="donut-legend">
            <div v-for="s in donutSegments" :key="s.label" class="legend-item">
              <span class="legend-swatch" :style="{ background: s.color }"></span>
              <span class="legend-label">{{ s.label }}</span>
              <span class="legend-val">{{ s.count.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Ostatnia aktywność -->
      <section class="section-card activity-card">
        <div class="card-header">
          <h2>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
            Ostatnia aktywność
          </h2>
        </div>
        <div class="activity-list">
          <TransitionGroup name="list">
            <div v-for="a in activity" :key="a.id" class="activity-row" @click="openActivityModal(a)">
              <span class="activity-dot" :class="a.level"></span>
              <div class="activity-body">
                <span class="activity-msg">{{ a.message }}</span>
                <span class="activity-meta">{{ a.source }} • {{ formatTimeAgo(a.timestamp) }}</span>
              </div>
              <svg class="activity-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </div>
          </TransitionGroup>
        </div>
      </section>
    </div>

    <!-- === ETL WORKFLOWY (KLIKALNE → MODAL) === -->
    <section class="section-card">
      <div class="card-header">
        <h2>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
          </svg>
          ETL Workflows
        </h2>
        <span class="badge-api">Dane z /api/business/etl</span>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Śr. czas</th>
            <th>Rekordy</th>
            <th>Success rate</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in etl" :key="e.workflow" class="clickable-row" @click="openEtlModal(e)">
            <td class="cell-mono">{{ e.workflow }}</td>
            <td>{{ e.avg_duration_min }} min</td>
            <td>{{ formatNum(e.rows_processed) }}</td>
            <td>
              <div class="mini-bar">
                <div class="mini-bar-fill" :style="{ width: e.success_rate + '%' }"></div>
              </div>
              <span class="mini-bar-label">{{ e.success_rate }}%</span>
            </td>
            <td>
              <span class="status-badge" :class="e.status">
                <span class="status-dot" :class="e.status"></span>
                {{ e.status === 'stable' ? 'Stable' : 'Degraded' }}
              </span>
            </td>
            <td>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- === SLA COMPLIANCE === -->
    <section class="section-card">
      <div class="card-header">
        <h2>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
          SLA Compliance
        </h2>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>Usługa</th>
            <th>Target</th>
            <th>Actual</th>
            <th>Incydenty</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in sla" :key="s.service">
            <td>{{ s.service }}</td>
            <td>{{ s.sla_target }}%</td>
            <td>
              <div class="sla-actual-bar">
                <div
                  class="sla-actual-fill"
                  :class="{ warning: s.actual < s.sla_target, critical: s.actual < s.sla_target - 1 }"
                  :style="{ width: Math.min(s.actual, 100) + '%' }"
                ></div>
              </div>
              <span class="sla-actual-label">{{ s.actual }}%</span>
            </td>
            <td>{{ s.incidents }}</td>
            <td>
              <span class="status-badge" :class="s.status">
                <span class="status-dot" :class="s.status"></span>
                {{ s.status === 'ok' ? 'OK' : 'Warning' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- === MODAL OVERLAY === -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="modal.show" class="modal-overlay" @click.self="closeModal">
          <div class="modal-panel">
            <div class="modal-header">
              <h3>{{ modal.title }}</h3>
              <button class="modal-close" @click="closeModal">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            <div class="modal-body" v-html="modal.body"></div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- API STATUS -->
    <div class="api-status">
      <span class="api-dot" :class="{ online: apiOk }"></span>
      <span>{{ apiOk ? 'API Business Hub online' : 'API niedostępne' }}</span>
      <button v-if="!apiOk" class="btn-retry" @click="fetchAll">Ponów</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'

const API_BASE = window.location.origin
const apiOk = ref(false)

// ---- stany ----
const kpis = ref([])
const etl = ref([])
const sla = ref([])
const alerts = ref([])
const activity = ref([])
const messages = ref([])

const modal = reactive({ show: false, title: '', body: '' })

// ---- brak animacji liczników JS — KPI wyświetla wartość finalną od razu (CSS cardSlide wystarczy) ----

// ---- generowanie sparklines dla KPI ----
function genSpark() {
  const pts = []
  for (let i = 0; i < 10; i++) {
    const x = i * 6
    const y = 24 - Math.random() * 20
    pts.push(`${x},${y}`)
  }
  return pts.join(' ')
}

// ---- mock danych dla wiadomości ----
function generateMessages() {
  const raw = {
    SENT: { count: 28450, color: '#00c853' },
    ACPT: { count: 27120, color: '#00e5ff' },
    RJCT: { count: 890, color: '#ff5252' },
    INVALID: { count: 340, color: '#ff9100' },
    READY: { count: 4120, color: '#536dfe' },
  }
  const total = Object.values(raw).reduce((s, v) => s + v.count, 0)
  return Object.entries(raw).map(([label, v]) => ({
    label,
    count: v.count,
    color: v.color,
    pct: Math.round((v.count / total) * 100),
  }))
}

const totalMsgs = computed(() => messages.value.reduce((s, m) => s + m.count, 0))
const successRate = computed(() => {
  const sent = messages.value.find(m => m.label === 'SENT')?.count || 1
  const acpt = messages.value.find(m => m.label === 'ACPT')?.count || 0
  return Math.round((acpt / sent) * 100)
})

// ---- donut segments ----
const donutSegments = computed(() => {
  const total = totalMsgs.value || 1
  const circumference = 2 * Math.PI * 64
  let offset = 0
  return messages.value.map(m => {
    const pct = m.count / total
    const dash = pct * circumference
    const seg = {
      ...m,
      dash: `${dash} ${circumference - dash}`,
      offset: -offset,
    }
    offset += dash
    return seg
  })
})

// ---- formaty ----
function formatNum(n) {
  return Number(n).toLocaleString('pl-PL')
}

function formatTimeAgo(ts) {
  const diff = Date.now() - new Date(ts).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m temu`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h temu`
  return `${Math.floor(hrs / 24)}d temu`
}

// ---- modale ----
function closeModal() {
  modal.show = false
}

function openKpiModal(k) {
  modal.title = k.label
  modal.body = `
    <div class="modal-kpi">
      <div class="modal-kpi-big">${k.current}${k.unit || ''}</div>
      <div class="modal-kpi-row">
        <span class="modal-label">Trend</span>
        <span class="modal-value" style="color: ${k.trend === 'up' ? 'var(--accent-primary)' : '#ff5252'}">
          ${k.trend === 'up' ? '▲' : '▼'} ${k.change}
        </span>
      </div>
      <div class="modal-kpi-row">
        <span class="modal-label">Szczegóły</span>
        <span class="modal-value">Wartość z ostatniej synchronizacji</span>
      </div>
      <div class="modal-kpi-row">
        <span class="modal-label">Ostatnia aktualizacja</span>
        <span class="modal-value">${new Date().toLocaleString('pl-PL')}</span>
      </div>
    </div>
  `
  modal.show = true
}

function openMsgModal(m) {
  modal.title = `Status: ${m.label}`
  modal.body = `
    <div class="modal-msg">
      <div class="modal-msg-bar" style="background: ${m.color}; width: 100%; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; color: #000;">
        ${m.count.toLocaleString()} (${m.pct}%)
      </div>
      <div style="margin-top: 16px; display: grid; gap: 10px;">
        <div class="modal-kpi-row"><span class="modal-label">Status</span><span class="modal-value">${m.label}</span></div>
        <div class="modal-kpi-row"><span class="modal-label">Liczba komunikatów</span><span class="modal-value">${m.count.toLocaleString()}</span></div>
        <div class="modal-kpi-row"><span class="modal-label">Udział procentowy</span><span class="modal-value">${m.pct}%</span></div>
        <div class="modal-kpi-row"><span class="modal-label">Przedział czasu</span><span class="modal-value">Ostatnie 24h</span></div>
      </div>
    </div>
  `
  modal.show = true
}

function openActivityModal(a) {
  modal.title = `Alert: ${a.source}`
  modal.body = `
    <div class="modal-activity">
      <div class="modal-kpi-row"><span class="modal-label">Źródło</span><span class="modal-value">${a.source}</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Wiadomość</span><span class="modal-value">${a.message}</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Poziom</span><span class="modal-value" style="text-transform: uppercase; color: ${a.level === 'critical' ? '#ff5252' : a.level === 'warning' ? '#ff9100' : '#00e5ff'}">${a.level}</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Czas</span><span class="modal-value">${formatTimeAgo(a.timestamp)}</span></div>
    </div>
  `
  modal.show = true
}

function openEtlModal(e) {
  modal.title = `ETL: ${e.workflow}`
  modal.body = `
    <div class="modal-etl">
      <div class="modal-kpi-row"><span class="modal-label">Workflow</span><span class="modal-value cell-mono">${e.workflow}</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Średni czas</span><span class="modal-value">${e.avg_duration_min} min</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Przetworzone rekordy</span><span class="modal-value">${formatNum(e.rows_processed)}</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Skuteczność</span><span class="modal-value">${e.success_rate}%</span></div>
      <div class="modal-kpi-row"><span class="modal-label">Status</span><span class="modal-value" style="color: ${e.status === 'stable' ? 'var(--accent-primary)' : '#ff9100'}">${e.status === 'stable' ? 'Stable' : 'Degraded'}</span></div>
    </div>
  `
  modal.show = true
}

// ---- fetch z API ----
async function fetchAll() {
  const endpoints = {
    kpi: '/api/business/kpi',
    trends: '/api/business/trends',
    etl: '/api/business/etl',
    sla: '/api/business/sla',
    alerts: '/api/business/alerts',
  }

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
            {
              label: 'Uptime systemu', color: 'green',
              icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
              current: d.uptime + '%', target: parseFloat(d.uptime),
              unit: '%', trend: d.uptime_trend, change: d.uptime_change + '%',
              spark: genSpark(),
            },
            {
              label: 'Transakcji / dzień', color: 'cyan',
              icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
              current: d.transactions.toLocaleString(), target: d.transactions,
              trend: d.transactions_trend, change: d.transactions_change + '%',
              spark: genSpark(),
            },
            {
              label: 'Śr. czas przetwarzania', color: 'orange',
              icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
              current: d.avg_processing_sec + 's', target: d.avg_processing_sec,
              unit: 's', trend: d.avg_processing_trend === 'up' ? 'down' : 'up',
              change: d.avg_processing_change + 's',
              spark: genSpark(),
            },
            {
              label: 'SLA Procesów ETL', color: 'purple',
              icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
              current: d.sla + '%', target: parseFloat(d.sla),
              unit: '%', trend: d.sla_trend, change: d.sla_change + '%',
              spark: genSpark(),
            },
          ]
          // KPI gotowe — animacja CSS cardSlide robi efekt wejścia
        } else if (key === 'etl') {
          etl.value = json.data
        } else if (key === 'sla') {
          sla.value = json.data
        } else if (key === 'alerts') {
          alerts.value = json.data
          activity.value = json.data
        }
      }
    } catch {
      // endpoint unavailable
    }
  }

  apiOk.value = anyOk
  messages.value = generateMessages()
}

onMounted(fetchAll)
</script>

<style scoped>
/* =============================================================
   Business Hub — Design System / shadcn-ui inspired
   ============================================================= */
.hub-view {
  width: 100%;
  max-width: var(--content-width, 1100px);
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.hub-section-header { margin-bottom: 28px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 600px; }

/* ---- Card header (shadcn-ui style) ---- */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
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
.badge-api {
  font-size: 10px;
  font-weight: 500;
  color: #536dfe;
  padding: 3px 10px;
  border-radius: 100px;
  background: rgba(83,109,254,0.1);
  white-space: nowrap;
}

.section-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 22px 24px;
  margin-bottom: 20px;
  transition: border-color 0.2s ease;
}

/* =============================================================
   KPI CARDS
   ============================================================= */
.kpi-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  gap: 14px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  animation: cardSlide 0.5s ease both;
  animation-delay: calc(var(--i) * 0.1s);
  position: relative;
  overflow: hidden;
}
.kpi-card:hover {
  border-color: rgba(255,255,255,0.15);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

@keyframes cardSlide {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.kpi-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.kpi-icon-wrapper.green { background: rgba(0,200,83,0.12); color: #00c853; }
.kpi-icon-wrapper.cyan { background: rgba(0,229,255,0.12); color: #00e5ff; }
.kpi-icon-wrapper.orange { background: rgba(255,145,0,0.12); color: #ff9100; }
.kpi-icon-wrapper.purple { background: rgba(83,109,254,0.12); color: #536dfe; }

.kpi-body { flex: 1; min-width: 0; }
.kpi-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  display: block;
  line-height: 1.2;
}
.kpi-label {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 2px;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kpi-trend {
  font-size: 11px;
  font-weight: 600;
  margin-top: 4px;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
.kpi-trend.up { color: #00c853; }
.kpi-trend.down { color: #ff5252; }

.kpi-spark {
  position: absolute;
  right: 8px;
  bottom: 8px;
  opacity: 0.4;
}
.spark-line.green { color: #00c853; }
.spark-line.cyan { color: #00e5ff; }
.spark-line.orange { color: #ff9100; }
.spark-line.purple { color: #536dfe; }

/* =============================================================
   MESSAGE STATUS BARS
   ============================================================= */
.message-card { border-left: 3px solid #536dfe; }
.msg-stats { display: flex; flex-direction: column; gap: 10px; }
.msg-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
}
.msg-row:hover { background: var(--bg-hover); }
.msg-label {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 140px;
}
.msg-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  animation: pulse 2s ease infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.msg-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  width: 60px;
}
.msg-count {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
}
.msg-bar-track {
  flex: 1;
  height: 10px;
  background: var(--bg-hover);
  border-radius: 100px;
  overflow: hidden;
}
.msg-bar-fill {
  height: 100%;
  border-radius: 100px;
  transition: width 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  animation: barGrow 1.2s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes barGrow {
  from { width: 0 !important; }
  to { width: var(--w); }
}
.msg-pct {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  min-width: 40px;
  text-align: right;
}
.msg-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
  font-size: 12px;
  color: var(--text-muted);
}
.msg-footer-success {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #00c853;
}
.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00c853;
  animation: pulse 1.5s ease infinite;
}

/* =============================================================
   TWO-COLUMN LAYOUT
   ============================================================= */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
@media (max-width: 800px) {
  .two-col { grid-template-columns: 1fr; }
}

/* =============================================================
   DONUT CHART
   ============================================================= */
.chart-card {
  display: flex;
  flex-direction: column;
  min-height: 260px;
}
.donut-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex: 1;
  padding: 8px 0;
}
.donut-svg {
  flex-shrink: 0;
  display: block;
}
.donut-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}
.legend-swatch {
  width: 12px;
  height: 12px;
  border-radius: 4px;
  flex-shrink: 0;
}
.legend-label {
  color: var(--text-secondary);
  min-width: 70px;
  font-weight: 500;
}
.legend-val {
  color: var(--text-primary);
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}

/* =============================================================
   ACTIVITY LIST
   ============================================================= */
.activity-card { min-height: 260px; }
.activity-list { display: flex; flex-direction: column; }
.activity-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid var(--border-color);
}
.activity-row:last-child { border: none; }
.activity-row:hover { background: var(--bg-hover); }
.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 2px;
}
.activity-dot.critical { background: #ff5252; animation: pulse 1s ease infinite; }
.activity-dot.warning { background: #ff9100; animation: pulse 2s ease infinite; }
.activity-dot.info { background: #00e5ff; }
.activity-body { flex: 1; min-width: 0; }
.activity-msg {
  font-size: 13px;
  color: var(--text-primary);
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.activity-meta {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
  display: block;
}
.activity-chevron { flex-shrink: 0; }

/* List transition */
.list-enter-active { transition: all 0.3s ease; }
.list-leave-active { transition: all 0.2s ease; }
.list-enter-from { opacity: 0; transform: translateX(-10px); }
.list-leave-to { opacity: 0; transform: translateX(10px); }

/* =============================================================
   TABLES (shadcn-ui style)
   ============================================================= */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.data-table thead th {
  text-align: left;
  padding: 10px 12px;
  color: var(--text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
}
.data-table tbody td {
  padding: 12px 12px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
}
.data-table tbody tr:last-child td { border: none; }
.data-table tbody tr:hover td { background: var(--bg-hover); }

.clickable-row { cursor: pointer; }
.clickable-row td:last-child { text-align: right; }

.cell-mono { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-primary); }

/* Mini bar in table */
.mini-bar {
  width: 80px;
  height: 6px;
  background: var(--bg-hover);
  border-radius: 100px;
  overflow: hidden;
  display: inline-block;
  vertical-align: middle;
}
.mini-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #00c853, #00e5ff);
  border-radius: 100px;
  transition: width 0.8s ease;
}
.mini-bar-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-primary);
  margin-left: 8px;
  vertical-align: middle;
}

/* SLA actual bar */
.sla-actual-bar {
  width: 80px;
  height: 6px;
  background: var(--bg-hover);
  border-radius: 100px;
  overflow: hidden;
  display: inline-block;
  vertical-align: middle;
}
.sla-actual-fill {
  height: 100%;
  background: var(--accent-primary);
  border-radius: 100px;
  transition: width 0.8s ease;
}
.sla-actual-fill.warning { background: #ff9100; }
.sla-actual-fill.critical { background: #ff5252; }
.sla-actual-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-primary);
  margin-left: 8px;
  vertical-align: middle;
}

/* Status badges */
.status-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 100px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}
.status-badge.stable, .status-badge.ok {
  background: rgba(0,200,83,0.1);
  color: #00c853;
}
.status-badge.warning, .status-badge.degraded {
  background: rgba(255,145,0,0.1);
  color: #ff9100;
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.status-dot.stable, .status-dot.ok { background: #00c853; }
.status-dot.warning, .status-dot.degraded { background: #ff9100; animation: pulse 1.5s ease infinite; }

/* =============================================================
   MODAL (Teleport)
   ============================================================= */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}
.modal-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 100%;
  max-width: 480px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border-color);
}
.modal-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}
.modal-close {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  transition: color 0.15s, background 0.15s;
}
.modal-close:hover { color: var(--text-primary); background: var(--bg-hover); }
.modal-body {
  padding: 20px 22px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Modal content styles (rendered as HTML) */
.modal-body :deep(.modal-kpi-big) {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
  padding: 16px 0;
}
.modal-body :deep(.modal-kpi-row) {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color);
}
.modal-body :deep(.modal-kpi-row:last-child) { border: none; }
.modal-body :deep(.modal-label) { color: var(--text-muted); }
.modal-body :deep(.modal-value) { color: var(--text-primary); font-weight: 500; text-align: right; }

/* Modal transition */
.modal-enter-active { transition: opacity 0.2s ease; }
.modal-leave-active { transition: opacity 0.15s ease; }
.modal-enter-from,
.modal-leave-to { opacity: 0; }
.modal-enter-active .modal-panel { animation: modalIn 0.25s ease; }
.modal-leave-active .modal-panel { animation: modalOut 0.15s ease; }
@keyframes modalIn {
  from { transform: scale(0.95) translateY(10px); opacity: 0; }
  to { transform: scale(1) translateY(0); opacity: 1; }
}
@keyframes modalOut {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(0.95); opacity: 0; }
}

/* =============================================================
   API STATUS
   ============================================================= */
.api-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 8px;
}
.api-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff5252;
}
.api-dot.online {
  background: #00c853;
  box-shadow: 0 0 8px rgba(0,200,83,0.4);
  animation: pulse 2s ease infinite;
}
.btn-retry {
  margin-left: auto;
  padding: 6px 14px;
  border-radius: 6px;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  transition: border-color 0.15s, color 0.15s;
}
.btn-retry:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
</style>
