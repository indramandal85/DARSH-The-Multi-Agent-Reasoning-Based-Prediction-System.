<template>
  <div
    ref="viewerRoot"
    class="graph-viewer"
    :class="[{ 'dense-mode': denseMode }, denseMode ? `dense-preset-${densePreset}` : '']"
    :style="viewerStyle"
    @click="clearSelection"
  >

    <!-- Header -->
    <div class="gv-header">
      <div class="gv-title">
        {{ graphName || 'Knowledge Graph' }}
        <span class="gv-counts">
          {{ nodeCount }} entities · {{ linkCount }} relationships
        </span>
      </div>
      <div class="gv-search">
        <input
          v-model="searchTerm"
          type="text"
          class="gv-search-input"
          placeholder="Search entity, company, event..."
        />
      </div>
      <div class="gv-controls">
        <button
          class="mode-btn"
          :class="{ active: viewMode === 'knowledge' }"
          @click="setMode('knowledge')"
        >
          Knowledge Graph
        </button>
        <button
          v-if="hasCausal"
          class="mode-btn"
          :class="{ active: viewMode === 'causal' }"
          @click="setMode('causal')"
        >
          Causal DAG
        </button>
        <button class="icon-btn" @click="focusMatches" title="Focus matched nodes">◎</button>
        <button class="icon-btn" @click="resetZoom" title="Reset zoom">⌖</button>
        <button class="icon-btn" @click="toggleFullscreen" :title="isFullscreen ? 'Exit fullscreen' : 'Open fullscreen'">⛶</button>
      </div>
    </div>

    <div class="gv-stat-strip">
      <div class="gv-stat">
        <span class="gv-stat-label">Mode</span>
        <span class="gv-stat-value">{{ viewMode === 'causal' ? 'Causal DAG' : 'Knowledge Graph' }}</span>
      </div>
      <div class="gv-stat">
        <span class="gv-stat-label">Matches</span>
        <span class="gv-stat-value">{{ matchedNodeCount }}</span>
      </div>
      <div class="gv-stat">
        <span class="gv-stat-label">Inspector</span>
        <span class="gv-stat-value">{{ selectedNode ? 'Node' : selectedLink ? 'Relation' : 'Idle' }}</span>
      </div>
    </div>

    <!-- Graph canvas -->
    <div ref="canvasWrapper" class="gv-canvas" :style="canvasStyle" @click="clearSelection">
      <svg ref="svgEl" width="100%" :height="svgHeight">
        <defs>
          <filter id="gv-node-bubble-shadow" x="-120%" y="-120%" width="340%" height="340%">
            <feDropShadow dx="0" dy="1.4" stdDeviation="1.8" flood-color="rgba(59,43,33,0.16)" />
          </filter>
          <marker id="arrow-kg" viewBox="0 0 10 6" refX="18" refY="3"
                  markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0 0 L10 3 L0 6 z" fill="#3a3f47"/>
          </marker>
          <marker id="arrow-causal" viewBox="0 0 10 6" refX="18" refY="3"
                  markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0 0 L10 3 L0 6 z" fill="#b58fff"/>
          </marker>
          <radialGradient
            v-for="palette in nodeBubblePalettes"
            :key="palette.key"
            :id="`gv-node-grad-${palette.key}`"
            cx="34%"
            cy="28%"
            r="76%"
          >
            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.98" />
            <stop offset="24%" :stop-color="palette.top" />
            <stop offset="72%" :stop-color="palette.mid" />
            <stop offset="100%" :stop-color="palette.base" />
          </radialGradient>
        </defs>
        <g ref="zoomGroup">
          <!-- Links -->
          <path
            v-for="(link, i) in visibleLinks"
            :key="'l'+i"
            :d="linkPath(link)"
            :class="[
              'gv-link',
              link.causal ? 'link-causal' : 'link-kg',
              link.inferred ? 'link-inferred' : ''
            ]"
            :stroke-width="linkStrokeWidth(link)"
            :marker-end="link.causal ? 'url(#arrow-causal)' : (link.inferred ? '' : 'url(#arrow-kg)')"
            @click.stop="selectLink(link)"
          />

          <g
            v-for="(link, i) in activeVisibleLinks"
            :key="'a'+i"
            class="gv-active-link-layer"
            pointer-events="none"
          >
            <g
              v-for="signal in activeLinkSignals(link, i)"
              :key="signal.id"
              class="gv-live-link-signal"
            >
              <path
                class="gv-live-link-signal-bar gv-live-link-signal-bar-back"
                :d="signal.backBarPath"
                :stroke="signal.color"
                :stroke-width="signal.barWidth"
                :opacity="signal.barOpacity"
              />
              <path
                class="gv-live-link-signal-tail"
                :d="signal.tailPath"
                :stroke="signal.color"
                :stroke-width="signal.tailWidth"
                :opacity="signal.tailOpacity"
              />
              <path
                class="gv-live-link-signal-diamond"
                :d="signal.diamondPath"
                :fill="signal.fill"
                :stroke="signal.color"
                :stroke-width="signal.strokeWidth"
              />
              <circle
                class="gv-live-link-signal-dot"
                :cx="signal.dotX"
                cy="0"
                :r="signal.dotRadius"
                :fill="signal.color"
              />
              <circle
                class="gv-live-link-signal-speck"
                :cx="signal.speckX"
                cy="0"
                :r="signal.speckRadius"
                :fill="signal.color"
                :opacity="signal.speckOpacity"
              />
              <path
                class="gv-live-link-signal-bar gv-live-link-signal-bar-front"
                :d="signal.frontBarPath"
                :stroke="signal.color"
                :stroke-width="signal.barWidth"
                :opacity="signal.frontBarOpacity"
              />
              <animateMotion
                :dur="signal.duration"
                :begin="signal.begin"
                repeatCount="indefinite"
                rotate="auto"
                :path="linkPath(link)"
              />
            </g>
          </g>

          <g
            v-for="(item, i) in edgeLabelDecorations"
            :key="'el'+i"
            class="gv-edge-label-group"
            :transform="`translate(${item.x} ${item.y})`"
            :style="{ '--gv-edge-label-size': `${item.fontSize}px` }"
          >
            <rect
              class="gv-edge-label-bg"
              :x="-item.width / 2"
              :y="-item.height / 2"
              :width="item.width"
              :height="item.height"
              :rx="item.radius"
              :ry="item.radius"
            />
            <text
              x="0"
              y="0"
              class="gv-edge-label"
              text-anchor="middle"
              dominant-baseline="middle"
            >{{ item.label }}</text>
          </g>

          <!-- Nodes -->
          <g
            v-for="node in simulationNodes"
            :key="node.id"
            class="gv-node"
            :class="{ selected: selectedNode?.id === node.id, dimmed: searchTerm && !nodeMatches(node) }"
            @click.stop="selectNode(node)"
            @mouseenter="hoveredNode = node"
            @mouseleave="hoveredNode = null"
          >
            <circle
              :cx="node.x"
              :cy="node.y"
              :r="nodeRadius(node) + (denseMode ? 1.35 : 1.8)"
              class="node-bubble-halo"
              :fill="nodeBubbleGlow(node.type)"
            />
            <circle
              :cx="node.x" :cy="node.y"
              :r="nodeRadius(node)"
              :class="['node-circle', 'node-bubble-main', nodeClass(node.type)]"
              :fill="nodeBubbleFill(node.type)"
              :stroke="nodeBubbleStroke(node.type)"
            />
            <circle
              :cx="node.x + nodeRadius(node) * 0.18"
              :cy="node.y + nodeRadius(node) * 0.2"
              :r="Math.max(0.9, nodeRadius(node) * 0.62)"
              class="node-bubble-core"
            />
            <ellipse
              :cx="node.x - nodeRadius(node) * 0.3"
              :cy="node.y - nodeRadius(node) * 0.34"
              :rx="Math.max(0.9, nodeRadius(node) * 0.42)"
              :ry="Math.max(0.6, nodeRadius(node) * 0.26)"
              :transform="`rotate(-24 ${node.x - nodeRadius(node) * 0.3} ${node.y - nodeRadius(node) * 0.34})`"
              class="node-bubble-highlight"
            />
            <text
              v-if="showNodeLabel(node)"
              :x="node.x" :y="node.y + nodeRadius(node) + 13"
              class="gv-node-label"
              text-anchor="middle"
            >{{ node.id.length > 16 ? node.id.slice(0,14)+'…' : node.id }}</text>
          </g>
        </g>
      </svg>

      <!-- Loading overlay -->
      <div v-if="loading" class="gv-loading">
        <div class="loading-spinner"></div>
        <p>Building graph layout...</p>
      </div>
    </div>

    <!-- Node detail panel -->
    <transition name="slide-panel">
      <div v-if="selectedNode" class="gv-panel" @click.stop>
        <div class="panel-close" @click="clearSelection">✕</div>
        <div class="panel-head">
          <div class="panel-head-copy">
            <div class="panel-kicker">Node Details</div>
            <div class="panel-name">{{ selectedNode.id }}</div>
          </div>
          <span class="panel-type-badge">{{ formatTypeLabel(selectedNode.type) }}</span>
        </div>
        <p class="panel-desc">{{ selectedNode.description || 'No description available.' }}</p>

        <div class="panel-chip-grid">
          <div class="panel-chip-card">
            <span class="panel-chip-label">Degree</span>
            <strong>{{ nodeConnectionStats(selectedNode).total }}</strong>
          </div>
          <div class="panel-chip-card">
            <span class="panel-chip-label">Outgoing</span>
            <strong>{{ nodeConnectionStats(selectedNode).outgoing }}</strong>
          </div>
          <div class="panel-chip-card">
            <span class="panel-chip-label">Incoming</span>
            <strong>{{ nodeConnectionStats(selectedNode).incoming }}</strong>
          </div>
          <div class="panel-chip-card">
            <span class="panel-chip-label">Category</span>
            <strong>{{ selectedNode.type }}</strong>
          </div>
        </div>

        <div class="panel-connections">
          <div class="panel-section-label">Connected With</div>
          <div
            v-for="conn in nodeConnections(selectedNode)"
            :key="conn.id"
            class="conn-item"
            @click="selectNode(conn)"
          >
            <span class="conn-direction">{{ conn.direction }}</span>
            <span class="conn-rel">{{ conn.relation }}</span>
            <span class="conn-name">{{ conn.id }}</span>
          </div>
          <p v-if="!nodeConnections(selectedNode).length" class="no-conn">
            No connections in current view.
          </p>
        </div>

        <div v-if="viewMode === 'causal' && causalStrength(selectedNode)" class="causal-info">
          <div class="panel-section-label">Causal strength</div>
          <div class="strength-bar-bg">
            <div class="strength-bar-fill"
                 :style="{ width: (causalStrength(selectedNode) * 100) + '%' }">
            </div>
          </div>
          <span class="strength-label">
            {{ (causalStrength(selectedNode) * 100).toFixed(0) }}%
          </span>
        </div>
      </div>
    </transition>

    <transition name="slide-panel">
      <div v-if="selectedLink" class="gv-relation-popup" @click.stop>
        <div class="panel-close" @click="selectedLink = null">✕</div>
        <div class="panel-head">
          <div class="panel-head-copy">
            <div class="panel-kicker">{{ selectedLink.causal ? 'Causal Link' : 'Relationship' }}</div>
            <div class="panel-name">{{ selectedLink.source }} → {{ selectedLink.target }}</div>
          </div>
          <span class="panel-type-badge">{{ selectedLink.relation || (selectedLink.causal ? 'CAUSES' : 'RELATES_TO') }}</span>
        </div>
        <div class="relation-grid">
          <div class="relation-row">
            <span class="relation-key">Label</span>
            <span class="relation-value">{{ selectedLink.relation || 'Linked entities' }}</span>
          </div>
          <div class="relation-row" v-if="selectedLink.causal">
            <span class="relation-key">Strength</span>
            <span class="relation-value">{{ ((selectedLink.strength || 0) * 100).toFixed(0) }}%</span>
          </div>
          <div class="relation-row" v-if="selectedLink.time_lag">
            <span class="relation-key">Lag</span>
            <span class="relation-value">{{ selectedLink.time_lag }}</span>
          </div>
        </div>
        <p class="panel-desc">
          {{ selectedLink.causal
            ? 'This edge is part of the causal inspection layer and contributes directional influence to downstream effects.'
            : 'This link comes from the extracted knowledge graph and shows a semantic or factual relationship between two entities.' }}
        </p>
      </div>
    </transition>

    <!-- Legend -->
    <div class="gv-legend">
      <div v-for="item in legend" :key="item.type" class="legend-item">
        <div class="legend-dot" :class="nodeClass(item.type)"></div>
        <span>{{ item.type }}</span>
      </div>
      <div v-if="viewMode === 'causal'" class="legend-item">
        <div class="legend-line causal"></div>
        <span>Causal edge (thickness = strength)</span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import axios from 'axios'

