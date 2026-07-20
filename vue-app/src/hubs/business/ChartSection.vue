<template>
  <div class="chart-section" ref="sectionRef">
    <!-- Nagłówek + przełącznik -->
    <div class="chart-top">
      <span class="chart-subtitle">Rozkład komunikatów</span>
      <div class="chart-tabs">
        <button
          v-for="t in tabs"
          :key="t.id"
          class="tab-btn"
          :class="{ active: activeTab === t.id }"
          @click="activeTab = t.id"
        >{{ t.label }}</button>
      </div>
    </div>

    <!-- ======================== -->
    <!-- B: Słupkowy — osobne słupki -->
    <!-- ======================== -->
    <div v-if="activeTab === 'stacked'" class="chart-body chart-body-stacked">
      <div class="stacked-wrap">
        <svg viewBox="0 0 420 240" class="stacked-svg">
          <!-- Oś Y — siatka i etykiety -->
          <g v-for="t in stackedYTicks" :key="'st'+t.pct">
            <line :x1="50" :y1="t.y" :x2="410" :y2="t.y" stroke="var(--border-color)" stroke-width="0.5" opacity="0.35"/>
            <text x="45" :y="t.y + 3" text-anchor="end" fill="var(--text-muted)" font-size="8" font-family="'JetBrains Mono', monospace">{{ formatK(t.val) }}</text>
          </g>

          <!-- Słupki -->
          <g v-for="(s, i) in stackedBars" :key="i">
            <rect
              :x="s.x"
              :y="s.y"
              :width="s.w"
              :height="s.h"
              :fill="s.color"
              rx="5"
              class="stack-seg"
              @mouseenter="showTip($event, s.label, s.count, s.color)"
              @mousemove="moveTip"
              @mouseleave="hideTip"
            />
            <!-- Wartość nad słupkiem -->
            <text :x="s.x + s.w / 2" :y="s.y - 6" text-anchor="middle" fill="var(--text-muted)" font-size="9" font-family="'JetBrains Mono', monospace">{{ s.shortCount }}</text>
            <!-- Etykieta pod słupkiem -->
            <text :x="s.x + s.w / 2" y="230" text-anchor="middle" fill="var(--text-secondary)" font-size="9" font-weight="600">{{ s.label }}</text>
          </g>
        </svg>
      </div>
    </div>

    <!-- ======================== -->
    <!-- C: Liniowy — wszystkie 5 -->
    <!-- ======================== -->
    <div v-if="activeTab === 'line'" class="chart-body">
      <svg viewBox="0 0 400 200" class="chart-svg">
        <!-- Siatka Y -->
        <line v-for="gl in lineGrid" :key="'gl'+gl.y" :x1="40" :y1="gl.y" :x2="390" :y2="gl.y" stroke="var(--border-color)" stroke-width="0.5" opacity="0.35"/>
        <text v-for="gl in lineGrid" :key="'yl'+gl.y" :x="36" :y="gl.y + 3" text-anchor="end" fill="var(--text-muted)" font-size="8">{{ formatK(gl.val) }}</text>
        <!-- Linie -->
        <path v-for="(ser, si) in lineSeries" :key="'ln'+si" :d="ser.path" :stroke="ser.color" stroke-width="2" fill="none" stroke-linecap="round" class="line-path"/>
        <!-- Punkty -->
        <circle v-for="(pt, pi) in linePoints" :key="'pt'+pi" :cx="pt.x" :cy="pt.y" r="3" :fill="pt.color" class="line-dot" @mouseenter="showTip($event, pt.label, pt.val, pt.color)" @mousemove="moveTip" @mouseleave="hideTip"/>
        <!-- Etykiety X z tłem -->
        <g v-for="xl in lineXLabs" :key="'xg'+xl.x">
          <rect :x="xl.x - 16" y="186" width="32" height="14" rx="3" fill="var(--bg-card)" opacity="0.85"/>
          <text :x="xl.x" :y="196" text-anchor="middle" fill="var(--text-muted)" font-size="8">{{ xl.label }}</text>
        </g>       </svg>
      <div class="line-legend">
        <div v-for="s in lineColors" :key="s.label" class="s-leg-item">
          <span class="s-leg-swatch" :style="{ background: s.color }"></span>
          <span class="s-leg-label-s">{{ s.label }}</span>
          <span class="s-leg-val">{{ s.pct }}%</span>
        </div>
      </div>
    </div>

    <!-- ======================== -->
    <!-- D: Donut                 -->
    <!-- ======================== -->
    <div v-if="activeTab === 'donut'" class="chart-body chart-donut-body">
      <svg viewBox="0 0 200 200" class="donut-svg">
        <circle cx="100" cy="100" r="76" fill="none" stroke="var(--bg-hover)" stroke-width="22"/>
        <circle v-for="(s, i) in donutSegments" :key="i" cx="100" cy="100" r="76" fill="none" :stroke="s.color" stroke-width="22" :stroke-dasharray="s.dash" :stroke-dashoffset="s.offset" style="transform:rotate(-90deg);transform-origin:100px 100px;transition:stroke-dashoffset 1.2s ease"/>
        <text x="100" y="90" text-anchor="middle" fill="var(--text-primary)" font-size="22" font-weight="700">{{ successRate }}%</text>
        <text x="100" y="110" text-anchor="middle" fill="var(--text-muted)" font-size="10">ACPT / ogółem</text>
      </svg>
      <div class="donut-legend-right">
        <div v-for="s in segments" :key="s.label" class="s-leg-item">
          <span class="s-leg-swatch" :style="{ background: s.color }"></span>
          <span class="s-leg-label">{{ s.label }}</span>
          <span class="s-leg-val">{{ s.pct }}%</span>
        </div>
      </div>
    </div>

    <!-- Tooltip -->
    <div v-if="tip.show" class="chart-tip" :style="{ left: tip.x + 'px', top: tip.y + 'px' }">
      <div class="tip-row">
        <span class="tip-swatch" :style="{ background: tip.color }"></span>
        <span class="tip-label">{{ tip.label }}</span>
        <span class="tip-val">{{ tip.val }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const props = defineProps({
  segments: { type: Array, required: true },
  successRate: { type: Number, default: 0 }
})

const SVG_W = 400

const activeTab = ref('stacked')
const tabs = [
  { id: 'stacked', label: 'B-stacked' },
  { id: 'line', label: 'C-line' },
  { id: 'donut', label: 'D-donut' },
]

// --- Tooltip ---
const tip = reactive({ show: false, x: 0, y: 0, label: '', val: '', color: '' })
const sectionRef = ref(null)
function showTip(e, label, val, color) { tip.show = true; tip.label = label; tip.val = val; tip.color = color; moveTip(e) }
function moveTip(e) {
  const r = sectionRef.value?.getBoundingClientRect()
  if (!r) return
  tip.x = e.clientX - r.left + 14
  tip.y = e.clientY - r.top - 10
}
function hideTip() { tip.show = false }

function formatK(v) {
  if (v >= 1000) return (v / 1000).toFixed(v >= 10000 ? 0 : 1) + 'k'
  return String(v)
}

// ===========================
// B — Osobne słupki (z osią Y w wartościach)
// ===========================
const stackedYTicks = computed(() => {
  const max = getMaxCount()
  const ticks = []
  for (let i = 0; i <= 4; i++) {
    const val = Math.round((max / 4) * i)
    const y = 215 - (val / max) * 180
    ticks.push({ pct: val, y, val })
  }
  return ticks
})

function getMaxCount() {
  let max = 0
  props.segments.forEach(s => { if (s.count > max) max = s.count })
  return Math.ceil(max / 5000) * 5000 || 5000
}

const stackedBars = computed(() => {
  const max = getMaxCount()
  const barW = 52
  const gap = 12
  const totalW = props.segments.length * barW + (props.segments.length - 1) * gap
  const startX = (420 - totalW) / 2
  const chartH = 180
  const barY = 35

  // Sort: największy na końcu (po prawej)
  const sorted = [...props.segments].sort((a, b) => b.count - a.count)

  return sorted.map((s, i) => {
    const h = (s.count / max) * chartH
    const x = startX + i * (barW + gap)
    return {
      x,
      y: barY + (chartH - h),
      w: barW,
      h: Math.max(h, 4),
      color: s.color,
      label: s.label,
      count: s.count.toLocaleString(),
      shortCount: formatK(s.count),
    }
  })
})

// ===========================
// C — Line (wszystkie 5 statusów)
// ===========================
const lineColors = computed(() =>
  props.segments.map(s => ({
    label: s.label,
    color: s.color,
    pct: s.pct,
  }))
)

const lineData = computed(() => {
  const LABELS = ['6:00','8:00','10:00','12:00','14:00','16:00','18:00','20:00']
  const result = {}
  // Dla każdego statusu wygeneruj profil dzienny
  props.segments.forEach(s => {
    const base = s.count
    // Profile: SENT i ACPT rosną w ciągu dnia, RJCT/INVALID maleją, READY stabilne
    const profile = s.label === 'SENT' || s.label === 'ACPT'
      ? [0.3, 0.5, 0.8, 1.0, 1.0, 0.9, 0.6, 0.3]
      : s.label === 'RJCT' || s.label === 'INVALID'
        ? [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
        : [0.5, 0.6, 0.8, 1.0, 1.0, 0.9, 0.7, 0.5] // READY
    const values = profile.map((p, i) => Math.round(base / 8 * p * (0.85 + Math.random() * 0.3)))
    result[s.label] = { values, color: s.color }
  })
  return { labels: LABELS, series: result }
})

const lineMax = computed(() => {
  let max = 0
  Object.values(lineData.value.series).forEach(s => {
    s.values.forEach(v => { if (v > max) max = v })
  })
  return Math.ceil(max / 1000) * 1000 || 1000
})

const lineGrid = computed(() => {
  const ticks = []
  for (let i = 0; i <= 4; i++) {
    const val = Math.round((lineMax.value / 4) * i)
    const y = 190 - (val / lineMax.value) * 160
    ticks.push({ y, val })
  }
  return ticks
})

function buildPath(values) {
  const points = values.map((v, i) => ({
    x: 40 + (i / (values.length - 1)) * 350,
    y: 190 - (v / lineMax.value) * 160,
  }))
  let d = `M${points[0].x},${points[0].y}`
  for (let i = 1; i < points.length - 1; i++) {
    const cx1 = (points[i].x + points[i + 1].x) / 2
    const cx2 = (points[i].x + points[i + 1].x) / 2
    d += ` C${cx1},${points[i].y} ${cx2},${points[i + 1].y} ${points[i + 1].x},${points[i + 1].y}`
  }
  return d
}

const lineSeries = computed(() =>
  Object.entries(lineData.value.series).map(([label, s]) => ({
    label,
    color: s.color,
    path: buildPath(s.values),
  }))
)

const linePoints = computed(() => {
  const pts = []
  Object.entries(lineData.value.series).forEach(([label, s]) => {
    s.values.forEach((v, i) => {
      pts.push({
        x: 40 + (i / (s.values.length - 1)) * 350,
        y: 190 - (v / lineMax.value) * 160,
        color: s.color,
        label: `${label} ${lineData.value.labels[i]}`,
        val: v.toLocaleString(),
      })
    })
  })
  return pts
})

const lineXLabs = computed(() =>
  lineData.value.labels.map((l, i) => ({
    x: 40 + (i / (lineData.value.labels.length - 1)) * 350,
    label: l,
  }))
)

// ===========================
// D — Donut (fix: successRate = ACPT/total)
// ===========================
const donutSegments = computed(() => {
  const total = props.segments.reduce((s, m) => s + m.count, 0) || 1
  const circumference = 2 * Math.PI * 76
  let offset = 0
  return props.segments.map(m => {
    const pct = m.count / total
    const dash = pct * circumference
    const seg = { ...m, dash: `${dash} ${circumference - dash}`, offset: -offset }
    offset += dash
    return seg
  })
})
</script>

<style scoped>
.chart-section {
  padding-top: 14px;
  margin-top: 12px;
  border-top: 1px solid var(--border-color);
}

/* Nagłówek + przełącznik */
.chart-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.chart-subtitle {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}
.chart-tabs {
  display: flex;
  gap: 4px;
}
.tab-btn {
  padding: 3px 10px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-hover);
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
  letter-spacing: 0.3px;
}
.tab-btn:hover {
  border-color: var(--accent-primary);
  color: var(--text-secondary);
}
.tab-btn.active {
  background: rgba(83,109,254,0.12);
  border-color: #536dfe;
  color: #536dfe;
}

/* Wspólne */
.chart-body {
  display: flex;
  align-items: center;
  gap: 20px;
}
.chart-svg {
  width: 100%;
  max-width: 400px;
  height: auto;
  display: block;
  flex-shrink: 0;
}

/* ======== B — Stacked ======== */
.chart-body-stacked {
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.stacked-wrap {
  width: 100%;
  max-width: 440px;
}
.stacked-svg {
  width: 100%;
  height: auto;
  display: block;
}
.stack-seg {
  cursor: pointer;
  transition: opacity 0.15s;
}
.stack-seg:hover {
  opacity: 0.85;
}

/* ======== C — Line ======== */
.line-path {
  transition: d 0.3s ease;
}
.line-dot {
  cursor: pointer;
  transition: r 0.15s;
  opacity: 0.7;
}
.line-dot:hover {
  r: 5;
  opacity: 1;
}
.line-legend {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

/* ======== D — Donut ======== */
.chart-donut-body {
  justify-content: center;
}
.donut-svg {
  width: 170px;
  height: 170px;
  display: block;
}
.donut-legend-right {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Legenda (wspólna) */
.s-leg-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
}
.s-leg-swatch {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  flex-shrink: 0;
}
.s-leg-label {
  color: var(--text-secondary);
  min-width: 50px;
  font-weight: 500;
}
.s-leg-label-s {
  color: var(--text-secondary);
  font-weight: 500;
}
.s-leg-val {
  color: var(--text-primary);
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
}

/* Tooltip */
.chart-tip {
  position: absolute;
  pointer-events: none;
  z-index: 10;
  background: var(--bg-overlay);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 6px 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  white-space: nowrap;
}
.tip-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--text-secondary);
}
.tip-swatch {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  flex-shrink: 0;
}
.tip-val {
  color: var(--text-primary);
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  margin-left: auto;
}
</style>
