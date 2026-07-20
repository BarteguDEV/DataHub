<template>
  <div class="hub-view" :style="{ maxWidth: contentWidth + 'px' }">
    <!-- ====== HEADER ====== -->
    <div class="planning-header">
      <div class="header-left">
        <h1 class="section-title">Planning Hub</h1>
        <p class="section-desc">Zapisuj tematy ze spotkań i układaj priorytety</p>
      </div>
      <div class="header-right">
        <!-- View toggle tabs -->
        <div class="view-tabs">
          <button
            class="view-tab"
            :class="{ active: viewMode === 'ranking' }"
            @click="viewMode = 'ranking'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
            Ranking
          </button>
          <button
            class="view-tab"
            :class="{ active: viewMode === 'matrix' }"
            @click="viewMode = 'matrix'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
              <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
            </svg>
            Matrix
          </button>
          <button
            class="view-tab"
            :class="{ active: viewMode === 'graph' }"
            @click="viewMode = 'graph'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/>
              <circle cx="12" cy="18" r="2"/>
              <line x1="8" y1="7" x2="11" y2="16"/><line x1="16" y1="7" x2="13" y2="16"/>
            </svg>
            Graf
          </button>
          <button
            class="view-tab"
            :class="{ active: viewMode === 'roadmap' }"
            @click="viewMode = 'roadmap'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="16" rx="2"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
              <line x1="7" y1="7" x2="7.01" y2="7"/>
              <line x1="12" y1="7" x2="12.01" y2="7"/>
              <line x1="17" y1="7" x2="17.01" y2="7"/>
              <line x1="7" y1="13" x2="11" y2="13"/>
              <line x1="14" y1="13" x2="19" y2="13"/>
            </svg>
            Harmonogram
          </button>
        </div>
      </div>
    </div>

    <div class="hub-layout">
      <!-- ====== BACKLOG SIDEBAR ====== -->
      <aside class="bp" :class="{ 'bp-collapsed': bpCollapsed }">
        <div class="bp-header">
          <h3 class="bp-title" v-show="!bpCollapsed">Backlog</h3>
          <span class="bp-count" v-show="!bpCollapsed">{{ topics.length }}</span>
          <button class="bp-toggle" @click="toggleBpCollapsed" :title="bpCollapsed ? 'Rozwiń' : 'Zwiń'">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline :points="bpCollapsed ? '9 18 15 12 9 6' : '18 9 12 15 6 9'"/>
            </svg>
          </button>
        </div>
        <div class="bp-body" v-show="!bpCollapsed">
          <div class="bp-add">
            <input
              v-model="bpNewTitle"
              type="text"
              placeholder="+ Nowy temat…"
              class="bp-input"
              @keyup.enter="bpAddTopic"
            />
          </div>
          <div class="bp-list">
            <div
              v-for="t in topics"
              :key="t.id"
              class="bp-item"
              :class="{ 'bp-item-done': t.status === 'done' }"
              draggable="true"
              @dragstart="onBpDragStart(t, $event)"
            >
              <span class="bp-item-title" :class="{ 'text-done': t.status === 'done' }">{{ t.title }}</span>
              <span class="bp-item-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
              <button
                class="bp-status"
                :class="'status-' + t.status"
                @click.stop="cycleStatus(t)"
                :title="statusLabel(t.status)"
              >
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <circle v-if="t.status === 'todo'" cx="12" cy="12" r="8"/>
                  <path v-if="t.status === 'in-progress'" d="M12 2v4M12 22v-4M2 12h4M22 12h-4"/>
                  <path v-if="t.status === 'ongoing'" d="M12 8v8M8 12h8"/>
                  <polyline v-if="t.status === 'done'" points="20 6 9 17 4 12"/>
                </svg>
              </button>
              <button class="bp-del" @click="deleteTopic(t.id)" title="Usuń">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            <div v-if="topics.length === 0" class="bp-empty">
              <p>Brak tematów</p>
            </div>
          </div>
        </div>
      </aside>

      <main class="hub-main">

    <!-- ====== QUICK-ADD ====== -->
    <div class="add-bar">
      <div class="add-input-wrapper">
        <svg class="add-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <input
          v-model="newTitle"
          type="text"
          placeholder="Dodaj temat…"
          class="add-input"
          @keyup.enter="addTopic"
        />
        <select v-model="newTag" class="tag-select">
          <option value="cross">cross</option>
          <option value="EMIR_3">EMIR_3</option>
          <option value="SFTR">SFTR</option>
          <option value="WITIP">WITIP</option>
          <option value="ARM">ARM</option>
        </select>
        <button class="add-btn" @click="addTopic" :disabled="!newTitle.trim()">Dodaj</button>
      </div>
    </div>

    <!-- ====== STATS BAR ====== -->
    <div class="stats-bar">
      <span class="stat-item">
        <span class="stat-num">{{ topics.length }}</span>
        tematów
      </span>
      <span class="stat-item">
        <span class="stat-num">{{ topics.filter(t => t.status === 'todo').length }}</span>
        do zrobienia
      </span>
      <span class="stat-item">
        <span class="stat-num">{{ topics.filter(t => t.status === 'in-progress').length }}</span>
        w trakcie
      </span>
      <span class="stat-item">
        <span class="stat-num">{{ topics.filter(t => t.status === 'ongoing').length }}</span>
        ciągłe
      </span>
      <span class="stat-item">
        <span class="stat-num">{{ topics.filter(t => t.status === 'done').length }}</span>
        zrobione
      </span>
    </div>

    <!-- ====== RANKING VIEW ====== -->
    <div v-if="viewMode === 'ranking'" class="ranking-view">
      <div class="ranking-list">
        <div
          v-for="(topic, idx) in rankedTopics"
          :key="topic.id"
          class="rank-card"
          :class="{ 'drag-over': dragOverId === topic.id }"
          draggable="true"
          @dragstart="onDragStart(topic, $event)"
          @dragover.prevent="onDragOver(topic)"
          @dragleave="dragOverId = null"
          @drop.prevent="onDrop(topic)"
          @dragend="dragOverId = null"
        >
          <span class="rank-number">{{ idx + 1 }}</span>
          <span class="drag-handle" title="Przeciągnij, aby zmienić kolejność">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/>
            </svg>
          </span>
          <span class="rank-title" :class="{ 'text-done': topic.status === 'done' }">{{ topic.title }}</span>
          <span class="rank-tag" :class="'tag-' + topic.tag">{{ topic.tag }}</span>
          <button
            v-if="topic.priority"
            class="prio-badge"
            :class="'prio-' + topic.priority"
            @click.stop="cyclePriority(topic)"
            :title="'Priorytet ' + topic.priority + ' — kliknij, aby zmienić'"
          >
            P{{ topic.priority }}
          </button>
          <button
            v-else
            class="prio-badge prio-none"
            @click.stop="cyclePriority(topic)"
            title="Kliknij, aby ustawić priorytet"
          >
            &ndash;
          </button>
          <button
            class="status-badge"
            :class="'status-' + topic.status"
            @click.stop="cycleStatus(topic)"
            :title="'Kliknij, aby zmienić status'"
          >
            {{ statusLabel(topic.status) }}
          </button>
          <button class="rank-delete" @click="deleteTopic(topic.id)" title="Usuń">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div v-if="rankedTopics.length === 0" class="empty-state">
          <p>Brak tematów. Dodaj pierwszy powyżej.</p>
        </div>
      </div>
    </div>

    <!-- ====== MATRIX VIEW ====== -->
    <div v-else-if="viewMode === 'matrix'" class="matrix-view">
      <div class="matrix-grid">
        <!-- Top row -->
        <div class="matrix-cell quadrant-qw" @dragover.prevent @drop.prevent="moveToQuadrant($event, 'quick-wins')">
          <div class="quadrant-label">
            <span class="quadrant-title">Quick Wins</span>
            <span class="quadrant-sub">Wysoka wartość • Mały nakład</span>
          </div>
          <div
            v-for="t in matrixTopics('quick-wins')"
            :key="t.id"
            class="matrix-card"
            draggable="true"
            @dragstart="onMatrixDragStart(t, $event)"
          >
            <span class="matrix-card-title" :class="{ 'text-done': t.status === 'done' }">{{ t.title }}</span>
            <span class="rank-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
            <button
              class="status-badge sm"
              :class="'status-' + t.status"
              @click.stop="cycleStatus(t)"
            >
              {{ statusLabel(t.status) }}
            </button>
            <button class="card-unassign" @click.stop="moveToBacklog(t)" title="Przenieś do backlogu">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/>
              </svg>
            </button>
          </div>
          <div v-if="matrixTopics('quick-wins').length === 0" class="quadrant-empty">
            Przeciągnij tematy tutaj
          </div>
        </div>

        <div class="matrix-cell quadrant-sb" @dragover.prevent @drop.prevent="moveToQuadrant($event, 'strategic-bets')">
          <div class="quadrant-label">
            <span class="quadrant-title">Strategic Bets</span>
            <span class="quadrant-sub">Wysoka wartość • Duży nakład</span>
          </div>
          <div
            v-for="t in matrixTopics('strategic-bets')"
            :key="t.id"
            class="matrix-card"
            draggable="true"
            @dragstart="onMatrixDragStart(t, $event)"
          >
            <span class="matrix-card-title" :class="{ 'text-done': t.status === 'done' }">{{ t.title }}</span>
            <span class="rank-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
            <button
              class="status-badge sm"
              :class="'status-' + t.status"
              @click.stop="cycleStatus(t)"
            >
              {{ statusLabel(t.status) }}
            </button>
            <button class="card-unassign" @click.stop="moveToBacklog(t)" title="Przenieś do backlogu">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/>
              </svg>
            </button>
          </div>
          <div v-if="matrixTopics('strategic-bets').length === 0" class="quadrant-empty">
            Przeciągnij tematy tutaj
          </div>
        </div>

        <!-- Bottom row -->
        <div class="matrix-cell quadrant-fi" @dragover.prevent @drop.prevent="moveToQuadrant($event, 'fill-ins')">
          <div class="quadrant-label">
            <span class="quadrant-title">Fill-ins</span>
            <span class="quadrant-sub">Niska wartość • Mały nakład</span>
          </div>
          <div
            v-for="t in matrixTopics('fill-ins')"
            :key="t.id"
            class="matrix-card"
            draggable="true"
            @dragstart="onMatrixDragStart(t, $event)"
          >
            <span class="matrix-card-title" :class="{ 'text-done': t.status === 'done' }">{{ t.title }}</span>
            <span class="rank-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
            <button
              class="status-badge sm"
              :class="'status-' + t.status"
              @click.stop="cycleStatus(t)"
            >
              {{ statusLabel(t.status) }}
            </button>
            <button class="card-unassign" @click.stop="moveToBacklog(t)" title="Przenieś do backlogu">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/>
              </svg>
            </button>
          </div>
          <div v-if="matrixTopics('fill-ins').length === 0" class="quadrant-empty">
            Przeciągnij tematy tutaj
          </div>
        </div>

        <div class="matrix-cell quadrant-mp" @dragover.prevent @drop.prevent="moveToQuadrant($event, 'money-pits')">
          <div class="quadrant-label">
            <span class="quadrant-title">Money Pits</span>
            <span class="quadrant-sub">Niska wartość • Duży nakład</span>
          </div>
          <div
            v-for="t in matrixTopics('money-pits')"
            :key="t.id"
            class="matrix-card"
            draggable="true"
            @dragstart="onMatrixDragStart(t, $event)"
          >
            <span class="matrix-card-title" :class="{ 'text-done': t.status === 'done' }">{{ t.title }}</span>
            <span class="rank-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
            <button
              class="status-badge sm"
              :class="'status-' + t.status"
              @click.stop="cycleStatus(t)"
            >
              {{ statusLabel(t.status) }}
            </button>
            Przeciągnij tematy tutaj
          </div>
        </div>
      </div>

    </div>

    <!-- ====== GRAPH VIEW ====== -->
    <div v-else-if="viewMode === 'graph'" class="graph-view">
      <div class="graph-wrap" :class="{ 'graph-fullscreen': graphFullscreen }">
      <!-- Graph toolbar -->
      <div class="graph-toolbar">
        <button
          class="graph-btn"
          :class="{ 'graph-btn-active': connectMode }"
          @click="toggleConnectMode"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
          </svg>
          {{ connectMode ? 'Zakończ' : 'Połącz tematy' }}
        </button>
        <span v-if="connectMode && connectSource" class="connect-hint">
          Wybrano: <strong>{{ connectSource.title }}</strong> — kliknij drugi temat
        </span>
        <span v-else-if="connectMode" class="connect-hint">
          Kliknij temat źródłowy (ten, który blokuje / testuje)
        </span>
        <div class="graph-legend">
          <span class="legend-item"><span class="legend-swatch swatch-blocks"></span>Blokuje</span>
          <span class="legend-item"><span class="legend-swatch swatch-tested_by"></span>Testowane przez</span>
          <span class="legend-item"><span class="legend-swatch swatch-depends_on"></span>Zależy od</span>
        </div>
        <button v-if="!graphFullscreen" class="graph-btn graph-btn-fullscreen" @click="toggleFullscreen" title="Fullscreen">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
          </svg>
        </button>
      </div><!-- /graph-toolbar -->

      <!-- Zoom info -->
      <div class="graph-zoom-bar">
        <button class="graph-zoom-btn" @click="graphZoomIn" title="Przybliż">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        </button>
        <span class="graph-zoom-label">{{ Math.round(graphZoom * 100) }}%</span>
        <button class="graph-zoom-btn" @click="graphZoomOut" title="Pomniejsz">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/></svg>
        </button>
        <button class="graph-zoom-btn graph-zoom-fit" @click="graphZoomReset" title="Dopasuj">Fit</button>
      </div>

      <!-- Graph canvas -->
      <div
        class="graph-canvas"
        ref="graphRef"
        @mousemove="onCanvasMouseMove"
        @mouseup="onCanvasMouseUp"
        @mouseleave="onCanvasMouseUp"
        @wheel.prevent="onGraphWheel"
        @click.self="onCanvasClick"
        :class="{ 'graph-canvas-panning': isPanning }"
      >
        <div
          class="graph-layer"
          @mousedown.self="onCanvasPanStart"
          :style="{ transform: 'scale(' + graphZoom + ')', transformOrigin: 'center top' }"
        >
        <!-- SVG overlay for connection lines -->
        <svg class="graph-svg" :width="canvasSize.w" :height="canvasSize.h">
          <defs>
            <marker id="g-arrow-blocks" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#ff5252" />
            </marker>
            <marker id="g-arrow-tested_by" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#536dfe" />
            </marker>
            <marker id="g-arrow-depends_on" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#ffb300" />
            </marker>
          </defs>
          <g v-for="dep in deps" :key="dep.id" @mouseenter="hoveredDep = dep.id" @mouseleave="hoveredDep = null">
            <!-- Krzywa Beziera -->
            <path
              v-if="getEdgeCurve(dep.from_id, dep.to_id, dep.type)"
              :d="getEdgeCurve(dep.from_id, dep.to_id, dep.type).d"
              :class="['dep-line', 'dep-line-' + dep.type, { 'dep-line-hover': hoveredDep === dep.id }]"
              :stroke-width="hoveredDep === dep.id ? 3 : 2"
              fill="none"
              stroke-linecap="round"
              :marker-end="'url(#g-arrow-' + dep.type + ')'"
              @click.stop="cycleDepType(dep)"
            />
            <!-- Pulsująca kropka -->
            <circle
              v-if="pulseDots[dep.id] !== undefined"
              :cx="getPointOnCurve(getEdgeCurve(dep.from_id, dep.to_id, dep.type), pulseDots[dep.id])?.x || 0"
              :cy="getPointOnCurve(getEdgeCurve(dep.from_id, dep.to_id, dep.type), pulseDots[dep.id])?.y || 0"
              r="4"
              class="pulse-dot"
              :class="'pulse-' + dep.type"
            />
            <!-- Delete button na środku krawędzi -->
            <g v-if="hoveredDep === dep.id" class="dep-delete-group" @click.stop="deleteDep(dep.id)">
              <circle
                :cx="getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midX || 0"
                :cy="getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midY || 0"
                r="10" fill="#ff5252"
              />
              <line
                :x1="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midX || 0) - 4"
                :y1="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midY || 0) - 4"
                :x2="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midX || 0) + 4"
                :y2="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midY || 0) + 4"
                stroke="white" stroke-width="2" stroke-linecap="round"
              />
              <line
                :x1="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midX || 0) + 4"
                :y1="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midY || 0) - 4"
                :x2="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midX || 0) - 4"
                :y2="(getEdgeCurve(dep.from_id, dep.to_id, dep.type)?.midY || 0) + 4"
                stroke="white" stroke-width="2" stroke-linecap="round"
              />
            </g>
          </g>
        </svg>

        <!-- Topic nodes -->
        <div
          v-for="t in topics"
          :key="t.id"
          class="graph-node"
          :class="{
            'graph-node-source': connectMode && connectSource?.id === t.id,
            'graph-node-target': connectMode && connectSource && connectSource.id !== t.id,
            'graph-node-done': t.status === 'done'
          }"
          :style="getPos(t.id) ? { left: getPos(t.id).x + 'px', top: getPos(t.id).y + 'px' } : { display: 'none' }"
          @mousedown.stop="onNodeMouseDown(t, $event)"
          @click.stop="onNodeClick(t)"
        >
          <span class="graph-node-title" :class="{ 'text-done': t.status === 'done' }">{{ t.title }}</span>
          <span class="graph-node-meta">
            <span class="rank-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
            <button
              class="status-badge sm"
              :class="'status-' + t.status"
              @click.stop="cycleStatus(t)"
            >
              {{ statusLabel(t.status) }}
            </button>
          </span>
        </div>

        <div v-if="topics.length === 0" class="graph-empty">
          <p>Dodaj tematy, aby tworzyć graf zależności</p>
        </div>
        </div><!-- /graph-layer -->
      </div><!-- /graph-canvas -->

      <!-- ====== JIRA RELATIONS PANEL ====== -->
      <div class="jira-panel" v-if="deps.length > 0">
        <button class="jira-toggle" @click="showJiraLinks = !showJiraLinks">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline :points="showJiraLinks ? '18 15 12 9 6 15' : '9 18 15 12 9 6'"/>
          </svg>
          <span class="jira-toggle-label">Relacje Jira</span>
          <span class="jira-badge">{{ deps.length }}</span>
          <span class="jira-toggle-hint" v-if="!showJiraLinks">Pokaż</span>
        </button>
        <div class="jira-body" v-show="showJiraLinks">
          <div class="jira-toolbar">
            <span class="jira-info">Wygenerowane relacje między zadaniami</span>
            <button class="jira-copy-btn" @click="copyJiraLinks" title="Kopiuj wszystko">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
              </svg>
              Kopiuj
            </button>
          </div>
          <div class="jira-list">
            <div v-for="(rel, ri) in jiraRelationships" :key="ri" class="jira-row">
              <span class="jira-from" :style="{ color: rel.color }">{{ rel.from }}</span>
              <span class="jira-arrow" :style="{ color: rel.color }">
                <svg width="14" height="10" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="2" y1="6" x2="20" y2="6"/><polyline points="15 2 20 6 15 10"/>
                </svg>
              </span>
              <span class="jira-label" :style="{ background: rel.color + '18', color: rel.color }">{{ rel.label }}</span>
              <span class="jira-to" :style="{ color: rel.color }">{{ rel.to }}</span>
            </div>
          </div>
        </div>
      </div><!-- /jira-panel -->
      </div><!-- /graph-wrap -->
      <button v-if="graphFullscreen" class="graph-fs-close" @click="toggleFullscreen">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>

    <!-- ====== ROADMAP VIEW ====== -->
    <div v-else class="roadmap-view">
      <!-- Toolbar -->
      <div class="rm-toolbar">
        <button class="rm-btn" @click="rmZoomOut" title="Pomniejsz">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/></svg>
        </button>
        <span class="rm-scale-label">{{ rmScaleLabel }}</span>
        <button class="rm-btn" @click="rmZoomIn" title="Przybliż">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        </button>
        <button class="rm-btn" @click="rmToday" title="Dzisiaj">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Dziś
        </button>
        <span class="rm-badge" v-if="criticalTopics.length">Ścieżka krytyczna: {{ criticalTopics.length }} tematów</span>
      </div>

      <!-- Timeline -->
      <div class="rm-container" ref="rmRef">
        <!-- Left column — list of topic lanes -->
        <div class="rm-lanes">
          <div class="rm-lane-header" v-for="t in rmScheduledTopics" :key="t.id">
            <div class="rm-lane-title">
              <span class="rm-lane-name" :class="{ 'text-done': t.status === 'done', 'rm-critical': isCritical(t) }">{{ t.title }}</span>
              <button class="rm-unschedule-btn" @click="rmUnschedule(t)" title="Cofnij do niezaplanowanych">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Right area — scrollable timeline -->
        <div class="rm-timeline-scroll" ref="rmScrollRef">
          <!-- Grid + header -->
          <div class="rm-timeline" :style="{ width: rmTotalWidth + 'px' }" @dragover.prevent @drop.prevent="rmTimelineDrop">
            <!-- Week headers -->
            <div class="rm-headers">
              <div
                v-for="(w, wi) in rmWeeks"
                :key="wi"
                class="rm-week-header"
                :class="{ 'rm-week-today': rmIsCurrentWeek(w) }"
                :style="{ width: rmColW + 'px' }"
              >
                <span class="rm-week-month">{{ w.month }}</span>
                <span class="rm-week-num">{{ w.label }}</span>
              </div>
            </div>

            <!-- Today marker -->
            <div class="rm-today-line" :style="{ left: rmTodayOffset + 'px' }"></div>

            <!-- Lanes body -->
            <div class="rm-body">
              <div
                v-for="t in rmScheduledTopics"
                :key="t.id"
                class="rm-lane"
                :style="{ height: rmLaneH + 'px' }"
              >
                <!-- Dependency arrows (SVG overlay) -->
                <svg class="rm-arrows" :width="rmTotalWidth" :height="rmLaneH" v-if="t.id === rmShowArrowsFor">
                  <!-- arrows rendered per active lane -->
                </svg>

                <!-- The bar -->
                <div
                  v-if="rmGetBar(t)"
                  class="rm-bar"
                  :class="['status-' + t.status, { 'rm-bar-critical': isCritical(t), 'rm-bar-done': t.status === 'done' }]"
                  :style="rmGetBar(t)"
                  @mousedown.stop="rmBarMouseDown(t, $event)"
                >
                  <span class="rm-bar-label">{{ t.title }}</span>
                  <span class="rm-bar-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
                  <!-- Right resize handle -->
                  <div class="rm-bar-handle" @mousedown.stop="rmHandleMouseDown(t, $event)"></div>
                </div>

                <!-- Week grid lines -->
                <div
                  v-for="(w, wi) in rmWeeks"
                  :key="'g' + wi"
                  class="rm-week-line"
                  :style="{ left: wi * rmColW + 'px', width: rmColW + 'px' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Unscheduled pool -->
      <div class="rm-unscheduled" v-if="rmUnscheduledTopics.length">
        <h4 class="rm-unscheduled-title">Niezaplanowane</h4>
        <div class="rm-unscheduled-list">
          <div
            v-for="t in rmUnscheduledTopics"
            :key="t.id"
            class="rm-unscheduled-card"
            draggable="true"
            @dragstart="rmUnschedDragStart(t, $event)"
          >
            <span class="rm-unscheduled-name">{{ t.title }}</span>
            <span class="rank-tag" :class="'tag-' + t.tag">{{ t.tag }}</span>
        </div>
      </div>
    </div>
    </div>
    </main>
  </div>