const layoutCache = new Map()

const props = defineProps({
  graphName: String,
  graphData: {
    type: Object,
    default: null,
  },
  canvasHeight: {
    type: Number,
    default: 480,
  },
  denseMode: {
    type: Boolean,
    default: false,
  },
  liveFocus: {
    type: Object,
    default: () => ({}),
  },
  nodeScale: {
    type: Number,
    default: 1,
  },
  edgeLengthScale: {
    type: Number,
    default: 1,
  },
  denseCompactFactor: {
    type: Number,
    default: 0.32,
  },
  denseZoomMultiplier: {
    type: Number,
    default: 1.24,
  },
  denseMinScale: {
    type: Number,
    default: 2.22,
  },
  denseMaxScale: {
    type: Number,
    default: 3.08,
  },
  denseCenterOnLoad: {
    type: Boolean,
    default: false,
  },
  showEdgeLabels: {
    type: Boolean,
    default: true,
  },
  densePreset: {
    type: String,
    default: 'default',
  },
})

const API         = 'http://localhost:5001'
const svgEl       = ref(null)
const zoomGroup   = ref(null)
const canvasWrapper = ref(null)
const viewerRoot  = ref(null)
const svgHeight   = ref(props.canvasHeight || 480)
const loading     = ref(false)
const viewMode    = ref('knowledge')
const isFullscreen = ref(false)
const selectedNode = ref(null)
const hoveredNode  = ref(null)
const selectedLink = ref(null)
const searchTerm = ref('')

const rawNodes    = ref([])
const rawLinks    = ref([])
const rawCausal   = ref([])
const nodeCount   = ref(0)
const linkCount   = ref(0)
const nodeDegrees = ref({})

const simulationNodes = ref([])
const simulationLinks = ref([])
const isMirofishDense = computed(() => props.denseMode && props.densePreset === 'mirofish')

const viewerStyle = computed(() => (
  isFullscreen.value
    ? { minHeight: `${svgHeight.value}px`, height: '100vh' }
    : props.denseMode
      ? { minHeight: `${svgHeight.value}px`, height: `${svgHeight.value}px` }
      : {}
))

const canvasStyle = computed(() => (
  isFullscreen.value
    ? { minHeight: `${svgHeight.value}px`, height: `${svgHeight.value}px`, flex: '1 1 auto' }
    : props.denseMode
      ? { minHeight: `${svgHeight.value}px`, height: `${svgHeight.value}px` }
      : {}
))

const hasCausal = computed(() => rawCausal.value.length > 0)

const visibleLinks = computed(() => {
  if (viewMode.value === 'causal') return simulationLinks.value.filter(l => l.causal)
  return simulationLinks.value.filter(l => !l.causal)
})

const matchedNodeCount = computed(() => {
  if (!searchTerm.value.trim()) return simulationNodes.value.length
  return simulationNodes.value.filter(node => nodeMatches(node)).length
})

const liveFocusTokens = computed(() => {
  const sourceTerms = Array.isArray(props.liveFocus?.focus_terms) ? props.liveFocus.focus_terms : []
  const tokens = new Set()
  sourceTerms.forEach(value => tokenizeFocusValue(value).forEach(token => tokens.add(token)))
  return Array.from(tokens).slice(0, 20)
})

