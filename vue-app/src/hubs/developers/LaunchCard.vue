<template>
  <div class="streamlit-launch">
    <div class="launch-card">
      <div class="launch-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ff5252" stroke-width="1.5">
          <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
        </svg>
      </div>
      <h2>Developerzy — Streamlit</h2>
      <p>Pełna aplikacja Developerzy dostępna jako osobna aplikacja Streamlit.<br>
      Zawiera: Jira, Confluence, IAM, TeamCity, Informatica.</p>

      <div class="launch-actions">
        <button class="btn-launch" @click="$emit('open')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
          Otwórz Streamlit
        </button>
        <button class="btn-check" :class="{ alive: isAlive }" @click="$emit('check')">
          <span class="check-dot"></span>
          {{ isAlive ? 'Streamlit online' : 'Sprawdź status' }}
        </button>
      </div>

      <div v-if="lastCheck" class="check-result" :class="{ error: !isAlive }">
        {{ isAlive ? '✓ Serwer Streamlit odpowiada' : '✗ Serwer nie odpowiada — uruchom: streamlit run vue-app/src/hubs/developers/streamlit_app.py --server.port 8501' }}
      </div>
    </div>

    <div class="module-list">
      <div class="mini-card" v-for="mod in modules" :key="mod.name">
        <div class="mini-icon" v-html="mod.icon"></div>
        <div>
          <div class="mini-name">{{ mod.name }}</div>
          <div class="mini-desc">{{ mod.desc }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isAlive: Boolean,
  lastCheck: Boolean,
  modules: Array,
})
defineEmits(['open', 'check'])
</script>

<style scoped>
.streamlit-launch { display: flex; flex-direction: column; gap: 24px; }
.launch-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 32px; }
.launch-icon { margin-bottom: 16px; }
.launch-card h2 { font-size: 22px; font-weight: 700; color: var(--text-primary); margin: 0 0 12px 0; }
.launch-card p { font-size: 14px; line-height: 1.7; color: var(--text-secondary); margin: 0 0 20px 0; }
.launch-actions { display: flex; align-items: center; gap: 12px; }
.btn-launch { display: flex; align-items: center; gap: 10px; padding: 12px 24px; border-radius: 10px; background: linear-gradient(135deg, #00c853, #00e676); color: #000; font-size: 14px; font-weight: 600; border: none; cursor: pointer; font-family: 'Inter', sans-serif; transition: all 0.2s; }
.btn-launch:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,200,83,0.3); }
.btn-check { display: flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 10px; background: var(--bg-hover); border: 1px solid var(--border-color); color: var(--text-secondary); font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s; font-family: 'Inter', sans-serif; }
.btn-check:hover { border-color: var(--accent-primary); color: var(--text-primary); }
.btn-check.alive { border-color: #00c853; color: #00c853; }
.check-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); }
.btn-check.alive .check-dot { background: #00c853; }
.check-result { margin-top: 12px; font-size: 13px; color: #00c853; padding: 10px 16px; background: rgba(0,200,83,0.05); border: 1px solid rgba(0,200,83,0.15); border-radius: 8px; }
.check-result.error { color: #ff5252; background: rgba(255,82,82,0.05); border-color: rgba(255,82,82,0.15); }
.module-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px,1fr)); gap: 12px; }
.mini-card { display: flex; align-items: center; gap: 14px; padding: 16px; background: var(--bg-hover); border: 1px solid var(--border-color); border-radius: 10px; }
.mini-icon { flex-shrink: 0; display: flex; }
.mini-name { font-size: 14px; font-weight: 600; color: var(--text-primary); }
.mini-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
</style>