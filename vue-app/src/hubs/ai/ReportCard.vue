<template>
  <article class="report-card" :class="{ expanded: active }" :style="{ '--card-accent': report.accent }">
    <div class="card-clickable" @click="$emit('toggle')">
      <div class="card-accent" :style="{ background: report.gradient }"></div>
      <div class="card-top">
        <div class="card-icon" v-html="report.icon"></div>
        <div class="card-top-right">
          <span v-if="report.status" class="card-status" :class="report.status">{{ report.statusLabel || report.status }}</span>
          <button v-if="active" class="card-close" @click.stop="$emit('toggle')" title="Zwiń">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
      </div>
      <h3 class="card-title">{{ report.title }}</h3>
      <p class="card-desc">{{ report.desc }}</p>
      <div v-if="report.metric" class="card-metric-circle">
        <svg viewBox="0 0 44 44" width="48" height="48" class="circle-svg">
          <circle cx="22" cy="22" r="18" fill="none" class="circle-track" stroke-width="3.5"/>
          <circle cx="22" cy="22" r="18" fill="none" class="circle-fill" stroke-width="3.5" stroke-dasharray="113.1" :stroke-dashoffset="circleOffset(report.metric.value)" stroke-linecap="round" transform="rotate(-90 22 22)" :stroke="report.metric.color || report.accent"/>
          <text x="22" y="22" text-anchor="middle" dominant-baseline="central" class="circle-text" :fill="report.metric.color || report.accent">{{ typeof report.metric.display === 'number' ? report.metric.display : report.metric.value }}</text>
        </svg>
        <div class="circle-meta">
          <span class="circle-label">{{ report.metric.label }}</span>
          <span v-if="report.metric.unit" class="circle-unit">{{ report.metric.unit }}</span>
        </div>
      </div>
    </div>

    <div class="card-extra" :class="{ open: active }">
      <div class="card-extra-inner">
        <div class="ex-section">
          <h4 class="ex-title"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>Kluczowe ustalenia</h4>
          <ul class="ex-list"><li v-for="(f, fi) in report.findings" :key="fi"><span class="ex-dot" :style="{ background: report.accent }"></span>{{ f }}</li></ul>
        </div>
        <div class="ex-section">
          <h4 class="ex-title"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>Rekomendacje</h4>
          <ul class="ex-list recs"><li v-for="(rec, ri) in report.recommendations" :key="ri"><span class="ex-arrow">→</span>{{ rec }}</li></ul>
        </div>
      </div>
    </div>

    <div class="card-tags"><span v-for="t in report.tags" :key="t" class="tag">{{ t }}</span></div>

    <div class="card-footer">
      <span class="card-meta"><span class="card-author">{{ report.author }}</span> · v{{ report.version }} · <span class="card-date">{{ report.date }}</span></span>
      <a v-if="active && report.url" :href="report.url" target="_blank" class="card-action-link pulse-glow" @click.stop><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>Pełny raport</a>
      <span v-else class="card-action" @click.stop="$emit('toggle')">{{ active ? 'Zwiń ▲' : 'Otwórz →' }}</span>
    </div>
  </article>
</template>

<script setup>
defineProps({ report: Object, active: Boolean })
defineEmits(['toggle'])

function circleOffset(value) {
  const circ = 2 * Math.PI * 18
  return circ * (1 - Math.min(100, Math.max(0, value)) / 100)
}
</script>

<style scoped>
.report-card { position: relative; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; display: flex; flex-direction: column; gap: 10px; transition: border-color 0.3s, box-shadow 0.3s; }
.report-card.expanded { grid-column: 1 / -1; border-color: var(--card-accent); box-shadow: 0 0 0 1px var(--card-accent); }
.card-clickable { padding: 20px 20px 0; cursor: pointer; }
.card-accent { height: 4px; border-radius: 14px 14px 0 0; margin: -1px -1px 0; }
.card-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 10px; }
.card-icon { color: var(--card-accent); display: flex; align-items: center; }
.card-top-right { display: flex; align-items: center; gap: 8px; }
.card-status { font-size: 9px; font-weight: 700; padding: 3px 8px; border-radius: 100px; text-transform: uppercase; letter-spacing: 0.5px; }
.card-status.new { background: rgba(83,109,254,0.12); color: #536dfe; }
.card-status.beta { background: rgba(255,145,0,0.12); color: #ff9100; }
.card-status.stable { background: rgba(0,200,83,0.12); color: #00c853; }
.card-close { background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 2px; border-radius: 4px; display: flex; }
.card-close:hover { color: var(--text-primary); background: var(--bg-hover); }
.card-title { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 0; line-height: 1.3; }
.card-desc { font-size: 12px; line-height: 1.5; color: var(--text-secondary); margin: 6px 0 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-metric-circle { display: flex; align-items: center; gap: 10px; margin-top: 12px; }
.circle-svg { flex-shrink: 0; }
.circle-track { stroke: var(--bg-hover); }
.circle-text { font-size: 10px; font-weight: 700; }
.circle-meta { display: flex; flex-direction: column; }
.circle-label { font-size: 11px; color: var(--text-secondary); }
.circle-unit { font-size: 10px; color: var(--text-muted); }
.card-extra { max-height: 0; overflow: hidden; transition: max-height 0.45s ease; }
.card-extra.open { max-height: 600px; }
.card-extra-inner { padding: 0 20px; display: flex; flex-direction: column; gap: 14px; border-top: 1px solid var(--border-color); margin-top: 12px; padding-top: 14px; }
.ex-title { font-size: 12px; font-weight: 600; color: var(--text-primary); margin: 0 0 6px; display: flex; align-items: center; gap: 6px; }
.ex-title svg { color: var(--card-accent); }
.ex-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px; }
.ex-list li { font-size: 12px; line-height: 1.5; color: var(--text-secondary); display: flex; gap: 6px; }
.ex-dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.ex-arrow { color: var(--accent-primary); font-weight: 700; flex-shrink: 0; }
.card-tags { display: flex; flex-wrap: wrap; gap: 4px; padding: 0 20px; }
.tag { font-size: 9px; font-weight: 500; color: var(--text-muted); padding: 2px 8px; border-radius: 100px; background: var(--bg-tag); }
.card-footer { display: flex; align-items: center; justify-content: space-between; padding: 10px 20px 14px; border-top: 1px solid var(--border-color); margin-top: auto; }
.card-meta { font-size: 10px; color: var(--text-muted); }
.card-author { font-weight: 600; color: var(--text-secondary); }
.card-date { font-family: 'JetBrains Mono', monospace; }
.card-action-link { display: inline-flex; align-items: center; gap: 5px; font-size: 11px; font-weight: 600; color: #00c853; text-decoration: none; padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(0,200,83,0.2); transition: all 0.2s; }
.card-action-link:hover { background: rgba(0,200,83,0.1); border-color: #00c853; }
.card-action { font-size: 11px; font-weight: 600; color: var(--text-muted); cursor: pointer; transition: color 0.15s; display: flex; align-items: center; gap: 4px; }
.card-action:hover { color: var(--accent-primary); }
.pulse-glow { animation: pulseGlow 2s ease-in-out infinite; }
@keyframes pulseGlow { 0%,100% { box-shadow: 0 0 0 0 rgba(0,200,83,0); } 50% { box-shadow: 0 0 8px 0 rgba(0,200,83,0.25); } }
</style>