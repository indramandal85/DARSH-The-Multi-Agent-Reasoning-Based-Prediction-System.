<template>
  <div ref="shellRef" class="swarm-shell" :class="`mode-${mode}`" @click="clearSelection">
    <div class="swarm-shell-header" @click.stop>
      <div>
        <div class="swarm-shell-label">{{ mode === 'running' ? 'Live Agent Field' : 'Swarm Intelligence Map' }}</div>
        <div class="swarm-shell-title">{{ mode === 'running' ? 'Realtime Cohort Activity' : 'Population-Weighted Cohort Field' }}</div>
      </div>
      <div class="swarm-chip-row">
        <span class="swarm-chip">{{ renderedNodes.length }} nodes</span>
        <span class="swarm-chip">{{ cohortLegend.length }} cohorts</span>
        <button class="swarm-chip swarm-chip-button" @click="zoomOut">-</button>
        <button class="swarm-chip swarm-chip-button" @click="zoomIn">+</button>
        <button class="swarm-chip swarm-chip-button" @click="resetViewport">Reset</button>
        <button class="swarm-chip swarm-chip-button" @click="toggleFullscreen" :title="isFullscreen ? 'Exit fullscreen' : 'Open fullscreen'">⛶</button>
      </div>
    </div>

    <div
      ref="boardRef"
      class="swarm-board"
      @mousedown="startPan"
      @wheel.prevent="onWheel"
      @click="clearSelection"
    >
      <svg
        class="swarm-svg"
        :viewBox="`0 0 ${boardWidth} ${boardHeight}`"
        role="img"
        aria-label="Animated market cohort swarm field"
      >
        <defs>
          <filter id="swarm-blur-lg" x="-60%" y="-60%" width="220%" height="220%">
            <feGaussianBlur stdDeviation="34" />
          </filter>
          <filter id="swarm-node-glow" x="-100%" y="-100%" width="300%" height="300%">
            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="rgba(255,255,255,0.45)" />
          </filter>
          <radialGradient
            v-for="cohort in cohortLegend"
            :key="`grad-${cohort.id}`"
            :id="gradientId(cohort.id)"
            cx="35%"
            cy="32%"
            r="72%"
          >
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.96" />
            <stop offset="26%" :stop-color="withOpacity(cohort.color, 0.98)" />
            <stop offset="76%" :stop-color="cohort.color" />
            <stop offset="100%" :stop-color="shadeHex(cohort.color, -0.18)" />
          </radialGradient>
        </defs>

        <rect x="0" y="0" :width="boardWidth" :height="boardHeight" class="swarm-board-bg" />

        <g :transform="viewportTransform">
          <g class="swarm-grid" aria-hidden="true">
            <line
              v-for="grid in verticalGrid"
              :key="`v-${grid}`"
              :x1="grid"
              y1="0"
              :x2="grid"
              :y2="boardHeight"
              class="swarm-grid-line"
            />
            <line
              v-for="grid in horizontalGrid"
              :key="`h-${grid}`"
              x1="0"
              :y1="grid"
              :x2="boardWidth"
              :y2="grid"
              class="swarm-grid-line"
            />
          </g>

          <g v-if="mode !== 'running'" class="swarm-classification-cells">
            <rect
              v-for="cell in classificationCells"
              :key="cell.id"
              :x="cell.x"
              :y="cell.y"
              :width="cell.w"
              :height="cell.h"
              :fill="withOpacity(cell.color, cell.opacity)"
            />
          </g>

          <g v-if="mode !== 'running'" class="swarm-soft-zones">
            <ellipse
              v-for="zone in softZones"
              :key="zone.id"
              :cx="zone.x"
              :cy="zone.y"
              :rx="zone.rx"
              :ry="zone.ry"
              :fill="withOpacity(zone.color, zone.opacity)"
              filter="url(#swarm-blur-lg)"
            />
          </g>

          <g v-if="mode !== 'running'" class="swarm-links">
            <path
              v-for="link in renderedLinks"
              :key="link.id"
              :d="link.path"
              :stroke="link.stroke"
              :stroke-width="link.strokeWidth"
              :opacity="link.opacity"
              fill="none"
              :class="['swarm-link', { active: link.isLiveActive, dimmed: link.isDimmed }]"
            />
          </g>

          <g v-if="mode !== 'running'" class="swarm-live-halos">
            <ellipse
              v-for="halo in liveHalos"
              :key="halo.id"
              :cx="halo.x"
              :cy="halo.y"
              :rx="halo.rx"
              :ry="halo.ry"
              :fill="withOpacity(halo.color, halo.opacity)"
              filter="url(#swarm-blur-lg)"
            />
          </g>

          <g class="swarm-nodes swarm-agent-field">
            <g
              v-for="node in renderedNodes"
              :key="node.id"
              :transform="agentNodeTransform(node)"
              :opacity="node.opacity"
              :class="['swarm-agent', {
                selected: selectedNode?.id === node.id,
                active: node.isLiveActive,
                dimmed: node.isDimmed
              }]"
              @click.stop="selectNode(node, $event)"
            >
              <g class="swarm-agent-body" :style="agentAnimationVars(node)">
                <ellipse
                  class="swarm-agent-aura"
                  cx="0"
                  cy="6.25"
                  :rx="node.isLiveActive ? 8.6 : 7.4"
                  :ry="node.isLiveActive ? 2.95 : 2.45"
                  :fill="withOpacity(node.statusColor, node.isLiveActive ? 0.24 : 0.14)"
                />
                <g class="swarm-agent-core">
                  <rect class="swarm-agent-side" x="-8.35" y="-2.3" width="1.45" height="4.6" rx="0.72" :fill="node.baseColor" opacity="0.92" />
                  <rect class="swarm-agent-side" x="6.9" y="-2.3" width="1.45" height="4.6" rx="0.72" :fill="node.baseColor" opacity="0.92" />
                  <rect class="swarm-agent-head" x="-7.1" y="-5.8" width="14.2" height="9.6" rx="3.25" :fill="node.faceColor" :stroke="node.stroke" :stroke-width="0.78" />
                  <rect class="swarm-agent-visor" x="-4.9" y="-3.05" width="9.8" height="4.45" rx="2.1" fill="rgba(255,255,255,0.94)" />
                  <rect class="swarm-agent-visor-sheen" x="-5.1" y="-3.12" width="2.45" height="4.6" rx="1.16" fill="rgba(255,255,255,0.26)" />
                  <rect class="swarm-agent-core-bar" x="-2.85" y="2.62" width="5.7" height="0.76" rx="0.38" :fill="withOpacity(node.statusColor, 0.78)" />
                  <ellipse class="swarm-agent-eye" cx="-2.25" cy="-0.82" rx="0.92" ry="0.92" :fill="node.eyeColor" />
                  <ellipse class="swarm-agent-eye" cx="2.25" cy="-0.82" rx="0.92" ry="0.92" :fill="node.eyeColor" />
                  <rect class="swarm-agent-mouth" x="-2.2" y="1.15" width="4.4" height="0.92" rx="0.46" fill="rgba(255,255,255,0.86)" opacity="0.94" />
                  <rect class="swarm-agent-base" x="-2.6" y="4.35" width="5.2" height="1.1" rx="0.55" :fill="node.baseColor" opacity="0.9" />
                </g>
                <g
                  v-if="senderSignal(node.id)"
                  class="swarm-agent-signal swarm-agent-signal-send"
                  :style="{ '--swarm-agent-signal-delay': `${senderSignal(node.id).delay}s` }"
                >
                  <ellipse class="swarm-agent-send-halo" cx="0" cy="-8.15" rx="7.2" ry="2.95" :fill="senderSignal(node.id).glow" />
                  <path class="swarm-agent-send-chevron" d="M -4.35 -8.45 L 0 -11.8 L 4.35 -8.45" :stroke="senderSignal(node.id).color" />
                  <circle class="swarm-agent-send-core" cx="0" cy="-8.35" r="1.2" :fill="senderSignal(node.id).color" />
                  <circle class="swarm-agent-send-pulse swarm-agent-send-pulse-center" cx="0" cy="-12.15" r="1.08" :fill="senderSignal(node.id).softColor" />
                  <circle class="swarm-agent-send-pulse swarm-agent-send-pulse-left" cx="-4.2" cy="-10.6" r="0.86" :fill="senderSignal(node.id).softColor" />
                  <circle class="swarm-agent-send-pulse swarm-agent-send-pulse-right" cx="4.2" cy="-10.6" r="0.86" :fill="senderSignal(node.id).softColor" />
                </g>
                <g
                  v-if="receiverSignal(node.id)"
                  class="swarm-agent-signal swarm-agent-signal-receive"
                  :style="{ '--swarm-agent-signal-delay': `${receiverSignal(node.id).delay}s` }"
                >
                  <ellipse class="swarm-agent-receive-halo" cx="0" cy="-8.1" rx="7.5" ry="3.1" :fill="receiverSignal(node.id).glow" />
                  <path class="swarm-agent-receive-chevron" d="M -4.3 -11.9 L 0 -8.5 L 4.3 -11.9" :stroke="receiverSignal(node.id).color" />
                  <path class="swarm-agent-receive-chevron swarm-agent-receive-chevron-inner" d="M -2.85 -10.15 L 0 -7.9 L 2.85 -10.15" :stroke="receiverSignal(node.id).softColor" />
                  <circle class="swarm-agent-receive-pulse" cx="0" cy="-12.2" r="1.02" :fill="receiverSignal(node.id).color" />
                  <circle class="swarm-agent-receive-core" cx="0" cy="-8.05" r="1.22" :fill="receiverSignal(node.id).softColor" />
                </g>
              </g>
            </g>
          </g>
        </g>
      </svg>

      <div v-if="selectedNode" class="swarm-node-popup" :style="popupStyle" @click.stop>
        <div class="popup-topline">
          <span class="popup-type">{{ selectedNode.label }}</span>
          <button class="popup-close" @click="clearSelection">✕</button>
        </div>
        <div class="popup-title">{{ selectedNode.cohortLabel }}</div>
        <div class="popup-chips">
          <span class="popup-chip" :style="{ borderColor: withOpacity(selectedNode.color, 0.38), color: selectedNode.color }">
            Cohort
          </span>
          <span class="popup-chip" :style="{ borderColor: withOpacity(selectedNode.statusColor, 0.38), color: selectedNode.statusColor }">
            {{ formatLabel(selectedNode.dominantOutcome) }}
          </span>
          <span class="popup-chip popup-chip-muted">{{ Math.round((selectedNode.confidence || 0) * 100) }}% confidence</span>
        </div>

        <div class="popup-block">
          <div class="popup-label">Current Thinking</div>
          <p class="popup-thinking">{{ truncateText(selectedNode.thinking, 154) }}</p>
        </div>

        <div class="popup-inline-grid">
          <div class="popup-inline-card">
            <span class="popup-inline-label">Action</span>
            <strong class="popup-inline-value">{{ truncateText(selectedNode.action, 92) }}</strong>
          </div>
          <div class="popup-inline-card">
            <span class="popup-inline-label">Current Stage</span>
            <strong class="popup-inline-value">{{ truncateText(runningStep || 'Simulation active', 84) }}</strong>
          </div>
        </div>

        <div class="popup-metrics">
          <div class="popup-metric">
            <span class="popup-metric-label">Population</span>
            <strong>{{ formatPopulation(selectedNode.population) }}</strong>
          </div>
          <div class="popup-metric">
            <span class="popup-metric-label">Velocity</span>
            <strong>{{ formatLabel(selectedNode.velocityLabel) }}</strong>
          </div>
        </div>

        <div class="popup-distribution">
          <div v-for="bar in distributionRows(selectedNode.distribution)" :key="bar.key" class="popup-distribution-row">
            <div class="popup-distribution-head">
              <span>{{ bar.label }}</span>
              <span>{{ bar.percent }}%</span>
            </div>
            <div class="popup-bar-track">
              <div class="popup-bar-fill" :style="{ width: `${bar.percent}%`, background: bar.color }"></div>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="cohortLegend.length || statusLegend.length"
        class="swarm-legend-overlay"
        :class="{
          'results-overlay': mode !== 'running',
          'running-overlay': mode === 'running'
        }"
        @click.stop
      >
        <div class="legend-section legend-section-compact">
          <div class="legend-title">Cohorts</div>
          <div class="legend-pills legend-pills-cohorts">
            <span v-for="cohort in cohortLegend" :key="`run-${cohort.id}`" class="legend-pill">
              <span class="legend-dot" :style="{ background: cohort.color }"></span>
              {{ cohort.label }}
            </span>
          </div>
        </div>

        <div class="legend-section legend-section-compact">
          <div class="legend-title">Status</div>
          <div class="legend-pills legend-pills-status">
            <span v-for="status in statusLegend" :key="`run-${status.key}`" class="legend-pill">
              <span class="legend-dot" :style="{ background: status.color }"></span>
              {{ status.label }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

const props = defineProps({
  populationModel: {
    type: Object,
    default: null,
  },
  config: {
    type: Object,
    default: () => ({}),
  },
  runningStep: {
    type: String,
    default: '',
  },
  mode: {
    type: String,
    default: 'results',
  },
  active: {
    type: Boolean,
    default: true,
  },
  liveFocus: {
    type: Object,
    default: () => ({}),
  },
})

const boardRef = ref(null)
const shellRef = ref(null)
const selectedNodeId = ref(null)
const popupCoords = ref({ left: '20px', top: '20px' })
const tick = ref(0)
const zoom = ref(1)
const isFullscreen = ref(false)
const pan = ref({ x: 0, y: 0 })
const isPanning = ref(false)
const panStart = ref({ x: 0, y: 0, panX: 0, panY: 0 })

const boardWidth = computed(() => Number(props.config?.swarmBoardWidth) || (props.mode === 'running' ? 1260 : 1240))
const boardHeight = computed(() => Number(props.config?.swarmBoardHeight) || (props.mode === 'running' ? 620 : 820))

const statusColors = {
  panic: '#f07cc6',
  cautious: '#7fcfff',
  optimistic: '#68ddd6',
  divided: '#b290ff',
  confident: '#5c96ff',
}

const cohortPalette = [
  '#7fcfff',
  '#5c96ff',
  '#68ddd6',
  '#b290ff',
  '#f07cc6',
  '#88e6ff',
  '#7ab5ff',
  '#86eadc',
  '#cfabff',
  '#7dd9ff',
  '#92b2ff',
  '#ff9ddf',
]

const cohortRoleDefaults = [
  { id: 'RETAIL_TRADER', label: 'Retail Trader', outcome: 'cautious', velocity: 'very_fast', population: 40_000_000 },
  { id: 'DOMESTIC_MUTUAL_FUND', label: 'Domestic Mutual Fund Manager', outcome: 'cautious', velocity: 'medium', population: 47_000_000 },
  { id: 'FII_ANALYST', label: 'Foreign Institutional Analyst', outcome: 'panic', velocity: 'fast', population: 12_000 },
  { id: 'FINANCIAL_MEDIA_EDITOR', label: 'Financial Media Editor', outcome: 'divided', velocity: 'very_fast', population: 1_200 },
  { id: 'BROKER_RESEARCH_DESK', label: 'Broker Research Desk', outcome: 'optimistic', velocity: 'fast', population: 3_500 },
  { id: 'CORPORATE_TREASURY', label: 'Corporate Treasury', outcome: 'cautious', velocity: 'medium', population: 8_000 },
  { id: 'PRIVATE_BANK_TREASURY', label: 'Private Bank Treasury', outcome: 'cautious', velocity: 'medium', population: 320 },
  { id: 'SECTOR_OPERATING_FIRM', label: 'Sector Operating Firm', outcome: 'optimistic', velocity: 'medium', population: 250_000 },
]

const statusLegend = [
  { key: 'panic', label: 'Risk Off / Panic', color: statusColors.panic },
  { key: 'cautious', label: 'Cautious', color: statusColors.cautious },
  { key: 'optimistic', label: 'Risk On / Optimistic', color: statusColors.optimistic },
  { key: 'divided', label: 'Divided', color: statusColors.divided },
  { key: 'confident', label: 'Confident', color: statusColors.confident },
]

const verticalGrid = computed(() => Array.from({ length: 12 }, (_, i) => 52 + i * 104))
const horizontalGrid = computed(() => Array.from({ length: 8 }, (_, i) => 48 + i * 92))
const viewportTransform = computed(() => `translate(${pan.value.x} ${pan.value.y}) scale(${zoom.value})`)
const selectedNode = computed(() =>
  renderedNodes.value.find(node => node.id === selectedNodeId.value) || null
)

const statusAnchors = computed(() => ({
  panic: { x: boardWidth.value * 0.76, y: boardHeight.value * 0.26 },
  cautious: { x: boardWidth.value * 0.28, y: boardHeight.value * 0.34 },
  optimistic: { x: boardWidth.value * 0.62, y: boardHeight.value * 0.67 },
  divided: { x: boardWidth.value * 0.78, y: boardHeight.value * 0.58 },
  confident: { x: boardWidth.value * 0.46, y: boardHeight.value * 0.2 },
}))

const activeCohortId = computed(() => {
  if (props.mode !== 'running') return ''
  const role = String(props.liveFocus?.market_role || '').trim()
  if (!role) return ''
  return cohortData.value.some(cohort => cohort.id === role) ? role : ''
})

const hasLiveFocus = computed(() => props.mode === 'running' && Boolean(activeCohortId.value))

const cohortData = computed(() => {
  const modelCohorts = props.populationModel?.cohort_breakdown
  if (Array.isArray(modelCohorts) && modelCohorts.length) {
    return modelCohorts
      .slice(0, Math.min(modelCohorts.length, Math.max(3, props.config?.numAgents || 5)))
      .map((cohort, index) => {
        const dominantOutcome = normalizeOutcome(cohort.dominant_outcome)
        const distribution = normalizeDistribution(cohort.belief_distribution, dominantOutcome)
        const confidence = clamp(cohort.avg_decision_confidence ?? cohort.outcome_confidence ?? 0.56, 0.12, 0.98)
        return {
          id: cohort.role_key || `COHORT_${index}`,
          label: cohort.label || formatLabel(cohort.role_key || `cohort_${index}`),
          dominantOutcome,
          distribution,
          confidence,
          representedPopulation: cohort.represented_population || 0,
          velocityLabel: deriveVelocityLabel(cohort.velocity_influence),
          color: cohortPalette[index % cohortPalette.length],
          statusColor: statusColors[dominantOutcome] || statusColors.cautious,
          thinking: buildThinkingLine(cohort.label || 'This cohort', dominantOutcome, props.runningStep, props.config?.eventType),
          action: buildActionLine(dominantOutcome, props.config?.eventType),
        }
      })
  }

  return cohortRoleDefaults.slice(0, Math.max(3, props.config?.numAgents || 5)).map((cohort, index) => {
    const confidence = deriveRunningConfidence(index)
    return {
      id: cohort.id,
      label: cohort.label,
      dominantOutcome: cohort.outcome,
      distribution: buildSyntheticDistribution(cohort.outcome, confidence, index),
      confidence,
      representedPopulation: cohort.population,
      velocityLabel: cohort.velocity,
      color: cohortPalette[index % cohortPalette.length],
      statusColor: statusColors[cohort.outcome] || statusColors.cautious,
      thinking: buildThinkingLine(cohort.label, cohort.outcome, props.runningStep, props.config?.eventType),
      action: buildActionLine(cohort.outcome, props.config?.eventType),
    }
  })
})

const softZones = computed(() => {
  const grouped = {}
  cohortData.value.forEach((cohort, index) => {
    const key = cohort.dominantOutcome
    if (!grouped[key]) grouped[key] = []
    grouped[key].push({ cohort, index })
  })

  return Object.entries(grouped).map(([outcome, rows], index) => {
    const anchor = statusAnchors.value[outcome] || statusAnchors.value.cautious
    const avgConfidence = rows.reduce((sum, row) => sum + row.cohort.confidence, 0) / rows.length
    return {
      id: `zone-${outcome}`,
      x: anchor.x + Math.sin(index + tick.value * 0.01) * 14,
      y: anchor.y + Math.cos(index + tick.value * 0.01) * 12,
      rx: 120 + rows.length * 34 + avgConfidence * 44,
      ry: 92 + rows.length * 26 + avgConfidence * 30,
      color: statusColors[outcome] || statusColors.cautious,
      opacity: 0.12 + Math.min(rows.length * 0.02, 0.08),
    }
  })
})

const classificationCells = computed(() => {
  const cols = 20
  const rows = 12
  const cells = []
  const cellW = boardWidth.value / cols
  const cellH = boardHeight.value / rows

  for (let row = 0; row < rows; row += 1) {
    for (let col = 0; col < cols; col += 1) {
      const cx = col * cellW + cellW / 2
      const cy = row * cellH + cellH / 2
      const scores = Object.entries(statusAnchors.value).map(([key, anchor]) => {
        const distance = Math.hypot(cx - anchor.x, cy - anchor.y)
        const strength = 1 / Math.max(distance / 140, 0.85)
        const cohortSupport = cohortData.value.filter(item => item.dominantOutcome === key).length || 0.4
        return {
          key,
          score: strength * cohortSupport,
        }
      }).sort((a, b) => b.score - a.score)

      const best = scores[0]
      const next = scores[1] || { score: 0 }
      const confidence = clamp((best.score - next.score) / Math.max(best.score, 0.001), 0.04, 0.18)
      cells.push({
        id: `cell-${row}-${col}`,
        x: col * cellW,
        y: row * cellH,
        w: cellW + 1,
        h: cellH + 1,
        color: statusColors[best.key] || statusColors.cautious,
        opacity: confidence,
      })
    }
  }

  return cells
})

const renderedNodes = computed(() => {
  const paddingX = 28
  const paddingY = 36
  const nodes = []
  const phase = props.mode === 'running' ? 0 : tick.value * 0.018
  const centerX = boardWidth.value / 2
  const centerY = boardHeight.value / 2
  const radialSpanX = boardWidth.value * 0.48
  const radialSpanY = boardHeight.value * 0.48
  const allocatedCounts = allocateNodeCounts(props.config?.numAgents || 5)

  cohortData.value.forEach((cohort, cohortIndex) => {
    const zone = statusAnchors.value[cohort.dominantOutcome] || statusAnchors.value.cautious
    const count = allocatedCounts[cohortIndex] || deriveNodeCount(cohort.representedPopulation, cohortData.value.length, props.config?.numAgents || 5)
    const cohortActive = hasLiveFocus.value && cohort.id === activeCohortId.value
    const cohortDimmed = hasLiveFocus.value && cohort.id !== activeCohortId.value

    for (let i = 0; i < count; i += 1) {
      const seedX = seededNumber(`${cohort.id}-${i}-x`)
      const seedY = seededNumber(`${cohort.id}-${i}-y`)
      const seedAngle = seededNumber(`${cohort.id}-${i}-angle`) * Math.PI * 2
      const seedRadius = Math.pow(seededNumber(`${cohort.id}-${i}-radius`), 0.78)
      const uniformX = paddingX + seedX * (boardWidth.value - paddingX * 2)
      const uniformY = paddingY + seedY * (boardHeight.value - paddingY * 2)
      const radialX = centerX + Math.cos(seedAngle) * radialSpanX * seedRadius
      const radialY = centerY + Math.sin(seedAngle) * radialSpanY * seedRadius
      const waveX = Math.sin(seedY * Math.PI * 2.8 + cohortIndex * 0.7) * 26
      const waveY = Math.cos(seedX * Math.PI * 2.6 + cohortIndex * 0.62) * 22
      const uniformWeight = props.mode === 'running' ? 0.91 : 0.82
      const radialWeight = 1 - uniformWeight
      const baseX = uniformX * uniformWeight + radialX * radialWeight + waveX
      const baseY = uniformY * uniformWeight + radialY * radialWeight + waveY
      const pull = props.mode === 'running'
        ? 0.0006 + cohort.confidence * 0.0018
        : 0.032 + cohort.confidence * 0.08
      const jitter = seededNumber(`${cohort.id}-${i}-j`)
      const x = baseX * (1 - pull) + zone.x * pull
      const y = baseY * (1 - pull) + zone.y * pull
      const confidencePulse = props.mode === 'running'
        ? 0
        : Math.sin(phase * 1.45 + i * 0.11 + cohortIndex) * 0.045
      const nodeConfidence = clamp(cohort.confidence + confidencePulse, 0.12, 0.98)
      const nodeDistribution = buildNodeDistribution(
        cohort.distribution,
        cohort.dominantOutcome,
        nodeConfidence,
        i + cohortIndex * 17
      )
      const baseRadius = props.mode === 'running'
        ? 3.1 + seededNumber(`r-${cohort.id}-${i}`) * 1.95
        : 3.45 + seededNumber(`r-${cohort.id}-${i}`) * 2.25
      const livePulse = props.mode === 'running'
        ? 0.5
        : Math.sin(phase * 2.35 + i * 0.12 + cohortIndex) * 0.5 + 0.5
      const nodeRadius = props.mode === 'running'
        ? baseRadius
        : cohortActive
          ? baseRadius * (1.05 + livePulse * 0.1)
          : cohortDimmed ? baseRadius * 0.94 : baseRadius
      const nodeOpacity = props.mode === 'running'
        ? (cohortDimmed ? 0.8 + seededNumber(`fade-${cohort.id}-${i}`) * 0.06 : cohortActive ? 0.96 : 0.9)
        : cohortDimmed
          ? 0.76 + seededNumber(`fade-${cohort.id}-${i}`) * 0.08
          : cohortActive ? 0.98 : 0.9
      const auraScale = 1 + (props.mode === 'running' ? 0.16 : 0.12) + jitter * 0.08
      const auraOpacity = props.mode === 'running'
        ? (cohortActive ? 0.68 + jitter * 0.1 : 0.42 + jitter * 0.08)
        : cohortActive ? 0.72 + jitter * 0.16 : 0.46 + jitter * 0.12
      const barOpacity = props.mode === 'running'
        ? (cohortActive ? 0.88 + jitter * 0.05 : 0.62 + jitter * 0.08)
        : cohortActive ? 0.9 + jitter * 0.06 : 0.68 + jitter * 0.1
      const motionX = (props.mode === 'running' ? 0.12 : 0.05) + seededNumber(`motion-x-${cohort.id}-${i}`) * (props.mode === 'running' ? 0.18 : 0.08)
      const motionY = (props.mode === 'running' ? 0.08 : 0.04) + seededNumber(`motion-y-${cohort.id}-${i}`) * (props.mode === 'running' ? 0.16 : 0.06)
      const motionTilt = 0.06 + seededNumber(`motion-tilt-${cohort.id}-${i}`) * (props.mode === 'running' ? 0.24 : 0.1)
      const floatDuration = 5.6 + seededNumber(`float-duration-${cohort.id}-${i}`) * 3.2
      const vibeDuration = 1.18 + seededNumber(`vibe-duration-${cohort.id}-${i}`) * 0.74
      const vibeX = 0.04 + seededNumber(`vibe-x-${cohort.id}-${i}`) * (props.mode === 'running' ? 0.08 : 0.04)
      const vibeY = 0.03 + seededNumber(`vibe-y-${cohort.id}-${i}`) * (props.mode === 'running' ? 0.06 : 0.03)
      const motionDelay = seededNumber(`motion-delay-${cohort.id}-${i}`) * 2.6
      const breatheDuration = 3 + seededNumber(`breathe-duration-${cohort.id}-${i}`) * 1.9
      const blinkDuration = 5.4 + seededNumber(`blink-duration-${cohort.id}-${i}`) * 3.8
      const blinkDelay = seededNumber(`blink-delay-${cohort.id}-${i}`) * 4.4
      const sheenDuration = 4.8 + seededNumber(`sheen-duration-${cohort.id}-${i}`) * 3.3
      const sheenDelay = seededNumber(`sheen-delay-${cohort.id}-${i}`) * 3.2
      const sheenOpacity = cohortActive ? 0.26 + jitter * 0.06 : 0.16 + jitter * 0.08

      nodes.push({
        id: `${cohort.id}-node-${i}`,
        label: `${cohort.label} Node ${i + 1}`,
        cohortId: cohort.id,
        cohortLabel: cohort.label,
        color: cohort.color,
        statusColor: cohort.statusColor,
        dominantOutcome: cohort.dominantOutcome,
        distribution: nodeDistribution,
        confidence: nodeConfidence,
        thinking: buildNodeThinking(cohort.label, cohort.dominantOutcome, props.runningStep, i),
        action: buildNodeActionLine(cohort.dominantOutcome, props.config?.eventType, i),
        velocityLabel: cohort.velocityLabel,
        population: cohort.representedPopulation,
        x: clamp(x, 20, boardWidth.value - 20),
        y: clamp(y, 24, boardHeight.value - 24),
        radius: nodeRadius,
        iconScale: (props.mode === 'running' ? 0.82 : 0.9) + nodeRadius * 0.066,
        rotation: (seededNumber(`rotation-${cohort.id}-${i}`) - 0.5) * (props.mode === 'running' ? 0.16 : (cohortActive ? 0.42 : 0.2)),
        auraScale,
        auraOpacity,
        barOpacity,
        motionX,
        motionY,
        motionTilt,
        floatDuration,
        vibeDuration,
        vibeX,
        vibeY,
        motionDelay,
        breatheDuration,
        blinkDuration,
        blinkDelay,
        sheenDuration,
        sheenDelay,
        sheenOpacity,
        fill: `url(#${gradientId(cohort.id)})`,
        faceColor: cohort.color,
        baseColor: shadeHex(cohort.color, -0.24),
        eyeColor: shadeHex(cohort.statusColor, -0.04),
        stroke: cohortActive
          ? withOpacity('#ffffff', 0.94)
          : withOpacity(shadeHex(cohort.color, -0.24), 0.78),
        strokeWidth: cohortActive ? 1.05 : (props.mode === 'running' ? 0.8 : 0.82),
        opacity: nodeOpacity,
        isLiveActive: cohortActive,
        isDimmed: cohortDimmed,
      })
    }
  })

  return nodes
})

const renderedLinks = computed(() => {
  const links = []
  const nodesByCohort = new Map()

  renderedNodes.value.forEach(node => {
    if (!nodesByCohort.has(node.cohortId)) nodesByCohort.set(node.cohortId, [])
    nodesByCohort.get(node.cohortId).push(node)
  })

  cohortData.value.forEach((cohort, cohortIndex) => {
    const cohortNodes = nodesByCohort.get(cohort.id) || []
    const step = props.mode === 'running'
      ? Math.max(24, Math.floor(cohortNodes.length / 5))
      : Math.max(6, Math.floor(cohortNodes.length / 14))
    for (let i = 0; i < cohortNodes.length - step; i += step) {
      const source = cohortNodes[i]
      const target = cohortNodes[Math.min(i + step, cohortNodes.length - 1)]
      const curveSeed = seededNumber(`link-${source.id}-${target.id}`)
      const controlX = (source.x + target.x) / 2 + ((curveSeed - 0.5) * 22)
      const controlY = (source.y + target.y) / 2 - 20
      links.push({
        id: `${source.id}-${target.id}`,
        color: cohort.color,
        path: `M ${source.x} ${source.y} Q ${controlX} ${controlY} ${target.x} ${target.y}`,
        sourceCohortId: cohort.id,
        targetCohortId: cohort.id,
      })
    }

    if (cohortIndex < cohortData.value.length - 1) {
      const source = cohortNodes[Math.floor(cohortNodes.length * 0.35)] || cohortNodes[0]
      const nextNodes = nodesByCohort.get(cohortData.value[cohortIndex + 1].id) || []
      const target = nextNodes[Math.floor(nextNodes.length * 0.55)] || nextNodes[0]
      if (source && target) {
        const controlX = (source.x + target.x) / 2
        const controlY = Math.min(source.y, target.y) - 56
        links.push({
          id: `cross-${source.id}-${target.id}`,
          color: cohortData.value[cohortIndex + 1].statusColor,
          path: `M ${source.x} ${source.y} Q ${controlX} ${controlY} ${target.x} ${target.y}`,
          sourceCohortId: cohort.id,
          targetCohortId: cohortData.value[cohortIndex + 1].id,
        })
      }
    }
  })

  return links.map(link => {
    const touchesActive = hasLiveFocus.value
      && (link.sourceCohortId === activeCohortId.value || link.targetCohortId === activeCohortId.value)
    return {
      ...link,
      isLiveActive: touchesActive,
      isDimmed: hasLiveFocus.value && !touchesActive,
      stroke: props.mode === 'running'
        ? 'rgba(176, 181, 191, 0.14)'
        : (touchesActive
            ? withOpacity(link.color, 0.56)
            : withOpacity(link.color, 0.12)),
      strokeWidth: props.mode === 'running'
        ? 0.68
        : (touchesActive ? 1.35 : 0.9),
      opacity: props.mode === 'running'
        ? 0.18
        : (hasLiveFocus.value ? (touchesActive ? 0.94 : 0.12) : 0.9),
    }
  })
})

const socialFeedLinks = computed(() => {
  if (props.mode !== 'running' || !hasLiveFocus.value) return []

  const activeNodes = renderedNodes.value.filter(node => node.cohortId === activeCohortId.value)
  if (!activeNodes.length) return []

  const links = []
  const otherCohorts = cohortData.value
    .filter(cohort => cohort.id !== activeCohortId.value)
    .slice(0, 6)

  otherCohorts.forEach((cohort, index) => {
    const cohortNodes = renderedNodes.value.filter(node => node.cohortId === cohort.id)
    if (!cohortNodes.length) return

    const source = activeNodes[(index * 3) % activeNodes.length]
    const target = cohortNodes[(index * 5 + 1) % cohortNodes.length]
    if (!source || !target) return

    const sourceHeadX = source.x
    const sourceHeadY = source.y - source.iconScale * 8.4
    const targetHeadX = target.x
    const targetHeadY = target.y - target.iconScale * 8.4
    const dx = targetHeadX - sourceHeadX
    const dy = targetHeadY - sourceHeadY
    const length = Math.max(Math.hypot(dx, dy), 1)
    const angleDeg = (Math.atan2(dy, dx) * 180) / Math.PI
    const progress = ((tick.value / 15) + index * 0.22) % 1
    const echoProgress = (progress + 0.34) % 1
    const tailProgress = (progress + 0.18) % 1
    const delay = (index % 4) * 0.18
    const guideDotCount = Math.max(7, Math.min(16, Math.floor(length / 20)))
    const guideDots = Array.from({ length: guideDotCount }, (_, guideIndex) => {
      const usableLength = Math.max(length - 22, 1)
      return 11 + (usableLength * guideIndex) / Math.max(guideDotCount - 1, 1)
    })
    links.push({
      id: `social-${source.id}-${target.id}-${index}`,
      sourceId: source.id,
      targetId: target.id,
      x1: sourceHeadX,
      y1: sourceHeadY,
      x2: targetHeadX,
      y2: targetHeadY,
      sourceHeadX,
      sourceHeadY,
      targetHeadX,
      targetHeadY,
      angleDeg,
      length,
      opacity: 0.2 + ((index % 3) * 0.04),
      strokeWidth: 0.68,
      packetX: length * progress,
      echoPacketX: length * echoProgress,
      tailPacketX: length * tailProgress,
      messageColor: index % 2 === 0 ? '#74cfff' : '#9a8fff',
      packetAccent: index % 2 === 0 ? '#b290ff' : '#66d6ff',
      guideColor: index % 2 === 0 ? 'rgba(111, 215, 255, 0.78)' : 'rgba(178, 144, 255, 0.76)',
      railColor: index % 2 === 0 ? 'rgba(116, 207, 255, 0.26)' : 'rgba(154, 143, 255, 0.24)',
      coreColor: index % 2 === 0 ? 'rgba(255, 255, 255, 0.84)' : 'rgba(243, 236, 255, 0.82)',
      packetGlow: index % 2 === 0 ? 'rgba(116, 207, 255, 0.22)' : 'rgba(154, 143, 255, 0.18)',
      receiverGlow: index % 2 === 0 ? 'rgba(111, 215, 255, 0.2)' : 'rgba(178, 144, 255, 0.18)',
      guideDots,
      delay,
    })
  })

  return links
})

const senderSignalMap = computed(() => {
  const map = new Map()
  socialFeedLinks.value.forEach(link => {
    if (!map.has(link.sourceId)) {
      map.set(link.sourceId, {
        color: '#b290ff',
        glow: 'rgba(178, 144, 255, 0.22)',
        softColor: '#efe7ff',
        delay: link.delay,
      })
    }
  })
  return map
})

const receiverSignalMap = computed(() => {
  const map = new Map()
  socialFeedLinks.value.forEach(link => {
    if (!map.has(link.targetId)) {
      map.set(link.targetId, {
        color: '#6fd7ff',
        glow: 'rgba(111, 215, 255, 0.24)',
        softColor: '#e6fbff',
        delay: link.delay,
      })
    }
  })
  return map
})

const cohortLegend = computed(() => cohortData.value.map(cohort => ({
  id: cohort.id,
  label: cohort.label,
  color: cohort.color,
})))

const liveHalos = computed(() => {
  if (!hasLiveFocus.value) return []
  const activeCohort = cohortData.value.find(cohort => cohort.id === activeCohortId.value)
  if (!activeCohort) return []
  const anchor = statusAnchors.value[activeCohort.dominantOutcome] || statusAnchors.value.cautious
  const pulse = Math.sin(tick.value * 0.14) * 0.5 + 0.5
  return [{
    id: `halo-${activeCohort.id}`,
    x: anchor.x,
    y: anchor.y,
    rx: 170 + pulse * 28,
    ry: 126 + pulse * 22,
    color: activeCohort.color,
    opacity: 0.12 + pulse * 0.06,
  }]
})

const popupStyle = computed(() => selectedNode.value ? popupCoords.value : {})

watch(() => props.mode, () => {
  selectedNodeId.value = null
  popupCoords.value = { left: '20px', top: '20px' }
  applyDefaultViewport()
})

let timer = null

onMounted(() => {
  applyDefaultViewport()
  syncTimer(props.active)
  window.addEventListener('mousemove', onPanMove)
  window.addEventListener('mouseup', stopPan)
  window.addEventListener('pointerdown', onGlobalPointerDown, true)
  document.addEventListener('fullscreenchange', syncFullscreenState)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  window.removeEventListener('mousemove', onPanMove)
  window.removeEventListener('mouseup', stopPan)
  window.removeEventListener('pointerdown', onGlobalPointerDown, true)
  document.removeEventListener('fullscreenchange', syncFullscreenState)
})

watch(() => props.active, (value) => {
  syncTimer(value)
})

function selectNode(node, event) {
  selectedNodeId.value = node.id
  popupCoords.value = computePopupCoords(event)
}

function clearSelection() {
  selectedNodeId.value = null
}

function syncFullscreenState() {
  isFullscreen.value = document.fullscreenElement === shellRef.value
}

async function toggleFullscreen() {
  if (!shellRef.value || !document.fullscreenEnabled) return
  if (document.fullscreenElement === shellRef.value) {
    await document.exitFullscreen()
    return
  }
  await shellRef.value.requestFullscreen()
}

function onGlobalPointerDown(event) {
  if (!selectedNodeId.value) return
  if (shellRef.value && !shellRef.value.contains(event.target)) {
    clearSelection()
  }
}

function syncTimer(isActive) {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  if (isActive) {
    const interval = clamp(
      Number(props.config?.animationIntervalMs) || 520,
      320,
      1200
    )
    timer = setInterval(() => {
      tick.value += 1
    }, interval)
  }
}

function normalizeOutcome(value) {
  if (!value) return 'cautious'
  const lower = String(value).toLowerCase()
  if (lower.includes('panic') || lower.includes('risk_off')) return 'panic'
  if (lower.includes('optimistic') || lower.includes('risk_on')) return 'optimistic'
  if (lower.includes('divide')) return 'divided'
  if (lower.includes('confident')) return 'confident'
  return 'cautious'
}

function normalizeDistribution(distribution, dominantOutcome) {
  const base = {
    panic: Number(distribution?.panic || 0),
    cautious: Number(distribution?.cautious || 0),
    optimistic: Number(distribution?.optimistic || 0),
    divided: Number(distribution?.divided || 0),
  }
  let total = Object.values(base).reduce((sum, value) => sum + value, 0)

  if (!total) {
    base[dominantOutcome] = dominantOutcome === 'confident' ? 0.52 : 0.58
    if (dominantOutcome !== 'cautious') base.cautious += 0.18
    if (dominantOutcome !== 'optimistic') base.optimistic += 0.1
    if (dominantOutcome !== 'panic') base.panic += 0.08
    if (dominantOutcome !== 'divided') base.divided += 0.06
    total = Object.values(base).reduce((sum, value) => sum + value, 0)
  }

  return Object.fromEntries(
    Object.entries(base).map(([key, value]) => [key, round(value / total, 3)])
  )
}

function buildSyntheticDistribution(outcome, confidence, index) {
  const mainKey = normalizeOutcome(outcome)
  const base = {
    panic: 0.08 + ((index % 2) * 0.01),
    cautious: 0.18,
    optimistic: 0.12,
    divided: 0.08,
  }
  base[mainKey] = clamp(0.45 + confidence * 0.3, 0.34, 0.76)
  if (mainKey !== 'cautious') base.cautious += 0.14
  if (mainKey === 'divided') {
    base.panic += 0.1
    base.optimistic += 0.1
  }
  const total = Object.values(base).reduce((sum, value) => sum + value, 0)
  return Object.fromEntries(Object.entries(base).map(([key, value]) => [key, round(value / total, 3)]))
}

function deriveRunningConfidence(index) {
  const step = (props.runningStep || '').toLowerCase()
  const base = step.includes('report') ? 0.74 : step.includes('round') || step.includes('agent') ? 0.61 : 0.47
  return clamp(base - index * 0.05, 0.24, 0.88)
}

function deriveVelocityLabel(value) {
  if (value == null) return 'medium'
  if (value >= 0.85) return 'very_fast'
  if (value >= 0.65) return 'fast'
  if (value >= 0.42) return 'medium'
  return 'steady'
}

function buildThinkingLine(label, dominantOutcome, runningStep, eventType) {
  const eventLabel = formatLabel(eventType || 'market event').toLowerCase()
  const statusText = {
    panic: 'is leaning defensive and scanning for capital-preservation cues',
    cautious: 'is balancing downside protection with selective positioning',
    optimistic: 'is leaning constructive and hunting for early beneficiaries',
    divided: 'is still split across competing interpretations of the event',
    confident: 'has built a strong conviction around the current read',
  }
  const stageText = runningStep
    ? ` Flow remains aligned to the current stage: ${runningStep}.`
    : ''
  return `${label} ${statusText[normalizeOutcome(dominantOutcome)] || statusText.cautious} as ${eventLabel} is processed.${stageText}`
}

function buildNodeThinking(label, dominantOutcome, runningStep, nodeIndex) {
  const variants = [
    'tracking headline drift versus sector sensitivity',
    'updating internal priors after cross-cohort signaling',
    'watching whether the first reaction is overextended',
    'balancing institutional cues against narrative momentum',
  ]
  const liveVariant = variants[(nodeIndex + Math.floor(tick.value / 8)) % variants.length]
  return `${label} node ${nodeIndex + 1} is ${liveVariant} and remains ${formatLabel(dominantOutcome)} while ${runningStep || 'the branch is still developing'}.`
}

function buildActionLine(dominantOutcome, eventType) {
  const eventLabel = formatLabel(eventType || 'general scenario').toLowerCase()
  const mapping = {
    panic: `Reduce risk exposure and watch for stress signals tied to ${eventLabel}.`,
    cautious: `Hold selective exposure and wait for stronger confirmation around ${eventLabel}.`,
    optimistic: `Rotate toward likely beneficiaries while liquidity remains supportive.`,
    divided: `Delay a full commitment and keep multiple scenarios open for ${eventLabel}.`,
    confident: `Lean into the highest-conviction read with tighter monitoring of invalidation signals.`,
  }
  return mapping[normalizeOutcome(dominantOutcome)] || mapping.cautious
}

function deriveTotalNodeBudget(agentCount) {
  const agents = Math.max(Number(agentCount) || 3, 1)
  const branches = Math.max(Number(props.config?.numBranches) || 1, 1)
  const rounds = Math.max(Number(props.config?.numRounds) || 2, 1)
  const densityScale = clamp(Number(props.config?.swarmNodeScale) || 1, 0.18, 1.2)
  return props.mode === 'running'
    ? clamp(
        Math.round((8 + agents * 7 + rounds * 5 + branches * 4) * densityScale),
        40,
        170
      )
    : clamp(
        Math.round((150 + agents * 20 + rounds * 12 + branches * 16) * densityScale),
        120,
        420
      )
}

function allocateNodeCounts(agentCount) {
  const totalNodes = deriveTotalNodeBudget(agentCount)
  const minPer = props.mode === 'running' ? 2 : 18
  const maxPer = props.mode === 'running' ? 22 : 110
  const populations = cohortData.value.map(item => Math.max(item.representedPopulation || 1, 1))
  const totalPopulation = populations.reduce((sum, value) => sum + value, 0) || 1
  const rawCounts = populations.map(population => (population / totalPopulation) * totalNodes)
  const counts = rawCounts.map(count => clamp(Math.floor(count), minPer, maxPer))
  let assigned = counts.reduce((sum, count) => sum + count, 0)

  if (assigned < totalNodes) {
    const remainderOrder = rawCounts
      .map((count, index) => ({ index, fraction: count - Math.floor(count) }))
      .sort((a, b) => b.fraction - a.fraction)

    let cursor = 0
    while (assigned < totalNodes && remainderOrder.length) {
      const candidate = remainderOrder[cursor % remainderOrder.length]?.index
      if (candidate == null) break
      if (counts[candidate] < maxPer) {
        counts[candidate] += 1
        assigned += 1
      }
      cursor += 1
      if (cursor > totalNodes * 3) break
    }
  } else if (assigned > totalNodes) {
    const reductionOrder = rawCounts
      .map((count, index) => ({ index, fraction: count - Math.floor(count) }))
      .sort((a, b) => a.fraction - b.fraction)

    let cursor = 0
    while (assigned > totalNodes && reductionOrder.length) {
      const candidate = reductionOrder[cursor % reductionOrder.length]?.index
      if (candidate == null) break
      if (counts[candidate] > minPer) {
        counts[candidate] -= 1
        assigned -= 1
      }
      cursor += 1
      if (cursor > totalNodes * 4) break
    }
  }

  return counts
}

function deriveNodeCount(population, cohortCount, agentCount) {
  const totalNodes = deriveTotalNodeBudget(agentCount)
  const scale = Math.max(population || 1, 1)
  const populations = cohortData.value.map(item => item.representedPopulation || 1)
  const totalPopulation = populations.reduce((sum, value) => sum + value, 0) || 1
  const weighted = Math.round((scale / totalPopulation) * totalNodes)
  return clamp(
    weighted || Math.round(totalNodes / Math.max(cohortCount, 1)),
    props.mode === 'running' ? 2 : 18,
    props.mode === 'running' ? 22 : 110
  )
}

function buildNodeDistribution(baseDistribution, dominantOutcome, confidence, nodeIndex) {
  const pulse = Math.sin(tick.value * 0.09 + nodeIndex * 0.33)
  const sway = 0.018 * pulse
  const distribution = {
    panic: baseDistribution?.panic || 0,
    cautious: baseDistribution?.cautious || 0,
    optimistic: baseDistribution?.optimistic || 0,
    divided: baseDistribution?.divided || 0,
  }

  if (dominantOutcome === 'panic') {
    distribution.panic += sway
    distribution.optimistic -= sway * 0.55
  } else if (dominantOutcome === 'optimistic') {
    distribution.optimistic += sway
    distribution.panic -= sway * 0.55
  } else if (dominantOutcome === 'divided') {
    distribution.divided += sway
    distribution.cautious -= sway * 0.35
  } else {
    distribution.cautious += sway
    distribution.divided -= sway * 0.4
  }

  const normalized = Object.fromEntries(
    Object.entries(distribution).map(([key, value]) => [key, Math.max(0.04, value)])
  )
  const total = Object.values(normalized).reduce((sum, value) => sum + value, 0) || 1
  return Object.fromEntries(
    Object.entries(normalized).map(([key, value]) => [key, round(value / total, 3)])
  )
}

function buildNodeActionLine(dominantOutcome, eventType, nodeIndex) {
  const cycle = Math.floor(tick.value / 10) + nodeIndex
  const actionSets = {
    panic: [
      `Cutting risk while monitoring spillover from ${formatLabel(eventType || 'general event').toLowerCase()}.`,
      'Rotating toward protection and faster liquidity.',
      'Watching whether stress signals broaden across connected cohorts.',
    ],
    cautious: [
      'Holding conviction but waiting for confirmation before a larger move.',
      'Comparing the first reaction against slower institutional flows.',
      'Filtering noise before leaning into a stronger position.',
    ],
    optimistic: [
      'Scanning for early beneficiaries and stronger narrative follow-through.',
      'Adding selective exposure where momentum looks durable.',
      'Checking whether cross-cohort confirmation supports a stronger upside read.',
    ],
    divided: [
      'Keeping multiple paths open while conflicting signals settle.',
      'Splitting attention across upside and downside branches.',
      'Waiting for one interpretation to dominate the field.',
    ],
    confident: [
      'Leaning into the highest-conviction path while watching invalidation signals.',
      'Pushing a stronger read into the network with tighter confidence control.',
      'Holding a concentrated view and testing whether others follow.',
    ],
  }
  const actions = actionSets[normalizeOutcome(dominantOutcome)] || actionSets.cautious
  return actions[cycle % actions.length]
}

function distributionRows(distribution) {
  return [
    { key: 'panic', label: 'Risk / Panic', percent: Math.round((distribution?.panic || 0) * 100), color: statusColors.panic },
    { key: 'cautious', label: 'Cautious', percent: Math.round((distribution?.cautious || 0) * 100), color: statusColors.cautious },
    { key: 'optimistic', label: 'Optimistic', percent: Math.round((distribution?.optimistic || 0) * 100), color: statusColors.optimistic },
    { key: 'divided', label: 'Divided', percent: Math.round((distribution?.divided || 0) * 100), color: statusColors.divided },
  ]
}

function agentNodeTransform(node) {
  return `translate(${node.x} ${node.y}) rotate(${node.rotation || 0}) scale(${node.iconScale || 1})`
}

function agentAnimationVars(node) {
  return {
    '--swarm-agent-aura-scale': round(node.auraScale || 1.14, 3),
    '--swarm-agent-aura-opacity': round(node.auraOpacity || 0.54, 2),
    '--swarm-agent-bar-opacity': round(node.barOpacity || 0.74, 2),
    '--swarm-agent-float-x': `${round(node.motionX || 0.18, 2)}px`,
    '--swarm-agent-float-y': `${round(node.motionY || 0.12, 2)}px`,
    '--swarm-agent-float-tilt': `${round(node.motionTilt || 0.14, 2)}deg`,
    '--swarm-agent-float-duration': `${round(node.floatDuration || 6.2, 2)}s`,
    '--swarm-agent-vibe-duration': `${round(node.vibeDuration || 1.56, 2)}s`,
    '--swarm-agent-vibe-x': `${round(node.vibeX || 0.08, 2)}px`,
    '--swarm-agent-vibe-y': `${round(node.vibeY || 0.06, 2)}px`,
    '--swarm-agent-breathe-duration': `${round(node.breatheDuration || 3.4, 2)}s`,
    '--swarm-agent-blink-duration': `${round(node.blinkDuration || 6.2, 2)}s`,
    '--swarm-agent-sheen-duration': `${round(node.sheenDuration || 5.8, 2)}s`,
    '--swarm-agent-delay': `${round(node.motionDelay || 0, 2)}s`,
    '--swarm-agent-blink-delay': `${round(node.blinkDelay || 0, 2)}s`,
    '--swarm-agent-sheen-delay': `${round(node.sheenDelay || 0, 2)}s`,
    '--swarm-agent-sheen-opacity': round(node.sheenOpacity || 0.2, 2),
  }
}

function senderSignal(nodeId) {
  return senderSignalMap.value.get(nodeId) || null
}

function receiverSignal(nodeId) {
  return receiverSignalMap.value.get(nodeId) || null
}

function seededNumber(seed) {
  let hash = 0
  for (let i = 0; i < seed.length; i += 1) {
    hash = ((hash << 5) - hash) + seed.charCodeAt(i)
    hash |= 0
  }
  return Math.abs(Math.sin(hash) * 10000) % 1
}

function withOpacity(hex, opacity) {
  const clean = hex.replace('#', '')
  const bigint = Number.parseInt(clean, 16)
  const r = (bigint >> 16) & 255
  const g = (bigint >> 8) & 255
  const b = bigint & 255
  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}

function shadeHex(hex, amount = 0) {
  const clean = hex.replace('#', '')
  const bigint = Number.parseInt(clean, 16)
  const shift = Math.round(255 * amount)
  const r = clamp(((bigint >> 16) & 255) + shift, 0, 255)
  const g = clamp(((bigint >> 8) & 255) + shift, 0, 255)
  const b = clamp((bigint & 255) + shift, 0, 255)
  return `#${[r, g, b].map(value => value.toString(16).padStart(2, '0')).join('')}`
}

function gradientId(id) {
  return `swarm-grad-${String(id || 'node').toLowerCase().replace(/[^a-z0-9]+/g, '-')}`
}

function truncateText(value, maxLength = 120) {
  const text = String(value || '').trim()
  if (!text) return ''
  return text.length > maxLength ? `${text.slice(0, maxLength - 3).trim()}...` : text
}

function formatLabel(value) {
  return String(value || '')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, letter => letter.toUpperCase())
}

