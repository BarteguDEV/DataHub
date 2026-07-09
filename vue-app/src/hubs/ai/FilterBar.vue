<template>
  <div class="filter-row">
    <button v-for="cat in categories" :key="cat.id" class="filter-btn" :class="{ active: active === cat.id }" @click="$emit('select', cat.id)">
      <span v-html="cat.icon" class="filter-icon"></span>
      <span class="filter-label">{{ cat.label }}</span>
      <span class="filter-count">{{ cat.count }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({ categories: Array, active: String })
defineEmits(['select'])
</script>

<style scoped>
.filter-row { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.filter-btn { display: inline-flex; align-items: center; gap: 6px; padding: 7px 16px; border-radius: 100px; border: 1px solid var(--border-color); background: var(--bg-card); color: var(--text-secondary); font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.2s ease; font-family: inherit; white-space: nowrap; }
.filter-btn:hover { border-color: rgba(83,109,254,0.3); color: var(--text-primary); background: var(--bg-hover); }
.filter-btn.active { background: rgba(83,109,254,0.12); border-color: #536dfe; color: #536dfe; }
.filter-icon { display: flex; align-items: center; opacity: 0.7; }
.filter-btn.active .filter-icon { opacity: 1; }
.filter-count { font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 100px; background: var(--bg-tag); color: var(--text-muted); margin-left: 2px; }
.filter-btn.active .filter-count { background: rgba(83,109,254,0.15); color: #536dfe; }
</style>