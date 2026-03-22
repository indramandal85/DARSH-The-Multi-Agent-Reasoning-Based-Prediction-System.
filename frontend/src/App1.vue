<template>
  <div id="app">

    <!-- ── Top bar ── -->
    <header class="topbar">
      <div class="topbar-left">
        <span class="logo">DARSH</span>
        <span class="version">v2.0</span>
      </div>
      <div class="topbar-right">
        <span class="status-dot" :class="apiOk ? 'green' : 'red'"></span>
        <span class="status-label">{{ apiOk ? 'API connected' : 'API offline' }}</span>
      </div>
    </header>

    <!-- ── Step progress bar ── -->
    <nav class="steps">
      <div
        v-for="(label, i) in stepLabels"
        :key="i"
        class="step"
        :class="{
          active   : currentStep === i,
          done     : currentStep > i,
          disabled : currentStep < i
        }"
        @click="currentStep > i ? currentStep = i : null"
      >
        <span class="step-num">{{ currentStep > i ? '✓' : i + 1 }}</span>
        <span class="step-label">{{ label }}</span>
      </div>
    </nav>

    <!-- ════════════════════════════════════════════════════
         SCREEN 0 — Document Input
    ════════════════════════════════════════════════════ -->
    <main v-if="currentStep === 0" class="screen">

      <h1 class="screen-title">Choose Input Source</h1>
      <p class="screen-sub">
        Upload a document, fetch today's live news, or load a historical event for backtesting.
      </p>

      <!-- Mode tabs -->
      <div class="mode-tabs">
        <button
          v-for="m in modes"
          :key="m.id"
          class="mode-tab"
          :class="{ active: inputMode === m.id }"
          @click="switchMode(m.id)"
        >
          <span class="tab-icon">{{ m.icon }}</span>
          {{ m.label }}
        </button>
      </div>

      <!-- ── Tab A: Manual Upload ── -->
      <div v-if="inputMode === 'upload'" class="mode-body">
        <p class="mode-desc">
          Upload any <code>.txt</code> document. The system builds a knowledge graph,
          causal DAG, and runs multi-agent simulation to predict social outcomes.
        </p>

        <div
          class="dropzone"
          :class="{ 'dropzone-ready': uploadedFilename }"
          @click="$refs.fileInput.click()"
          @dragover.prevent
          @drop.prevent="handleDrop"
        >
          <div v-if="!uploadedFilename" class="dropzone-empty">
            <div class="drop-arrow">↑</div>
            <p>Click or drag a <strong>.txt</strong> file here</p>
            <span class="drop-hint">Max ~5,000 words for best results</span>
          </div>
          <div v-else class="dropzone-done">
            <span class="check-big">✓</span>
            <p>{{ uploadedFilename }}</p>
            <span class="drop-hint">{{ uploadedWordCount }} words loaded</span>
          </div>
        </div>
        <input ref="fileInput" type="file" accept=".txt,.md" style="display:none" @change="handleFileUpload" />
      </div>

      <!-- ── Tab B: Live News ── -->
      <div v-if="inputMode === 'live'" class="mode-body">
        <div class="info-banner info-blue">
          <strong>Forward prediction mode.</strong>
          Fetches today's real news from BBC, Reuters, Economic Times and Moneycontrol.
          Use this to predict what will happen next — not to test past accuracy.
        </div>

        <div class="field-group">
          <label class="field-label">Topics <span class="field-hint">(comma-separated keywords)</span></label>
          <input
            v-model="liveTopics"
            type="text"
            class="field-input"
            placeholder="RBI, interest rate, India inflation, 2025"
            @keyup.enter="fetchLiveNews"
          />
          <p class="field-note">Be specific. "RBI interest rate India 2025" works better than just "rates".</p>
        </div>

        <button class="btn-secondary" @click="fetchLiveNews" :disabled="!liveTopics.trim() || fetchLoading">
          {{ fetchLoading ? 'Fetching RSS feeds...' : 'Fetch Live News' }}
        </button>

        <div v-if="fetchMessage" class="status-pill" :class="fetchError ? 'pill-red' : 'pill-green'">
          {{ fetchMessage }}
        </div>
      </div>

      <!-- ── Tab C: Historical Backtest ── -->
      <div v-if="inputMode === 'historical'" class="mode-body">
        <div class="info-banner info-amber">
          <strong>Backtest mode.</strong>
          The system predicts the outcome without seeing it.
          After simulation you reveal the actual outcome and get a Brier score.
        </div>

        <div class="field-group">
          <label class="field-label">Select Historical Event</label>
          <select v-model="selectedEventId" class="field-select">
            <option value="" disabled>Choose an event...</option>
            <option
              v-for="ev in historicalEvents"
              :key="ev.event_id"
              :value="ev.event_id"
            >
              {{ ev.date }} — {{ ev.description.slice(0, 65) }}...
            </option>
          </select>
        </div>

        <div v-if="selectedEventId && selectedEventMeta" class="event-card">
          <div class="event-row">
            <span class="event-key">Domain</span>
            <span class="event-val">{{ selectedEventMeta.domain }}</span>
          </div>
          <div class="event-row">
            <span class="event-key">Date</span>
            <span class="event-val">{{ selectedEventMeta.date }}</span>
          </div>
          <div class="event-row">
            <span class="event-key">Actual outcome</span>
            <span class="event-val hidden-outcome">Hidden until after simulation ✦</span>
          </div>
        </div>

        <button class="btn-secondary" @click="loadHistorical" :disabled="!selectedEventId || fetchLoading">
          {{ fetchLoading ? 'Loading document...' : 'Load Historical Document' }}
        </button>

        <div v-if="fetchMessage" class="status-pill" :class="fetchError ? 'pill-red' : 'pill-green'">
          {{ fetchMessage }}
        </div>
      </div>

      <!-- ── Document ready: Build graph button ── -->
      <transition name="slide-up">
        <div v-if="uploadedFilename" class="build-section">
          <div class="file-badge">
            <span class="file-icon">📄</span>
            <span class="file-name">{{ uploadedFilename }}</span>
            <span class="file-words">{{ uploadedWordCount }} words</span>
          </div>

          <button
            class="btn-primary"
            @click="buildGraph"
            :disabled="isBuilding"
          >
            {{ isBuilding ? 'Building knowledge graph...' : 'Build Knowledge Graph →' }}
          </button>

          <div v-if="graphMessage" class="status-pill" :class="graphError ? 'pill-red' : 'pill-green'">
            {{ graphMessage }}
          </div>

          <!-- Graph build progress -->
          <div v-if="isBuilding" class="progress-bar">
            <div class="progress-fill indeterminate"></div>
          </div>

          <div v-if="graphResult" class="graph-result">
            <div class="graph-stat">
              <span class="stat-num">{{ graphResult.entity_count }}</span>
              <span class="stat-lbl">entities</span>
            </div>
            <div class="graph-divider"></div>
            <div class="graph-stat">
              <span class="stat-num">{{ graphResult.edge_count }}</span>
              <span class="stat-lbl">relationships</span>
            </div>
          </div>
        </div>
      </transition>

    </main>

    <!-- ════════════════════════════════════════════════════
         SCREEN 1 — Configure Simulation
    ════════════════════════════════════════════════════ -->
    <main v-if="currentStep === 1" class="screen">

      <h1 class="screen-title">Configure Simulation</h1>
      <p class="screen-sub">
        Define the scenario. The multi-agent society will reason about this situation
        across parallel simulation branches.
      </p>

      <div class="config-grid">

        <div class="field-group">
          <label class="field-label">Prediction topic</label>
          <input v-model="config.topic" type="text" class="field-input"
                 placeholder="RBI emergency rate hike impact on Indian economy" />
        </div>

        <div class="field-group">
          <label class="field-label">Initial situation</label>
          <textarea v-model="config.situation" class="field-textarea" rows="3"
                    placeholder="Describe the current world state that agents will start from..."></textarea>
        </div>

        <div class="field-group">
          <label class="field-label">
            Events per round
            <span class="field-hint">(one per line, up to 3)</span>
          </label>
          <textarea v-model="config.eventsRaw" class="field-textarea" rows="3"
                    placeholder="Round 1: Economists warn of recession risk&#10;Round 2: Banks announce EMI increases&#10;Round 3: Government responds"></textarea>
        </div>

        <div class="config-row">
          <div class="field-group half">
            <label class="field-label">Agents per branch</label>
            <div class="slider-wrap">
              <input type="range" v-model.number="config.numAgents" min="3" max="10" step="1" class="field-slider" />
              <span class="slider-val">{{ config.numAgents }}</span>
            </div>
          </div>
          <div class="field-group half">
            <label class="field-label">Parallel branches</label>
            <div class="slider-wrap">
              <input type="range" v-model.number="config.numBranches" min="1" max="5" step="1" class="field-slider" />
              <span class="slider-val">{{ config.numBranches }}</span>
            </div>
          </div>
        </div>

        <div class="field-group">
          <label class="field-label">Simulation rounds</label>
          <div class="slider-wrap">
            <input type="range" v-model.number="config.numRounds" min="2" max="5" step="1" class="field-slider" />
            <span class="slider-val">{{ config.numRounds }}</span>
          </div>
        </div>

      </div>

      <!-- Time estimate -->
      <div class="estimate-card">
        <span class="estimate-label">Estimated runtime</span>
        <span class="estimate-time">~{{ estimatedMinutes }} minutes</span>
        <span class="estimate-detail">
          {{ config.numBranches }} branches × {{ config.numAgents }} agents × {{ config.numRounds }} rounds
          = {{ config.numBranches * config.numAgents * config.numRounds * 3 }} LLM calls
        </span>
      </div>

      <button class="btn-primary" @click="runSimulation">
        Run Simulation →
      </button>

    </main>

    <!-- ════════════════════════════════════════════════════
         SCREEN 2 — Running
    ════════════════════════════════════════════════════ -->
    <main v-if="currentStep === 2" class="screen screen-center">

      <div class="running-indicator">
        <div class="pulse-ring"></div>
        <div class="pulse-core"></div>
      </div>

      <h1 class="screen-title">Simulation Running</h1>

      <p class="running-step">{{ runningStep || 'Initialising agents...' }}</p>
      <p v-if="runningStep && runningStep.includes('report')" class="report-progress-hint">
      Report generation takes 12–18 minutes. Each section is one LLM call.
      </p>

      <div class="progress-bar wide">
        <div class="progress-fill indeterminate"></div>
      </div>

      <div class="running-meta">
        <div class="meta-chip">{{ config.numBranches }} branches</div>
        <div class="meta-chip">{{ config.numAgents }} agents</div>
        <div class="meta-chip">{{ config.numRounds }} rounds</div>
        <div v-if="inputMode === 'historical'" class="meta-chip chip-amber">Backtest mode</div>
        <div v-if="inputMode === 'live'" class="meta-chip chip-blue">Live news mode</div>
      </div>

      <p class="running-hint">
        This takes {{ estimatedMinutes }}–{{ estimatedMinutes + 3 }} minutes.
        The page polls automatically — do not refresh.
      </p>

    </main>

    <!-- ════════════════════════════════════════════════════
         SCREEN 3 — Results
    ════════════════════════════════════════════════════ -->
    <main v-if="currentStep === 3" class="screen">

      <h1 class="screen-title">Prediction Results</h1>

      <!-- Outcome distribution bars -->
      <div class="outcome-card">
        <div class="outcome-header">
          <span>Outcome probability distribution</span>
          <span class="branch-count">{{ simResult.num_branches }} branches</span>
        </div>

        <div
          v-for="(prob, outcome) in sortedOutcomes"
          :key="outcome"
          class="outcome-row"
        >
          <span class="outcome-label">{{ outcome }}</span>
          <div class="outcome-bar-bg">
            <div
              class="outcome-bar-fill"
              :class="outcomeColor(outcome)"
              :style="{ width: animateBars ? prob + '%' : '0%' }"
            ></div>
          </div>
          <span class="outcome-pct">{{ prob.toFixed(1) }}%</span>
        </div>
      </div>

      <!-- Dominant outcome badge -->
      <div class="dominant-badge" :class="outcomeColor(simResult.dominant_outcome)">
        <span class="badge-label">Dominant prediction</span>
        <span class="badge-outcome">{{ simResult.dominant_outcome?.toUpperCase() }}</span>
        <span class="badge-prob">{{ (simResult.outcome_probs?.[simResult.dominant_outcome] || 0).toFixed(1) }}% of branches</span>
      </div>

      <!-- Prediction summary -->
      <div class="prediction-summary">
        <p>{{ simResult.prediction }}</p>
      </div>

      <!-- ── Backtest scoring panel (historical mode only) ── -->
      <div v-if="inputMode === 'historical' && actualOutcome" class="backtest-panel">
        <div class="backtest-title">Historical Backtest Scoring</div>

        <div v-if="!brierResult" class="backtest-reveal">
          <p class="backtest-hint">
            The simulation ran without seeing the actual outcome.
            Reveal it now to get your Brier score.
          </p>
          <button class="btn-secondary" @click="scorePrediction">
            Reveal Actual Outcome & Score →
          </button>
        </div>

        <div v-else class="brier-table">
          <div class="brier-row">
            <span class="brier-key">Predicted</span>
            <span class="brier-val">{{ brierResult.dominant_predicted }}</span>
          </div>
          <div class="brier-row">
            <span class="brier-key">Actual outcome</span>
            <span class="brier-val" :class="brierResult.correct ? 'val-correct' : 'val-wrong'">
              {{ brierResult.actual_outcome }}
              {{ brierResult.correct ? '✓ Correct' : '✗ Wrong' }}
            </span>
          </div>
          <div class="brier-row">
            <span class="brier-key">Brier score</span>
            <span class="brier-val">{{ brierResult.brier_score }} — {{ brierResult.interpretation }}</span>
          </div>
        </div>
      </div>

      <!-- Full report toggle -->
      <div class="report-section">
        <button class="btn-ghost" @click="showReport = !showReport">
          {{ showReport ? 'Hide report ▲' : 'Show full 6-section report ▼' }}
        </button>

        <div v-if="showReport" class="report-body">
          <pre class="report-text">{{ simResult.report }}</pre>
        </div>
      </div>

      <!-- Actions row -->
      <div class="actions-row">
        <button class="btn-secondary" @click="downloadReport">
          Download Report (.md)
        </button>
        <button class="btn-ghost" @click="resetAll">
          ← Start New Prediction
        </button>
      </div>

    </main>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import axios from 'axios'