function formatPopulation(value) {
  const numeric = Number(value || 0)
  if (numeric >= 10_000_000) return `${(numeric / 10_000_000).toFixed(1)}Cr`
  if (numeric >= 100_000) return `${(numeric / 100_000).toFixed(1)}L`
  if (numeric >= 1_000) return `${(numeric / 1_000).toFixed(1)}K`
  return `${numeric}`
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value))
}

function round(value, digits = 2) {
  const factor = 10 ** digits
  return Math.round(value * factor) / factor
}

function computePopupCoords(event) {
  const boxWidth = 338
  const boxHeight = 402
  const viewportWidth = window.innerWidth || 1440
  const viewportHeight = window.innerHeight || 900
  const clientX = event?.clientX ?? 80
  const clientY = event?.clientY ?? 120
  const left = clamp(clientX + 18, 12, viewportWidth - boxWidth - 12)
  const top = clientY > viewportHeight * 0.55
    ? clamp(clientY - boxHeight - 18, 12, viewportHeight - boxHeight - 12)
    : clamp(clientY + 18, 12, viewportHeight - boxHeight - 12)
  return {
    left: `${left}px`,
    top: `${top}px`,
  }
}

function swarmContentMetrics() {
  const nodes = renderedNodes.value
  if (!nodes.length) return null

  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity

  nodes.forEach(node => {
    const extentX = Math.max(12, 13.5 * (node.iconScale || 1))
    const extentY = Math.max(10, 11.5 * (node.iconScale || 1))
    minX = Math.min(minX, node.x - extentX)
    maxX = Math.max(maxX, node.x + extentX)
    minY = Math.min(minY, node.y - extentY)
    maxY = Math.max(maxY, node.y + extentY)
  })

  const boundsWidth = Math.max(1, maxX - minX)
  const boundsHeight = Math.max(1, maxY - minY)
  const paddingX = props.mode === 'running' ? 30 : 36
  const paddingY = props.mode === 'running' ? 30 : 42
  const fitZoom = Math.min(
    Math.max((boardWidth.value - paddingX * 2) / boundsWidth, 0.08),
    Math.max((boardHeight.value - paddingY * 2) / boundsHeight, 0.08)
  )

  return {
    minX,
    maxX,
    minY,
    maxY,
    centerX: (minX + maxX) / 2,
    centerY: (minY + maxY) / 2,
    fitZoom,
  }
}