const liveActiveNodeIds = computed(() => {
  if (!liveFocusTokens.value.length || !simulationNodes.value.length) return new Set()

  const scored = simulationNodes.value
    .map(node => {
      const haystack = `${node.id || ''} ${node.type || ''} ${node.description || ''}`.toLowerCase()
      let score = 0
      liveFocusTokens.value.forEach(token => {
        if (haystack.includes(token)) score += token.length > 6 ? 2 : 1
      })
      return { id: node.id, score }
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, props.denseMode ? 18 : 12)

  return new Set(scored.map(item => item.id))
})

const activeVisibleLinks = computed(() => {
  const liveLinks = visibleLinks.value.filter(link => linkIsLiveActive(link))
  if (!props.denseMode) return liveLinks
  return liveLinks
    .sort((a, b) => {
      const aScore = Number(a.causal) * 2 + Number(!a.inferred)
      const bScore = Number(b.causal) * 2 + Number(!b.inferred)
      return bScore - aScore
    })
    .slice(0, 28)
})

watch(() => props.canvasHeight, () => {
  updateSvgHeight()
})

const edgeLabelLinks = computed(() => {
  if (!props.showEdgeLabels) return []

  const ranked = visibleLinks.value
    .filter(link => !link.causal && !link.inferred && link.relation && link.relation !== 'CONTEXT_NEAR')
    .map(link => ({
      link,
      score:
        (nodeDegrees.value[link.source] || 0) +
        (nodeDegrees.value[link.target] || 0) +
        (liveActiveNodeIds.value.has(link.source) || liveActiveNodeIds.value.has(link.target) ? 8 : 0),
    }))
    .sort((a, b) => b.score - a.score)

  const maxLabels = isMirofishDense.value ? 168 : (props.denseMode ? 72 : 120)
  const minLabelDX = isMirofishDense.value ? 24 : 42
  const minLabelDY = isMirofishDense.value ? 10 : 16
  const chosen = []
  const occupied = []

  for (const item of ranked) {
    if (chosen.length >= maxLabels) break
    const pos = linkLabelPosition(item.link)
    const tooClose = occupied.some(other => Math.abs(other.x - pos.x) < minLabelDX && Math.abs(other.y - pos.y) < minLabelDY)
    if (tooClose) continue
    occupied.push(pos)
    chosen.push(item.link)
  }

  return chosen
})

const edgeLabelDecorations = computed(() => {
  const fontSize = edgeLabelFontSize()
  const height = fontSize + (isMirofishDense.value ? 3.8 : (props.denseMode ? 4.4 : 5.2))
  const radius = height / 2
  const paddingX = isMirofishDense.value ? 3.4 : (props.denseMode ? 4.2 : 4.8)
  const widthFactor = isMirofishDense.value ? 0.5 : (props.denseMode ? 0.53 : 0.56)

  return edgeLabelLinks.value.map(link => {
    const label = relationLabel(link)
    const pos = linkLabelPosition(link)
    const width = Math.max(fontSize * 2.1, label.length * fontSize * widthFactor + paddingX * 2)

    return {
      link,
      label,
      x: pos.x,
      y: pos.y,
      width,
      height,
      radius,
      fontSize,
    }
  })
})

const denseLabelIds = computed(() => {
  const ranked = Object.entries(nodeDegrees.value)
    .sort((a, b) => b[1] - a[1])
    .slice(0, props.denseMode ? 18 : 18)
    .map(([id]) => id)
  return new Set(ranked)
})

const legend = [
  { type: 'PERSON' }, { type: 'ORGANIZATION' },
  { type: 'EVENT' }, { type: 'CONCEPT' }, { type: 'PLACE' }
]

const nodeBubblePalettes = [
  {
    key: 'person',
    top: '#c7e0ff',
    mid: '#63a6ff',
    base: '#2f78e2',
    stroke: 'rgba(255, 255, 255, 0.98)',
    glow: 'rgba(96, 156, 255, 0.18)',
  },
  {
    key: 'org',
    top: '#c7f2e3',
    mid: '#42c8a1',
    base: '#168769',
    stroke: 'rgba(255, 255, 255, 0.98)',
    glow: 'rgba(41, 171, 133, 0.16)',
  },
  {
    key: 'event',
    top: '#ffd0d6',
    mid: '#f17b8b',
    base: '#cc4458',
    stroke: 'rgba(255, 255, 255, 0.98)',
    glow: 'rgba(217, 83, 104, 0.16)',
  },
  {
    key: 'concept',
    top: '#e3d4ff',
    mid: '#b286f3',
    base: '#7f49cb',
    stroke: 'rgba(255, 255, 255, 0.98)',
    glow: 'rgba(153, 103, 220, 0.16)',
  },
  {
    key: 'place',
    top: '#d9f7ff',
    mid: '#7ed6ff',
    base: '#3b94ff',
    stroke: 'rgba(255, 255, 255, 0.98)',
    glow: 'rgba(96, 192, 255, 0.18)',
  },
  {
    key: 'unknown',
    top: '#ffffff',
    mid: '#edf2f8',
    base: '#c8d1dc',
    stroke: 'rgba(255, 255, 255, 0.98)',
    glow: 'rgba(202, 211, 222, 0.18)',
  },
]

// ── Load graph data ───────────────────────────────────────────────────────
async function loadGraph() {
  if (!props.graphName && !props.graphData) return
  loading.value = true
  selectedNode.value = null

  try {
    const data = props.graphData
      ? props.graphData
      : (await axios.get(`${API}/api/graph/${props.graphName}`)).data

    rawNodes.value  = data.nodes  || []
    rawLinks.value  = data.links  || []
    rawCausal.value = data.causal_links || []
    nodeCount.value = data.node_count || rawNodes.value.length
    linkCount.value = data.link_count || (rawLinks.value.length + rawCausal.value.length)

    const cached = layoutCache.get(layoutCacheKey())
    if (
      cached &&
      cached.nodeCount === rawNodes.value.length &&
      cached.linkCount === rawLinks.value.length &&
      cached.causalCount === rawCausal.value.length
    ) {
      nodeDegrees.value = cached.nodeDegrees
      simulationNodes.value = cached.nodes.map(node => ({ ...node }))
      simulationLinks.value = cached.links.map(link => ({ ...link }))
      applyDefaultDenseView()
      return
    }

    if (rawNodes.value.every(node => Number.isFinite(node.x) && Number.isFinite(node.y))) {
      applyPresetLayout()
      return
    }

    await nextTick()
    runForceLayout()

  } catch (e) {
    console.error('Graph load error:', e)
  } finally {
    loading.value = false
  }
}

function applyPresetLayout() {
  const allLinks = [
    ...rawLinks.value.map(link => ({ ...link, causal: false })),
    ...rawCausal.value.map(link => ({ ...link, causal: true }))
  ]

  const degrees = {}
  rawNodes.value.forEach(node => { degrees[node.id] = 0 })
  allLinks.forEach(link => {
    degrees[link.source] = (degrees[link.source] || 0) + 1
    degrees[link.target] = (degrees[link.target] || 0) + 1
  })
  nodeDegrees.value = degrees

  simulationNodes.value = rawNodes.value.map(node => ({
    ...node,
    vx: 0,
    vy: 0,
  }))

  if (props.denseMode && simulationNodes.value.length) {
    const xs = simulationNodes.value.map(node => node.x)
    const ys = simulationNodes.value.map(node => node.y)
    const centerX = (Math.min(...xs) + Math.max(...xs)) / 2
    const centerY = (Math.min(...ys) + Math.max(...ys)) / 2
    const compact = clamp(props.denseCompactFactor || 0.88, 0.46, 0.96)
    const compactX = isMirofishDense.value ? clamp(compact * 0.88, 0.4, 0.94) : compact
    const compactY = isMirofishDense.value ? clamp(compact * 0.98, 0.46, 0.98) : compact

    simulationNodes.value = simulationNodes.value.map(node => ({
      ...node,
      x: centerX + (node.x - centerX) * compactX,
      y: centerY + (node.y - centerY) * compactY,
    }))
  }

  const nodeMap = {}
  simulationNodes.value.forEach(node => {
    nodeMap[node.id] = node
  })

  simulationLinks.value = allLinks.map(link => {
    const source = nodeMap[link.source]
    const target = nodeMap[link.target]
    if (!source || !target) return null
    return {
      ...link,
      x1: source.x,
      y1: source.y,
      x2: target.x,
      y2: target.y,
    }
  }).filter(Boolean)

  layoutCache.set(layoutCacheKey(), {
    nodeCount: rawNodes.value.length,
    linkCount: rawLinks.value.length,
    causalCount: rawCausal.value.length,
    nodeDegrees: { ...nodeDegrees.value },
    nodes: simulationNodes.value.map(node => ({ ...node })),
    links: simulationLinks.value.map(link => ({ ...link })),
  })

  applyDefaultDenseView()
}

// ── Force-directed layout (pure JS, no D3 needed) ────────────────────────
function runForceLayout() {
  const W = canvasWrapper.value?.clientWidth  || 700
  const H = svgHeight.value
  const centerX = W / 2
  const centerY = H / 2

  const allLinks = [
    ...rawLinks.value.map(l => ({ ...l, causal: false })),
    ...rawCausal.value.map(l => ({ ...l, causal: true }))
  ]

  const degrees = {}
  rawNodes.value.forEach(node => { degrees[node.id] = 0 })
  allLinks.forEach(link => {
    degrees[link.source] = (degrees[link.source] || 0) + 1
    degrees[link.target] = (degrees[link.target] || 0) + 1
  })
  nodeDegrees.value = degrees

  const hubIds = Object.entries(degrees)
    .sort((a, b) => b[1] - a[1])
    .slice(0, Math.min(6, rawNodes.value.length))
    .map(([id]) => id)

  // Initialize node positions with a denser, hub-aware seed so sparse
  // military/event graphs don't immediately fly to the borders.
  const nodes = rawNodes.value.map((n, index) => {
    const degree = degrees[n.id] || 0
    const hubIndex = hubIds.indexOf(n.id)
    const angle = hubIndex >= 0
      ? (Math.PI * 2 * hubIndex) / Math.max(hubIds.length, 1)
      : Math.random() * Math.PI * 2

    let radius
    if (hubIndex >= 0) {
      radius = props.denseMode ? 40 + hubIndex * 22 : 80 + hubIndex * 35
    } else if (props.denseMode) {
      const spread = Math.max(70, Math.min(Math.min(W, H) * 0.28, 260))
      radius = 35 + Math.random() * spread + Math.max(0, 18 - degree * 3)
    } else {
      radius = 120 + Math.random() * 220
    }

    const jitter = props.denseMode ? 18 : 42

    return {
      ...n,
      x: centerX + Math.cos(angle) * radius + (Math.random() - 0.5) * jitter,
      y: centerY + Math.sin(angle) * radius + (Math.random() - 0.5) * jitter,
      vx: 0,
      vy: 0
    }
  })

  const nodeMap = {}
  nodes.forEach(n => { nodeMap[n.id] = n })

  // Run simulation
  const iterations = props.denseMode ? 146 : 124
  const k = Math.sqrt((W * H) / (nodes.length || 1))
  const repulsionScale = props.denseMode ? 0.016 : 0.15
  const attractionScale = props.denseMode ? 0.074 : 0.05
  const centerPull = props.denseMode ? 0.028 : 0.01
  const margin = props.denseMode ? 26 : 40

  for (let iter = 0; iter < iterations; iter++) {
    const cooling = 1 - iter / iterations

    // Repulsion between all nodes
    for (let i = 0; i < nodes.length; i++) {
      nodes[i].vx = 0
      nodes[i].vy = 0
    }

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x
        const dy = nodes[i].y - nodes[j].y
        const dist = Math.sqrt(dx*dx + dy*dy) || 1
        const force = (k * k) / Math.max(dist, props.denseMode ? 22 : 14)
        const fx = (dx / dist) * force * repulsionScale
        const fy = (dy / dist) * force * repulsionScale
        nodes[i].vx += fx
        nodes[i].vy += fy
        nodes[j].vx -= fx
        nodes[j].vy -= fy
      }
    }

    // Attraction along links
    allLinks.forEach(link => {
      const s = nodeMap[link.source]
      const t = nodeMap[link.target]
      if (!s || !t) return
      const dx = t.x - s.x
      const dy = t.y - s.y
      const dist = Math.sqrt(dx*dx + dy*dy) || 1
      const desiredLength = props.denseMode
        ? (link.inferred ? 26 : 36) * clamp(props.edgeLengthScale || 1, 0.35, 1.4)
        : 160
      const force = ((dist - desiredLength) / k) * attractionScale
      s.vx += (dx / dist) * force
      s.vy += (dy / dist) * force
      t.vx -= (dx / dist) * force
      t.vy -= (dy / dist) * force
    })

    // Center gravity
    nodes.forEach(n => {
      const degree = degrees[n.id] || 0
      const gravityBoost = props.denseMode ? 1 + Math.min(degree, 8) * 0.08 : 1
      n.vx += (centerX - n.x) * centerPull * gravityBoost
      n.vy += (centerY - n.y) * centerPull * gravityBoost
    })

    // Apply velocity with cooling
    nodes.forEach(n => {
      n.x += n.vx * cooling
      n.y += n.vy * cooling
      n.x = Math.max(margin, Math.min(W - margin, n.x))
      n.y = Math.max(margin, Math.min(H - margin, n.y))
    })
  }

  if (props.denseMode) {
    const compactFactor = clamp(props.denseCompactFactor || 0.32, 0.16, 0.6)
    nodes.forEach(n => {
      n.x = centerX + (n.x - centerX) * compactFactor
      n.y = centerY + (n.y - centerY) * compactFactor
    })
  }

  simulationNodes.value = nodes

  // Build link coordinate data
  simulationLinks.value = allLinks.map(link => {
    const s = nodeMap[link.source]
    const t = nodeMap[link.target]
    if (!s || !t) return null
    return {
      ...link,
      x1: s.x, y1: s.y,
      x2: t.x, y2: t.y
    }
  }).filter(Boolean)

  layoutCache.set(layoutCacheKey(), {
    nodeCount: rawNodes.value.length,
    linkCount: rawLinks.value.length,
    causalCount: rawCausal.value.length,
    nodeDegrees: { ...nodeDegrees.value },
    nodes: simulationNodes.value.map(node => ({ ...node })),
    links: simulationLinks.value.map(link => ({ ...link })),
  })

  applyDefaultDenseView()
}