import GraphViewer from './GraphViewer.vue'

const API = 'http://localhost:5001'

// ── Core navigation ──────────────────────────────────────────────────────────
const currentStep = ref(0)
const stepLabels  = ['Input', 'Configure', 'Running', 'Results']
const apiOk       = ref(false)

// ── Input mode ───────────────────────────────────────────────────────────────
const modes = [
  { id: 'upload',     label: 'Manual Upload',      icon: '📄' },
  { id: 'live',       label: 'Live News',           icon: '📡' },
  { id: 'historical', label: 'Historical Backtest', icon: '🔍' }
]
const inputMode = ref('upload')

// ── Upload state ─────────────────────────────────────────────────────────────
const uploadedFilename = ref('')
const uploadedWordCount = ref(0)

// ── Live news state ───────────────────────────────────────────────────────────
const liveTopics   = ref('')
const fetchLoading = ref(false)
const fetchMessage = ref('')
const fetchError   = ref(false)

// ── Historical state ──────────────────────────────────────────────────────────
const historicalEvents  = ref([])
const selectedEventId   = ref('')
const actualOutcome     = ref('')     // revealed only after simulation
const brierResult       = ref(null)

const selectedEventMeta = computed(() =>
  historicalEvents.value.find(e => e.event_id === selectedEventId.value) || null
)