function swarmConfiguredZoomBounds() {
  return {
    minZoom: Number(props.config?.swarmMinZoom) || (props.mode === 'running' ? 2.02 : 1.62),
    maxZoom: Number(props.config?.swarmMaxZoom) || (props.mode === 'running' ? 2.88 : 2.32),
  }
}

function swarmDefaultViewportZoom(metrics = swarmContentMetrics()) {
  if (!metrics) {
    return Number(props.config?.swarmDefaultZoom) || (props.mode === 'running' ? 2.22 : 1.94)
  }

  const { minZoom, maxZoom } = swarmConfiguredZoomBounds()
  const zoomMultiplier = Number(props.config?.swarmZoomMultiplier) || (props.mode === 'running' ? 1.46 : 1.3)
  return clamp(
    metrics.fitZoom * zoomMultiplier,
    minZoom,
    maxZoom
  )
}

function swarmZoomOutLimit() {
  const metrics = swarmContentMetrics()
  if (!metrics) return 0.7
  return Math.max(0.7, Math.min(metrics.fitZoom, swarmDefaultViewportZoom(metrics)))
}

function fitSwarmToViewport(targetZoom = null) {
  const metrics = swarmContentMetrics()
  if (!metrics) return
  const minZoom = swarmZoomOutLimit()
  zoom.value = clamp(targetZoom == null ? minZoom : targetZoom, minZoom, 3.4)
  pan.value = {
    x: Math.round(boardWidth.value / 2 - metrics.centerX * zoom.value),
    y: Math.round(boardHeight.value / 2 - metrics.centerY * zoom.value),
  }
}