// ── Interaction helpers ───────────────────────────────────────────────────
function setMode(mode) {
  viewMode.value   = mode
  clearSelection()
}

function selectNode(node) {
  selectedNode.value = node
  selectedLink.value = null
}

function selectLink(link) {
  selectedLink.value = link
  selectedNode.value = null
}

function clearSelection() {
  selectedNode.value = null
  selectedLink.value = null
}

function onGlobalPointerDown(event) {
  if (!selectedNode.value && !selectedLink.value) return
  if (viewerRoot.value && !viewerRoot.value.contains(event.target)) {
    clearSelection()
  }
}

function nodeMatches(node) {
  const query = searchTerm.value.trim().toLowerCase()
  if (!query) return true
  return (
    String(node.id || '').toLowerCase().includes(query) ||
    String(node.type || '').toLowerCase().includes(query) ||
    String(node.description || '').toLowerCase().includes(query)
  )
}

function tokenizeFocusValue(value) {
  const stopWords = new Set([
    'round', 'stage', 'branch', 'general', 'market', 'event',
    'agent', 'agents', 'label', 'time', 'window', 'while',
    'with', 'this', 'that', 'from', 'into', 'across', 'around',
    'before', 'after', 'under', 'during', 'about', 'their',
    'thinking', 'updated', 'belief', 'action', 'complete',
    'start', 'started', 'developing', 'current'
  ])

  return String(value || '')
    .toLowerCase()
    .split(/[^a-z0-9_]+/)
    .map(token => token.replaceAll('_', ' ').trim())
    .flatMap(token => token.split(/\s+/))
    .map(token => token.trim())
    .filter(token => token.length >= 4 && !stopWords.has(token))
}

function linkIsLiveActive(link) {
  return liveActiveNodeIds.value.has(link.source) || liveActiveNodeIds.value.has(link.target)
}

function nodeConnections(node) {
  const conns = []
  simulationLinks.value.forEach(link => {
    if (link.source === node.id) {
      const target = simulationNodes.value.find(n => n.id === link.target)
      if (target) conns.push({
        ...target,
        direction: '→',
        relation : link.relation || ''
      })
    }
    if (link.target === node.id) {
      const source = simulationNodes.value.find(n => n.id === link.source)
      if (source) conns.push({
        ...source,
        direction: '←',
        relation : link.relation || ''
      })
    }
  })
  return conns
}

function nodeConnectionStats(node) {
  const outgoing = simulationLinks.value.filter(link => link.source === node.id).length
  const incoming = simulationLinks.value.filter(link => link.target === node.id).length
  return {
    outgoing,
    incoming,
    total: outgoing + incoming,
  }
}

function causalStrength(node) {
  const link = rawCausal.value.find(
    l => l.source === node.id || l.target === node.id)
  return link?.strength || null
}

function nodeRadius(node) {
  // Larger nodes = more connections
  const degree = nodeDegrees.value[node.id] || 0
  const scaleFactor = clamp(props.nodeScale || 1, 0.18, 1.5)
  if (props.denseMode) {
    const radius = Math.min(12 * scaleFactor, (5 + degree * 0.5) * scaleFactor)
    return isMirofishDense.value ? radius * 1.16 : radius
  }
  return Math.min(18 * scaleFactor, (6 + degree * 1.2) * scaleFactor)
}

function showNodeLabel(node) {
  if (!props.denseMode) return true
  if (selectedNode.value?.id === node.id) return true
  if (hoveredNode.value?.id === node.id) return true
  if (searchTerm.value.trim()) return nodeMatches(node)
  return denseLabelIds.value.has(node.id)
}

function layoutCacheKey() {
  const identity = props.graphData?.cacheKey || props.graphName || 'graph'
  return `${identity}:${props.denseMode ? 'dense' : 'standard'}:${props.densePreset}:${svgHeight.value}:${props.nodeScale}:${props.edgeLengthScale}:${props.denseCompactFactor}`
}

function formatTypeLabel(value) {
  return String(value || 'Entity')
    .replaceAll('_', ' ')
    .toLowerCase()
    .replace(/\b\w/g, letter => letter.toUpperCase())
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value))
}

function linkPath(link) {
  const dx = link.x2 - link.x1
  const dy = link.y2 - link.y1
  const dist = Math.sqrt(dx * dx + dy * dy) || 1
  const mx = (link.x1 + link.x2) / 2
  const my = (link.y1 + link.y2) / 2

  if (!props.denseMode && !link.causal) {
    return `M ${link.x1} ${link.y1} L ${link.x2} ${link.y2}`
  }

  const curvature = link.causal
    ? Math.min(isMirofishDense.value ? 34 : 48, dist * (isMirofishDense.value ? 0.08 : 0.12))
    : Math.min(
        isMirofishDense.value ? 16 : 30,
        dist * (link.inferred ? (isMirofishDense.value ? 0.03 : 0.06) : (isMirofishDense.value ? 0.05 : 0.1))
      )
  const nx = -dy / dist
  const ny = dx / dist
  const cx = mx + nx * curvature
  const cy = my + ny * curvature
  return `M ${link.x1} ${link.y1} Q ${cx} ${cy} ${link.x2} ${link.y2}`
}

function linkLabelPosition(link) {
  const dx = link.x2 - link.x1
  const dy = link.y2 - link.y1
  const dist = Math.sqrt(dx * dx + dy * dy) || 1
  const mx = (link.x1 + link.x2) / 2
  const my = (link.y1 + link.y2) / 2
  const nx = -dy / dist
  const ny = dx / dist
  const offset = props.denseMode ? 7 : 10
  return {
    x: mx + nx * offset,
    y: my + ny * offset,
  }
}

function relationLabel(link) {
  const value = String(link.relation || '')
  if (isMirofishDense.value) {
    return value.length > 36 ? `${value.slice(0, 34)}…` : value
  }
  return value.length > 28 ? `${value.slice(0, 26)}…` : value
}

function activeLinkAccent(link) {
  if (link.causal) {
    return {
      color: 'rgba(181, 143, 255, 0.96)',
    }
  }

  return {
    color: 'rgba(102, 198, 255, 0.96)',
  }
}