// ── Graph build state ─────────────────────────────────────────────────────────
const isBuilding  = ref(false)
const graphMessage = ref('')
const graphError  = ref(false)
const graphResult = ref(null)
const graphJobId  = ref(null)
const graphName   = ref('')

// ── Simulation config ─────────────────────────────────────────────────────────
const config = ref({
  topic      : '',
  situation  : '',
  eventsRaw  : '',
  numAgents  : 5,
  numBranches: 3,
  numRounds  : 3
})

// ── Simulation running state ──────────────────────────────────────────────────
const runJobId    = ref(null)
const runningStep = ref('')
let   runPoller   = null

// ── Results state ─────────────────────────────────────────────────────────────
const simResult   = ref({})
const showReport  = ref(false)
const animateBars = ref(false)

// ── Computed ──────────────────────────────────────────────────────────────────
const estimatedMinutes = computed(() => {
  const calls = config.value.numBranches * config.value.numAgents * config.value.numRounds * 3
  return Math.max(4, Math.round(calls * 0.08))
})

const sortedOutcomes = computed(() => {
  const probs = simResult.value.outcome_probs || {}
  return Object.fromEntries(
    Object.entries(probs).sort((a, b) => b[1] - a[1])
  )
})

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  checkApi()
  loadHistoricalList()
})