function swarmViewportCenter() {
  return {
    x: boardWidth.value / 2,
    y: boardHeight.value / 2,
  }
}

function setSwarmZoomFromViewportCenter(nextZoom) {
  const center = swarmViewportCenter()
  const contentX = (center.x - pan.value.x) / zoom.value
  const contentY = (center.y - pan.value.y) / zoom.value
  zoom.value = nextZoom
  pan.value = {
    x: Math.round(center.x - contentX * zoom.value),
    y: Math.round(center.y - contentY * zoom.value),
  }
}

function zoomIn() {
  setSwarmZoomFromViewportCenter(clamp(round(zoom.value + 0.12, 2), swarmZoomOutLimit(), 3.4))
}

function zoomOut() {
  const minZoom = swarmZoomOutLimit()
  const targetZoom = clamp(round(zoom.value - 0.12, 2), minZoom, 3.4)
  if (targetZoom <= minZoom + 0.0001) {
    fitSwarmToViewport(minZoom)
    return
  }
  setSwarmZoomFromViewportCenter(targetZoom)
}

function resetViewport() {
  applyDefaultViewport()
}

function applyDefaultViewport() {
  const centerOnLoad = props.config?.swarmCenterOnLoad !== false
  const nodes = renderedNodes.value
  if (!nodes.length) {
    const defaultZoom = Number(props.config?.swarmDefaultZoom) || (props.mode === 'running' ? 2.22 : 1.94)
    zoom.value = defaultZoom
    pan.value = {
      x: Math.round(centerOnLoad
        ? (boardWidth.value / 2 - (boardWidth.value / 2) * defaultZoom)
        : -boardWidth.value * (defaultZoom - 1) * (props.mode === 'running' ? 0.24 : 0.28)),
      y: Math.round(centerOnLoad
        ? (boardHeight.value / 2 - (boardHeight.value / 2) * defaultZoom)
        : -boardHeight.value * (defaultZoom - 1) * (props.mode === 'running' ? 0.08 : 0.14)),
    }
    return
  }

  const xs = nodes.map(node => node.x)
  const ys = nodes.map(node => node.y)
  const minX = Math.min(...xs)
  const maxX = Math.max(...xs)
  const minY = Math.min(...ys)
  const maxY = Math.max(...ys)
  const boundsWidth = Math.max(1, maxX - minX)
  const boundsHeight = Math.max(1, maxY - minY)
  const fitScale = Math.min(
    (boardWidth.value - (props.mode === 'running' ? 92 : 104)) / boundsWidth,
    (boardHeight.value - (props.mode === 'running' ? 92 : 126)) / boundsHeight
  )
  const zoomMultiplier = Number(props.config?.swarmZoomMultiplier) || (props.mode === 'running' ? 1.46 : 1.3)
  const { minZoom, maxZoom } = swarmConfiguredZoomBounds()
  const defaultZoom = clamp(
    fitScale * zoomMultiplier,
    minZoom,
    maxZoom
  )
  const centerX = (minX + maxX) / 2
  const centerY = (minY + maxY) / 2

  zoom.value = defaultZoom
  const desiredX = boardWidth.value / 2 - centerX * defaultZoom
  const desiredY = boardHeight.value / 2 - centerY * defaultZoom
  if (centerOnLoad) {
    pan.value = {
      x: Math.round(desiredX),
      y: Math.round(desiredY),
    }
    return
  }
  const padding = props.mode === 'running' ? 30 : 36
  const minPanX = boardWidth.value - maxX * defaultZoom - padding
  const maxPanX = -minX * defaultZoom + padding
  const minPanY = boardHeight.value - maxY * defaultZoom - padding
  const maxPanY = -minY * defaultZoom + padding
  pan.value = {
    x: Math.round(clamp(desiredX, Math.min(minPanX, maxPanX), Math.max(minPanX, maxPanX))),
    y: Math.round(clamp(desiredY, Math.min(minPanY, maxPanY), Math.max(minPanY, maxPanY))),
  }
}

