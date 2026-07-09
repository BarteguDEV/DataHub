<template>
  <div class="collapse-card" :class="{ open: isOpen }">
    <button class="collapse-trigger" @click="isOpen = !isOpen">
      <span class="collapse-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
        Karta uruchamiania
      </span>
      <span class="collapse-badge">{{ modules.length }} modułów</span>
      <svg class="collapse-chevron" :class="{ rotated: isOpen }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6 9 12 15 18 9"/>
      </svg>
    </button>
    <div class="collapse-body">
      <div class="launch-card compact">
        <div class="launch-actions">
          <button class="btn-launch" @click="$emit('open')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            Otwórz w nowej karcie
          </button>
        </div>
        <div class="module-list inline">
          <div class="mini-card" v-for="mod in modules" :key="mod.name">
            <div class="mini-icon" v-html="mod.icon"></div>
            <div>
              <div class="mini-name">{{ mod.name }}</div>
              <div class="mini-desc">{{ mod.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ modules: Array })
defineEmits(['open'])

const isOpen = ref(false)
</script>

<style scoped>
.collapse-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; overflow: hidden; transition: border-color 0.2s; }
.collapse-card:hover { border-color: rgba(255,255,255,0.12); }
.collapse-trigger { display: flex; align-items: center; gap: 10px; width: 100%; padding: 14px 18px; background: none; border: none; color: var(--text-secondary); font-size: 13px; font-weight: 500; font-family: 'Inter', sans-serif; cursor: pointer; transition: background 0.15s, color 0.15s; }
.collapse-trigger:hover { background: var(--bg-hover); color: var(--text-primary); }
.collapse-label { display: flex; align-items: center; gap: 8px; color: var(--accent-primary); font-weight: 600; }
.collapse-badge { font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 100px; background: var(--bg-hover); color: var(--text-muted); margin-left: auto; }
.collapse-chevron { flex-shrink: 0; transition: transform 0.25s ease; color: var(--text-muted); }
.collapse-chevron.rotated { transform: rotate(180deg); }
.collapse-body { max-height: 0; overflow: hidden; transition: max-height 0.4s cubic-bezier(0.16,1,0.3,1); }
.collapse-card.open .collapse-body { max-height: 600px; border-top: 1px solid var(--border-color); }
.launch-card.compact { background: none; border: none; padding: 16px 18px; }
.launch-actions { display: flex; align-items: center; gap: 12px; }
.btn-launch { display: flex; align-items: center; gap: 10px; padding: 12px 24px; border-radius: 10px; background: linear-gradient(135deg, #00c853, #00e676); color: #000; font-size: 14px; font-weight: 600; border: none; cursor: pointer; font-family: 'Inter', sans-serif; transition: all 0.2s; }
.btn-launch:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,200,83,0.3); }
.module-list.inline { margin-top: 16px; display: grid; grid-template-columns: repeat(auto-fill, minmax(250px,1fr)); gap: 12px; }
.mini-card { display: flex; align-items: center; gap: 14px; padding: 16px; background: var(--bg-hover); border: 1px solid var(--border-color); border-radius: 10px; }
.mini-icon { flex-shrink: 0; display: flex; }
.mini-name { font-size: 14px; font-weight: 600; color: var(--text-primary); }
.mini-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
</style>