function activeLinkSignals(link, index) {
  const accent = activeLinkAccent(link)
  const denseFactor = isMirofishDense.value ? 0.84 : (props.denseMode ? 0.92 : 1)
  const leadSize = (link.causal ? 3.7 : 3.2) * denseFactor
  const echoSize = (link.causal ? 2.95 : 2.5) * denseFactor
  const leadDuration = (2.65 + (index % 5) * 0.16 + (link.causal ? 0.22 : 0)).toFixed(2)
  const echoDuration = (3.2 + (index % 4) * 0.14 + (link.causal ? 0.18 : 0)).toFixed(2)
  const leadTail = 4.1 * denseFactor
  const echoTail = 3.2 * denseFactor
  const leadBarWidth = isMirofishDense.value ? 0.5 : 0.62
  const echoBarWidth = isMirofishDense.value ? 0.42 : 0.5

  return [
    {
      id: `${index}-signal-lead`,
      duration: `${leadDuration}s`,
      begin: `${(index % 6) * 0.18}s`,
      color: accent.color,
      fill: 'rgba(255,255,255,0.97)',
      diamondPath: diamondPath(leadSize),
      tailPath: `M ${-leadTail} 0 L ${-(leadSize * 0.8)} 0`,
      tailWidth: isMirofishDense.value ? 0.46 : 0.54,
      tailOpacity: 0.7,
      backBarPath: `M ${-(leadSize * 1.62)} 0 L ${-(leadSize * 1.02)} 0`,
      frontBarPath: `M ${(leadSize * 1.02)} 0 L ${(leadSize * 1.62)} 0`,
      barWidth: leadBarWidth,
      barOpacity: 0.68,
      frontBarOpacity: 0.88,
      strokeWidth: isMirofishDense.value ? 0.48 : 0.58,
      dotX: leadSize * 0.86,
      dotRadius: 0.7 * denseFactor,
      speckX: -leadSize * 1.12,
      speckRadius: 0.42 * denseFactor,
      speckOpacity: 0.52,
    },
    {
      id: `${index}-signal-echo`,
      duration: `${echoDuration}s`,
      begin: `${0.32 + (index % 5) * 0.14}s`,
      color: accent.color,
      fill: 'rgba(255,255,255,0.94)',
      diamondPath: diamondPath(echoSize),
      tailPath: `M ${-echoTail} 0 L ${-(echoSize * 0.78)} 0`,
      tailWidth: isMirofishDense.value ? 0.38 : 0.44,
      tailOpacity: 0.48,
      backBarPath: `M ${-(echoSize * 1.56)} 0 L ${-(echoSize * 0.98)} 0`,
      frontBarPath: `M ${(echoSize * 0.98)} 0 L ${(echoSize * 1.56)} 0`,
      barWidth: echoBarWidth,
      barOpacity: 0.44,
      frontBarOpacity: 0.62,
      strokeWidth: isMirofishDense.value ? 0.4 : 0.46,
      dotX: echoSize * 0.82,
      dotRadius: 0.56 * denseFactor,
      speckX: -echoSize * 1.08,
      speckRadius: 0.28 * denseFactor,
      speckOpacity: 0.36,
    },
  ]
}

function diamondPath(size) {
  return `M ${-size} 0 L 0 ${-size * 0.74} L ${size} 0 L 0 ${size * 0.74} Z`
}

function edgeLabelFontSize() {
  if (isMirofishDense.value) return 4.9
  if (props.denseMode) return 5.5
  return 6.6
}

function linkStrokeWidth(link) {
  if (link.causal) return (link.strength || 0.5) * 2.5 + 0.5
  if (props.denseMode) {
    if (isMirofishDense.value) {
      return link.inferred
        ? Math.max(0.18, (link.weight || 0.5) * 0.3)
        : Math.max(0.42, (link.weight || 0.5) * 0.5)
    }
    return link.inferred
      ? Math.max(0.32, (link.weight || 0.5) * 0.72)
      : 0.72
  }
  return 0.6
}

function nodeClass(type) {
  const map = {
    'PERSON'      : 'node-person',
    'ORGANIZATION': 'node-org',
    'EVENT'       : 'node-event',
    'CONCEPT'     : 'node-concept',
    'PLACE'       : 'node-place'
  }
  return map[type] || 'node-unknown'
}

function nodeBubblePalette(type) {
  const paletteMap = {
    PERSON: 'person',
    ORGANIZATION: 'org',
    EVENT: 'event',
    CONCEPT: 'concept',
    PLACE: 'place',
  }
  const key = paletteMap[type] || 'unknown'
  return nodeBubblePalettes.find(palette => palette.key === key) || nodeBubblePalettes[nodeBubblePalettes.length - 1]
}

function nodeBubbleFill(type) {
  return `url(#gv-node-grad-${nodeBubblePalette(type).key})`
}

function nodeBubbleStroke(type) {
  return nodeBubblePalette(type).stroke
}

function nodeBubbleGlow(type) {
  return nodeBubblePalette(type).glow
}

function resetZoom() {
  if (props.denseMode) {
    applyDefaultDenseView()
    return
  }
  translateX = 0
  translateY = 0
  scale = 1
  applyTransform()
}

function graphViewportMetrics() {
  const W = canvasWrapper.value?.clientWidth || 700
  const H = svgHeight.value
  const nodes = simulationNodes.value
  if (!nodes.length) return null

  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity

  nodes.forEach(node => {
    const extent = nodeRadius(node) + (props.denseMode ? (isMirofishDense.value ? 5 : 7) : 10)
    minX = Math.min(minX, node.x - extent)
    maxX = Math.max(maxX, node.x + extent)
    minY = Math.min(minY, node.y - extent)
    maxY = Math.max(maxY, node.y + extent)
  })

  const contentWidth = Math.max(1, maxX - minX)
  const contentHeight = Math.max(1, maxY - minY)
  const paddingX = props.denseMode ? (isMirofishDense.value ? 18 : 24) : 34
  const paddingY = props.denseMode ? (isMirofishDense.value ? 22 : 28) : 38
  const fitScale = Math.min(
    Math.max((W - paddingX * 2) / contentWidth, 0.08),
    Math.max((H - paddingY * 2) / contentHeight, 0.08)
  )

  return {
    W,
    H,
    minX,
    maxX,
    minY,
    maxY,
    centerX: (minX + maxX) / 2,
    centerY: (minY + maxY) / 2,
    fitScale,
  }
}

function graphDefaultScale(metrics = graphViewportMetrics()) {
  if (!props.denseMode) return 1
  if (!metrics) return isMirofishDense.value ? 2.08 : 1.82

  const minScale = Number.isFinite(props.denseMinScale) ? props.denseMinScale : 2.22
  const maxScale = Number.isFinite(props.denseMaxScale) ? props.denseMaxScale : 3.08
  const targetScale = metrics.fitScale * (props.denseZoomMultiplier || 1.24)
  return clamp(targetScale, Math.min(minScale, maxScale), Math.max(minScale, maxScale))
}

function graphExpandedMaxScale() {
  const baseMaxScale = props.denseMode
    ? (Number.isFinite(props.denseMaxScale) ? props.denseMaxScale : 3.08)
    : 3

  return baseMaxScale * 2
}

function graphZoomLimits() {
  const metrics = graphViewportMetrics()
  const maxScale = graphExpandedMaxScale()

  if (!metrics) {
    return {
      minScale: props.denseMode ? Math.min(graphDefaultScale(metrics), 1) : 0.3,
      maxScale,
      metrics,
    }
  }

  const defaultScale = graphDefaultScale(metrics)
  return {
    minScale: Math.max(0.3, Math.min(metrics.fitScale, defaultScale)),
    maxScale: Math.max(maxScale, defaultScale),
    metrics,
  }
}

function fitGraphToViewport(targetScale = null) {
  const { minScale, metrics } = graphZoomLimits()
  if (!metrics) return
  scale = targetScale == null ? minScale : clamp(targetScale, minScale, Math.max(minScale, graphZoomLimits().maxScale))
  translateX = Math.round(metrics.W / 2 - metrics.centerX * scale)
  translateY = Math.round(metrics.H / 2 - metrics.centerY * scale)
  applyTransform()
}

function applyDefaultDenseView() {
  if (!props.denseMode) {
    translateX = 0
    translateY = 0
    scale = 1
    applyTransform()
    return
  }
  const metrics = graphViewportMetrics()
  if (!metrics) {
    const W = canvasWrapper.value?.clientWidth || 700
    const H = svgHeight.value
    scale = isMirofishDense.value ? 2.08 : 1.82
    translateX = Math.round(W * (isMirofishDense.value ? -0.31 : -0.26))
    translateY = Math.round(H * (isMirofishDense.value ? -0.22 : -0.18))
    applyTransform()
    return
  }

  scale = graphDefaultScale(metrics)
  const desiredX = metrics.W / 2 - metrics.centerX * scale
  const desiredY = metrics.H / 2 - metrics.centerY * scale
  if (props.denseCenterOnLoad) {
    translateX = Math.round(desiredX)
    translateY = Math.round(desiredY)
    applyTransform()
    return
  }
  const padding = isMirofishDense.value ? 12 : 24
  const minTranslateX = metrics.W - metrics.maxX * scale - padding
  const maxTranslateX = -metrics.minX * scale + padding
  const minTranslateY = metrics.H - metrics.maxY * scale - padding
  const maxTranslateY = -metrics.minY * scale + padding

  translateX = Math.round(
    clamp(desiredX, Math.min(minTranslateX, maxTranslateX), Math.max(minTranslateX, maxTranslateX))
  )
  translateY = Math.round(
    clamp(desiredY, Math.min(minTranslateY, maxTranslateY), Math.max(minTranslateY, maxTranslateY))
  )
  applyTransform()
}

function focusMatches() {
  const matches = simulationNodes.value.filter(node => nodeMatches(node))
  if (!matches.length) return
  const avgX = matches.reduce((sum, node) => sum + node.x, 0) / matches.length
  const avgY = matches.reduce((sum, node) => sum + node.y, 0) / matches.length
  const W = canvasWrapper.value?.clientWidth || 700
  const H = svgHeight.value
  translateX = W / 2 - avgX * scale
  translateY = H / 2 - avgY * scale
  applyTransform()
}

// ── Simple pan/zoom via mouse drag ────────────────────────────────────────
let isDragging = false
let startX = 0, startY = 0
let translateX = 0, translateY = 0
let scale = 1