// ── API health ────────────────────────────────────────────────────────────────
async function checkApi() {
  try {
    await axios.get(`${API}/api/health`)
    apiOk.value = true
  } catch {
    apiOk.value = false
  }
}

// ── Mode switch ───────────────────────────────────────────────────────────────
function switchMode(mode) {
  inputMode.value     = mode
  uploadedFilename.value = ''
  uploadedWordCount.value = 0
  fetchMessage.value  = ''
  fetchError.value    = false
  graphMessage.value  = ''
  graphError.value    = false
  graphResult.value   = null
  actualOutcome.value = ''
  brierResult.value   = null
}

// ── Manual file upload ────────────────────────────────────────────────────────
function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  if (file) uploadFile(file)
}

function handleFileUpload(e) {
  const file = e.target.files[0]
  if (file) uploadFile(file)
}

async function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await axios.post(`${API}/api/upload`, form)
    uploadedFilename.value  = res.data.filename
    uploadedWordCount.value = res.data.word_count
  } catch (e) {
    graphMessage.value = 'Upload failed: ' + (e.response?.data?.error || e.message)
    graphError.value   = true
  }
}

// ── Live news fetch ───────────────────────────────────────────────────────────
async function fetchLiveNews() {
  const topics = liveTopics.value.split(',').map(t => t.trim()).filter(Boolean)
  if (!topics.length) return

  fetchLoading.value = true
  fetchMessage.value = 'Connecting to RSS feeds...'
  fetchError.value   = false

  try {
    const res = await axios.post(`${API}/api/fetch-news`, { topics })
    const jobId = res.data.job_id

    const poll = setInterval(async () => {
      const s = await axios.get(`${API}/api/status/${jobId}`)
      const d = s.data

      if (d.status === 'complete') {
        clearInterval(poll)
        fetchLoading.value      = false
        uploadedFilename.value  = d.filename
        uploadedWordCount.value = d.word_count || 0
        fetchMessage.value      = d.message || `✓ ${d.article_count} articles fetched`
        if (d.warning) fetchMessage.value += ' ⚠ ' + d.warning
      } else if (d.status === 'error') {
        clearInterval(poll)
        fetchLoading.value = false
        fetchMessage.value = 'Error: ' + d.error
        fetchError.value   = true
      } else {
        fetchMessage.value = d.step || 'Fetching...'
      }
    }, 2000)

  } catch (e) {
    fetchLoading.value = false
    fetchMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    fetchError.value   = true
  }
}