function startPan(event) {
  if (event.target?.closest?.('.swarm-agent')) return
  isPanning.value = true
  panStart.value = {
    x: event.clientX,
    y: event.clientY,
    panX: pan.value.x,
    panY: pan.value.y,
  }
}

function onPanMove(event) {
  if (!isPanning.value || !boardRef.value) return
  const rect = boardRef.value.getBoundingClientRect()
  const scaleX = boardWidth.value / Math.max(rect.width, 1)
  const scaleY = boardHeight.value / Math.max(rect.height, 1)
  const dx = (event.clientX - panStart.value.x) * scaleX
  const dy = (event.clientY - panStart.value.y) * scaleY
  pan.value = {
    x: panStart.value.panX + dx,
    y: panStart.value.panY + dy,
  }
}

function stopPan() {
  isPanning.value = false
}

function onWheel(event) {
  const direction = event.deltaY > 0 ? -0.1 : 0.1
  if (direction < 0) {
    const minZoom = swarmZoomOutLimit()
    const targetZoom = clamp(round(zoom.value + direction, 2), minZoom, 2.6)
    if (targetZoom <= minZoom + 0.0001) {
      fitSwarmToViewport(minZoom)
      return
    }
    setSwarmZoomFromViewportCenter(targetZoom)
    return
  }

  setSwarmZoomFromViewportCenter(clamp(round(zoom.value + direction, 2), swarmZoomOutLimit(), 2.6))
}
</script>

