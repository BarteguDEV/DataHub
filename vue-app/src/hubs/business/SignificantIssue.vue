<template>
  <section class="section-card issue-card">
    <div class="card-header">
      <h2>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
        Significant Issue
      </h2>
    </div>

    <!-- Karty systemów -->
    <div class="issue-grid">
      <div
        v-for="item in items"
        :key="item.id"
        class="issue-card-item"
      >
        <div class="issue-item-header">
          <span class="issue-badge">{{ item.id }}</span>
          <span class="issue-name">{{ item.name }}</span>
        </div>
        <div class="issue-number">{{ formatNum(item.backlog) }}</div>
        <div class="issue-label">zaległości</div>
        <div class="issue-bar-track">
          <div
            class="issue-bar-fill"
            :style="{ width: item.pct + '%', background: item.color }"
          ></div>
        </div>
        <div class="issue-meta">
          <span class="issue-trend" :class="item.trend">
            {{ item.trend === 'up' ? '▲' : '▼' }} {{ item.change }}
          </span>
          <span class="issue-pct">{{ item.pct }}% udziału</span>
        </div>
      </div>
    </div>

    <!-- Grupowy wykres słupkowy — tydzień -->
    <div class="weekly-chart-section">
      <div class="weekly-chart-header">
        <span class="compact-chart-header">Napływ vs. rozwiązane — ostatnie 7 dni</span>
        <div class="chart-legend">
          <span class="legend-dot" style="background: var(--chart-inflow)"></span>
          <span class="legend-label">napływ</span>
          <span class="legend-dot" style="background: var(--chart-resolved)"></span>
          <span class="legend-label">rozwiązane</span>
        </div>
      </div>

      <div
        class="chart-container"
        @mouseleave="tooltip.visible = false"
      >
        <!-- Oś Y -->
        <div class="y-axis">
          <div v-for="tick in yTicks" :key="tick" class="y-tick">
            <span class="y-tick-label">{{ tick }}</span>
          </div>
        </div>

        <!-- Obszar wykresu -->
        <div class="chart-area" ref="chartArea">
          <!-- Linie siatki Y -->
          <div
            v-for="(tick, i) in yTicks"
            :key="'grid-' + i"
            class="grid-line"
            :style="{ bottom: (i / (yTicks.length - 1)) * 100 + '%' }"
          ></div>

          <!-- Słupki -->
          <div
            v-for="(day, di) in weekData"
            :key="di"
            class="bar-group"
            :style="{ left: (di / (weekData.length - 1)) * 100 + '%' }"
          >
            <!-- inflow -->
            <div
              class="bar bar-inflow"
              :style="{
                height: (day.inflow / yMax) * 100 + '%',
                background: 'var(--chart-inflow)'
              }"
              @mouseenter="showTooltip($event, day.date, 'napływ', day.inflow)"
              @mousemove="moveTooltip"
            ></div>
            <!-- resolved -->
            <div
              class="bar bar-resolved"
              :style="{
                height: (day.resolved / yMax) * 100 + '%',
                background: 'var(--chart-resolved)'
              }"
              @mouseenter="showTooltip($event, day.date, 'rozwiązane', day.resolved)"
              @mousemove="moveTooltip"
            ></div>
          </div>

          <!-- Etykiety X -->
          <div
            v-for="(day, di) in weekData"
            :key="'xl-' + di"
            class="x-label"
            :style="{ left: (di / (weekData.length - 1)) * 100 + '%' }"
          >{{ formatDateLabel(day.date) }}</div>
        </div>

        <!-- Tooltip -->
        <div
          v-if="tooltip.visible"
          class="chart-tooltip"
          :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
        >
          <div class="tt-date">{{ tooltip.date }}</div>
          <div class="tt-row">
            <span class="tt-swatch" :style="{ background: tooltip.color }"></span>
            <span class="tt-label">{{ tooltip.series }}</span>
            <span class="tt-value">{{ tooltip.value }}</span>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="chart-footer">
        <div class="footer-trend">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2.5">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
            <polyline points="17 6 23 6 23 12"/>
          </svg>
          Rozwiązywalność wzrosła o <strong>5.2%</strong> w tym tygodniu
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

function formatNum(n) {
  return Number(n).toLocaleString('pl-PL')
}

// --- Weekly chart data: 01/07/2026 – 07/07/2026 ---
const weekRaw = [
  { date: '2026-07-01', inflow: 187, resolved: 145 },
  { date: '2026-07-02', inflow: 203, resolved: 178 },
  { date: '2026-07-03', inflow: 156, resolved: 162 },
  { date: '2026-07-04', inflow: 234, resolved: 198 },
  { date: '2026-07-05', inflow: 172, resolved: 185 },
  { date: '2026-07-06', inflow: 218, resolved: 209 },
  { date: '2026-07-07', inflow: 196, resolved: 211 },
]