// ── Historical event load ─────────────────────────────────────────────────────
async function loadHistoricalList() {
  try {
    const res = await axios.get(`${API}/api/historical-events`)
    historicalEvents.value = res.data.events || []
  } catch {
    historicalEvents.value = []
  }
}

async function loadHistorical() {
  if (!selectedEventId.value) return

  fetchLoading.value = true
  fetchMessage.value = 'Loading historical document...'
  fetchError.value   = false

  try {
    const res = await axios.post(`${API}/api/load-historical`,
      { event_id: selectedEventId.value })
    const d = res.data

    fetchLoading.value      = false
    uploadedFilename.value  = d.filename
    uploadedWordCount.value = d.word_count || 0
    actualOutcome.value     = d.actual_outcome   // stored but not shown
    fetchMessage.value      = '✓ ' + d.message

  } catch (e) {
    fetchLoading.value = false
    fetchMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    fetchError.value   = true
  }
}

// ── Build knowledge graph ─────────────────────────────────────────────────────
async function buildGraph() {
  if (!uploadedFilename.value) return

  isBuilding.value   = true
  graphMessage.value = 'Extracting entities and building graph...'
  graphError.value   = false
  graphResult.value  = null

  // Derive graph name from filename
  graphName.value = uploadedFilename.value.replace(/\.[^.]+$/, '')

  try {
    const res = await axios.post(`${API}/api/build-graph`,
      { filename: uploadedFilename.value })
    graphJobId.value = res.data.job_id

    const poll = setInterval(async () => {
      const s = await axios.get(`${API}/api/status/${graphJobId.value}`)
      const d = s.data

      if (d.status === 'complete') {
        clearInterval(poll)
        isBuilding.value   = false
        graphMessage.value = `✓ Graph built — ${d.entity_count} entities, ${d.edge_count} relationships`
        graphResult.value  = d

        // Pre-fill topic from filename
        if (!config.value.topic && graphName.value) {
          config.value.topic = graphName.value.replace(/_/g, ' ')
        }

        setTimeout(() => { currentStep.value = 1 }, 1200)

      } else if (d.status === 'error') {
        clearInterval(poll)
        isBuilding.value   = false
        graphMessage.value = 'Error: ' + d.error
        graphError.value   = true
      } else {
        graphMessage.value = d.step || 'Building...'
      }
    }, 3000)

  } catch (e) {
    isBuilding.value   = false
    graphMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    graphError.value   = true
  }
}

// ── Run simulation ────────────────────────────────────────────────────────────
async function runSimulation() {
  const events = config.value.eventsRaw
    .split('\n').map(l => l.trim()).filter(Boolean)

  if (!config.value.topic.trim()) {
    alert('Please enter a prediction topic.')
    return
  }

  currentStep.value = 2
  runningStep.value = 'Starting simulation branches...'

  try {
    const res = await axios.post(`${API}/api/run-simulation`, {
      topic      : config.value.topic,
      situation  : config.value.situation ||
                   'An event has occurred. Agents will reason about its implications.',
      events     : events.length ? events : [
        'Situation continues to develop.',
        'Expert analysis and reactions published.',
        'Policy responses observed.'
      ],
      num_agents  : config.value.numAgents,
      num_branches: config.value.numBranches,
      num_rounds  : config.value.numRounds
    })

    runJobId.value = res.data.job_id

    runPoller = setInterval(async () => {
      const s = await axios.get(`${API}/api/status/${runJobId.value}`)
      const d = s.data

      if (d.status === 'complete') {
        clearInterval(runPoller)
        simResult.value = d
        currentStep.value = 3
        await nextTick()
        setTimeout(() => { animateBars.value = true }, 100)

      } else if (d.status === 'error') {
        clearInterval(runPoller)
        runningStep.value = 'Error: ' + d.error
      } else {
        runningStep.value = d.step || 'Agents reasoning...'
      }
    }, 5000)

  } catch (e) {
    runningStep.value = 'Error: ' + (e.response?.data?.error || e.message)
  }
}

