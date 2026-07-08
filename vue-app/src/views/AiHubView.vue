<template>
  <div class="hub-view">
    <!-- Header -->
    <div class="hub-section-header">
      <h1 class="section-title">AI Hub</h1>
      <p class="section-desc">
        Raporty wygenerowane przez AI na podstawie analizy systemu — SQL, ETL, zależności, jakość danych i ryzyko wdrożeń.
        Kliknij kartę, aby zobaczyć szczegóły i podgląd raportu.
      </p>
    </div>

    <!-- Category filter pills -->
    <div class="filter-row">
      <button
        v-for="cat in filterCategories"
        :key="cat.id"
        class="filter-btn"
        :class="{ active: activeCategory === cat.id }"
        @click="activeCategory = cat.id"
      >
        <span v-html="cat.icon" class="filter-icon"></span>
        <span class="filter-label">{{ cat.label }}</span>
        <span class="filter-count">{{ cat.count }}</span>
      </button>
    </div>

    <!-- Reports grid -->
    <div class="report-grid">
      <article
        v-for="(r, index) in sortedReports"
        :key="r.id"
        class="report-card"
        :class="['report-card', { expanded: activeReport === r.id }]"
        :style="{ '--card-accent': r.accent }"
      >
        <!-- Klikalna część karty (zawsze widoczna) -->
        <div class="card-clickable" @click="openReport(r.id)">
          <!-- Accent bar -->
          <div class="card-accent" :style="{ background: r.gradient }"></div>

          <!-- Top row: icon + status badge + close btn when expanded -->
          <div class="card-top">
            <div class="card-icon" v-html="r.icon"></div>
            <div class="card-top-right">
              <span v-if="r.status" class="card-status" :class="r.status">{{ r.statusLabel || r.status }}</span>
              <button v-if="activeReport === r.id" class="card-close" @click.stop="activeReport = null" title="Zwiń">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Title & description -->
          <h3 class="card-title">{{ r.title }}</h3>
          <p class="card-desc">{{ r.desc }}</p>

          <!-- Metric circular progress -->
          <div v-if="r.metric" class="card-metric-circle">
            <svg viewBox="0 0 44 44" width="48" height="48" class="circle-svg">
              <circle cx="22" cy="22" r="18" fill="none" class="circle-track" stroke-width="3.5"/>
              <circle cx="22" cy="22" r="18" fill="none" class="circle-fill" stroke-width="3.5"
                stroke-dasharray="113.1"
                :stroke-dashoffset="circleOffset(r.metric.value)"
                stroke-linecap="round"
                transform="rotate(-90 22 22)"
                :stroke="r.metric.color || r.accent"/>
              <text x="22" y="22" text-anchor="middle" dominant-baseline="central"
                class="circle-text" :fill="r.metric.color || r.accent">
                {{ typeof r.metric.display === 'number' ? r.metric.display : r.metric.value }}
              </text>
            </svg>
            <div class="circle-meta">
              <span class="circle-label">{{ r.metric.label }}</span>
              <span v-if="r.metric.unit" class="circle-unit">{{ r.metric.unit }}</span>
            </div>
          </div>
        </div>

        <!-- === Rozszerzona zawartość (widoczna po kliknięciu) === -->
        <div class="card-extra" :class="{ open: activeReport === r.id }">
          <div class="card-extra-inner">
            <!-- Findings -->
            <div class="ex-section">
              <h4 class="ex-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                Kluczowe ustalenia
              </h4>
              <ul class="ex-list">
                <li v-for="(f, fi) in r.findings" :key="fi">
                  <span class="ex-dot" :style="{ background: r.accent }"></span>
                  {{ f }}
                </li>
              </ul>
            </div>

            <!-- Recommendations -->
            <div class="ex-section">
              <h4 class="ex-title">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                Rekomendacje
              </h4>
              <ul class="ex-list recs">
                <li v-for="(rec, ri) in r.recommendations" :key="ri">
                  <span class="ex-arrow">→</span>
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Tags + Footer (zawsze widoczne) -->
        <div class="card-tags">
          <span v-for="t in r.tags" :key="t" class="tag">{{ t }}</span>
        </div>

        <div class="card-footer">
          <span class="card-meta"><span class="card-author">{{ r.author }}</span> · v{{ r.version }} · <span class="card-date">{{ r.date }}</span></span>
          <a v-if="activeReport === r.id && r.url" :href="r.url" target="_blank" class="card-action-link pulse-glow" @click.stop>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
            </svg>
            Pełny raport
          </a>
          <span v-else class="card-action" @click.stop="openReport(r.id)">
            {{ activeReport === r.id ? 'Zwiń ▲' : 'Otwórz →' }}
          </span>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeReport = ref(null)