</div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useContentWidth } from '@/stores/width'

// ====== STATE ======
const { contentWidth } = useContentWidth()
const viewMode = ref('ranking')
const newTitle = ref('')
const newTag = ref('cross')
const topics = ref([])
const loading = ref(true)

// Backlog sidebar
const bpCollapsed = ref(false)
const bpNewTitle = ref('')

function toggleBpCollapsed() {
  bpCollapsed.value = !bpCollapsed.value
}

function bpAddTopic() {
  const title = bpNewTitle.value.trim()
  if (!title) return
  const topic = {
    id: nextId++,
    title,
    tag: newTag.value,
    status: 'todo',
    quadrant: null,
    priority: null,
    order: topics.value.length,
    start_date: null,
    end_date: null,
  }
  topics.value.push(topic)
  createTopicOnServer(topic)
  bpNewTitle.value = ''
}

// Drag state (ranking)
const dragOverId = ref(null)
let draggedTopic = null

const STATUS_CYCLE = ['todo', 'in-progress', 'ongoing', 'done']

const STATUS_LABELS = {
  'todo': 'Do zrobienia',
  'in-progress': 'W trakcie',
  'ongoing': 'Ciągłe',
  'done': 'Zrobione',
}

function statusLabel(status) {
  return STATUS_LABELS[status] || status
}

