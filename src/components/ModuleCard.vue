<template>
  <div
    class="module-card"
    :class="{ clickable: isClickable, launching: isLaunching }"
    @click="handleClick"
  >
    <div class="card-icon-wrapper" :style="{ background: iconBg }">
      <span class="card-icon" v-html="icon"></span>
    </div>

    <div class="card-body">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-desc">{{ description }}</p>

      <div v-if="tags" class="card-tags">
        <span v-for="tag in tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
    </div>

    <div class="card-footer">
      <span v-if="status" class="status-indicator" :class="status">
        <span class="status-dot"></span>
        {{ statusLabel }}
      </span>
      <span v-if="to" class="card-action">
        {{ isExternal ? 'Uruchom →' : 'Otwórz →' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  icon: { type: String, required: true },
  title: { type: String, required: true },
  description: { type: String, required: true },
  to: { type: String, default: null },
  iconBg: { type: String, default: 'var(--bg-hover)' },
  tags: { type: Array, default: null },
  status: { type: String, default: null },
  external: { type: Boolean, default: false },
  streamlitUrl: { type: String, default: null },
  actionable: { type: Boolean, default: true },
})

const emit = defineEmits(['launch-streamlit'])
const router = useRouter()
const isLaunching = ref(false)

const statusLabel = computed(() => {
  const labels = { active: 'Aktywny', beta: 'Beta', coming: 'Wkrótce', stable: 'Stabilny' }
  return labels[props.status] || props.status
})

const isClickable = computed(() => !!(props.to || props.streamlitUrl || props.actionable))

const isExternal = computed(() => props.external || !!props.streamlitUrl)

function handleClick() {
  if (!isClickable.value) return

  // Priorytet 1: Streamlit URL — emituj event do rodzica
  if (props.streamlitUrl) {
    isLaunching.value = true
    emit('launch-streamlit', { title: props.title, url: props.streamlitUrl })
    setTimeout(() => (isLaunching.value = false), 1500)
    return
  }

  // Priorytet 2: External link
  if (props.external) {
    window.open(props.to, '_blank', 'noopener')
    return
  }

  // Priorytet 3: Route wewnętrzna
  if (props.to) {
    router.push(props.to)
    return
  }

  // Priorytet 4: Brak to/url — emituj event, rodzic zdecyduje
  emit('launch-streamlit', { title: props.title, url: null })
}
</script>

<style scoped>
.module-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.25s ease;
  cursor: default;
}

.module-card.clickable {
  cursor: pointer;
}

.module-card.clickable:hover {
  border-color: var(--accent-primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.module-card.launching {
  border-color: var(--accent-primary);
  box-shadow: 0 0 20px rgba(0, 200, 83, 0.2);
  animation: pulse-border 0.8s ease infinite;
}

@keyframes pulse-border {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0, 200, 83, 0.3); }
  50% { box-shadow: 0 0 0 8px rgba(0, 200, 83, 0); }
}

.card-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.card-icon {
  display: flex;
  align-items: center;
}

.card-body {
  flex: 1;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px 0;
}

.card-desc {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 12px;
}

.tag {
  font-size: 11px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 100px;
  background: var(--bg-tag);
  color: var(--text-muted);
  letter-spacing: 0.2px;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-muted);
}

.status-indicator.active .status-dot { background: #00c853; }
.status-indicator.active { color: #00c853; }

.status-indicator.beta .status-dot { background: #ff9100; }
.status-indicator.beta { color: #ff9100; }

.status-indicator.coming .status-dot { background: #536dfe; }
.status-indicator.coming { color: #536dfe; }

.status-indicator.stable .status-dot { background: #00e5ff; }
.status-indicator.stable { color: #00e5ff; }

.card-action {
  font-size: 13px;
  font-weight: 600;
  color: var(--accent-primary);
}
</style>
