<template>
  <section class="kpi-bar">
    <article v-for="(k, i) in kpis" :key="k.label" class="kpi-card" :style="{ '--i': i }" @click="$emit('open', k)">
      <div class="kpi-icon-wrapper" :class="k.color"><span class="kpi-icon" v-html="k.icon"></span></div>
      <div class="kpi-body">
        <span class="kpi-value">{{ k.current }}</span>
        <span class="kpi-label">{{ k.label }}</span>
        <span class="kpi-trend" :class="k.trend">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
            <polyline :points="k.trend === 'up' ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"/>
          </svg>{{ k.change }}
        </span>
      </div>
      <div class="kpi-spark">
        <svg width="60" height="28" viewBox="0 0 60 28">
          <polyline :points="k.spark" fill="none" stroke="currentColor" stroke-width="1.5" class="spark-line" :class="k.color"/>
        </svg>
      </div>
    </article>
  </section>
</template>

<script setup>
defineProps({ kpis: Array })
defineEmits(['open'])
</script>

<style scoped>
.kpi-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 20px; display: flex; gap: 14px; cursor: pointer; transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s; animation: cardSlide 0.5s ease both; animation-delay: calc(var(--i) * 0.1s); position: relative; overflow: hidden; }
.kpi-card:hover { border-color: rgba(255,255,255,0.15); transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
@keyframes cardSlide { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.kpi-icon-wrapper { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.kpi-icon-wrapper.green { background: rgba(0,200,83,0.12); color: #00c853; }
.kpi-icon-wrapper.cyan { background: rgba(0,229,255,0.12); color: #00e5ff; }
.kpi-icon-wrapper.orange { background: rgba(255,145,0,0.12); color: #ff9100; }
.kpi-icon-wrapper.purple { background: rgba(83,109,254,0.12); color: #536dfe; }
.kpi-body { flex: 1; min-width: 0; }
.kpi-value { font-size: 22px; font-weight: 700; color: var(--text-primary); display: block; line-height: 1.2; }
.kpi-label { font-size: 11px; color: var(--text-secondary); margin-top: 2px; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.kpi-trend { font-size: 11px; font-weight: 600; margin-top: 4px; display: inline-flex; align-items: center; gap: 3px; }
.kpi-trend.up { color: #00c853; }
.kpi-trend.down { color: #ff5252; }
.kpi-spark { position: absolute; right: 8px; bottom: 8px; opacity: 0.4; }
.spark-line.green { color: #00c853; }
.spark-line.cyan { color: #00e5ff; }
.spark-line.orange { color: #ff9100; }
.spark-line.purple { color: #536dfe; }
</style>