<style scoped>
.swarm-shell {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 100%;
  height: 100%;
}

.swarm-shell:fullscreen {
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  padding: 16px;
  box-sizing: border-box;
  gap: 12px;
  background: rgba(255, 252, 247, 0.99);
}

.swarm-shell:fullscreen .swarm-board {
  min-height: 0;
  flex: 1;
}

.swarm-shell:fullscreen .swarm-node-popup {
  max-height: calc(100vh - 48px);
  overflow: auto;
}

.swarm-shell-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  flex-wrap: wrap;
  padding-left: 10px;
  padding-right: 6px;
}

.swarm-shell-label {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(116, 88, 69, 0.7);
  margin-bottom: 6px;
}

.swarm-shell-title {
  font-size: 22px;
  line-height: 1.1;
  font-weight: 800;
  color: #2e211b;
}

.swarm-chip-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.swarm-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 9px 14px;
  border: 1px solid rgba(137, 169, 231, 0.34);
  background: rgba(248, 251, 255, 0.86);
  font-size: 13px;
  color: #675241;
}

.swarm-chip-button {
  font-family: inherit;
  cursor: pointer;
  min-width: 44px;
}

.swarm-board {
  flex: 1;
  position: relative;
  min-height: 680px;
  border-radius: 28px;
  overflow: hidden;
  border: 1px solid rgba(232, 206, 182, 0.78);
  background:
    radial-gradient(circle at 18% 14%, rgba(247, 186, 89, 0.16), transparent 32%),
    radial-gradient(circle at 82% 12%, rgba(108, 187, 255, 0.14), transparent 28%),
    radial-gradient(circle at 50% 88%, rgba(154, 118, 255, 0.09), transparent 26%),
    rgba(255, 252, 247, 0.96);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.82),
    0 28px 48px rgba(160, 106, 69, 0.12);
}

