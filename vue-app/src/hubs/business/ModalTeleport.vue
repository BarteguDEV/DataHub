<template>
  <Teleport to="body">
    <transition name="modal">
      <div class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-panel">
          <div class="modal-header">
            <h3>{{ title }}</h3>
            <button class="modal-close" @click="$emit('close')">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
          <div class="modal-body" v-html="body"></div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
defineProps({ title: String, body: String })
defineEmits(['close'])
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 20px; }
.modal-panel { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; width: 100%; max-width: 480px; max-height: 80vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 22px; border-bottom: 1px solid var(--border-color); }
.modal-header h3 { font-size: 16px; font-weight: 700; color: var(--text-primary); margin: 0; }
.modal-close { background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; border-radius: 6px; display: flex; transition: color 0.15s, background 0.15s; }
.modal-close:hover { color: var(--text-primary); background: var(--bg-hover); }
.modal-body { padding: 20px 22px; font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
.modal-body :deep(.modal-kpi-big) { font-size: 36px; font-weight: 700; color: var(--text-primary); text-align: center; padding: 16px 0; }
.modal-body :deep(.modal-kpi-row) { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-color); }
.modal-body :deep(.modal-kpi-row:last-child) { border: none; }
.modal-body :deep(.modal-label) { color: var(--text-muted); }
.modal-body :deep(.modal-value) { color: var(--text-primary); font-weight: 500; text-align: right; }
.modal-enter-active { transition: opacity 0.2s ease; }
.modal-leave-active { transition: opacity 0.15s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal-panel { animation: modalIn 0.25s ease; }
.modal-leave-active .modal-panel { animation: modalOut 0.15s ease; }
@keyframes modalIn { from { transform: scale(0.95) translateY(10px); opacity: 0; } to { transform: scale(1) translateY(0); opacity: 1; } }
@keyframes modalOut { from { transform: scale(1); opacity: 1; } to { transform: scale(0.95); opacity: 0; } }
</style>