// ── Backtest scoring ──────────────────────────────────────────────────────────
async function scorePrediction() {
  if (!actualOutcome.value || !simResult.value.outcome_probs) return
  try {
    const res = await axios.post(`${API}/api/score-prediction`, {
      predicted_probs: simResult.value.outcome_probs,
      actual_outcome : actualOutcome.value,
      event_id       : selectedEventId.value || 'unknown'
    })
    brierResult.value = res.data
  } catch (e) {
    console.error('Scoring failed:', e)
  }
}

// ── Download report ───────────────────────────────────────────────────────────
function downloadReport() {
  const content = simResult.value.report || 'No report available.'
  const blob    = new Blob([content], { type: 'text/markdown' })
  const url     = URL.createObjectURL(blob)
  const a       = document.createElement('a')
  a.href        = url
  a.download    = `neuroswarm_report_${Date.now()}.md`
  a.click()
  URL.revokeObjectURL(url)
}

// ── Reset ─────────────────────────────────────────────────────────────────────
function resetAll() {
  currentStep.value      = 0
  inputMode.value        = 'upload'
  uploadedFilename.value = ''
  uploadedWordCount.value = 0
  liveTopics.value       = ''
  fetchMessage.value     = ''
  fetchError.value       = false
  fetchLoading.value     = false
  selectedEventId.value  = ''
  actualOutcome.value    = ''
  brierResult.value      = null
  graphMessage.value     = ''
  graphError.value       = false
  graphResult.value      = null
  isBuilding.value       = false
  runningStep.value      = ''
  simResult.value        = {}
  animateBars.value      = false
  showReport.value       = false
  config.value = { topic: '', situation: '', eventsRaw: '', numAgents: 5, numBranches: 3, numRounds: 3 }
  if (runPoller) clearInterval(runPoller)
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function outcomeColor(outcome) {
  const map = {
    panic    : 'bar-red',
    cautious : 'bar-amber',
    optimistic: 'bar-green',
    divided  : 'bar-blue'
  }
  return map[outcome?.toLowerCase()] || 'bar-blue'
}
</script>

<style>
/* ── Tokens ──────────────────────────────────────────────────────────────── */
:root {
  --bg       : #0d0f11;
  --surface  : #161a1e;
  --surface2 : #1e2329;
  --border   : rgba(255,255,255,0.08);
  --border2  : rgba(255,255,255,0.14);
  --text     : #e8eaed;
  --muted    : #868d96;
  --accent   : #4f9eff;
  --green    : #3ecf8e;
  --amber    : #f5a623;
  --red      : #e05252;
  --radius   : 10px;
  --radius-sm: 6px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
}

#app {
  max-width: 720px;
  margin: 0 auto;
  padding: 0 20px 60px;
}

/* ── Topbar ──────────────────────────────────────────────────────────────── */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0 12px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
}

.logo {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text);
}

.version {
  font-size: 11px;
  color: var(--muted);
  margin-left: 8px;
  background: var(--surface2);
  padding: 2px 7px;
  border-radius: 20px;
  border: 1px solid var(--border);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  color: var(--muted);
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.status-dot.green { background: var(--green); }
.status-dot.red   { background: var(--red); }

/* ── Step nav ────────────────────────────────────────────────────────────── */
.steps {
  display: flex;
  gap: 4px;
  margin-bottom: 36px;
}

.step {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--muted);
  border: 1px solid transparent;
  transition: all 0.2s;
  flex: 1;
  justify-content: center;
}

.step.active {
  background: var(--surface2);
  border-color: var(--border2);
  color: var(--text);
}

.step.done {
  color: var(--green);
  cursor: pointer;
}

.step.done:hover {
  background: var(--surface);
}

.step-num {
  font-size: 11px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--surface2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step.active .step-num { background: var(--accent); color: #fff; }
.step.done .step-num   { background: var(--green);  color: #000; }

/* ── Screen ──────────────────────────────────────────────────────────────── */
.screen {
  animation: fadeIn 0.25s ease;
}
.screen-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-top: 40px;
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

.screen-title {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.03em;
  margin-bottom: 8px;
}

.screen-sub {
  color: var(--muted);
  font-size: 13px;
  margin-bottom: 28px;
  line-height: 1.7;
}

/* ── Mode tabs ───────────────────────────────────────────────────────────── */
.mode-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}

.mode-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--muted);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 12px;
  font-family: inherit;
  transition: all 0.15s;
  white-space: nowrap;
}

.mode-tab:hover { color: var(--text); border-color: var(--border2); }

.mode-tab.active {
  background: var(--surface2);
  border-color: var(--accent);
  color: var(--accent);
}