.mode-running .swarm-board {
  background:
    radial-gradient(circle, rgba(188, 182, 177, 0.22) 1.2px, transparent 1.5px),
    #fefdfb;
  background-size: 20px 20px, auto;
}

.mode-results .swarm-board {
  min-height: 800px;
}

.mode-running .swarm-board {
  min-height: 500px;
}

.swarm-svg {
  width: 100%;
  height: 100%;
  display: block;
  cursor: grab;
}

.swarm-svg:active {
  cursor: grabbing;
}

.swarm-board-bg {
  fill: rgba(255, 252, 247, 0.14);
}

.mode-running .swarm-board-bg {
  fill: rgba(255, 255, 255, 0.02);
}

.swarm-grid-line {
  stroke: rgba(194, 165, 142, 0.16);
  stroke-width: 1;
}

.swarm-classification-cells {
  mix-blend-mode: multiply;
}

.swarm-node {
  opacity: 0.92;
  cursor: pointer;
  transition: r 180ms ease, opacity 180ms ease, filter 180ms ease, stroke-width 180ms ease;
}

.swarm-agent {
  cursor: pointer;
  transition: opacity 220ms ease, filter 220ms ease;
  transform-origin: center;
}

.swarm-agent-body,
.swarm-agent-core,
.swarm-agent-aura,
.swarm-agent-core-bar,
.swarm-agent-eye,
.swarm-agent-visor-sheen {
  transform-box: fill-box;
  transform-origin: center;
}

.swarm-agent-body {
  animation: swarmAgentFloat var(--swarm-agent-float-duration, 6.2s) cubic-bezier(0.37, 0, 0.23, 1) infinite;
  animation-delay: var(--swarm-agent-delay, 0s);
}

.swarm-agent-core {
  animation: swarmAgentVibe var(--swarm-agent-vibe-duration, 1.56s) ease-in-out infinite;
  animation-delay: var(--swarm-agent-delay, 0s);
}