const weekData = computed(() => weekRaw)
const yMax = computed(() => {
  const max = Math.max(...weekRaw.flatMap(d => [d.inflow, d.resolved]))
  // zaokrąglij w górę do setek
  return Math.ceil(max / 100) * 100
})
const yTicks = computed(() => {
  const ticks = []
  for (let i = 0; i <= 4; i++) {
    ticks.push(Math.round((yMax.value / 4) * i))
  }
  return ticks
})

function formatDateLabel(dateStr) {
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit' })
}

// --- Tooltip ---
const tooltip = reactive({
  visible: false,
  x: 0,
  y: 0,
  date: '',
  series: '',
  value: '',
  color: ''
})
const chartArea = ref(null)

function showTooltip(e, dateStr, series, value) {
  const colorMap = { napływ: 'var(--chart-inflow)', rozwiązane: 'var(--chart-resolved)' }
  const d = new Date(dateStr + 'T00:00:00')
  tooltip.date = d.toLocaleDateString('pl-PL', { weekday: 'short', day: '2-digit', month: '2-digit' })
  tooltip.series = series
  tooltip.value = value
  tooltip.color = colorMap[series] || '#888'
  tooltip.visible = true
  moveTooltip(e)
}

function moveTooltip(e) {
  const rect = chartArea.value?.getBoundingClientRect()
  if (!rect) return
  tooltip.x = e.clientX - rect.left + 12
  tooltip.y = e.clientY - rect.top - 10
}
</script>

<style scoped>
.section-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 22px 24px;
  margin-bottom: 20px;
}
.issue-card {
  --chart-inflow: #536dfe;
  --chart-resolved: #00c853;
  border-left: 3px solid #ff5252;
}
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
  color: #ff5252;
  flex-shrink: 0;
}
.issue-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.issue-card-item {
  background: var(--bg-hover);
  border-radius: 10px;
  padding: 14px 16px;
  border-left: 3px solid transparent;
  transition: background 0.15s;
}
.issue-card-item:hover {
  background: var(--bg-surface);
}
.issue-item-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.issue-badge {
  font-size: 10px;
  font-weight: 700;
  color: var(--text-muted);
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  letter-spacing: 0.5px;
}
.issue-name {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}
.issue-number {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;
  line-height: 1.1;
}
.issue-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.issue-bar-track {
  height: 6px;
  background: var(--bg-card);
  border-radius: 100px;
  overflow: hidden;
  margin-bottom: 8px;
}
.issue-bar-fill {
  height: 100%;
  border-radius: 100px;
  transition: width 1s cubic-bezier(0.16,1,0.3,1);
  animation: barGrow 1s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes barGrow {
  from { width: 0 !important; }
}
.issue-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 11px;
}
.issue-trend {
  font-weight: 600;
}
.issue-trend.up { color: #ff5252; }
.issue-trend.down { color: var(--accent-primary); }
.issue-pct {
  color: var(--text-muted);
}

/* Weekly grouped bar chart */
.weekly-chart-section {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid var(--border-color);
}
.weekly-chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.compact-chart-header {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}
.chart-legend {
  display: flex;
  align-items: center;
  gap: 12px;
}
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  flex-shrink: 0;
}
.legend-label {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 500;
}

.chart-container {
  display: flex;
  position: relative;
}

.y-axis {
  display: flex;
  flex-direction: column-reverse;
  justify-content: space-between;
  width: 40px;
  min-height: 180px;
  padding-bottom: 28px;
  flex-shrink: 0;
}
.y-tick {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 0;
  position: relative;
}
.y-tick-label {
  font-size: 9px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
  transform: translateY(-50%);
}

.chart-area {
  flex: 1;
  position: relative;
  min-height: 180px;
  padding-bottom: 28px;
}

.grid-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--border-color);
  opacity: 0.5;
}

.bar-group {
  position: absolute;
  bottom: 28px;
  display: flex;
  gap: 3px;
  align-items: flex-end;
  transform: translateX(-50%);
  height: calc(100% - 28px);
}

.bar {
  width: 18px;
  border-radius: 3px 3px 0 0;
  cursor: pointer;
  transition: opacity 0.15s;
  min-height: 4px;
}
.bar:hover {
  opacity: 0.8;
}

.x-label {
  position: absolute;
  bottom: 0;
  transform: translateX(-50%);
  font-size: 9px;
  color: var(--text-muted);
  font-family: 'JetBrains Mono', monospace;
  white-space: nowrap;
}

/* Tooltip */
.chart-tooltip {
  position: absolute;
  pointer-events: none;
  z-index: 10;
  background: var(--bg-overlay);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  white-space: nowrap;
}
.tt-date {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.tt-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
}
.tt-swatch {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  flex-shrink: 0;
}
.tt-label {
  color: var(--text-secondary);
}
.tt-value {
  color: var(--text-primary);
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  margin-left: auto;
}

/* Footer */
.chart-footer {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}
.footer-trend {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
}
.footer-trend strong {
  color: var(--accent-primary);
}
</style>