const PRIORITY_CYCLE = [1, 2, 3, 4, 5, null]

function cycleStatus(topic) {
  const idx = STATUS_CYCLE.indexOf(topic.status)
  topic.status = STATUS_CYCLE[(idx + 1) % STATUS_CYCLE.length]
  saveTopic(topic)
}

function cyclePriority(topic) {
  const idx = PRIORITY_CYCLE.indexOf(topic.priority)
  topic.priority = PRIORITY_CYCLE[(idx + 1) % PRIORITY_CYCLE.length]
  saveTopic(topic)
}
async function loadTopics() {
  loading.value = true
  try {
    const res = await fetch('/api/planning/topics')
    if (res.ok) {
      topics.value = await res.json()
    }
  } catch { /* use local state */ }
  loading.value = false
}

async function saveTopic(topic) {
  try {
    await fetch(`/api/planning/topics/${topic.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: topic.title,
        tag: topic.tag,
        status: topic.status,
        quadrant: topic.quadrant,
        priority: topic.priority,
        order: topic.order,
        start_date: topic.start_date || null,
        end_date: topic.end_date || null,
      }),
    })
  } catch { /* ignore */ }
}

async function createTopicOnServer(topic) {
  try {
    const res = await fetch('/api/planning/topics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: topic.title, tag: topic.tag, status: topic.status }),
    })
    if (res.ok) {
      const saved = await res.json()
      topic.id = saved.id
    }
  } catch { /* keep local id */ }
}

async function deleteTopicOnServer(id) {
  try {
    await fetch(`/api/planning/topics/${id}`, { method: 'DELETE' })
  } catch { /* ignore */ }
}

// ====== COMPUTED ======
const rankedTopics = computed(() =>
  [...topics.value].sort((a, b) => a.order - b.order)
)

const backlogTopics = computed(() =>
  topics.value.filter(t => t.quadrant === null || t.quadrant === 'backlog')
)

function matrixTopics(quadrant) {
  return topics.value.filter(t => t.quadrant === quadrant)
}

// ====== ACTIONS ======
let nextId = 1

function addTopic() {
  const title = newTitle.value.trim()
  if (!title) return
  const topic = {
    id: nextId++,
    title,
    tag: newTag.value,
    status: 'todo',
    quadrant: null,
    priority: null,
    order: topics.value.length,
  }
  topics.value.push(topic)
  createTopicOnServer(topic)
  newTitle.value = ''
}

function deleteTopic(id) {
  topics.value = topics.value.filter(t => t.id !== id)
  deleteTopicOnServer(id)
}

// ====== DRAG & DROP (Ranking) ======
function onDragStart(topic, event) {
  draggedTopic = topic
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', String(topic.id))
}

function onDragOver(topic) {
  dragOverId.value = topic.id
}

function onDrop(targetTopic) {
  if (!draggedTopic || draggedTopic.id === targetTopic.id) {
    dragOverId.value = null
    return
  }
  const sorted = rankedTopics.value
  const oldIdx = sorted.findIndex(t => t.id === draggedTopic.id)
  const newIdx = sorted.findIndex(t => t.id === targetTopic.id)
  if (oldIdx === -1 || newIdx === -1) return

  const item = sorted.splice(oldIdx, 1)[0]
  sorted.splice(newIdx, 0, item)

  // Reassign order & sync to server
  sorted.forEach((t, i) => {
    const topic = topics.value.find(t2 => t2.id === t.id)
    if (topic) {
      topic.order = i
      saveTopic(topic)
    }
  })
  dragOverId.value = null
  draggedTopic = null
}

// ====== DRAG & DROP (Matrix) ======
function onMatrixDragStart(topic, event) {
  draggedTopic = topic
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', String(topic.id))
}

function onBpDragStart(topic, event) {
  draggedTopic = topic
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', String(topic.id))
}

function moveToQuadrant(event, quadrant) {
  if (!draggedTopic) return
  const topic = topics.value.find(t => t.id === draggedTopic.id)
  if (topic) {
    topic.quadrant = quadrant
    saveTopic(topic)
  }
  draggedTopic = null
}

function moveToBacklog(topic) {
  topic.quadrant = null
  saveTopic(topic)
}

// ====== GRAPH VIEW — Zależności ======
const deps = ref([])
const connectMode = ref(false)
const connectSource = ref(null)
const hoveredDep = ref(null)
const graphRef = ref(null)

// Zoom grafu
const graphZoom = ref(1)
const ZOOM_MIN = 0.25, ZOOM_MAX = 1, ZOOM_STEP = 0.1
const graphFullscreen = ref(false)

function toggleFullscreen() {
  graphFullscreen.value = !graphFullscreen.value
}

watch(graphFullscreen, (val) => {
  if (val) {
    document.addEventListener('keydown', onFsKeydown)
  } else {
    document.removeEventListener('keydown', onFsKeydown)
  }
})
function onFsKeydown(e) {
  if (e.key === 'Escape') graphFullscreen.value = false
}

function graphZoomIn() {
  graphZoom.value = Math.min(ZOOM_MAX, +(graphZoom.value + ZOOM_STEP).toFixed(2))
}
function graphZoomOut() {
  graphZoom.value = Math.max(ZOOM_MIN, +(graphZoom.value - ZOOM_STEP).toFixed(2))
}
function graphZoomReset() {
  graphZoom.value = 1
}
function onGraphWheel(e) {
  const delta = e.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP
  graphZoom.value = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, +(graphZoom.value + delta).toFixed(2)))
}

// Pozycje węzłów na grafie
const nodePositions = ref({})
const NODE_W = 180
const NODE_H = 64
let simFrame = 0
let simTimer = null
let edgeCache = {}

// Stałe fizyki
const PHYS_REPULSION   = 8000
const PHYS_ATTRACTION  = 0.004
const PHYS_REST_LENGTH = 220
const PHYS_GRAVITY     = 0.0006
const PHYS_DAMPING     = 0.75
const PHYS_SETTLE      = 200    // ~3s at 60fps

// Inicjalizacja pozycji — zwarty klaster w środku canvasu
function initNodePositions() {
  const canvasEl = graphRef.value
  const cw = canvasEl ? canvasEl.clientWidth : 600
  const ch = canvasEl ? canvasEl.clientHeight : 400
  const cx = cw / 2, cy = ch / 2

  const spread = Math.max(20, topics.value.length * 25)
  topics.value.forEach((t, i) => {
    if (nodePositions.value[t.id] === undefined) {
      const angle = (i / topics.value.length) * Math.PI * 2
      const r = spread * (0.5 + Math.random() * 0.5)
      nodePositions.value[t.id] = {
        x: cx + Math.cos(angle) * r,
        y: cy + Math.sin(angle) * r,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
      }
    }
  })
  simFrame = 0
  startGraphSimulation()
}

// Jeden krok symulacji siłowej
function stepPhysics() {
  const pos = nodePositions.value
  const ids = topics.value.map(t => t.id)
  if (ids.length < 2) return

  const cw = graphRef.value ? graphRef.value.clientWidth : 600
  const ch = graphRef.value ? graphRef.value.clientHeight : 400
  const cx = cw / 2, cy = ch / 2

  // Zbierz siły
  const forces = {}
  for (const id of ids) forces[id] = { fx: 0, fy: 0 }

  // Repulsja: każdy z każdym
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      const a = pos[ids[i]], b = pos[ids[j]]
      if (!a || !b) continue
      let dx = a.x - b.x, dy = a.y - b.y
      const dist = Math.sqrt(dx * dx + dy * dy) || 1
      const f = PHYS_REPULSION / (dist * dist)
      const fx = f * (dx / dist), fy = f * (dy / dist)
      forces[ids[i]].fx += fx; forces[ids[i]].fy += fy
      forces[ids[j]].fx -= fx; forces[ids[j]].fy -= fy
    }
  }

  // Atrakcja wzdłuż krawędzi
  for (const dep of deps.value) {
    const a = pos[dep.from_id], b = pos[dep.to_id]
    if (!a || !b) continue
    let dx = b.x - a.x, dy = b.y - a.y
    const dist = Math.sqrt(dx * dx + dy * dy) || 1
    const stretch = dist - PHYS_REST_LENGTH
    const f = stretch * PHYS_ATTRACTION
    const fx = f * (dx / dist), fy = f * (dy / dist)
    forces[dep.from_id].fx += fx; forces[dep.from_id].fy += fy
    forces[dep.to_id].fx -= fx;   forces[dep.to_id].fy -= fy
  }

  // Grawitacja do centrum
  for (const id of ids) {
    const p = pos[id]
    if (!p) continue
    forces[id].fx += (cx - p.x) * PHYS_GRAVITY
    forces[id].fy += (cy - p.y) * PHYS_GRAVITY
  }

  // Rozwiązywanie kolizji bounding boxów — odpychanie nakładających się węzłów
  const COLL_PUSH = 0.6
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      const a = pos[ids[i]], b = pos[ids[j]]
      if (!a || !b) continue
      const ox = Math.max(0, NODE_W - Math.abs(a.x - b.x))
      const oy = Math.max(0, NODE_H - Math.abs(a.y - b.y))
      if (ox > 0 && oy > 0) {
        // Nakładają się — odpychamy w kierunku najmniejszego overlapu
        let dirX = a.x - b.x, dirY = a.y - b.y
        if (Math.abs(dirX) < 0.01 && Math.abs(dirY) < 0.01) {
          dirX = 1; dirY = 1
        }
        if (ox < oy) {
          const sign = dirX > 0 ? 1 : -1
          forces[ids[i]].fx += ox * sign * COLL_PUSH
          forces[ids[j]].fx -= ox * sign * COLL_PUSH
        } else {
          const sign = dirY > 0 ? 1 : -1
          forces[ids[i]].fy += oy * sign * COLL_PUSH
          forces[ids[j]].fy -= oy * sign * COLL_PUSH
        }
      }
    }
  }

  // Zastosuj siły
  const progress = Math.min(simFrame / PHYS_SETTLE, 1)
  const damping = PHYS_DAMPING + (0.92 - PHYS_DAMPING) * progress

  for (const id of ids) {
    const p = pos[id], f = forces[id]
    if (!p || !f) continue
    p.vx = (p.vx + f.fx) * damping
    p.vy = (p.vy + f.fy) * damping

    const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy)
    if (speed > 6) { p.vx = (p.vx / speed) * 6; p.vy = (p.vy / speed) * 6 }

    p.x += p.vx
    p.y += p.vy

    // Tylko lewa/górna krawędź — prawa/dolna są otwarte, canvas rośnie
    if (p.x < 0) { p.x = 0; p.vx *= -0.3 }
    if (p.y < 0) { p.y = 0; p.vy *= -0.3 }
  }

  simFrame++
  // Wymuś reaktywność — nowy obiekt referencyjnie
  nodePositions.value = { ...nodePositions.value }

  // Nie zatrzymujemy — symulacja biegnie cały czas,
  // a damping narasta, więc po chwili węzły są stabilne
  // (przeciągnięcie węzła restartuje damping przez startGraphSimulation)
}

function startGraphSimulation() {
  stopGraphSimulation()
  simTimer = setInterval(stepPhysics, 16) // ~60fps
}

function stopGraphSimulation() {
  if (simTimer) { clearInterval(simTimer); simTimer = null }
}

function getPos(id) {
  const p = nodePositions.value[id]
  if (!p) return null
  return {
    x: p.x, y: p.y,
    cx: p.x + NODE_W / 2,   // center x
    cy: p.y + NODE_H / 2,   // center y
    t: p.y,                  // top
    b: p.y + NODE_H,        // bottom
    l: p.x,                  // left
    r: p.x + NODE_W,        // right
  }
}

// Krzywa Beziera dla krawędzi — zwraca d dla SVG path + środek
function getEdgeCurve(fromId, toId, type) {
  const from = getPos(fromId), to = getPos(toId)
  if (!from || !to) return null

  const dx = to.cx - from.cx, dy = to.cy - from.cy
  const dist = Math.sqrt(dx * dx + dy * dy) || 1
  const curvFactor = { blocks: 0.2, tested_by: 0.25, depends_on: 0.22 }[type] || 0.2

  // Wektor prostopadły
  const px = -dy / dist, py = dx / dist
  const mx = (from.cx + to.cx) / 2, my = (from.cy + to.cy) / 2
  const offset = dist * curvFactor
  const cpx = mx + px * offset, cpy = my + py * offset

  // Punkt startowy i końcowy na krawędzi węzłów (przód/tył)
  let startX, startY, endX, endY
  if (Math.abs(dx) > Math.abs(dy)) {
    // przewaga w poziomie
    if (dx > 0) { startX = from.r; startY = from.cy; endX = to.l; endY = to.cy }
    else        { startX = from.l; startY = from.cy; endX = to.r; endY = to.cy }
  } else {
    if (dy > 0) { startX = from.cx; startY = from.b; endX = to.cx; endY = to.t }
    else        { startX = from.cx; startY = from.t; endX = to.cx; endY = to.b }
  }

  // Środek krzywej (do przycisku usuń i pulsów)
  const mid = bezierPoint(startX, startY, cpx, cpy, endX, endY, 0.5)

  return {
    d: `M${startX},${startY} Q${cpx},${cpy} ${endX},${endY}`,
    midX: mid.x, midY: mid.y,
    startX, startY, cpx, cpy, endX, endY,
    len: dist,
  }
}

function bezierPoint(ax, ay, cpx, cpy, bx, by, t) {
  const t1 = 1 - t
  return {
    x: t1 * t1 * ax + 2 * t1 * t * cpx + t * t * bx,
    y: t1 * t1 * ay + 2 * t1 * t * cpy + t * t * by,
  }
}

// Punkt wzdłuż krzywej dla danego parametru t (0-1)
function getPointOnCurve(curve, t) {
  if (!curve) return null
  return bezierPoint(curve.startX, curve.startY, curve.cpx, curve.cpy, curve.endX, curve.endY, t)
}

// Pulsowe kropki na krawędziach
const pulseDots = ref({}) // { depId: progress }

function initPulses() {
  const p = {}
  for (const dep of deps.value) {
    p[dep.id] = Math.random()
  }
  pulseDots.value = p
}

let pulseTimer = null

function startPulseAnimation() {
  stopPulseAnimation()
  pulseTimer = setInterval(() => {
    const p = { ...pulseDots.value }
    for (const id of Object.keys(p)) {
      p[id] = (p[id] || 0) + 0.008
      if (p[id] > 1) p[id] = 0
    }
    pulseDots.value = p
  }, 30)
}

function stopPulseAnimation() {
  if (pulseTimer) { clearInterval(pulseTimer); pulseTimer = null }
}

const canvasSize = computed(() => {
  const keys = Object.keys(nodePositions.value)
  if (keys.length === 0) return { w: 800, h: 400 }
  let maxX = 0, maxY = 0
  for (const id of keys) {
    const p = nodePositions.value[id]
    if (p.x + NODE_W > maxX) maxX = p.x + NODE_W
    if (p.y + NODE_H > maxY) maxY = p.y + NODE_H
  }
  return { w: Math.max(800, maxX + 80), h: Math.max(400, maxY + 80) }
})

// Obserwuj zmiany topics → restartuj symulację
watch(() => topics.value.length, () => {
  if (viewMode.value === 'graph') {
    initNodePositions()
    initPulses()
    startPulseAnimation()
  }
})

// Obserwuj widok — start/stop symulacji i pulsów
watch(viewMode, (mode) => {
  if (mode === 'graph') {
    initNodePositions()
    initPulses()
    startPulseAnimation()
  } else {
    stopGraphSimulation()
    stopPulseAnimation()
  }
})

// Obserwuj zmiany w depso — restartuj pulse
watch(deps, () => {
  if (viewMode.value === 'graph') {
    initPulses()
    simFrame = 0
    startGraphSimulation()
  }
}, { deep: true })

// ====== API — zależności ======
async function loadDeps() {
  try {
    const res = await fetch('/api/planning/dependencies')
    if (res.ok) deps.value = await res.json()
  } catch { /* ignore */ }
}

async function createDepOnServer(fromId, toId, type) {
  try {
    const res = await fetch('/api/planning/dependencies', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ from_id: fromId, to_id: toId, type }),
    })
    if (res.ok) {
      const saved = await res.json()
      deps.value.push(saved)
    }
  } catch { /* ignore */ }
}

async function deleteDepOnServer(depId) {
  try {
    await fetch(`/api/planning/dependencies/${depId}`, { method: 'DELETE' })
  } catch { /* ignore */ }
}

// ====== INTERAKCJA GRAFU ======

// Przesuwanie tła (pan)
const isPanning = ref(false)
let panStartX = 0, panStartY = 0
let panScrollX = 0, panScrollY = 0

function onCanvasPanStart(e) {
  if (connectMode.value) return
  isPanning.value = true
  panStartX = e.clientX
  panStartY = e.clientY
  panScrollX = graphRef.value.scrollLeft
  panScrollY = graphRef.value.scrollTop
  graphRef.value.style.cursor = 'grabbing'
}

function onCanvasPanMove(e) {
  if (!isPanning.value) return
  const dx = e.clientX - panStartX
  const dy = e.clientY - panStartY
  graphRef.value.scrollLeft = panScrollX - dx
  graphRef.value.scrollTop = panScrollY - dy
}

function onCanvasPanEnd() {
  if (!isPanning.value) return
  isPanning.value = false
  if (graphRef.value) graphRef.value.style.cursor = ''
}

function toggleConnectMode() {
  connectMode.value = !connectMode.value
  if (!connectMode.value) connectSource.value = null
}

function onCanvasClick() {
  // Kliknięcie w tło canvasu w trybie łączenia — czyści zaznaczenie źródła
  if (connectMode.value) connectSource.value = null
}

function onNodeClick(t) {
  if (!connectMode.value) return
  if (!connectSource.value) {
    connectSource.value = t
  } else if (connectSource.value.id !== t.id) {
    createDepOnServer(connectSource.value.id, t.id, 'blocks')
    connectSource.value = null
    // Tryb pozostaje aktywny — można dalej łączyć
  } else {
    connectSource.value = null
  }
}

// Przeciąganie węzłów
const dragState = ref(null)

function onNodeMouseDown(t, event) {
  if (connectMode.value) return
  const pos = nodePositions.value[t.id]
  if (!pos) return
  dragState.value = {
    id: t.id,
    startX: event.clientX,
    startY: event.clientY,
    origX: pos.x,
    origY: pos.y,
  }
}

function onCanvasMouseMove(event) {
  if (isPanning.value) {
    onCanvasPanMove(event)
    return
  }
  if (!dragState.value) return
  const dx = event.clientX - dragState.value.startX
  const dy = event.clientY - dragState.value.startY
  const existing = nodePositions.value[dragState.value.id] || {}
  nodePositions.value[dragState.value.id] = {
    ...existing,
    x: Math.max(0, dragState.value.origX + dx),
    y: Math.max(0, dragState.value.origY + dy),
  }
}

function onCanvasMouseUp() {
  if (isPanning.value) {
    onCanvasPanEnd()
    return
  }
  if (dragState.value) {
    // Restart symulacji po przeciągnięciu — damping odświeżony, węzły reagują dynamicznie
    simFrame = 0
    startGraphSimulation()
  }
  dragState.value = null
}

// Cykl typu zależności: blocks → tested_by → depends_on → blocks
const DEP_TYPE_CYCLE = ['blocks', 'tested_by', 'depends_on']

function cycleDepType(dep) {
  const idx = DEP_TYPE_CYCLE.indexOf(dep.type)
  dep.type = DEP_TYPE_CYCLE[(idx + 1) % DEP_TYPE_CYCLE.length]
  // Wyślij aktualizację — dla POC delete+create
  deleteDepOnServer(dep.id)
  createDepOnServer(dep.from_id, dep.to_id, dep.type)
  deps.value = deps.value.filter(d => d.id !== dep.id)
}

function deleteDep(depId) {
  deps.value = deps.value.filter(d => d.id !== depId)
  deleteDepOnServer(depId)
  hoveredDep.value = null
}

// Nadpisany onMounted — ładuj tematy i zależności
onMounted(() => {
  loadTopics()
  loadDeps()
})

// Cleanup przy unmount — zatrzymaj symulację, pulsy i listener fullscreena
onUnmounted(() => {
  stopGraphSimulation()
  stopPulseAnimation()
  document.removeEventListener('keydown', onFsKeydown)
})

// ====== ROADMAP / HARMONOGRAM ======
const rmRef = ref(null)
const rmScrollRef = ref(null)
const rmColW = ref(100)
const rmLaneH = 48
const rmShowArrowsFor = ref(null)
let rmDragState = null
let rmResizeState = null

const DAY_MS = 86400000

// Dziś na północ od strefy czasowej
function rmTodayDate() {
  const d = new Date()
  return new Date(d.getFullYear(), d.getMonth(), d.getDate())
}

function rmMonday(date) {
  const d = new Date(date)
  const day = d.getDay()
  const diff = d.getDate() - day + (day === 0 ? -6 : 1)
  d.setDate(diff)
  d.setHours(0, 0, 0, 0)
  return d
}

function rmAddDays(date, days) {
  const d = new Date(date)
  d.setDate(d.getDate() + days)
  return d
}

function rmFormatISO(d) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function rmDaysBetween(a, b) {
  return Math.round((b - a) / DAY_MS)
}

// Zakres tygodni widoczny na osi
const rmTimelineStart = ref(null) // Date — Monday of first week
const RM_NUM_WEEKS = ref(16)

function rmInitTimeline() {
  if (!rmTimelineStart.value) {
    const today = rmTodayDate()
    rmTimelineStart.value = rmAddDays(rmMonday(today), -28) // 4 weeks back
  }
}

const rmWeeks = computed(() => {
  rmInitTimeline()
  const weeks = []
  let cursor = new Date(rmTimelineStart.value)
  for (let i = 0; i < RM_NUM_WEEKS.value; i++) {
    const monthNames = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze', 'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru']
    const mon = monthNames[cursor.getMonth()]
    const day = cursor.getDate()
    const year = cursor.getFullYear()
    weeks.push({
      label: `${day} ${mon}`,
      month: (i === 0 || cursor.getMonth() !== rmAddDays(cursor, -7).getMonth()) ? mon + (year !== rmTodayDate().getFullYear() ? ` ${year}` : '') : '',
      date: new Date(cursor),
    })
    cursor = rmAddDays(cursor, 7)
  }
  return weeks
})

const rmTotalWidth = computed(() => rmWeeks.value.length * rmColW.value)

const rmTodayOffset = computed(() => {
  if (!rmTimelineStart.value) return 0
  const days = rmDaysBetween(rmTimelineStart.value, rmTodayDate())
  return Math.max(0, days * (rmColW.value / 7))
})

function rmIsCurrentWeek(w) {
  const today = rmTodayDate()
  const weekStart = w.date
  const weekEnd = rmAddDays(weekStart, 7)
  return today >= weekStart && today < weekEnd
}

// Podziel tematy na zaplanowane i nie
const rmScheduledTopics = computed(() =>
  topics.value.filter(t => t.start_date)
)

const rmUnscheduledTopics = computed(() =>
  topics.value.filter(t => !t.start_date)
)

const rmScaleLabel = computed(() => {
  if (rmColW.value <= 60) return 'Miesiąc'
  if (rmColW.value <= 90) return '2 tygodnie'
  return 'Tydzień'
})

function rmZoomIn() {
  rmColW.value = Math.min(rmColW.value + 20, 200)
}
function rmZoomOut() {
  rmColW.value = Math.max(rmColW.value - 20, 40)
}
function rmToday() {
  if (rmScrollRef.value) {
    rmScrollRef.value.scrollLeft = 0
  }
}

// Oblicz pozycję i szerokość paska
function rmGetBar(t) {
  if (!t.start_date) return null
  const start = new Date(t.start_date + 'T00:00:00')
  const end = t.end_date ? new Date(t.end_date + 'T00:00:00') : new Date(start)
  if (!rmTimelineStart.value) return null
  const daysFromStart = rmDaysBetween(rmTimelineStart.value, start)
  const duration = Math.max(1, rmDaysBetween(start, end) + 1)
  const pxPerDay = rmColW.value / 7
  return {
    left: Math.round(daysFromStart * pxPerDay) + 'px',
    width: Math.round(duration * pxPerDay) + 'px',
  }
}

// Przeciąganie paska (zmiana dat rozpoczęcia+zakończenia razem)
function rmBarMouseDown(t, e) {
  if (!t.start_date) return
  const start = new Date(t.start_date + 'T00:00:00')
  const end = t.end_date ? new Date(t.end_date + 'T00:00:00') : new Date(start)
  const duration = rmDaysBetween(start, end)
  rmDragState = {
    topic: t,
    startDate: new Date(start),
    duration,
    mouseStartX: e.clientX,
    pxPerDay: rmColW.value / 7,
  }
  document.addEventListener('mousemove', rmBarMouseMove)
  document.addEventListener('mouseup', rmBarMouseUp)
}

function rmBarMouseMove(e) {
  if (!rmDragState) return
  const dx = e.clientX - rmDragState.mouseStartX
  const dayShift = Math.round(dx / rmDragState.pxPerDay)
  const newStart = rmAddDays(rmDragState.startDate, dayShift)
  const t = rmDragState.topic
  t.start_date = rmFormatISO(newStart)
  if (rmDragState.duration > 0) {
    const newEnd = rmAddDays(newStart, rmDragState.duration)
    t.end_date = rmFormatISO(newEnd)
  } else {
    t.end_date = null
  }
}

function rmBarMouseUp() {
  if (rmDragState) {
    saveTopic(rmDragState.topic)
  }
  rmDragState = null
  document.removeEventListener('mousemove', rmBarMouseMove)
  document.removeEventListener('mouseup', rmBarMouseUp)
}

// Przeciąganie prawego uchwytu (zmiana tylko end_date)
function rmHandleMouseDown(t, e) {
  if (!t.end_date) {
    t.end_date = t.start_date
  }
  const end = new Date(t.end_date + 'T00:00:00')
  rmResizeState = {
    topic: t,
    origEnd: end,
    mouseStartX: e.clientX,
    pxPerDay: rmColW.value / 7,
  }
  document.addEventListener('mousemove', rmHandleMouseMove)
  document.addEventListener('mouseup', rmHandleMouseUp)
}

function rmHandleMouseMove(e) {
  if (!rmResizeState) return
  const dx = e.clientX - rmResizeState.mouseStartX
  const dayShift = Math.round(dx / rmResizeState.pxPerDay)
  const newEnd = rmAddDays(rmResizeState.origEnd, dayShift)
  const t = rmResizeState.topic
  const start = new Date(t.start_date + 'T00:00:00')
  if (newEnd >= start) {
    t.end_date = rmFormatISO(newEnd)
  }
}

function rmHandleMouseUp() {
  if (rmResizeState) {
    saveTopic(rmResizeState.topic)
  }
  rmResizeState = null
  document.removeEventListener('mousemove', rmHandleMouseMove)
  document.removeEventListener('mouseup', rmHandleMouseUp)
}

// Cofnij do niezaplanowanych
function rmUnschedule(t) {
  t.start_date = null
  t.end_date = null
  saveTopic(t)
}

// Drag z niezaplanowanych na oś czasu
function rmUnschedDragStart(t, e) {
  e.dataTransfer.setData('text/plain', String(t.id))
  e.dataTransfer.effectAllowed = 'move'
}

// Drop na osi czasu — oblicza datę z pozycji myszy
function rmTimelineDrop(e) {
  const id = parseInt(e.dataTransfer.getData('text/plain'))
  if (isNaN(id)) return
  const topic = topics.value.find(t => t.id === id)
  if (!topic || !rmScrollRef.value || !rmTimelineStart.value) return

  const rect = rmScrollRef.value.getBoundingClientRect()
  const scrollLeft = rmScrollRef.value.scrollLeft
  const x = e.clientX - rect.left + scrollLeft
  const pxPerDay = rmColW.value / 7
  const daysFromStart = Math.max(0, Math.round(x / pxPerDay))
  const dropDate = rmAddDays(rmTimelineStart.value, daysFromStart)

  // Ustaw na poniedziałek tygodnia, w który upuszczono
  const scheduledDate = rmMonday(dropDate)
  topic.start_date = rmFormatISO(scheduledDate)
  topic.end_date = rmFormatISO(rmAddDays(scheduledDate, 13)) // domyślnie 2 tygodnie
  saveTopic(topic)
}

// ====== JIRA RELATIONS PANEL ======
const showJiraLinks = ref(false)

const jiraRelationships = computed(() => {
  // Mapa topic.id → numer sekwencyjny (ZADANIE-1, ZADANIE-2, …)
  const topicNum = {}
  topics.value.forEach((t, i) => { topicNum[t.id] = i + 1 })

  const colorMap = {
    blocks: '#ff5252',
    tested_by: '#536dfe',
    depends_on: '#ffb300',
  }
  const labelMap = {
    blocks: 'blokuje',
    tested_by: 'testowane przez',
    depends_on: 'zależy od',
  }

  return deps.value.map(dep => {
    const from = topics.value.find(t => t.id === dep.from_id)
    const to = topics.value.find(t => t.id === dep.to_id)
    if (!from || !to) return null
    const color = colorMap[dep.type] || '#888'
    return {
      from: `ZADANIE-${topicNum[from.id]} [${from.title}]`,
      to: `ZADANIE-${topicNum[to.id]} [${to.title}]`,
      label: labelMap[dep.type] || dep.type,
      color,
    }
  }).filter(Boolean)
})

function copyJiraLinks() {
  const text = jiraRelationships.value
    .map(r => `${r.from} — ${r.label} → ${r.to}`)
    .join('\n')
  if (!text) return
  navigator.clipboard.writeText(text).catch(() => {
    // fallback
    const ta = document.createElement('textarea')
    ta.value = text
    ta.style.position = 'fixed'
    ta.style.left = '-9999px'
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
  })
}

// ====== ŚCIEŻKA KRYTYCZNA ======
const criticalTopics = computed(() => {
  const depsList = deps.value.filter(d => d.type === 'blocks')
  // Forward pass: oblicz najwcześniejszy możliwy koniec
  const earliestEnd = {}
  const latestStart = {}
  const topicMap = {}
  topics.value.forEach(t => { topicMap[t.id] = t })

  // Buduj graf
  const successors = {} // topicId → [topicId]
  const predecessors = {} // topicId → [topicId]
  depsList.forEach(d => {
    if (!successors[d.from_id]) successors[d.from_id] = []
    successors[d.from_id].push(d.to_id)
    if (!predecessors[d.to_id]) predecessors[d.to_id] = []
    predecessors[d.to_id].push(d.from_id)
  })

  // Forward pass: znajdź tematy bez poprzedników (startowe)
  const scheduled = topics.value.filter(t => t.start_date)
  scheduled.forEach(t => {
    if (t.start_date && t.end_date) {
      const start = new Date(t.start_date + 'T00:00:00')
      const end = new Date(t.end_date + 'T00:00:00')
      earliestEnd[t.id] = { date: end, duration: rmDaysBetween(start, end) + 1 }
    }
  })

  // Dla tematów zależnych: EE[następca] = max(EE[poprzedników]) + duration następcy
  // Topo sort dla scheduled topics
  const visited = new Set()
  const order = []
  function topoVisit(id) {
    if (visited.has(id)) return
    visited.add(id)
    ;(successors[id] || []).forEach(sid => topoVisit(sid))
    order.push(id)
  }
  scheduled.forEach(t => topoVisit(t.id))

  // Forward
  order.forEach(id => {
    const t = topicMap[id]
    if (!t || !t.start_date) return
    const start = new Date(t.start_date + 'T00:00:00')
    const end = t.end_date ? new Date(t.end_date + 'T00:00:00') : new Date(start)
    const dur = rmDaysBetween(start, end) + 1
    const preds = predecessors[id] || []
    let maxPredEnd = 0
    preds.forEach(pid => {
      if (earliestEnd[pid] && earliestEnd[pid].date) {
        const diff = rmDaysBetween(rmTimelineStart.value || start, earliestEnd[pid].date)
        if (diff > maxPredEnd) maxPredEnd = diff
      }
    })
    if (!earliestEnd[id]) {
      earliestEnd[id] = { date: end, duration: dur }
    }
  })

  // Backward pass
  const projectEnd = scheduled.reduce((max, t) => {
    if (earliestEnd[t.id]) {
      const ts = earliestEnd[t.id].date.getTime()
      return ts > max ? ts : max
    }
    return max
  }, 0)

  scheduled.forEach(t => {
    if (t.start_date) {
      const start = new Date(t.start_date + 'T00:00:00')
      const end = t.end_date ? new Date(t.end_date + 'T00:00:00') : new Date(start)
      const dur = rmDaysBetween(start, end) + 1
      const succs = successors[t.id] || []
      let minSuccStart = projectEnd
      succs.forEach(sid => {
        const st = topicMap[sid]
        if (st && st.start_date) {
          const ss = new Date(st.start_date + 'T00:00:00')
          const sst = ss.getTime()
          if (sst < minSuccStart) minSuccStart = sst
        }
      })
      const latestEnd = new Date(minSuccStart - DAY_MS)
      const latestStartDate = rmAddDays(latestEnd, -(dur - 1))
      latestStart[t.id] = latestStartDate
    }
  })

  // Krytyczne: earliestEnd ≈ actual end
  const critical = []
  scheduled.forEach(t => {
    if (!t.start_date) return
    const actualEnd = t.end_date ? new Date(t.end_date + 'T00:00:00') : new Date(t.start_date + 'T00:00:00')
    const ee = earliestEnd[t.id]
    if (ee && Math.abs(rmDaysBetween(actualEnd, ee.date)) <= 2) {
      critical.push(t.id)
    }
  })
  return critical
})

function isCritical(t) {
  return criticalTopics.value.includes(t.id)
}

onMounted(() => {
  loadTopics()
  loadDeps()
})
</script>

<style scoped>
.hub-view {
  width: 100%;
  max-width: var(--content-width, 1200px);
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* ====== HEADER ====== */
.planning-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 24px;
}

.header-left {
  flex: 1;
}

.header-right {
  flex-shrink: 0;
}

.view-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-hover);
  border-radius: 10px;
  padding: 3px;
}

.view-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
}

.view-tab:hover {
  color: var(--text-primary);
}

.view-tab.active {
  background: var(--bg-card);
  color: var(--accent-primary);
  box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}

/* ====== QUICK-ADD ====== */
.add-bar {
  margin-bottom: 16px;
}

.add-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 4px 4px 4px 16px;
  transition: border-color 0.2s;
}

.add-input-wrapper:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.08);
}

.add-icon {
  color: var(--text-muted);
  flex-shrink: 0;
}

.add-input {
  flex: 1;
  padding: 10px 0;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 15px;
  font-family: inherit;
  outline: none;
}

.add-input::placeholder {
  color: var(--text-muted);
}

.tag-select {
  padding: 6px 10px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-hover);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s;
}

.tag-select:hover {
  border-color: var(--accent-primary);
}

.add-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  background: var(--accent-gradient);
  color: #000;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.add-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 200, 83, 0.25);
}

.add-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

/* ====== STATS BAR ====== */
.stats-bar {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: var(--bg-hover);
  border-radius: 10px;
}

.stat-item {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-num {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

/* ====== RANKING VIEW ====== */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rank-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  cursor: grab;
  transition: border-color 0.15s, background 0.15s, transform 0.15s;
  user-select: none;
}

.rank-card:hover {
  border-color: rgba(0, 200, 83, 0.2);
  background: var(--bg-hover);
}

.rank-card:active {
  cursor: grabbing;
}

.rank-card.drag-over {
  border-color: var(--accent-primary);
  background: rgba(0, 200, 83, 0.06);
  transform: scale(1.01);
}

.rank-number {
  width: 24px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-muted);
  text-align: center;
  flex-shrink: 0;
}

.drag-handle {
  display: flex;
  color: var(--text-muted);
  flex-shrink: 0;
  opacity: 0.4;
}

.rank-card:hover .drag-handle {
  opacity: 0.8;
}

.rank-title {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.text-done {
  text-decoration: line-through;
  opacity: 0.5;
}

/* Status badge */
.status-badge {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  padding: 3px 10px;
  border-radius: 100px;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-badge.sm {
  font-size: 9px;
  padding: 2px 8px;
}

.status-todo {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-muted);
}
.status-todo:hover {
  background: rgba(255, 255, 255, 0.1);
}

.status-in-progress {
  background: rgba(83, 109, 254, 0.12);
  color: #536dfe;
}
.status-in-progress:hover {
  background: rgba(83, 109, 254, 0.2);
}

.status-ongoing {
  background: rgba(255, 179, 0, 0.12);
  color: #ffb300;
}
.status-ongoing:hover {
  background: rgba(255, 179, 0, 0.2);
}

.status-done {
  background: rgba(0, 200, 83, 0.12);
  color: #00c853;
}
.status-done:hover {
  background: rgba(0, 200, 83, 0.2);
}

/* Rank card states */
.rank-card.status-done-card {
  opacity: 0.6;
}

/* Matrix card done state */
.matrix-card .text-done,
.backlog-card .text-done {
  text-decoration: line-through;
  opacity: 0.5;
}

.prio-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 24px;
  border: none;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 800;
  font-family: inherit;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s;
}
.prio-badge:hover {
  transform: scale(1.1);
}

.prio-none {
  background: rgba(255,255,255,0.04);
  color: var(--text-muted);
}
.prio-1 {
  background: rgba(255, 23, 68, 0.2);
  color: #ff1744;
  box-shadow: 0 0 0 1px rgba(255, 23, 68, 0.2);
}
.prio-2 {
  background: rgba(255, 145, 0, 0.2);
  color: #ff9100;
  box-shadow: 0 0 0 1px rgba(255, 145, 0, 0.2);
}
.prio-3 {
  background: rgba(255, 179, 0, 0.2);
  color: #ffb300;
  box-shadow: 0 0 0 1px rgba(255, 179, 0, 0.2);
}
.prio-4 {
  background: rgba(0, 200, 83, 0.2);
  color: #00c853;
  box-shadow: 0 0 0 1px rgba(0, 200, 83, 0.2);
}
.prio-5 {
  background: rgba(83, 109, 254, 0.2);
  color: #536dfe;
  box-shadow: 0 0 0 1px rgba(83, 109, 254, 0.2);
}

.rank-tag {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 3px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}

.tag-cross {
  background: rgba(83, 109, 254, 0.12);
  color: #536dfe;
}
.tag-EMIR_3 {
  background: rgba(0, 200, 83, 0.12);
  color: #00c853;
}
.tag-SFTR {
  background: rgba(0, 229, 255, 0.12);
  color: #00e5ff;
}
.tag-WITIP {
  background: rgba(255, 145, 0, 0.12);
  color: #ff9100;
}
.tag-ARM {
  background: rgba(255, 82, 82, 0.12);
  color: #ff5252;
}

.rank-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all 0.15s;
  flex-shrink: 0;
}

.rank-card:hover .rank-delete {
  opacity: 0.6;
}

.rank-delete:hover {
  opacity: 1 !important;
  background: rgba(255, 82, 82, 0.12);
  color: #ff5252;
}

.empty-state {
  padding: 48px 24px;
  text-align: center;
  color: var(--text-muted);
  font-size: 14px;
}

.empty-state.small {
  padding: 24px;
}

/* ====== MATRIX VIEW ====== */
.matrix-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.matrix-cell {
  min-height: 200px;
  padding: 16px;
  border-radius: 12px;
  border: 1px dashed var(--border-color);
  background: var(--bg-hover);
  transition: background 0.2s, border-color 0.2s;
}

.matrix-cell.drag-over {
  border-color: var(--accent-primary);
  background: rgba(0, 200, 83, 0.04);
}

.quadrant-qw {
  border-color: rgba(0, 200, 83, 0.2);
  background: rgba(0, 200, 83, 0.03);
}
.quadrant-sb {
  border-color: rgba(83, 109, 254, 0.2);
  background: rgba(83, 109, 254, 0.03);
}
.quadrant-fi {
  border-color: rgba(255, 145, 0, 0.2);
  background: rgba(255, 145, 0, 0.03);
}
.quadrant-mp {
  border-color: rgba(255, 82, 82, 0.2);
  background: rgba(255, 82, 82, 0.03);
}

.quadrant-label {
  margin-bottom: 12px;
}

.quadrant-title {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.quadrant-sub {
  display: block;
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 2px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.quadrant-empty {
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
  padding: 24px 0;
  opacity: 0.5;
}

.matrix-card {
  padding: 10px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 6px;
  cursor: grab;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: border-color 0.15s, transform 0.15s;
}

.matrix-card:hover {
  border-color: rgba(0, 200, 83, 0.2);
  transform: translateY(-1px);
}

.matrix-card:active {
  cursor: grabbing;
}

.card-unassign {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all 0.15s;
  flex-shrink: 0;
}

.matrix-card:hover .card-unassign {
  opacity: 0.5;
}

.card-unassign:hover {
  opacity: 1 !important;
  background: rgba(255, 82, 82, 0.1);
  color: #ff5252;
}

.matrix-card-title {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

/* ====== BACKLOG SIDEBAR ====== */
.bp {
  width: 280px;
  flex-shrink: 0;
  border-right: 1px solid var(--border-color);
  background: var(--bg-hover);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.2s;
}

.bp-collapsed {
  width: 48px;
}

.bp-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 14px 12px;
  border-bottom: 1px solid var(--border-color);
  flex-shrink: 0;
}

.bp-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
}

.bp-count {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--bg-card);
  padding: 2px 7px;
  border-radius: 100px;
  flex-shrink: 0;
}

.bp-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  flex-shrink: 0;
}
.bp-toggle:hover {
  background: var(--bg-card);
  color: var(--text-primary);
}

.bp-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.bp-add {
  padding: 8px 12px;
  flex-shrink: 0;
}

.bp-input {
  width: 100%;
  padding: 7px 10px;
  border: 1px solid var(--border-color);
  border-radius: 7px;
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: 12px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.bp-input:focus {
  border-color: var(--accent-primary);
}
.bp-input::placeholder {
  color: var(--text-muted);
}

.bp-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px 12px;
}

.bp-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 6px;
  border-radius: 6px;
  transition: background 0.1s;
  cursor: default;
}
.bp-item:hover {
  background: var(--bg-card);
}
.bp-item-done {
  opacity: 0.5;
}

.bp-item-title {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.bp-item-tag {
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 1px 5px;
  border-radius: 3px;
  flex-shrink: 0;
  opacity: 0.8;
}

.bp-status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s;
}
.bp-status.status-in-progress { color: #536dfe; }
.bp-status.status-ongoing { color: #ffb300; }
.bp-status.status-done { color: #00c853; }
.bp-status:hover {
  background: rgba(255,255,255,0.06);
}

.bp-del {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all 0.15s;
  flex-shrink: 0;
}
.bp-item:hover .bp-del {
  opacity: 0.4;
}
.bp-del:hover {
  opacity: 1 !important;
  background: rgba(255, 82, 82, 0.12);
  color: #ff5252;
}

.bp-empty {
  padding: 24px 8px;
  text-align: center;
  color: var(--text-muted);
  font-size: 12px;
}

/* ====== HUB MAIN LAYOUT ====== */
.hub-layout {
  display: flex;
  flex: 1;
  min-height: 0;
  gap: 0;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.hub-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 16px 20px;
}

/* ====== GRAPH VIEW ====== */
.graph-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.graph-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}

.graph-btn:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
}

.graph-btn-active {
  background: rgba(0, 200, 83, 0.08);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.connect-hint {
  font-size: 13px;
  color: var(--text-muted);
}

.connect-hint strong {
  color: var(--text-primary);
}

.graph-legend {
  display: flex;
  gap: 16px;
  margin-left: auto;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.legend-swatch {
  width: 16px;
  height: 3px;
  border-radius: 2px;
  flex-shrink: 0;
}

.swatch-blocks {
  background: #ff5252;
}

.swatch-tested_by {
  background: #536dfe;
}

.swatch-depends_on {
  background: #ffb300;
}

.graph-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* Fullscreen */
.graph-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  position: relative;
}
.graph-fullscreen {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: var(--bg-primary);
  padding: 16px;
}
.graph-fs-close {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 210;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.graph-fs-close:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
}

/* Zoom bar */
.graph-zoom-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  flex-shrink: 0;
}
.graph-zoom-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 26px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
  font-family: inherit;
  transition: all 0.15s;
}
.graph-zoom-btn:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
}
.graph-zoom-fit {
  width: auto;
  padding: 0 8px;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.graph-zoom-label {
  font-size: 11px;
  color: var(--text-muted);
  min-width: 38px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}

.graph-layer {
  position: relative;
  min-width: 100%;
  min-height: 100%;
  transform-origin: center top;
}

.graph-canvas {
  position: relative;
  flex: 1;
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  min-height: 450px;
  overflow: auto;
  cursor: grab;
}
.graph-canvas-panning {
  cursor: grabbing;
  user-select: none;
}

.graph-svg {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}

.graph-svg line,
.graph-svg g {
  pointer-events: auto;
}

.dep-line {
  stroke-linecap: round;
  stroke-dasharray: 6 4;
  transition: stroke-width 0.15s, opacity 0.15s;
  cursor: pointer;
  animation: drawLine 0.4s ease-out forwards;
}

@keyframes drawLine {
  from {
    stroke-dashoffset: 500;
  }
  to {
    stroke-dashoffset: 0;
  }
}

.dep-line-blocks {
  stroke: #ff5252;
}

.dep-line-tested_by {
  stroke: #536dfe;
}

.dep-line-depends_on {
  stroke: #ffb300;
}

.dep-line-hover {
  stroke-dasharray: none;
  filter: drop-shadow(0 0 6px currentColor);
}

.dep-delete-group {
  cursor: pointer;
  animation: fadeIn 0.15s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.7); }
  to { opacity: 1; transform: scale(1); }
}

.graph-node {
  position: absolute;
  width: 180px;
  padding: 10px 12px;
  background: var(--bg-card);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  cursor: grab;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.15s, border-color 0.2s;
  user-select: none;
  z-index: 2;
  /* Multi-layer glow */
  box-shadow:
    0 0 0 1px rgba(0, 200, 83, 0.03),
    0 0 12px rgba(0, 200, 83, 0.04),
    0 0 30px rgba(0, 200, 83, 0.02);
}

.graph-node:hover {
  border-color: rgba(0, 200, 83, 0.3);
  box-shadow:
    0 0 0 1px rgba(0, 200, 83, 0.06),
    0 0 16px rgba(0, 200, 83, 0.08),
    0 0 40px rgba(0, 200, 83, 0.04),
    0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.graph-node:active {
  cursor: grabbing;
  transform: scale(0.97);
}

/* ====== Pulse dots na krawędziach ====== */
.pulse-dot {
  pointer-events: none;
  filter: blur(0.5px);
  animation: pulseDot 1.5s ease-in-out infinite;
}
.pulse-blocks    { fill: rgba(255, 82, 82, 0.7); }
.pulse-tested_by { fill: rgba(83, 109, 254, 0.7); }
.pulse-depends_on { fill: rgba(255, 179, 0, 0.7); }

@keyframes pulseDot {
  0%, 100% { opacity: 0.5; r: 3; }
  50%      { opacity: 1;   r: 5; }
}

.graph-node-done {
  opacity: 0.6;
}

/* Connect mode — source node pulsing */
.graph-node-source {
  border-color: var(--accent-primary) !important;
  box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.2), 0 0 20px rgba(0, 200, 83, 0.1);
  animation: nodePulse 1.5s ease-in-out infinite;
}

@keyframes nodePulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(0, 200, 83, 0.2), 0 0 20px rgba(0, 200, 83, 0.1); }
  50% { box-shadow: 0 0 0 6px rgba(0, 200, 83, 0.15), 0 0 30px rgba(0, 200, 83, 0.05); }
}

/* Connect mode — available targets glow */
.graph-node-target {
  cursor: pointer !important;
  border-color: rgba(0, 200, 83, 0.3);
  animation: targetGlow 2s ease-in-out infinite;
}

@keyframes targetGlow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0, 200, 83, 0.1); }
  50% { box-shadow: 0 0 0 4px rgba(0, 200, 83, 0.15); }
}

.graph-node-title {
  display: block;
  width: 100%;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.graph-node-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
}

.graph-empty {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 14px;
}

/* ====== JIRA RELATIONS PANEL ====== */
.jira-panel {
  margin-top: 12px;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background: var(--bg-card);
  overflow: hidden;
  flex-shrink: 0;
}

.jira-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 10px 14px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.15s;
}
.jira-toggle:hover {
  background: var(--bg-hover);
}

.jira-toggle-label {
  flex: 1;
  text-align: left;
}

.jira-badge {
  font-size: 10px;
  font-weight: 700;
  background: var(--accent-primary);
  color: #000;
  padding: 1px 7px;
  border-radius: 100px;
}

.jira-toggle-hint {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 400;
}

.jira-body {
  border-top: 1px solid var(--border-color);
  padding: 10px 14px 14px;
}

.jira-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.jira-info {
  font-size: 11px;
  color: var(--text-muted);
}

.jira-copy-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-hover);
  color: var(--text-secondary);
  font-size: 11px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
}
.jira-copy-btn:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.jira-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.jira-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 8px;
  border-radius: 6px;
  background: var(--bg-hover);
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  transition: background 0.15s;
}
.jira-row:hover {
  background: rgba(0, 200, 83, 0.04);
}

.jira-from {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.jira-arrow {
  flex-shrink: 0;
  display: flex;
  opacity: 0.6;
}

.jira-label {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 7px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}

.jira-to {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

/* ====== ROADMAP / HARMONOGRAM ====== */
.roadmap-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.rm-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  flex-shrink: 0;
}

.rm-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  border-radius: 7px;
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
}
.rm-btn:hover {
  border-color: var(--accent-primary);
  color: var(--text-primary);
}

.rm-scale-label {
  font-size: 11px;
  color: var(--text-muted);
  min-width: 70px;
}

.rm-badge {
  margin-left: auto;
  font-size: 11px;
  color: #ff5252;
  background: rgba(255, 82, 82, 0.1);
  padding: 4px 12px;
  border-radius: 100px;
  font-weight: 600;
}

.rm-container {
  display: flex;
  flex: 1;
  min-height: 0;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  background: var(--bg-card);
}

.rm-lanes {
  flex-shrink: 0;
  width: 200px;
  border-right: 1px solid var(--border-color);
  background: var(--bg-hover);
  overflow: hidden;
}

.rm-lane-header {
  height: 48px;
  display: flex;
  align-items: center;
  padding: 0 8px 0 14px;
  border-bottom: 1px solid var(--border-color);
}

.rm-lane-title {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 4px;
  overflow: hidden;
}

.rm-lane-name {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rm-critical {
  color: #ff5252 !important;
}

.rm-unschedule-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all 0.15s;
  flex-shrink: 0;
}
.rm-lane-header:hover .rm-unschedule-btn {
  opacity: 0.4;
}
.rm-unschedule-btn:hover {
  opacity: 1 !important;
  background: rgba(255, 82, 82, 0.1);
  color: #ff5252;
}

.rm-timeline-scroll {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  min-width: 0;
}

.rm-timeline {
  position: relative;
  min-height: 100%;
}

.rm-headers {
  display: flex;
  position: sticky;
  top: 0;
  z-index: 5;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
}

.rm-week-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 6px 8px;
  border-right: 1px solid var(--border-color);
  flex-shrink: 0;
  min-height: 42px;
}

.rm-week-today {
  background: rgba(0, 200, 83, 0.04);
}

.rm-week-month {
  font-size: 9px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  line-height: 1.2;
  min-height: 11px;
}

.rm-week-num {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 500;
}

.rm-week-today .rm-week-num {
  color: var(--accent-primary);
  font-weight: 700;
}

.rm-today-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--accent-primary);
  z-index: 4;
  pointer-events: none;
  opacity: 0.5;
}

.rm-body {
  position: relative;
}

.rm-lane {
  position: relative;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
}

.rm-week-line {
  position: absolute;
  top: 0;
  height: 100%;
  border-right: 1px solid var(--border-color);
  pointer-events: none;
  opacity: 0.3;
}

.rm-bar {
  position: absolute;
  height: 30px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 8px;
  cursor: grab;
  z-index: 3;
  transition: box-shadow 0.15s;
  overflow: hidden;
  min-width: 20px;
  background: rgba(83, 109, 254, 0.15);
  border: 1px solid rgba(83, 109, 254, 0.25);
  color: var(--text-primary);
}

.rm-bar:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

.rm-bar.status-in-progress {
  background: rgba(83, 109, 254, 0.18);
  border-color: rgba(83, 109, 254, 0.35);
}

.rm-bar.status-ongoing {
  background: rgba(255, 179, 0, 0.15);
  border-color: rgba(255, 179, 0, 0.25);
}

.rm-bar.status-done {
  background: rgba(0, 200, 83, 0.12);
  border-color: rgba(0, 200, 83, 0.2);
}

.rm-bar.status-todo {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.rm-bar-done {
  opacity: 0.5;
}

.rm-bar-critical {
  border-width: 2px;
  border-color: #ff5252 !important;
  box-shadow: 0 0 0 1px rgba(255, 82, 82, 0.15), 0 0 12px rgba(255, 82, 82, 0.08);
}

.rm-bar-critical:hover {
  box-shadow: 0 0 0 2px rgba(255, 82, 82, 0.2), 0 2px 12px rgba(255, 82, 82, 0.12);
}

.rm-bar-label {
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1;
  min-width: 0;
}

.rm-bar-tag {
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 1px 5px;
  border-radius: 3px;
  flex-shrink: 0;
  opacity: 0.8;
}

.rm-bar-handle {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 8px;
  cursor: ew-resize;
  opacity: 0;
  transition: opacity 0.15s;
}

.rm-bar:hover .rm-bar-handle {
  opacity: 1;
  background: rgba(0,0,0,0.06);
}

.rm-unscheduled {
  margin-top: 16px;
}

.rm-unscheduled-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rm-unscheduled-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.rm-unscheduled-card {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--bg-hover);
  border: 1px dashed var(--border-color);
  border-radius: 8px;
  cursor: grab;
  transition: border-color 0.15s;
  font-size: 12px;
  color: var(--text-secondary);
  user-select: none;
}

.rm-unscheduled-card:hover {
  border-color: var(--accent-primary);
  background: rgba(0, 200, 83, 0.04);
}

.rm-unscheduled-name {
  font-weight: 500;
  color: var(--text-primary);
}
</style>