.swarm-agent.selected,
.swarm-agent:hover {
  filter: url(#swarm-node-glow);
}

.swarm-agent.active {
  animation: swarmAgentGlow 2.4s ease-in-out infinite;
}

.swarm-agent.dimmed {
  opacity: 0.74;
}

.swarm-agent-head,
.swarm-agent-base,
.swarm-agent-side {
  vector-effect: non-scaling-stroke;
}

.swarm-agent-eye {
  animation: swarmAgentBlink var(--swarm-agent-blink-duration, 6.8s) linear infinite;
  animation-delay: var(--swarm-agent-blink-delay, 0s);
}

.swarm-agent-aura {
  opacity: 0.18;
  filter: blur(0.35px);
  animation: swarmAgentAura var(--swarm-agent-breathe-duration, 3.4s) ease-in-out infinite;
  animation-delay: var(--swarm-agent-delay, 0s);
}

.swarm-agent-core-bar {
  opacity: 0.62;
  mix-blend-mode: screen;
  animation: swarmAgentCoreBar calc(var(--swarm-agent-breathe-duration, 3.4s) * 0.92) ease-in-out infinite;
  animation-delay: var(--swarm-agent-delay, 0s);
}

.swarm-agent-visor-sheen {
  opacity: 0;
  mix-blend-mode: screen;
  animation: swarmAgentVisorSheen var(--swarm-agent-sheen-duration, 5.8s) ease-in-out infinite;
  animation-delay: var(--swarm-agent-sheen-delay, 0s);
}

.swarm-node:hover,
.swarm-node.selected {
  opacity: 1;
  filter: url(#swarm-node-glow);
}

.swarm-node.active {
  filter: url(#swarm-node-glow);
  animation: swarmNodePulse 1.1s ease-in-out infinite;
}

.swarm-node.dimmed {
  opacity: 0.64;
}

.swarm-node.selected {
  stroke: rgba(255, 255, 255, 0.92);
  stroke-width: 1.2;
}

.swarm-link {
  transition: opacity 180ms ease, stroke 180ms ease, stroke-width 180ms ease;
}

.swarm-link.active {
  animation: swarmLinkPulse 1.2s ease-in-out infinite;
}

.swarm-link.dimmed {
  opacity: 0.1;
}

.swarm-agent-signal {
  pointer-events: none;
}

.swarm-agent-send-halo,
.swarm-agent-receive-halo {
  opacity: 0.22;
  animation: swarmAgentSignalHalo 1.9s ease-in-out infinite;
  animation-delay: var(--swarm-agent-signal-delay, 0s);
}

.swarm-agent-send-chevron,
.swarm-agent-receive-chevron {
  fill: none;
  stroke-width: 0.9;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.7;
  filter: drop-shadow(0 0 6px rgba(124, 116, 255, 0.18));
  animation: swarmAgentSignalTrace 1.9s ease-in-out infinite;
  animation-delay: var(--swarm-agent-signal-delay, 0s);
}

.swarm-agent-receive-chevron {
  animation-delay: calc(var(--swarm-agent-signal-delay, 0s) + 0.12s);
}

.swarm-agent-send-core,
.swarm-agent-receive-core {
  filter: drop-shadow(0 0 8px rgba(124, 116, 255, 0.22));
  animation: swarmAgentSignalOrb 1.9s ease-in-out infinite;
  animation-delay: var(--swarm-agent-signal-delay, 0s);
}

.swarm-agent-send-pulse,
.swarm-agent-receive-pulse {
  filter: drop-shadow(0 0 7px rgba(124, 116, 255, 0.2));
  animation-delay: var(--swarm-agent-signal-delay, 0s);
}

.swarm-agent-send-pulse {
  animation: swarmAgentSignalPulse 1.8s ease-out infinite;
}

.swarm-agent-receive-pulse {
  animation: swarmAgentReceivePulse 1.7s ease-in infinite;
}

.swarm-agent-send-pulse-left {
  animation-delay: calc(var(--swarm-agent-signal-delay, 0s) + 0.08s);
}

.swarm-agent-send-pulse-right {
  animation-delay: calc(var(--swarm-agent-signal-delay, 0s) + 0.16s);
}

.swarm-agent-receive-chevron-inner {
  opacity: 0.78;
  animation-delay: calc(var(--swarm-agent-signal-delay, 0s) + 0.08s);
}

.swarm-node-popup {
  position: fixed;
  width: 338px;
  min-height: 360px;
  padding: 14px 14px 13px;
  border-radius: 18px;
  background: rgba(255, 252, 248, 0.95);
  border: 1px solid rgba(228, 205, 184, 0.95);
  box-shadow: 0 22px 44px rgba(92, 62, 46, 0.16);
  backdrop-filter: blur(14px);
  z-index: 3;
  overflow: hidden;
}

.swarm-legend-overlay {
  position: absolute;
  left: 16px;
  right: auto;
  bottom: 16px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  width: min(396px, calc(100% - 32px));
  z-index: 2;
  pointer-events: auto;
}

.swarm-legend-overlay.results-overlay {
  left: 14px;
  right: 14px;
  bottom: 14px;
  width: auto;
  grid-template-columns: minmax(320px, 1.1fr) minmax(320px, 1fr);
}

.swarm-legend-overlay.running-overlay {
  left: 18px;
  right: auto;
  width: min(940px, calc(100% - 36px));
  grid-template-columns: minmax(0, 1.16fr) minmax(0, 0.84fr);
  align-items: start;
}

@keyframes swarmNodePulse {
  0% { filter: url(#swarm-node-glow); }
  50% { filter: url(#swarm-node-glow); }
  100% { filter: url(#swarm-node-glow); }
}

@keyframes swarmAgentGlow {
  0% { opacity: 0.94; filter: url(#swarm-node-glow); }
  50% { opacity: 1; filter: url(#swarm-node-glow); }
  100% { opacity: 0.94; filter: url(#swarm-node-glow); }
}

@keyframes swarmAgentFloat {
  0% {
    transform: translate(0px, 0px) rotate(calc(var(--swarm-agent-float-tilt, 0.14deg) * -0.2));
  }
  24% {
    transform: translate(var(--swarm-agent-float-x, 0.18px), calc(var(--swarm-agent-float-y, 0.12px) * -1)) rotate(var(--swarm-agent-float-tilt, 0.14deg));
  }
  52% {
    transform: translate(calc(var(--swarm-agent-float-x, 0.18px) * -0.65), calc(var(--swarm-agent-float-y, 0.12px) * 0.18)) rotate(calc(var(--swarm-agent-float-tilt, 0.14deg) * -0.56));
  }
  78% {
    transform: translate(calc(var(--swarm-agent-float-x, 0.18px) * 0.28), calc(var(--swarm-agent-float-y, 0.12px) * -0.48)) rotate(calc(var(--swarm-agent-float-tilt, 0.14deg) * 0.34));
  }
  100% {
    transform: translate(0px, 0px) rotate(calc(var(--swarm-agent-float-tilt, 0.14deg) * -0.2));
  }
}

@keyframes swarmAgentVibe {
  0%, 100% {
    transform: translate(0px, 0px);
  }
  18% {
    transform: translate(var(--swarm-agent-vibe-x, 0.08px), calc(var(--swarm-agent-vibe-y, 0.06px) * -1));
  }
  34% {
    transform: translate(calc(var(--swarm-agent-vibe-x, 0.08px) * -0.72), var(--swarm-agent-vibe-y, 0.06px));
  }
  53% {
    transform: translate(calc(var(--swarm-agent-vibe-x, 0.08px) * 0.42), calc(var(--swarm-agent-vibe-y, 0.06px) * -0.42));
  }
  76% {
    transform: translate(calc(var(--swarm-agent-vibe-x, 0.08px) * -0.38), calc(var(--swarm-agent-vibe-y, 0.06px) * 0.24));
  }
}

@keyframes swarmAgentAura {
  0% {
    opacity: calc(var(--swarm-agent-aura-opacity, 0.54) * 0.48);
    transform: scale(0.92);
  }
  50% {
    opacity: var(--swarm-agent-aura-opacity, 0.54);
    transform: scale(var(--swarm-agent-aura-scale, 1.14));
  }
  100% {
    opacity: calc(var(--swarm-agent-aura-opacity, 0.54) * 0.48);
    transform: scale(0.92);
  }
}

@keyframes swarmAgentCoreBar {
  0% {
    opacity: calc(var(--swarm-agent-bar-opacity, 0.74) * 0.52);
    transform: scaleX(0.76);
  }
  50% {
    opacity: var(--swarm-agent-bar-opacity, 0.74);
    transform: scaleX(1.06);
  }
  100% {
    opacity: calc(var(--swarm-agent-bar-opacity, 0.74) * 0.52);
    transform: scaleX(0.76);
  }
}

@keyframes swarmAgentBlink {
  0%, 42%, 46%, 73%, 77%, 100% {
    transform: scaleY(1);
    opacity: 1;
  }
  43%, 45%, 74%, 76% {
    transform: scaleY(0.16);
    opacity: 0.78;
  }
}

@keyframes swarmAgentVisorSheen {
  0%, 18% {
    transform: translateX(-2.8px) rotate(16deg);
    opacity: 0;
  }
  32% {
    opacity: calc(var(--swarm-agent-sheen-opacity, 0.2) * 0.72);
  }
  50% {
    transform: translateX(4.8px) rotate(16deg);
    opacity: var(--swarm-agent-sheen-opacity, 0.2);
  }
  64%, 100% {
    transform: translateX(5.2px) rotate(16deg);
    opacity: 0;
  }
}

@keyframes swarmLinkPulse {
  0% { opacity: 0.7; }
  50% { opacity: 1; }
  100% { opacity: 0.7; }
}

@keyframes swarmSocialPulse {
  0% { opacity: 0.16; }
  50% { opacity: 0.42; }
  100% { opacity: 0.16; }
}

@keyframes swarmAgentSignalHalo {
  0%, 100% {
    opacity: 0.16;
    transform: scale(0.9);
  }
  50% {
    opacity: 0.34;
    transform: scale(1.08);
  }
}

@keyframes swarmAgentSignalTrace {
  0%, 100% {
    opacity: 0.42;
    transform: translateY(0px) scaleX(0.94);
  }
  50% {
    opacity: 0.88;
    transform: translateY(-0.5px) scaleX(1.04);
  }
}

@keyframes swarmAgentSignalOrb {
  0%, 100% {
    opacity: 0.56;
    transform: scale(0.92);
  }
  50% {
    opacity: 1;
    transform: scale(1.16);
  }
}

@keyframes swarmAgentSignalPulse {
  0% {
    opacity: 0.18;
    transform: translateY(0px) scale(0.7);
  }
  40% {
    opacity: 0.92;
    transform: translateY(-1.35px) scale(1.02);
  }
  100% {
    opacity: 0;
    transform: translateY(-4.9px) scale(1.18);
  }
}

@keyframes swarmAgentReceivePulse {
  0% {
    opacity: 0.12;
    transform: translateY(-3.6px) scale(0.72);
  }
  46% {
    opacity: 0.92;
    transform: translateY(-0.55px) scale(1);
  }
  100% {
    opacity: 0.08;
    transform: translateY(1.6px) scale(0.82);
  }
}

.popup-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 6px;
}

.popup-type {
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(116, 88, 69, 0.72);
}

.popup-close {
  border: 0;
  background: transparent;
  color: rgba(116, 88, 69, 0.72);
  cursor: pointer;
  font-size: 13px;
}

.popup-title {
  font-size: 20px;
  line-height: 1.08;
  font-weight: 800;
  color: #2d201a;
  margin-bottom: 9px;
  min-height: 40px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.popup-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 10px;
}

.popup-chip {
  display: inline-flex;
  align-items: center;
  padding: 6px 9px;
  border-radius: 999px;
  border: 1px solid;
  background: rgba(255, 255, 255, 0.82);
  font-size: 10px;
  font-weight: 600;
}

.popup-chip-muted {
  border-color: rgba(197, 179, 162, 0.76);
  color: #6d5647;
}

.popup-block {
  margin-bottom: 10px;
  min-height: 64px;
}

.popup-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(116, 88, 69, 0.72);
  margin-bottom: 5px;
}

.popup-block p,
.popup-thinking {
  margin: 0;
  font-size: 11px;
  line-height: 1.46;
  color: #59483e;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.popup-inline-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: 10px;
  align-items: stretch;
}

.popup-inline-card {
  padding: 10px 10px 9px;
  border-radius: 13px;
  border: 1px solid rgba(222, 210, 197, 0.76);
  background: rgba(255, 255, 255, 0.74);
  min-height: 96px;
  overflow: hidden;
}

.popup-inline-label {
  display: block;
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(116, 88, 69, 0.68);
  margin-bottom: 5px;
}

.popup-inline-card strong {
  display: block;
  font-size: 11px;
  line-height: 1.38;
  color: #34261f;
}

.popup-inline-value {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.popup-metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: 10px;
}

.popup-metric {
  padding: 10px 10px;
  border-radius: 13px;
  background: rgba(247, 249, 255, 0.72);
  border: 1px solid rgba(209, 221, 245, 0.66);
}

.popup-metric-label {
  display: block;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(116, 88, 69, 0.72);
  margin-bottom: 5px;
}

.popup-metric strong {
  font-size: 13px;
  color: #2d201a;
}

.popup-distribution {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.popup-distribution-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.popup-distribution-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10px;
  color: #5d4a3e;
  gap: 8px;
}

.popup-distribution-head span:first-child {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.popup-bar-track {
  width: 100%;
  height: 5px;
  border-radius: 999px;
  background: rgba(223, 214, 204, 0.44);
  overflow: hidden;
}

.popup-bar-fill {
  height: 100%;
  border-radius: inherit;
}

.legend-section {
  padding: 14px 16px;
  border-radius: 18px;
  border: 1px solid rgba(232, 206, 182, 0.72);
  background: rgba(255, 251, 246, 0.84);
}

.legend-section-compact {
  padding: 9px 10px;
  background: rgba(255, 251, 246, 0.54);
  backdrop-filter: blur(30px);
  box-shadow: 0 12px 28px rgba(160, 106, 69, 0.1);
}

.mode-results .legend-pills-cohorts,
.mode-results .legend-pills-status {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.legend-title {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(116, 88, 69, 0.72);
  margin-bottom: 8px;
}

.legend-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.mode-running .legend-pills-cohorts {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px 8px;
}

.mode-running .legend-pills-status {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 8px;
}

.legend-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(227, 207, 191, 0.72);
  font-size: 11.5px;
  color: #5c493d;
  white-space: normal;
  flex: 0 0 auto;
  min-height: 38px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ── Theme Refresh ─────────────────────────────────────────────────────── */
.swarm-shell {
  --swarm-surface: rgba(255, 255, 255, 0.9);
  --swarm-surface-soft: rgba(246, 249, 255, 0.9);
  --swarm-panel: rgba(249, 251, 255, 0.94);
  --swarm-border: rgba(145, 163, 226, 0.24);
  --swarm-border-strong: rgba(145, 163, 226, 0.38);
  --swarm-shadow: rgba(92, 110, 176, 0.13);
  --swarm-text: #263250;
  --swarm-muted: #6f7b9a;
}

.swarm-shell:fullscreen {
  background: rgba(247, 249, 255, 0.99);
}

.swarm-shell-label,
.popup-type,
.popup-label,
.popup-inline-label,
.popup-metric-label,
.legend-title {
  color: rgba(111, 123, 154, 0.78);
}

.swarm-shell-title,
.popup-title,
.popup-metric strong {
  color: var(--swarm-text);
}

.swarm-chip {
  border-color: rgba(145, 163, 226, 0.28);
  background: rgba(248, 251, 255, 0.9);
  color: var(--swarm-muted);
}

.swarm-board {
  border-color: rgba(145, 163, 226, 0.24);
  background:
    radial-gradient(circle at 18% 14%, rgba(114, 201, 255, 0.14), transparent 32%),
    radial-gradient(circle at 84% 16%, rgba(181, 145, 255, 0.14), transparent 28%),
    radial-gradient(circle at 52% 88%, rgba(103, 224, 236, 0.08), transparent 26%),
    rgba(250, 252, 255, 0.98);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.88),
    0 30px 54px rgba(95, 112, 180, 0.12);
}

.mode-running .swarm-board {
  background:
    radial-gradient(circle, rgba(166, 178, 221, 0.24) 1.2px, transparent 1.45px),
    #fbfcff;
}

.swarm-board-bg {
  fill: rgba(245, 248, 255, 0.16);
}

.swarm-grid-line {
  stroke: rgba(162, 176, 220, 0.18);
}

.swarm-link.active {
  animation: swarmLinkPulse 1.2s ease-in-out infinite;
}

.swarm-node-popup {
  background: rgba(249, 251, 255, 0.95);
  border-color: rgba(145, 163, 226, 0.28);
  box-shadow: 0 24px 46px rgba(95, 112, 180, 0.16);
}

.popup-close,
.popup-chip-muted,
.popup-block p,
.popup-thinking,
.popup-distribution-head,
.legend-pill {
  color: var(--swarm-muted);
}

.popup-inline-card strong {
  color: var(--swarm-text);
}

.popup-chip {
  background: rgba(255, 255, 255, 0.9);
}

.popup-chip-muted {
  border-color: rgba(180, 193, 230, 0.7);
}

.popup-inline-card {
  border-color: rgba(145, 163, 226, 0.18);
  background: rgba(255, 255, 255, 0.82);
}

.popup-metric {
  background: rgba(244, 248, 255, 0.92);
  border-color: rgba(145, 163, 226, 0.24);
}

.popup-bar-track {
  background: rgba(207, 216, 243, 0.5);
}

.legend-section {
  border-color: rgba(145, 163, 226, 0.22);
  background: rgba(249, 251, 255, 0.86);
}

.legend-section-compact {
  background: rgba(249, 251, 255, 0.58);
  box-shadow: 0 14px 30px rgba(95, 112, 180, 0.12);
}

.legend-pill {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(145, 163, 226, 0.2);
}

.swarm-agent-send-chevron,
.swarm-agent-send-core,
.swarm-agent-send-pulse {
  filter: drop-shadow(0 0 7px rgba(178, 144, 255, 0.26));
}

.swarm-agent-receive-chevron,
.swarm-agent-receive-core,
.swarm-agent-receive-pulse {
  filter: drop-shadow(0 0 7px rgba(111, 215, 255, 0.24));
}

@media (max-width: 1200px) {
  .swarm-board {
    min-height: 580px;
  }

  .swarm-node-popup {
    width: min(338px, calc(100% - 24px));
  }
}

@media (max-width: 900px) {
  .swarm-legend-overlay {
    width: calc(100% - 24px);
    grid-template-columns: 1fr;
  }

  .mode-results .legend-pills-cohorts,
  .mode-results .legend-pills-status,
  .mode-running .legend-pills-cohorts,
  .mode-running .legend-pills-status {
    grid-template-columns: 1fr;
  }

  .swarm-shell-title {
    font-size: 20px;
  }

  .swarm-board {
    min-height: 520px;
  }
}
</style>