.tab-icon { font-size: 13px; }

.mode-body { padding: 4px 0; }

.mode-desc {
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 20px;
  line-height: 1.7;
}

/* ── Info banners ────────────────────────────────────────────────────────── */
.info-banner {
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  line-height: 1.6;
  margin-bottom: 20px;
  border-left: 3px solid;
}

.info-blue  { background: rgba(79,158,255,0.07); border-color: var(--accent); color: #a8c8ff; }
.info-amber { background: rgba(245,166,35,0.07); border-color: var(--amber);  color: #f5c86a; }

/* ── Drop zone ───────────────────────────────────────────────────────────── */
.dropzone {
  border: 1.5px dashed var(--border2);
  border-radius: var(--radius);
  padding: 40px 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  margin-bottom: 0;
}

.dropzone:hover { border-color: var(--accent); background: rgba(79,158,255,0.03); }

.dropzone-ready { border-color: var(--green); background: rgba(62,207,142,0.04); }

.dropzone-empty { color: var(--muted); }
.drop-arrow { font-size: 28px; margin-bottom: 10px; color: var(--border2); }
.drop-hint  { font-size: 11px; color: var(--muted); display: block; margin-top: 6px; }

.dropzone-done { color: var(--green); }
.check-big     { font-size: 28px; display: block; margin-bottom: 8px; }

/* ── Fields ──────────────────────────────────────────────────────────────── */
.field-group {
  margin-bottom: 18px;
}

.field-label {
  display: block;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-bottom: 7px;
}

.field-hint { text-transform: none; letter-spacing: 0; font-weight: 400; }

.field-input,
.field-textarea,
.field-select {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  padding: 10px 12px;
  transition: border-color 0.15s;
  outline: none;
}

.field-input:focus,
.field-textarea:focus,
.field-select:focus { border-color: var(--accent); }

.field-textarea { resize: vertical; }

.field-note { font-size: 11px; color: var(--muted); margin-top: 5px; }

/* ── Sliders ─────────────────────────────────────────────────────────────── */
.slider-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.field-slider {
  flex: 1;
  accent-color: var(--accent);
}

.slider-val {
  font-size: 18px;
  font-weight: 600;
  color: var(--accent);
  min-width: 28px;
  text-align: center;
}

/* ── Event card ──────────────────────────────────────────────────────────── */
.event-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  margin: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.event-row { display: flex; justify-content: space-between; font-size: 12px; }
.event-key { color: var(--muted); }
.event-val { color: var(--text); }
.hidden-outcome { color: var(--amber); font-size: 12px; }

/* ── Build section ───────────────────────────────────────────────────────── */
.build-section {
  margin-top: 24px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
}

.file-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 9px 13px;
  margin-bottom: 14px;
  font-size: 12px;
}

.file-icon  { font-size: 14px; }
.file-name  { flex: 1; color: var(--text); }
.file-words { color: var(--muted); font-size: 11px; }

.graph-result {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 14px;
  padding: 14px 18px;
  background: var(--surface2);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

.graph-stat     { display: flex; flex-direction: column; align-items: center; }
.stat-num       { font-size: 28px; font-weight: 700; color: var(--accent); }
.stat-lbl       { font-size: 11px; color: var(--muted); }
.graph-divider  { width: 1px; height: 36px; background: var(--border); }

/* ── Config grid ─────────────────────────────────────────────────────────── */
.config-grid  { display: flex; flex-direction: column; gap: 4px; margin-bottom: 24px; }
.config-row   { display: flex; gap: 20px; }
.half         { flex: 1; }

.estimate-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.estimate-label  { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
.estimate-time   { font-size: 22px; font-weight: 700; color: var(--amber); }
.estimate-detail { font-size: 11px; color: var(--muted); }

/* ── Running screen ──────────────────────────────────────────────────────── */
.running-indicator {
  position: relative;
  width: 64px;
  height: 64px;
  margin-bottom: 28px;
}

.pulse-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid var(--amber);
  animation: pulse-out 1.8s ease-out infinite;
}

.pulse-core {
  position: absolute;
  inset: 14px;
  border-radius: 50%;
  background: var(--amber);
  opacity: 0.9;
}

@keyframes pulse-out {
  0%   { transform: scale(1); opacity: 0.7; }
  100% { transform: scale(2.2); opacity: 0; }
}

.running-step  { color: var(--muted); font-size: 13px; margin: 10px 0 20px; }
.running-hint  { color: var(--muted); font-size: 12px; margin-top: 20px; max-width: 380px; }

.running-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 12px;
}

.meta-chip {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 20px;
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--muted);
}

.chip-amber { border-color: var(--amber); color: var(--amber); }
.chip-blue  { border-color: var(--accent); color: var(--accent); }