const activeCategory = ref('all')

/* ──────────── ALL REPORTS ──────────── */
const allReports = [
  // ── SQL & OPTIMIZATION ──
  {
    id: 'sql-performance-advisor',
    category: 'sql',
    title: 'SQL Performance Advisor',
    desc: 'Analiza zapytań SQL (Oracle/Snowflake) pod kątem wydajności. Wykrywa FULL TABLE SCAN, brak indeksów, CARTESIAN JOIN i proponuje optymalizacje.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    accent: '#7c4dff',
    gradient: 'linear-gradient(135deg, #7c4dff, #536dfe)',
    tags: ['SQL', 'Performance', 'Oracle', 'Snowflake'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'A. Kowalski',
    version: '2.3.1',
    url: '/ai-reports/sql-performance-advisor.html',
    metric: { label: 'Performance Score', value: 92, unit: '/100', display: 92, color: '#7c4dff' },
    findings: ['5 zapytań z FULL TABLE SCAN na tabelach >1M rekordów', 'Brak indeksu na JOIN w 3 kluczowych widokach', 'CARTESIAN JOIN wykryty w raportach miesięcznych', 'Niepotrzebny DISTINCT w 2 zapytaniach agregujących'],
    recommendations: ['Dodaj indeksy kompozytowe na kolumnach JOIN', 'Zastosuj PARTITION BY dla tabel faktów', 'Zamień DISTINCT na EXISTS w podzapytaniach', 'Przepisz CARTESIAN JOIN na INNER JOIN z kluczami'],
  },
  {
    id: 'sql-code-review',
    category: 'sql',
    title: 'AI Code Review for SQL',
    desc: 'Automatyczny przegląd kodu SQL jak Senior Developer. Analiza czytelności, standardów, wydajności i potencjalnych błędów.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    accent: '#651fff',
    gradient: 'linear-gradient(135deg, #651fff, #d500f9)',
    tags: ['Code Review', 'SQL', 'Best Practices'],
    status: 'beta',
    statusLabel: 'BETA',
    date: '2026-07-07',
    author: 'M. Nowak',
    version: '1.0.5',
    url: '/ai-reports/sql-code-review.html',
    metric: { label: 'Code Quality', value: 74, unit: '/100', display: 74, color: '#651fff' },
    findings: ['Niespójne nazewnictwo (CamelCase vs SNAKE_CASE) w 12 miejscach', 'Brak komentarzy w złożonych CTE', 'Użycie SELECT * w 8 widokach produkcyjnych', 'Brak obsługi NULL w kolumnach numerycznych'],
    recommendations: ['Ustandaryzuj nazewnictwo na SNAKE_CASE', 'Dodaj komentarze do każdego CTE >10 linii', 'Zamień SELECT * na jawne kolumny', 'Dodaj COALESCE/NVL dla kolumn numerycznych'],
  },
  {
    id: 'sql-lineage',
    category: 'sql',
    title: 'SQL Lineage Report',
    desc: 'Analiza zależności między tabelami i widokami w Oracle/Snowflake. Mapowanie przepływu danych od źródła do DWH z wykryciem krytycznych ścieżek.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    accent: '#536dfe',
    gradient: 'linear-gradient(135deg, #536dfe, #448aff)',
    tags: ['SQL', 'Lineage', 'Oracle', 'Snowflake'],
    status: 'stable',
    statusLabel: 'STABILNY',
    date: '2026-07-04',
    author: 'K. Wiśniewska',
    version: '3.1.0',
    url: '/ai-reports/sql-lineage.html',
    metric: { label: 'Pokrycie', value: 95, unit: '%', display: 95, color: '#536dfe' },
    findings: ['12 łańcuchów zależności wykrytych', '3 krytyczne ścieżki bez backupu', '2 widoki z cyklicznymi referencjami'],
    recommendations: ['Dodaj materializację dla krytycznych widoków', 'Przerwij cykle w zależnościach'],
  },

  // ── ETL & DEPENDENCIES ──
  {
    id: 'etl-dependency',
    category: 'etl',
    title: 'ETL Dependency Analyzer',
    desc: 'Analiza eksportu Informatica PowerCenter XML. Generuje pełną mapę zależności z wykryciem nieużywanych mappingów i osieroconych workflow.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/><line x1="12" y1="22" x2="12" y2="15.5"/><polyline points="22 8.5 12 15.5 2 8.5"/></svg>',
    accent: '#00c853',
    gradient: 'linear-gradient(135deg, #00c853, #00e676)',
    tags: ['ETL', 'Informatica', 'Dependency', 'XML'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'J. Kamiński',
    version: '2.0.2',
    url: '/ai-reports/etl-dependency.html',
    metric: { label: 'Pokrycie analizy', value: 88, unit: '%', display: 88, color: '#00c853' },
    findings: ['Nieużywane: 3 mappingi, 2 sesje, 1 workflow', '5 mappingów o zbyt wysokiej złożoności (>50 transformacji)', '7 duplikujących się transformacji Expression', '2 osierocone workflow bez sesji'],
    recommendations: ['Usuń nieużywane obiekty (redukcja kosztów utrzymania)', 'Podziel złożone mappingi na warstwy', 'Wydziel powielone Expression do osobnych obiektów'],
  },
  {
    id: 'etl-complexity',
    category: 'etl',
    title: 'ETL Complexity Report',
    desc: 'Wylicza stopień skomplikowania procesów ETL na podstawie transformacji, lookupów, joinów i zagnieżdżonych mappingów z wykresem radarowym.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>',
    accent: '#00e676',
    gradient: 'linear-gradient(135deg, #00e676, #69f0ae)',
    tags: ['ETL', 'Complexity', 'Analytics'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'P. Lewandowski',
    version: '1.0.3',
    url: '/ai-reports/etl-complexity.html',
    metric: { label: 'Complexity Score', value: 72, unit: '/100', display: 72, color: '#ffab00' },
    findings: ['Średnia liczba transformacji na mapping: 34', '8 mappingów z kategorii "krytyczny"', 'Najwyższy wynik: 94/100 (mapping FCT_SALES_LOAD)', 'Wąskie gardła w warstwie BUFF'],
    recommendations: ['Refaktoryzuj mappingi z score >80', 'Wprowadź standardowe szablony ETL', 'Dodaj warstwę stagingową dla lookupów'],
  },
  {
    id: 'data-flow',
    category: 'etl',
    title: 'Data Flow Visualizer',
    desc: 'Interaktywny graf przepływu danych od źródła przez Landing, BUFF, DM do raportu. Węzły z liczbą rekordów, zależnościami i schedulerem.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>',
    accent: '#00bcd4',
    gradient: 'linear-gradient(135deg, #00bcd4, #18ffff)',
    tags: ['Data Flow', 'Visualization', 'ETL'],
    status: 'beta',
    statusLabel: 'BETA',
    date: '2026-07-07',
    author: 'T. Zieliński',
    version: '3.2.0',
    url: '/ai-reports/data-flow.html',
    metric: { label: 'Węzłów w grafie', value: 47, unit: '', display: 47, color: '#00bcd4' },
    findings: ['3 źródła → 5 landingi → 8 BUFF → 12 DM → 24 raporty', 'Największy przepływ: Core Banking (12M rekordów/dzień)', '2 węzły z opóźnieniem >4h'],
    recommendations: ['Zoptymalizuj węzły z opóźnieniem', 'Dodaj monitoring przepływów krytycznych'],
  },
  {
    id: 'duplicate-logic',
    category: 'etl',
    title: 'Duplicate Logic Detector',
    desc: 'Znajduje powieloną logikę ETL — identyczne CASE, JOIN, Expression i funkcje w SQL i mappingach. Wskazuje miejsca do refaktoryzacji.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
    accent: '#009688',
    gradient: 'linear-gradient(135deg, #009688, #4db6ac)',
    tags: ['ETL', 'Duplicate', 'Refactor', 'SQL'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'E. Mazur',
    version: '1.1.0',
    url: '/ai-reports/duplicate-logic.html',
    metric: { label: 'Duplikacje wykryte', value: 23, unit: '', display: 23, color: '#ff5252' },
    findings: ['8 identycznych CASE WHEN w różnych mappingach', '5 powielonych JOIN między widokami', '7 duplikatów Expression w sesjach', '3 identyczne funkcje PL/SQL w pakietach'],
    recommendations: ['Wydziel CASE do osobnego widoku', 'Stwórz funkcję dla powielonych JOIN', 'Zrefaktoryzuj Expression do shared objects'],
  },
  {
    id: 'data-mapping',
    category: 'etl',
    title: 'Data Mapping Prototype',
    desc: 'Prototyp mapowania danych między systemem źródłowym (Core Banking) a DWH. Diagram przepływu, transformacje i wykryte luki w mapowaniu.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    accent: '#ff9100',
    gradient: 'linear-gradient(135deg, #ff9100, #ffc400)',
    tags: ['Mapping', 'ETL', 'DWH'],
    status: 'stable',
    statusLabel: 'STABILNY',
    date: '2026-07-04',
    author: 'R. Krawczyk',
    version: '2.1.4',
    url: '/ai-reports/data-mapping.html',
    metric: { label: 'Pokrycie mapowania', value: 84, unit: '%', display: 84, color: '#ff9100' },
    findings: ['15 pól źródłowych bez mapowania', '3 transformacje o niepotwierdzonej logice', 'Luki w mapowaniu wymiarów'],
    recommendations: ['Uzupełnij brakujące mapowania', 'Zweryfikuj logikę transformacji'],
  },

  // ── RISK & QUALITY ──
  {
    id: 'deployment-risk',
    category: 'risk',
    title: 'Deployment Risk Analyzer',
    desc: 'Ocena ryzyka wdrożenia na podstawie Deployment Group, XML, Jira i Git. Klasyfikacja Low/Medium/High z pełnym uzasadnieniem.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    accent: '#ff5252',
    gradient: 'linear-gradient(135deg, #ff5252, #ff8a80)',
    tags: ['Deployment', 'Risk', 'Jira', 'Git'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'A. Wójcik',
    version: '1.2.0',
    url: '/ai-reports/deployment-risk.html',
    metric: { label: 'Risk Score', value: 68, unit: '/100', display: 68, color: '#ff5252' },
    findings: ['Wpływ na 12 procesów downstream', 'Zmiana dotyczy 8 krytycznych tabel', 'Wymagany restart schedulerów', 'Brak testów regresyjnych dla 3 mappingów'],
    recommendations: ['Wykonaj pełny regression test', 'Zaplanuj okno wdrożeniowe poza godzinami batch', 'Przygotuj rollback script'],
  },
  {
    id: 'oracle-impact',
    category: 'risk',
    title: 'Oracle Object Impact Analyzer',
    desc: 'Analiza wpływu zmian na tabelach, widokach i procedurach. Znajduje wszystkie zależne obiekty i wylicza Impact Score z ścieżkami zależności.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    accent: '#ff1744',
    gradient: 'linear-gradient(135deg, #ff1744, #d50000)',
    tags: ['Oracle', 'Impact', 'Objects', 'Dependencies'],
    status: 'beta',
    statusLabel: 'BETA',
    date: '2026-07-07',
    author: 'B. Szymański',
    version: '3.0.1',
    url: '/ai-reports/oracle-impact.html',
    metric: { label: 'Impact Score', value: 81, unit: '/100', display: 81, color: '#ff1744' },
    findings: ['34 zależne widoki od tabeli FCT_SALES', '12 procedur wymagających rekompilacji', '7 mappingów ETL korzystających z obiektu', '4 raporty BI oparte na zmienianym widoku'],
    recommendations: ['Przeanalizuj każdą ścieżkę zależności', 'Zaplanuj zmianę poza godzinami szczytu', 'Powiadom właścicieli raportów BI'],
  },
  {
    id: 'data-quality',
    category: 'risk',
    title: 'Data Quality Analyzer',
    desc: 'Kompleksowa analiza jakości danych: NULL, duplikaty, spójność FK/PK, wartości odstające i zakresy dat. Quality Score z listą problemów.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    accent: '#ffab00',
    gradient: 'linear-gradient(135deg, #ffab00, #ffd740)',
    tags: ['Data Quality', 'Validation', 'DQ'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'Ł. Dąbrowski',
    version: '2.0.0',
    url: '/ai-reports/data-quality.html',
    metric: { label: 'Quality Score', value: 76, unit: '/100', display: 76, color: '#ffab00' },
    findings: ['12.4% NULL w kluczowych kolumnach', '2 345 duplikatów PK w tabeli CUSTOMER_DIM', 'Niespójność dat między warstwą DM a Raportami', '8 wartości odstających w kolumnach finansowych'],
    recommendations: ['Uruchom proces czyszczenia duplikatów', 'Dodaj constrainty NOT NULL', 'Zweryfikuj zakresy dat w procesach ETL'],
  },
  {
    id: 'test-generator',
    category: 'risk',
    title: 'Auto Test Generator',
    desc: 'Automatycznie wygenerowane testy na podstawie analizy SQL. Wykrywa brakujące referencje, duplikacje i niespójności ETL z rekomendacjami AI.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    accent: '#d500f9',
    gradient: 'linear-gradient(135deg, #d500f9, #e040fb)',
    tags: ['Testy', 'SQL', 'Automatyzacja'],
    status: 'stable',
    statusLabel: 'STABILNY',
    date: '2026-07-04',
    author: 'D. Woźniak',
    version: '1.3.2',
    url: '/ai-reports/test-generator.html',
    metric: { label: 'Pokrycie testami', value: 67, unit: '%', display: 67, color: '#d500f9' },
    findings: ['45 testów wygenerowanych', '12 brakujących referencji wykrytych', '8 duplikacji w logice ETL'],
    recommendations: ['Rozszerz testy o przypadki brzegowe', 'Automatyzuj walidację po deploymentach'],
  },

  // ── DOCUMENTATION & RELEASES ──
  {
    id: 'doc-generator',
    category: 'docs',
    title: 'Documentation Generator',
    desc: 'Automatyczne generowanie dokumentacji technicznej procesów ETL: opis biznesowy, źródła, transformacje, zależności, scheduler i diagram. Wynik w Markdown/HTML/PDF.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    accent: '#448aff',
    gradient: 'linear-gradient(135deg, #448aff, #82b1ff)',
    tags: ['Documentation', 'ETL', 'Markdown', 'PDF'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'K. Kozłowski',
    version: '2.1.0',
    url: '/ai-reports/doc-generator.html',
    metric: { label: 'Dokumentacja', value: 100, unit: '%', display: '✓ Gotowe', color: '#448aff' },
    findings: ['5 procesów udokumentowanych', '3 diagramy przepływu wygenerowane', 'Dokumentacja w 3 formatach: MD, HTML, PDF'],
    recommendations: ['Dodaj sekcję SLA dla każdego procesu', 'Zintegruj z Confluence API'],
  },
  {
    id: 'release-summary',
    category: 'docs',
    title: 'Release Summary Generator',
    desc: 'Raport wydania na podstawie Deployment Group: Jira, Git, SQL, XML, Workflow, TeamCity. Executive Summary ze zmianami i checklistą post-deployment.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    accent: '#2979ff',
    gradient: 'linear-gradient(135deg, #2979ff, #448aff)',
    tags: ['Release', 'Jira', 'Git', 'Deployment'],
    status: 'beta',
    statusLabel: 'BETA',
    date: '2026-07-07',
    author: 'M. Jankowski',
    version: '3.0.0',
    url: '/ai-reports/release-summary.html',
    metric: { label: 'Przygotowanie', value: 85, unit: '%', display: 85, color: '#2979ff' },
    findings: ['Release R-2026.07: 12 zmian, 8 Jira ticketów', '3 nowe tabele, 2 usunięte obiekty', '4 workflow zmodyfikowane', 'Wymagany restart schedulerów'],
    recommendations: ['Wykonaj such-run przed deploymentem', 'Przygotuj raport po-wdrożeniowy', 'Zaktualizuj runbook'],
  },
  {
    id: 'scheduler-optimization',
    category: 'docs',
    title: 'Scheduler Optimization Report',
    desc: 'Analiza harmonogramów AutomateNow: wykrywanie kolizji, wąskich gardeł, optymalizacja równoległości z propozycją nowego harmonogramu i wykresem Gantta.',
    icon: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    accent: '#00e5ff',
    gradient: 'linear-gradient(135deg, #00e5ff, #18ffff)',
    tags: ['Scheduler', 'AutomateNow', 'Optimization'],
    status: 'new',
    statusLabel: 'NOWY',
    date: '2026-07-08',
    author: 'A. Kwiatkowska',
    version: '1.0.4',
    url: '/ai-reports/scheduler-optimization.html',
    metric: { label: 'Optymalizacja', value: 40, unit: '% oszczędności', display: 40, color: '#00e5ff' },
    findings: ['5 kolizji okien batchowych', '3 joby z czasem wykonania >6h', 'Niewykorzystana równoległość w oknie nocnym', 'Wąskie gardło: proces ładowania DM'],
    recommendations: ['Przesuń joby poza kolizje', 'Zwiększ równoległość w oknie 00-04', 'Podziel najdłuższe joby na mniejsze partie'],
  },
]

/* ──────────── CATEGORY DEFINITIONS ──────────── */
const categories = {
  all: { id: 'all', label: 'Wszystkie', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>' },
  sql: { id: 'sql', label: 'SQL & Optymalizacja', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>' },
  etl: { id: 'etl', label: 'ETL & Zależności', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/></svg>' },
  risk: { id: 'risk', label: 'Ryzyko & Jakość', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>' },
  docs: { id: 'docs', label: 'Dokumentacja & Release', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>' },
}

const filterCategories = computed(() => {
  return Object.values(categories).map(c => ({
    ...c,
    count: c.id === 'all' ? allReports.length : allReports.filter(r => r.category === c.id).length,
  }))
})

/* ──────────── COMPUTED ──────────── */
const filteredReports = computed(() => {
  if (activeCategory.value === 'all') return allReports
  return allReports.filter(r => r.category === activeCategory.value)
})

/** Filtruje + przestawia rozszerzony kafelek na początek jego rzędu,
 *  aby mógł zająć grid-column: 1 / -1 bez zjeżdżania do niższego rzędu */
const sortedReports = computed(() => {
  const list = filteredReports.value
  if (!activeReport.value) return list

  const activeIdx = list.findIndex(r => r.id === activeReport.value)
  if (activeIdx < 0 || activeIdx === 0) return list

  const rowStart = Math.floor(activeIdx / 3) * 3
  if (activeIdx === rowStart) return list

  const result = [...list]
  const [card] = result.splice(activeIdx, 1)
  result.splice(rowStart, 0, card)
  return result
})

/* ──────────── ACTIONS ──────────── */
function openReport(id) {
  activeReport.value = activeReport.value === id ? null : id
}

/** Wylicza stroke-dashoffset dla kołowego wskaźnika postępu */
function circleOffset(value) {
  const r = 18
  const circ = 2 * Math.PI * r
  return circ * (1 - Math.min(100, Math.max(0, value)) / 100)
}
</script>

<style scoped>
/* ───────── LAYOUT ───────── */
.hub-view { width: 100%; max-width: var(--content-width, 1200px); }

.hub-section-header { margin-bottom: 12px; }
.section-title { font-size: 24px; font-weight: 700; color: var(--text-primary); margin: 0 0 8px 0; letter-spacing: -0.3px; }
.section-desc { font-size: 14px; line-height: 1.6; color: var(--text-secondary); margin: 0; max-width: 680px; }

/* ───────── FILTER PILLS ───────── */
.filter-row {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 16px;
  border-radius: 100px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  white-space: nowrap;
}

.filter-btn:hover {
  border-color: rgba(83, 109, 254, 0.3);
  color: var(--text-primary);
  background: var(--bg-hover);
}

.filter-btn.active {
  background: rgba(83, 109, 254, 0.12);
  border-color: #536dfe;
  color: #536dfe;
}

.filter-icon { display: flex; align-items: center; opacity: 0.7; }
.filter-btn.active .filter-icon { opacity: 1; }

.filter-count {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 7px;
  border-radius: 100px;
  background: var(--bg-tag);
  color: var(--text-muted);
  margin-left: 2px;
}

.filter-btn.active .filter-count {
  background: rgba(83, 109, 254, 0.15);
  color: #536dfe;
}

/* ───────── REPORT GRID (CSS Grid) ───────── */
.report-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  grid-auto-flow: row dense;
  margin-bottom: 24px;
}

/* ───────── REPORT CARD ───────── */
.report-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0;
  transition: border-color 0.35s ease,
              box-shadow 0.35s ease;
  align-self: start;
  z-index: 1;
}

.report-card:hover {
  border-color: rgba(255, 255, 255, 0.12);
}

/* ── Rozszerzenie: kafelek rozciąga się na wszystkie kolumny ── */
/* row dense automatycznie wypełnia puste komórki po lewej */
.report-card.expanded {
  grid-column: 1 / -1;
  border-color: var(--card-accent, #536dfe);
  box-shadow: 0 0 0 1px var(--card-accent, #536dfe), 0 16px 48px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

.card-clickable {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-clickable:hover .card-icon {
  transform: scale(1.1);
}

.card-accent { height: 4px; flex-shrink: 0; border-radius: 14px 14px 0 0; overflow: hidden; }

/* ───────── CARD TOP ───────── */
.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  padding-top: 14px;
}

.card-top-right {
  display: flex;
  align-items: center;
  gap: 6px;
}

.card-icon {
  color: var(--card-accent, #536dfe);
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

/* Close button */
.card-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-hover);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
  padding: 0;
}

.card-close:hover {
  border-color: #ff5252;
  color: #ff5252;
  background: rgba(255, 82, 82, 0.1);
}

/* Status badges */
.card-status {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.8px;
  padding: 3px 10px;
  border-radius: 100px;
  text-transform: uppercase;
}

.card-status.new {
  background: rgba(0, 200, 83, 0.12);
  color: #00c853;
  border: 1px solid rgba(0, 200, 83, 0.2);
}

.card-status.beta {
  background: rgba(83, 109, 254, 0.12);
  color: #536dfe;
  border: 1px solid rgba(83, 109, 254, 0.2);
}

.card-status.stable {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

/* ───────── CARD CONTENT ───────── */
.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  padding: 0 20px;
  margin: 0;
  line-height: 1.3;
}

.card-desc {
  font-size: 12.5px;
  line-height: 1.6;
  color: var(--text-secondary);
  padding: 0 20px;
  margin: 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.report-card.expanded .card-desc {
  -webkit-line-clamp: unset;
  overflow: visible;
}

/* ───────── METRIC CIRCLE ───────── */
.card-metric-circle {
  padding: 4px 20px 0 20px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.circle-svg {
  flex-shrink: 0;
}

.circle-track {
  stroke: var(--bg-tag);
}

.circle-fill {
  transition: stroke-dashoffset 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.circle-text {
  font-size: 11px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.circle-meta {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.circle-label {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.3;
}

.circle-unit {
  font-size: 10px;
  color: var(--text-muted);
  opacity: 0.6;
}

/* ──────── ROZSZERZONA ZAWARTOŚĆ (wewnątrz kafelka) ──────── */
.card-extra {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transition: max-height 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              opacity 0.35s ease,
              margin 0.35s ease;
  margin: 0 20px;
}

.card-extra.open {
  max-height: 600px;
  opacity: 1;
}

/* Gdy kafelek rozszerzony: findings + recs w dwóch kolumnach obok siebie */
.report-card.expanded .card-extra-inner {
  flex-direction: row;
  gap: 24px;
}

.report-card.expanded .ex-section {
  flex: 1;
  min-width: 0;
}

.report-card.expanded .ex-section:first-child {
  border-right: 1px solid var(--border-color);
  padding-right: 24px;
}

/* ── EX-(Sekcje) ── */
.ex-section {}

.ex-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  gap: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ex-title svg {
  flex-shrink: 0;
  opacity: 0.6;
}

.card-extra-inner {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ex-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ex-list li {
  font-size: 12px;
  line-height: 1.5;
  color: var(--text-secondary);
  padding-left: 14px;
  position: relative;
}

.ex-dot {
  position: absolute;
  left: 0;
  top: 6px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
}

.ex-list.recs li { padding-left: 16px; }
.ex-arrow {
  position: absolute;
  left: 0;
  color: var(--card-accent, #536dfe);
  font-weight: 700;
  font-size: 12px;
}

/* ───────── TAGS ───────── */
.card-tags {
  padding: 0 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: auto;
}

.tag {
  font-size: 10.5px;
  font-weight: 500;
  padding: 2px 9px;
  border-radius: 100px;
  background: var(--bg-tag);
  color: var(--text-muted);
  border: 1px solid transparent;
  transition: all 0.15s;
}

.report-card:hover .tag {
  border-color: var(--border-color);
  color: var(--text-secondary);
}

/* ───────── FOOTER ───────── */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-top: 1px solid var(--border-color);
  gap: 8px;
}

.card-meta {
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
  min-width: 0;
}

.card-author {
  color: var(--text-secondary);
  font-weight: 500;
}

.card-date { color: var(--text-muted); }

.card-action {
  font-size: 12px;
  font-weight: 600;
  color: var(--card-accent, #536dfe);
  cursor: pointer;
  transition: transform 0.2s;
  user-select: none;
  white-space: nowrap;
}

.report-card:not(.expanded) .card-action:hover {
  transform: translateX(3px);
}

.card-action-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 600;
  color: var(--card-accent, #536dfe);
  text-decoration: none;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--card-accent, #536dfe);
  transition: all 0.15s;
  white-space: nowrap;
}
.card-action-link:hover {
  background: color-mix(in srgb, var(--card-accent, #536dfe) 10%, transparent);
}

/* ── Pulsujący glow dla przycisku "Pełny raport" ── */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 4px color-mix(in srgb, var(--card-accent, #536dfe) 30%, transparent);
  }
  50% {
    box-shadow: 0 0 12px color-mix(in srgb, var(--card-accent, #536dfe) 50%, transparent),
                0 0 24px color-mix(in srgb, var(--card-accent, #536dfe) 20%, transparent);
  }
}

.card-action-link.pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

/* ───────── RESPONSIVE ───────── */
@media (max-width: 960px) {
  .report-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  /* Na wąskim ekranie findings i recs jeden pod drugim */
  .report-card.expanded .card-extra-inner {
    flex-direction: column !important;
    gap: 14px !important;
  }
  .report-card.expanded .ex-section:first-child {
    border-right: none !important;
    padding-right: 0 !important;
  }
}

@media (max-width: 560px) {
  .report-grid {
    grid-template-columns: 1fr !important;
  }
  .report-card.expanded .card-extra-inner {
    flex-direction: column !important;
  }
  .report-card.expanded .ex-section:first-child {
    border-right: none !important;
    padding-right: 0 !important;
  }
}
</style>
