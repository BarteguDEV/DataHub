<template>
  <div class="hub-view">
    <div class="hub-section-header">
      <h1 class="section-title">AI Innovation Lab</h1>
      <p class="section-desc">
        Raporty wygenerowane przez AI (Claude/Codex) na podstawie analizy systemu.
        Każdy raport to osobny dokument HTML z wnioskami i rekomendacjami.
      </p>
    </div>

    <div class="section-row">
      <span class="badge">RAPORTY AI</span>
    </div>

    <!-- Lista raportów -->
    <div class="report-grid">
      <article
        v-for="r in reports"
        :key="r.id"
        class="report-card"
        :class="{ active: activeReport === r.id }"
        @click="openReport(r.id)"
      >
        <div class="card-accent" :style="{ background: r.color }"></div>
        <div class="card-icon" v-html="r.icon"></div>
        <h3 class="card-title">{{ r.title }}</h3>
        <p class="card-desc">{{ r.desc }}</p>
        <div class="card-tags">
          <span v-for="t in r.tags" :key="t" class="tag">{{ t }}</span>
        </div>
        <div class="card-footer">
          <span class="card-date">{{ r.date }}</span>
          <span class="card-action">
            {{ activeReport === r.id ? 'Podgląd ▼' : 'Otwórz →' }}
          </span>
        </div>
      </article>
    </div>

    <!-- Podgląd raportu (iframe) -->
    <transition name="slide">
      <div v-if="activeReport" class="report-preview">
        <div class="preview-header">
          <div class="preview-info">
            <span class="preview-dot"></span>
            <span class="preview-name">{{ currentReport?.title }}</span>
          </div>
          <div class="preview-actions">
            <a
              :href="currentReport?.url"
              target="_blank"
              class="preview-btn"
              title="Otwórz w nowej karcie"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </a>
            <button class="preview-btn close" @click="activeReport = null">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>
        <iframe
          v-if="currentReport"
          :src="currentReport.url"
          class="preview-frame"
          frameborder="0"
        ></iframe>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeReport = ref(null)

const reports = [
  {
    id: 'sql-lineage',
    title: 'SQL Lineage Report',
    desc: 'Analiza zależności między tabelami i widokami w Oracle/Snowflake. Mapowanie przepływu danych od źródła do DWH z wykryciem krytycznych ścieżek.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    color: 'linear-gradient(135deg, #00c853, #00e5ff)',
    tags: ['SQL', 'Lineage', 'Oracle', 'Snowflake'],
    date: '2026-07-04',
    url: '/ai-reports/sql-lineage-report.html',
  },
  {
    id: 'test-generator',
    title: 'Auto Test Generator',
    desc: 'Automatycznie wygenerowane testy na podstawie analizy SQL. Wykrywa brakujące referencje, duplikacje i niespójności ETL z rekomendacjami AI.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    color: 'linear-gradient(135deg, #536dfe, #d500f9)',
    tags: ['Testy', 'SQL', 'Automatyzacja'],
    date: '2026-07-04',
    url: '/ai-reports/test-generator-report.html',
  },
  {
    id: 'data-mapping',
    title: 'Data Mapping Prototype',
    desc: 'Prototyp mapowania danych między systemem źródłowym (Core Banking) a DWH. Diagram przepływu, transformacje i wykryte luki w mapowaniu.',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    color: 'linear-gradient(135deg, #ff9100, #ff3d00)',
    tags: ['Mapping', 'ETL', 'DWH'],
    date: '2026-07-04',
    url: '/ai-reports/data-mapping-report.html',
  },
]

const currentReport = computed(() =>
  reports.find(r => r.id === activeReport.value)
)

function openReport(id) {
  activeReport.value = activeReport.value === id ? null : id
}
</script>

<style scoped>
.hub-view { max-width: 1100px; }

.hub-section-header { margin-bottom: 12px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 600px; }

.section-row { margin-bottom: 20px; }
.badge { font-size: 11px; font-weight: 600; letter-spacing: 1.5px; color: #536dfe; padding: 4px 14px; border-radius: 100px; background: rgba(83,109,254,0.1); border: 1px solid rgba(83,109,254,0.15); }

/* Report grid */
.report-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }

.report-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 0;
  transition: all 0.25s ease;
}

.report-card:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(0,0,0,0.4); }
.report-card.active { border-color: #536dfe; box-shadow: 0 0 0 1px #536dfe; }

.card-accent { height: 4px; flex-shrink: 0; }

.card-icon {
  padding: 0 20px;
  padding-top: 16px;
}

.report-card:nth-child(1) .card-icon { color: #00c853; }
.report-card:nth-child(2) .card-icon { color: #536dfe; }
.report-card:nth-child(3) .card-icon { color: #ff9100; }

.card-title { font-size: 16px; font-weight: 600; color: var(--text-primary); padding: 0 20px; margin: 0; }
.card-desc { font-size: 13px; line-height: 1.6; color: var(--text-secondary); padding: 0 20px; margin: 0; flex: 1; }

.card-tags { padding: 0 20px; display: flex; flex-wrap: wrap; gap: 6px; }
.tag { font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 100px; background: var(--bg-tag); color: var(--text-muted); }

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-top: 1px solid var(--border-color);
}

.card-date { font-size: 11px; color: var(--text-muted); }
.card-action { font-size: 12px; font-weight: 600; color: #536dfe; }

/* Preview panel */
.report-preview {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  background: var(--bg-card);
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-color);
}

.preview-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.preview-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #536dfe;
}

.preview-actions {
  display: flex;
  gap: 6px;
}

.preview-btn {
  display: flex;
  align-items: center;
  padding: 6px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
  text-decoration: none;
}

.preview-btn:hover { border-color: #536dfe; color: #536dfe; }
.preview-btn.close:hover { border-color: #ff5252; color: #ff5252; }

.preview-frame {
  width: 100%;
  height: 600px;
  background: #0b0d11;
}

/* Transitions */
.slide-enter-active, .slide-leave-active { transition: all 0.3s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