/* ── Progress bar ────────────────────────────────────────────────────────── */
.progress-bar {
  height: 3px;
  background: var(--surface2);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 8px;
  width: 100%;
}

.progress-bar.wide { width: 320px; max-width: 100%; }

.progress-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 2px;
  transition: width 0.5s ease;
}

.progress-fill.indeterminate {
  width: 40% !important;
  animation: slide-right 1.6s ease-in-out infinite;
}

@keyframes slide-right {
  0%   { transform: translateX(-120%); }
  100% { transform: translateX(300%); }
}

/* ── Results ─────────────────────────────────────────────────────────────── */
.outcome-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
}

.outcome-header {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 16px;
}

.branch-count { color: var(--muted); }

.outcome-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.outcome-label { font-size: 12px; width: 80px; flex-shrink: 0; color: var(--muted); }
.outcome-pct   { font-size: 13px; font-weight: 600; width: 48px; text-align: right; }

.outcome-bar-bg {
  flex: 1;
  height: 8px;
  background: var(--surface2);
  border-radius: 4px;
  overflow: hidden;
}

.outcome-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.9s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.bar-red   { background: var(--red); }
.bar-amber { background: var(--amber); }
.bar-green { background: var(--green); }
.bar-blue  { background: var(--accent); }

.dominant-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: var(--radius-sm);
  margin-bottom: 16px;
  border: 1px solid currentColor;
}

.dominant-badge.bar-red   { color: var(--red);   background: rgba(224,82,82,0.07); }
.dominant-badge.bar-amber { color: var(--amber); background: rgba(245,166,35,0.07); }
.dominant-badge.bar-green { color: var(--green); background: rgba(62,207,142,0.07); }
.dominant-badge.bar-blue  { color: var(--accent); background: rgba(79,158,255,0.07); }

.badge-label   { font-size: 11px; opacity: 0.7; }
.badge-outcome { font-size: 18px; font-weight: 700; flex: 1; }
.badge-prob    { font-size: 12px; opacity: 0.8; }

.prediction-summary {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  font-size: 13px;
  color: var(--muted);
  line-height: 1.7;
  margin-bottom: 16px;
}

/* ── Backtest panel ──────────────────────────────────────────────────────── */
.backtest-panel {
  background: var(--surface);
  border: 1px solid var(--amber);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
}

.backtest-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--amber);
  margin-bottom: 14px;
}

.backtest-hint { font-size: 12px; color: var(--muted); margin-bottom: 14px; line-height: 1.6; }
.backtest-reveal { }

.brier-table  { display: flex; flex-direction: column; gap: 10px; }

.brier-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

.brier-row:last-child { border-bottom: none; padding-bottom: 0; }
.brier-key  { color: var(--muted); }
.brier-val  { font-weight: 500; }
.val-correct { color: var(--green); }
.val-wrong   { color: var(--red); }

/* ── Report ──────────────────────────────────────────────────────────────── */
.report-section  { margin-bottom: 16px; }
.report-body     { margin-top: 12px; }

.report-text {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 16px;
  font-family: inherit;
  font-size: 12px;
  line-height: 1.8;
  color: var(--muted);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 480px;
  overflow-y: auto;
}

/* ── Actions row ─────────────────────────────────────────────────────────── */
.actions-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 8px;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.btn-primary {
  width: 100%;
  padding: 13px 20px;
  background: var(--accent);
  border: none;
  border-radius: var(--radius-sm);
  color: #fff;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.1s;
}

.btn-primary:hover:not(:disabled) { opacity: 0.88; }
.btn-primary:active:not(:disabled) { transform: scale(0.99); }
.btn-primary:disabled { opacity: 0.35; cursor: not-allowed; }

.btn-secondary {
  padding: 10px 18px;
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: var(--radius-sm);
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  cursor: pointer;
  transition: border-color 0.15s;
}

.btn-secondary:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.btn-secondary:disabled { opacity: 0.35; cursor: not-allowed; }

.btn-ghost {
  padding: 10px 18px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--muted);
  font-family: inherit;
  font-size: 13px;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}

.btn-ghost:hover { color: var(--text); border-color: var(--border2); }

/* ── Status pill ─────────────────────────────────────────────────────────── */
.status-pill {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--muted);
}

.pill-green { border-color: var(--green); color: var(--green); }
.pill-red   { border-color: var(--red);   color: var(--red); }

/* ── Transition ──────────────────────────────────────────────────────────── */
.slide-up-enter-active { animation: slideUp 0.3s ease; }
@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

code {
  background: var(--surface2);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: inherit;
  font-size: 12px;
  color: var(--accent);
}

.report-progress-hint {
  font-size: 11px;
  color: var(--muted);
  margin-top: 6px;
  opacity: 0.7;
}
</style>