function applyTransform() {
  if (zoomGroup.value) {
    zoomGroup.value.setAttribute(
      'transform',
      `translate(${translateX},${translateY}) scale(${scale})`
    )
  }
}

function graphViewportCenter() {
  return {
    x: (canvasWrapper.value?.clientWidth || 700) / 2,
    y: svgHeight.value / 2,
  }
}

function setGraphScaleFromViewportCenter(nextScale) {
  const center = graphViewportCenter()
  const contentX = (center.x - translateX) / scale
  const contentY = (center.y - translateY) / scale
  scale = nextScale
  translateX = Math.round(center.x - contentX * scale)
  translateY = Math.round(center.y - contentY * scale)
  applyTransform()
}

function updateSvgHeight() {
  if (isFullscreen.value) {
    const reserved = props.denseMode ? 56 : 144
    svgHeight.value = Math.max(props.canvasHeight || 480, window.innerHeight - reserved)
    return
  }
  svgHeight.value = props.canvasHeight || 480
}

function syncFullscreenState() {
  isFullscreen.value = document.fullscreenElement === viewerRoot.value
  updateSvgHeight()
}

async function toggleFullscreen() {
  if (!viewerRoot.value || !document.fullscreenEnabled) return
  if (document.fullscreenElement === viewerRoot.value) {
    await document.exitFullscreen()
    return
  }
  await viewerRoot.value.requestFullscreen()
}

function onMouseDown(e) {
  isDragging = true
  startX = e.clientX - translateX
  startY = e.clientY - translateY
}

function onMouseMove(e) {
  if (!isDragging) return
  translateX = e.clientX - startX
  translateY = e.clientY - startY
  applyTransform()
}

function onMouseUp() { isDragging = false }

function onWheel(e) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  const { minScale, maxScale } = graphZoomLimits()
  const targetScale = clamp(scale * delta, minScale, maxScale)

  if (e.deltaY > 0 && targetScale <= minScale + 0.0001) {
    fitGraphToViewport(minScale)
    return
  }

  setGraphScaleFromViewportCenter(targetScale)
}

onMounted(() => {
  updateSvgHeight()
  loadGraph()
  const svg = svgEl.value
  if (svg) {
    svg.addEventListener('mousedown', onMouseDown)
    svg.addEventListener('mousemove', onMouseMove)
    svg.addEventListener('mouseup',   onMouseUp)
    svg.addEventListener('wheel',     onWheel, { passive: false })
  }
  window.addEventListener('pointerdown', onGlobalPointerDown, true)
  window.addEventListener('resize', updateSvgHeight)
  document.addEventListener('fullscreenchange', syncFullscreenState)
})

onUnmounted(() => {
  const svg = svgEl.value
  if (svg) {
    svg.removeEventListener('mousedown', onMouseDown)
    svg.removeEventListener('mousemove', onMouseMove)
    svg.removeEventListener('mouseup',   onMouseUp)
    svg.removeEventListener('wheel',     onWheel)
  }
  window.removeEventListener('pointerdown', onGlobalPointerDown, true)
  window.removeEventListener('resize', updateSvgHeight)
  document.removeEventListener('fullscreenchange', syncFullscreenState)
})

watch(() => props.graphName, loadGraph)
watch(() => props.graphData, loadGraph, { deep: true })
watch(() => props.canvasHeight, (value) => {
  svgHeight.value = value || 480
  nextTick(() => runForceLayout())
})
watch(hasCausal, (value) => {
  if (!value && viewMode.value === 'causal') {
    viewMode.value = 'knowledge'
  }
})
</script>

<style scoped>
.graph-viewer {
  position: relative;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  margin-top: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.graph-viewer.dense-mode {
  margin-top: 0;
  border-radius: 22px;
  border-color: rgba(226, 209, 194, 0.88);
  background: rgba(255, 252, 249, 0.98);
  min-height: 100%;
}

.graph-viewer.dense-preset-mirofish {
  border-radius: 18px;
  border-color: rgba(219, 214, 208, 0.92);
  background: rgba(255, 255, 253, 0.99);
}

.graph-viewer:fullscreen {
  width: 100vw;
  height: 100vh;
  margin-top: 0;
  padding: 16px;
  box-sizing: border-box;
  border-radius: 0;
  display: flex;
  flex-direction: column;
  background: rgba(255, 253, 250, 0.99);
}

.graph-viewer:fullscreen .gv-canvas {
  flex: 1;
  min-height: 0;
}

.graph-viewer:fullscreen .gv-panel,
.graph-viewer:fullscreen .gv-relation-popup {
  max-height: calc(100vh - 40px);
  overflow: auto;
}

.graph-viewer.dense-mode .gv-header {
  position: absolute;
  inset: 18px 18px auto 18px;
  z-index: 9;
  padding: 0;
  border-bottom: 0;
  background: transparent;
  display: grid;
  grid-template-columns: minmax(220px, auto) minmax(260px, 0.9fr) auto;
  align-items: start;
  gap: 12px;
  pointer-events: none;
}

.graph-viewer.dense-preset-mirofish .gv-header {
  inset: 12px 12px auto 12px;
  grid-template-columns: minmax(180px, auto) minmax(220px, 0.75fr) auto;
  gap: 10px;
}

.graph-viewer.dense-mode .gv-title {
  font-size: 18px;
  font-weight: 700;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(222, 212, 202, 0.9);
  box-shadow: 0 18px 36px rgba(92, 62, 46, 0.12);
  pointer-events: auto;
}

.graph-viewer.dense-preset-mirofish .gv-title {
  font-size: 16px;
  padding: 11px 14px;
  border-radius: 16px;
  box-shadow: 0 14px 26px rgba(92, 62, 46, 0.1);
}

.gv-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  background: rgba(255, 244, 229, 0.96);
  flex-wrap: wrap;
  gap: 10px;
}

.gv-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 10px;
}

.gv-counts {
  font-size: 11px;
  color: var(--muted);
  font-weight: 400;
}

.graph-viewer.dense-mode .gv-counts {
  font-size: 12.5px;
}

.graph-viewer.dense-preset-mirofish .gv-counts {
  font-size: 11px;
}

.gv-search {
  flex: 1;
  min-width: 180px;
  max-width: 320px;
}

.graph-viewer.dense-mode .gv-search {
  max-width: none;
  min-width: 260px;
  pointer-events: auto;
}

.gv-search-input {
  width: 100%;
  padding: 8px 11px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.82);
  color: var(--text);
  font-size: 12px;
  font-family: inherit;
}

.graph-viewer.dense-mode .gv-search-input {
  padding: 13px 18px;
  font-size: 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.92);
  border-color: rgba(222, 212, 202, 0.9);
  box-shadow: 0 18px 36px rgba(92, 62, 46, 0.1);
}

.graph-viewer.dense-preset-mirofish .gv-search-input {
  padding: 11px 15px;
  font-size: 13px;
  border-radius: 16px;
  box-shadow: 0 14px 26px rgba(92, 62, 46, 0.08);
}

.gv-controls { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }

.graph-viewer.dense-mode .gv-controls {
  justify-content: flex-end;
  pointer-events: auto;
}

.gv-stat-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  padding: 10px 16px;
  border-bottom: 1px solid rgba(209, 122, 62, 0.12);
  background: rgba(255, 249, 242, 0.9);
}

.graph-viewer.dense-mode .gv-stat-strip {
  display: none;
}

.gv-stat {
  padding: 9px 10px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(209, 122, 62, 0.1);
}

.gv-stat-label {
  display: block;
  font-size: 10px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 4px;
}

.gv-stat-value {
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
}

.mode-btn {
  padding: 5px 12px;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--border);
  border-radius: 5px;
  color: var(--muted);
  cursor: pointer;
  font-family: inherit;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.graph-viewer.dense-mode .mode-btn,
.graph-viewer.dense-mode .icon-btn {
  padding: 11px 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.92);
  border-color: rgba(222, 212, 202, 0.9);
  box-shadow: 0 18px 36px rgba(92, 62, 46, 0.1);
}

.graph-viewer.dense-preset-mirofish .mode-btn,
.graph-viewer.dense-preset-mirofish .icon-btn {
  padding: 9px 13px;
  border-radius: 14px;
  box-shadow: 0 14px 24px rgba(92, 62, 46, 0.08);
}

.mode-btn:hover:not(.disabled) { color: var(--text); border-color: var(--border2); }
.mode-btn.active { color: var(--accent); border-color: var(--accent); background: rgba(255, 237, 221, 0.96); }
.mode-btn.disabled { opacity: 0.35; cursor: not-allowed; }

.btn-hint { font-size: 10px; color: var(--muted); }

.icon-btn {
  padding: 5px 9px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--border);
  border-radius: 5px;
  color: var(--muted);
  cursor: pointer;
  font-size: 14px;
  transition: all 0.15s;
}

.icon-btn:hover { color: var(--text); }

.gv-canvas {
  position: relative;
  background: #fafaf9;
  cursor: grab;
}

.graph-viewer.dense-mode .gv-canvas {
  background:
    radial-gradient(circle at top left, rgba(255, 148, 109, 0.1), transparent 26%),
    radial-gradient(circle at bottom right, rgba(90, 179, 255, 0.08), transparent 24%),
    radial-gradient(circle, rgba(188, 182, 177, 0.22) 1.2px, transparent 1.5px),
    #fefdfb;
  background-size: auto, auto, 20px 20px, auto;
  min-height: 100%;
}

