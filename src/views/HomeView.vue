<template>
  <div class="home">
    <header class="page-header">
      <div class="header-content">
        <h1 class="page-title">Enterprise Hub Portal</h1>
        <p class="page-subtitle">
          Centralny punkt dostępu do narzędzi developerskich, raportowania biznesowego
          i innowacji AI. Wybierz hub, aby kontynuować.
        </p>
      </div>
      <div class="header-meta">
        <div class="meta-chip">
          <span class="chip-dot"></span>
          System online
        </div>
        <div class="meta-chip version">v0.1.0 POC</div>
      </div>
    </header>

    <section class="hub-cards">
      <article class="hub-card ddt" @click="$router.push('/ddt')">
        <div class="hub-card-bg"></div>
        <div class="hub-card-content">
          <div class="hub-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
            </svg>
          </div>
          <h2 class="hub-title">DDT — Developer Dev Tools</h2>
          <p class="hub-desc">
            Integracje z Jira, Confluence, IAM, TeamCity, Informatica PowerCenter
            oraz zestaw narzędzi developerskich w Streamlit.
          </p>
          <div class="hub-stats">
            <span class="stat"><strong>12</strong> modułów</span>
            <span class="stat"><strong>Python</strong> + Streamlit</span>
          </div>
          <div class="hub-action">
            <span class="action-label">Przejdź do huba</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
      </article>

      <article class="hub-card apex" @click="$router.push('/apex')">
        <div class="hub-card-bg"></div>
        <div class="hub-card-content">
          <div class="hub-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>
            </svg>
          </div>
          <h2 class="hub-title">APEX — Business Intelligence</h2>
          <p class="hub-desc">
            Dashboardy KPI, raporty codzienne, statystyki systemowe i helicopter view
            na całą organizację.
          </p>
          <div class="hub-stats">
            <span class="stat"><strong>24</strong> dashboardy</span>
            <span class="stat"><strong>Oracle</strong> + Snowflake</span>
          </div>
          <div class="hub-action">
            <span class="action-label">Przejdź do huba</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
      </article>

      <article class="hub-card ai" @click="$router.push('/ai')">
        <div class="hub-card-bg"></div>
        <div class="hub-card-content">
          <div class="hub-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"/><circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          <h2 class="hub-title">AI Innovation Lab</h2>
          <p class="hub-desc">
            Koncepty AI zgodne z regulacjami bankowymi, raporty HTML, eksperymenty
            i rozwiązania zatwierdzone do użytku wewnętrznego.
          </p>
          <div class="hub-stats">
            <span class="stat"><strong>8</strong> konceptów</span>
            <span class="stat"><strong>Raporty</strong> HTML</span>
          </div>
          <div class="hub-action">
            <span class="action-label">Przejdź do huba</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
      </article>
    </section>

    <section class="quick-stats">
      <div class="stat-card">
        <span class="stat-value">3</span>
        <span class="stat-label">Huby</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">44</span>
        <span class="stat-label">Moduły</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">12</span>
        <span class="stat-label">Integracje</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">Azure</span>
        <span class="stat-label">Target Cloud</span>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  max-width: 1200px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 40px;
  gap: 24px;
}

.header-content {
  flex: 1;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
}

.header-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
  flex-shrink: 0;
}

.meta-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 6px 14px;
  border-radius: 100px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
}

.meta-chip.version {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
}

.chip-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #00c853;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* Hub Cards */
.hub-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.hub-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  transition: all 0.3s ease;
}

.hub-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.hub-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.hub-card.ddt .hub-card-bg { background: linear-gradient(90deg, #00c853, #00e5ff); }
.hub-card.apex .hub-card-bg { background: linear-gradient(90deg, #ff9100, #ff3d00); }
.hub-card.ai .hub-card-bg { background: linear-gradient(90deg, #536dfe, #d500f9); }

.hub-card-content {
  position: relative;
  padding: 28px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hub-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-hover);
}

.hub-card.ddt .hub-icon { color: #00c853; }
.hub-card.apex .hub-icon { color: #ff9100; }
.hub-card.ai .hub-icon { color: #536dfe; }

.hub-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.hub-desc {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
}

.hub-stats {
  display: flex;
  gap: 16px;
}

.stat {
  font-size: 12px;
  color: var(--text-muted);
}

.stat strong {
  color: var(--text-primary);
  font-weight: 600;
}

.hub-action {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--accent-primary);
  margin-top: 4px;
}

.hub-card:hover .hub-action svg {
  transform: translateX(4px);
  transition: transform 0.2s ease;
}

/* Quick Stats */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}
</style>