.graph-viewer.dense-preset-mirofish .gv-canvas {
  background:
    radial-gradient(circle at top left, rgba(255, 148, 109, 0.07), transparent 24%),
    radial-gradient(circle at bottom right, rgba(90, 179, 255, 0.06), transparent 22%),
    radial-gradient(circle, rgba(188, 182, 177, 0.18) 1.15px, transparent 1.3px),
    #fffefc;
  background-size: auto, auto, 18px 18px, auto;
}

.gv-canvas:active { cursor: grabbing; }

/* Node styles */
.node-circle {
  transition: opacity 0.16s ease, stroke-width 0.16s ease, filter 0.16s ease, transform 0.16s ease;
}

.node-bubble-main {
  stroke-width: 1.05;
  filter: url(#gv-node-bubble-shadow);
}

.graph-viewer.dense-mode .node-bubble-main {
  stroke-width: 0.96;
}

.node-bubble-halo {
  opacity: 0.16;
  transition: opacity 0.16s ease, transform 0.16s ease;
}

.graph-viewer.dense-preset-mirofish .node-bubble-halo {
  opacity: 0.13;
}

.node-bubble-core {
  fill: rgba(255, 255, 255, 0.14);
  opacity: 0.56;
  pointer-events: none;
}

.graph-viewer.dense-preset-mirofish .node-bubble-core {
  opacity: 0.48;
}

.node-bubble-highlight {
  fill: rgba(255, 255, 255, 0.72);
  opacity: 0.88;
  pointer-events: none;
}

.graph-viewer.dense-preset-mirofish .node-bubble-highlight {
  opacity: 0.78;
}

.node-person,
.node-org,
.node-event,
.node-concept,
.node-place,
.node-unknown {
  stroke-linejoin: round;
}

.gv-node { cursor: pointer; transition: opacity 0.15s ease; }
.gv-node:hover .node-bubble-main {
  opacity: 0.94;
  filter: url(#gv-node-bubble-shadow);
}
.gv-node:hover .node-bubble-halo {
  opacity: 0.24;
}
.gv-node.selected .node-bubble-main {
  stroke: #3b2b21;
  stroke-width: 2.25;
}
.gv-node.selected .node-bubble-halo {
  opacity: 0.28;
}
.gv-node.dimmed { opacity: 0.24; }

.gv-node-label {
  font-size: 10px;
  fill: #374151;
  pointer-events: none;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.graph-viewer.dense-mode .gv-node-label {
  font-size: 6.7px;
  fill: rgba(108, 94, 84, 0.56);
}

.graph-viewer.dense-preset-mirofish .gv-node-label {
  font-size: 5.6px;
  fill: rgba(107, 100, 94, 0.72);
}

.gv-edge-label-group {
  pointer-events: none;
  user-select: none;
}

.gv-edge-label-bg {
  fill: rgba(255, 255, 255, 0.84);
  stroke: rgba(255, 255, 255, 0.94);
  stroke-width: 0.75px;
}

.graph-viewer.dense-mode .gv-edge-label-bg {
  fill: rgba(255, 255, 255, 0.88);
}

.graph-viewer.dense-preset-mirofish .gv-edge-label-bg {
  fill: rgba(255, 255, 255, 0.92);
  stroke: rgba(248, 246, 242, 0.98);
  stroke-width: 0.6px;
}

.gv-edge-label {
  font-size: var(--gv-edge-label-size, 7.2px);
  fill: #6b7280;
  paint-order: stroke;
  stroke: rgba(255, 255, 255, 0.72);
  stroke-width: 1.25px;
  stroke-linejoin: round;
  pointer-events: none;
  user-select: none;
  letter-spacing: 0.01em;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.graph-viewer.dense-preset-mirofish .gv-edge-label {
  fill: rgba(120, 116, 112, 0.8);
  stroke-width: 0.95px;
}

/* Link styles */
.gv-link       { fill: none; opacity: 0.65; }
.link-kg       { stroke: rgba(156, 163, 175, 0.5); }
.link-causal   { stroke: #f2a93b; opacity: 0.78; }

.gv-live-link-signal {
  opacity: 0.98;
  animation: gvSignalPulse 1.85s ease-in-out infinite;
}

.gv-live-link-signal-tail {
  fill: none;
  stroke-linecap: round;
  animation: gvSignalTail 1.9s ease-in-out infinite;
}

.gv-live-link-signal-bar {
  fill: none;
  stroke-linecap: round;
  animation: gvSignalBar 1.9s ease-in-out infinite;
}

.gv-live-link-signal-diamond {
  stroke-linejoin: round;
  animation: gvSignalDiamond 1.9s ease-in-out infinite;
}

.gv-live-link-signal-dot {
  animation: gvSignalDot 1.9s ease-in-out infinite;
}

.gv-live-link-signal-speck {
  animation: gvSignalSpeck 1.9s ease-in-out infinite;
}

.graph-viewer.dense-mode .gv-link {
  opacity: 0.88;
}

.graph-viewer.dense-preset-mirofish .gv-link {
  opacity: 0.82;
}

.graph-viewer.dense-mode .link-kg {
  stroke: rgba(150, 149, 148, 0.26);
}

.graph-viewer.dense-preset-mirofish .link-kg {
  stroke: rgba(132, 134, 139, 0.22);
}

.graph-viewer.dense-mode .link-inferred {
  stroke: rgba(160, 156, 152, 0.18);
  opacity: 0.48;
}

.graph-viewer.dense-preset-mirofish .link-inferred {
  stroke: rgba(147, 148, 152, 0.12);
  opacity: 0.34;
}

/* Loading overlay */
.gv-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 245, 234, 0.86);
  color: var(--muted);
  font-size: 13px;
  gap: 12px;
}

.graph-viewer.dense-mode .gv-loading {
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(6px);
}

.loading-spinner {
  width: 28px;
  height: 28px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

@keyframes gvSignalPulse {
  0%, 100% {
    opacity: 0.82;
  }
  50% {
    opacity: 1;
  }
}

@keyframes gvSignalTail {
  0%, 100% {
    opacity: 0.26;
  }
  50% {
    opacity: 0.72;
  }
}

@keyframes gvSignalBar {
  0%, 100% {
    opacity: 0.34;
  }
  50% {
    opacity: 0.9;
  }
}

@keyframes gvSignalDiamond {
  0%, 100% {
    transform: scale(0.92);
  }
  50% {
    transform: scale(1);
  }
}

@keyframes gvSignalDot {
  0%, 100% {
    opacity: 0.72;
    transform: scale(0.88);
  }
  50% {
    opacity: 1;
    transform: scale(1.08);
  }
}

@keyframes gvSignalSpeck {
  0%, 100% {
    opacity: 0.18;
  }
  50% {
    opacity: 0.46;
  }
}

/* Detail panel */
.gv-panel {
  position: absolute;
  top: 60px;
  right: 12px;
  width: 260px;
  background: rgba(255, 248, 240, 0.96);
  border: 1px solid var(--border2);
  border-radius: 14px;
  padding: 13px;
  z-index: 10;
}

.graph-viewer.dense-mode .gv-panel,
.graph-viewer.dense-mode .gv-relation-popup {
  backdrop-filter: blur(14px);
  border-radius: 22px;
  box-shadow: 0 28px 58px rgba(92, 62, 46, 0.16);
}

.graph-viewer.dense-mode .gv-panel {
  top: 110px;
  right: 18px;
  width: 326px;
  max-height: calc(100% - 138px);
  overflow: auto;
  background: rgba(255, 255, 255, 0.97);
  border-color: rgba(224, 216, 208, 0.94);
}

.gv-relation-popup {
  position: absolute;
  left: 12px;
  bottom: 56px;
  width: 280px;
  background: rgba(255, 248, 240, 0.98);
  border: 1px solid var(--border2);
  border-radius: 12px;
  padding: 14px;
  z-index: 10;
}

.graph-viewer.dense-mode .gv-relation-popup {
  top: 110px;
  right: 18px;
  left: auto;
  bottom: auto;
  width: 326px;
  background: rgba(255, 255, 255, 0.97);
  border-color: rgba(224, 216, 208, 0.94);
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
  padding-right: 22px;
}

.panel-head-copy {
  min-width: 0;
}

.panel-kicker {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 5px;
}

.panel-type-badge {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(27, 154, 131, 0.12);
  color: #1b9a83;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.panel-close {
  position: absolute;
  top: 10px;
  right: 12px;
  cursor: pointer;
  color: var(--muted);
  font-size: 12px;
}

.panel-close:hover { color: var(--text); }

.panel-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  padding-right: 20px;
}

.panel-desc {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 12px;
}

.panel-chip-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: 12px;
}

.panel-chip-card {
  padding: 9px 10px;
  border-radius: 12px;
  background: rgba(249, 248, 245, 0.9);
  border: 1px solid rgba(219, 205, 193, 0.78);
}

.panel-chip-label {
  display: block;
  margin-bottom: 4px;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.panel-chip-card strong {
  font-size: 12px;
  color: var(--text);
}

.panel-section-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
  margin-bottom: 8px;
}

.panel-connections { margin-bottom: 10px; }

.conn-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  padding: 5px 0;
  border-bottom: 1px solid rgba(209, 122, 62, 0.12);
  cursor: pointer;
}

.conn-item:hover { color: var(--accent); }
.conn-direction  { color: var(--muted); width: 14px; }
.conn-rel        { color: var(--muted); font-size: 10px; flex: 1; }
.conn-name       { font-weight: 500; }
.no-conn         { font-size: 11px; color: var(--muted); }

.relation-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 10px 0 12px;
}

.relation-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  font-size: 11px;
}

.relation-key {
  color: var(--muted);
}

.relation-value {
  color: var(--text);
  font-weight: 600;
  text-align: right;
}

.causal-info     { margin-top: 10px; }

.strength-bar-bg {
  height: 5px;
  background: rgba(236, 221, 203, 0.75);
  border-radius: 3px;
  margin: 6px 0;
  overflow: hidden;
}

.strength-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #ef6b4a 0%, #f2a93b 100%);
  border-radius: 3px;
}

.strength-label { font-size: 11px; color: var(--amber); }

/* Legend */
.gv-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 10px 16px;
  border-top: 1px solid var(--border);
  background: rgba(255, 246, 235, 0.88);
}

.graph-viewer.dense-mode .gv-legend {
  position: absolute;
  left: 18px;
  bottom: 18px;
  z-index: 8;
  max-width: 382px;
  border: 1px solid rgba(224, 208, 195, 0.88);
  border-top: 1px solid rgba(224, 208, 195, 0.88);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 36px rgba(92, 62, 46, 0.12);
  padding: 12px 14px;
}

.graph-viewer.dense-preset-mirofish .gv-legend {
  left: 12px;
  bottom: 12px;
  max-width: 318px;
  padding: 10px 12px;
  border-radius: 16px;
  box-shadow: 0 14px 24px rgba(92, 62, 46, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--muted);
}

.graph-viewer.dense-mode .legend-item {
  font-size: 13px;
}

.graph-viewer.dense-preset-mirofish .legend-item {
  font-size: 11px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1.5px solid;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.78),
    0 1px 2px rgba(59, 43, 33, 0.12);
}

.legend-dot.node-person  {
  background: radial-gradient(circle at 34% 30%, #ffffff 0%, #c7e0ff 26%, #63a6ff 68%, #2f78e2 100%);
  border-color: #2f78e2;
}
.legend-dot.node-org     {
  background: radial-gradient(circle at 34% 30%, #ffffff 0%, #c7f2e3 26%, #42c8a1 68%, #168769 100%);
  border-color: #168769;
}
.legend-dot.node-event   {
  background: radial-gradient(circle at 34% 30%, #ffffff 0%, #ffd0d6 26%, #f17b8b 68%, #cc4458 100%);
  border-color: #cc4458;
}
.legend-dot.node-concept {
  background: radial-gradient(circle at 34% 30%, #ffffff 0%, #e3d4ff 26%, #b286f3 68%, #7f49cb 100%);
  border-color: #7f49cb;
}
.legend-dot.node-place   {
  background: radial-gradient(circle at 34% 30%, #ffffff 0%, #ffe6b0 26%, #efbf56 68%, #c48313 100%);
  border-color: #c48313;
}

.legend-line {
  width: 24px;
  height: 2px;
}

.legend-line.causal { background: var(--amber); }

/* ── Theme Refresh ─────────────────────────────────────────────────────── */
.graph-viewer {
  --gv-bg: rgba(255, 255, 255, 0.98);
  --gv-bg-soft: rgba(246, 249, 255, 0.98);
  --gv-bg-panel: rgba(250, 252, 255, 0.94);
  --gv-border: rgba(144, 162, 226, 0.24);
  --gv-border-strong: rgba(144, 162, 226, 0.42);
  --gv-shadow: rgba(92, 108, 170, 0.14);
  --gv-text: #253252;
  --gv-muted: #6f7a98;
  --gv-accent: #8a74ff;
  --gv-accent-soft: rgba(138, 116, 255, 0.14);
  --gv-blue-soft: rgba(103, 198, 255, 0.14);
  --gv-canvas-dot: rgba(163, 176, 222, 0.24);
  --border: var(--gv-border);
  --border2: var(--gv-border-strong);
  --text: var(--gv-text);
  --muted: var(--gv-muted);
  --accent: var(--gv-accent);
  --amber: #b58fff;
}

.graph-viewer {
  background: var(--gv-bg);
  border-color: var(--gv-border);
  box-shadow: 0 20px 44px var(--gv-shadow);
}

.graph-viewer.dense-mode,
.graph-viewer.dense-preset-mirofish,
.graph-viewer:fullscreen {
  background: var(--gv-bg-soft);
  border-color: var(--gv-border);
}

.gv-header,
.gv-stat-strip {
  border-color: rgba(144, 162, 226, 0.14);
}

.gv-header {
  background: rgba(244, 247, 255, 0.94);
}

.graph-viewer.dense-mode .gv-title,
.gv-search-input,
.mode-btn,
.icon-btn,
.gv-stat,
.gv-panel,
.gv-relation-popup,
.gv-legend {
  border-color: var(--gv-border);
  box-shadow: 0 18px 38px rgba(97, 116, 180, 0.1);
}

.graph-viewer.dense-mode .gv-title,
.graph-viewer.dense-mode .gv-search-input,
.graph-viewer.dense-mode .mode-btn,
.graph-viewer.dense-mode .icon-btn,
.gv-panel,
.gv-relation-popup,
.gv-legend {
  background: var(--gv-bg-panel);
}

.gv-title,
.gv-stat-value,
.panel-name,
.relation-value {
  color: var(--gv-text);
}

.gv-counts,
.gv-stat-label,
.btn-hint,
.panel-kicker,
.panel-desc,
.panel-section-label,
.relation-key,
.legend-item,
.conn-direction,
.conn-rel,
.no-conn,
.strength-label {
  color: var(--gv-muted);
}

.gv-search-input,
.mode-btn,
.icon-btn,
.gv-stat,
.panel-chip-card,
.conn-item,
.gv-legend {
  border-color: rgba(144, 162, 226, 0.18);
}

.gv-search-input {
  background: rgba(255, 255, 255, 0.92);
  color: var(--gv-text);
}

.graph-viewer.dense-mode .gv-search-input,
.graph-viewer.dense-mode .mode-btn,
.graph-viewer.dense-mode .icon-btn {
  border-color: rgba(150, 168, 232, 0.26);
}

.mode-btn {
  background: rgba(255, 255, 255, 0.82);
  color: var(--gv-muted);
}

.mode-btn.active {
  color: var(--gv-accent);
  border-color: rgba(138, 116, 255, 0.34);
  background: rgba(244, 241, 255, 0.96);
}

.icon-btn:hover,
.mode-btn:hover:not(.disabled),
.conn-item:hover {
  color: var(--gv-text);
  border-color: var(--gv-border-strong);
}

.gv-canvas {
  background: #f9fbff;
}

.graph-viewer.dense-mode .gv-canvas,
.graph-viewer.dense-preset-mirofish .gv-canvas {
  background:
    radial-gradient(circle at top left, rgba(108, 191, 255, 0.12), transparent 28%),
    radial-gradient(circle at top right, rgba(188, 145, 255, 0.12), transparent 24%),
    radial-gradient(circle at bottom right, rgba(105, 232, 245, 0.09), transparent 24%),
    radial-gradient(circle, var(--gv-canvas-dot) 1.15px, transparent 1.35px),
    #fbfcff;
}

.gv-node.selected .node-bubble-main {
  stroke: #4d60a4;
}

.gv-node-label {
  fill: #4f5b7a;
}

.graph-viewer.dense-mode .gv-node-label {
  fill: rgba(86, 101, 143, 0.66);
}

.graph-viewer.dense-preset-mirofish .gv-node-label {
  fill: rgba(88, 99, 140, 0.72);
}

.gv-edge-label-bg {
  fill: rgba(255, 255, 255, 0.92);
  stroke: rgba(236, 241, 255, 0.98);
}

.gv-edge-label {
  fill: #7380a1;
  stroke: rgba(255, 255, 255, 0.88);
}

.link-causal {
  stroke: #b58fff;
  opacity: 0.86;
}

.graph-viewer.dense-mode .link-kg {
  stroke: rgba(136, 150, 192, 0.28);
}

.graph-viewer.dense-preset-mirofish .link-kg {
  stroke: rgba(136, 150, 192, 0.22);
}

.gv-loading {
  background: rgba(248, 250, 255, 0.9);
  color: var(--gv-muted);
}

.loading-spinner {
  border-color: rgba(144, 162, 226, 0.24);
  border-top-color: var(--gv-accent);
}

.panel-type-badge {
  background: rgba(103, 198, 255, 0.14);
  color: #4c7cf7;
}

.panel-chip-card {
  background: rgba(246, 249, 255, 0.92);
}

.conn-item {
  border-bottom-color: rgba(144, 162, 226, 0.14);
}

.strength-bar-bg {
  background: rgba(222, 229, 249, 0.78);
}

.strength-bar-fill {
  background: linear-gradient(90deg, #67c6ff 0%, #8a74ff 100%);
}

.legend-line.causal {
  background: #b58fff;
}

.gv-legend {
  background: rgba(247, 250, 255, 0.9);
}

.legend-dot {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.86),
    0 1px 2px rgba(82, 96, 142, 0.14);
}

.legend-dot.node-place   {
  background: radial-gradient(circle at 34% 30%, #ffffff 0%, #d9f7ff 26%, #7ed6ff 68%, #3b94ff 100%);
  border-color: #3b94ff;
}

/* Slide panel transition */
.slide-panel-enter-active { animation: slidePanel 0.2s ease; }
.slide-panel-leave-active { animation: slidePanel 0.15s ease reverse; }
@keyframes slidePanel { from { opacity:0; transform: translateX(10px); } to { opacity:1; transform: none; } }
</style>
