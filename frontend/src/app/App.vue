<template>
  <div id="app">

    <!-- ════════════════════════════════════════════════════
         HOME SCREEN
    ════════════════════════════════════════════════════ -->
    <div v-if="showHome" class="home">
      <div class="home-grid" aria-hidden="true">
        <div v-for="i in 80" :key="i" class="grid-cell" :style="gridCellStyle(i)"></div>
      </div>
      <div class="home-agent-rain" aria-hidden="true">
        <span
          v-for="index in 128"
          :key="`home-bot-${index}`"
          class="landing-bot"
          :style="homeBotStyle(index)"
        ></span>
      </div>
      <div class="home-nodes" aria-hidden="true">
        <div v-for="n in homeNodes" :key="n.id" class="home-node"
             :style="{ left: n.x+'%', top: n.y+'%', animationDelay: n.delay+'s', width: n.size+'px', height: n.size+'px' }">
        </div>
      </div>

      <header class="home-topbar">
        <div class="home-brand" @click="scrollHomeSection('home-get-started')">
          <img class="brand-mark-img home-brand-icon" src="/darsh-mark.svg" alt="DARSH logo" />
          <span class="home-brand-mark">DARSH</span>
        </div>
        <nav class="home-marketing-nav">
          <button class="home-marketing-link" @click="scrollHomeSection('home-get-started')">Get Started</button>
          <button class="home-marketing-link" @click="scrollHomeSection('home-introduction')">Introduction</button>
          <button class="home-marketing-link" @click="scrollHomeSection('home-moves')">Five Moves</button>
          <button class="home-marketing-link" @click="scrollHomeSection('home-about')">About Us</button>
        </nav>
        <div class="home-topbar-actions">
          <button class="home-topbar-demo" type="button" @click="previewDemoLiveRun">See Demo Live Run</button>
          <button class="home-topbar-secondary" @click="scrollHomeSection('home-moves')">See The Flow</button>
        </div>
      </header>

      <main class="home-scroll">
        <div class="home-stage">
          <section id="home-get-started" class="home-panel home-hero-panel home-reveal">
            <div class="home-panel-shell">
              <div class="home-eyebrow">Get Started</div>
              <div class="home-hero-strip">
                <span v-for="pill in homeHeroPills" :key="pill" class="hero-pill">{{ pill }}</span>
              </div>

              <div class="home-hero-visual" aria-hidden="true">
                <div class="hero-visual-ring ring-one"></div>
                <div class="hero-visual-ring ring-two"></div>
                <div class="hero-visual-ring ring-three"></div>
                <div class="hero-visual-core">
                  <img class="hero-visual-logo" src="/darsh-mark.svg" alt="DARSH neural mark" />
                  <div class="hero-visual-core-title">DARSH</div>
                  <div class="hero-visual-core-subtitle">Pre-Decision Behavioral Intelligence</div>
                </div>
                <span class="hero-visual-chip chip-a">Graph Memory</span>
                <span class="hero-visual-chip chip-b">Agent Society</span>
                <span class="hero-visual-chip chip-c">Belief Motion</span>
                <span class="hero-visual-chip chip-d">Explainable Results</span>
              </div>

              <h1 class="home-title">
                <span class="title-brand">DARSH</span>
              </h1>
              <p class="home-tagline">
                Turn complex events into a clear, visual forecast.<br>
                Run DARSH locally with zero API cost and explore how people, organizations, and communities may react before you decide.
              </p>
              <p class="home-supporting-copy">
                The original DARSH app is locally runnable, cost-aware, and built for explainable forecasting. It turns documents, market events, and historical scenarios into a reasoning workbench with graph memory, heterogeneous agents, visible belief motion, and grounded reporting.
              </p>
              <div class="home-hero-cta-row">
                <button class="home-cta" @click="enterApp">
                  <span>Start Exploring</span><span class="cta-arrow">→</span>
                </button>
                <button class="home-ghost-cta" @click="scrollHomeSection('home-introduction')">See How It Works</button>
              </div>
              <div class="home-stats">
                <div class="home-stat"><span class="hstat-num">Local</span><span class="hstat-lbl">runs on your machine</span></div>
                <div class="hstat-sep"></div>
                <div class="home-stat"><span class="hstat-num">Zero API</span><span class="hstat-lbl">cost at runtime</span></div>
                <div class="hstat-sep"></div>
                <div class="home-stat"><span class="hstat-num">Multi</span><span class="hstat-lbl">scenario branches</span></div>
                <div class="hstat-sep"></div>
                <div class="home-stat"><span class="hstat-num">Clear</span><span class="hstat-lbl">decision reports</span></div>
              </div>
              <div class="home-capabilities">
                <span>Upload a brief</span><span class="cap-dot">·</span>
                <span>Run it locally</span><span class="cap-dot">·</span>
                <span>Test historical scenarios</span><span class="cap-dot">·</span>
                <span>See the likely paths ahead</span>
              </div>
              <div class="home-tech">Built for local-first forecasting, scenario review, and decision support in one place.</div>
            </div>
          </section>

          <section id="home-introduction" class="home-panel home-section-panel home-reveal">
            <div class="home-panel-shell">
              <div class="home-section-head">
                <div class="home-section-kicker">Introduction</div>
                <h2 class="home-section-title">Where graph memory, agent society, and belief motion make the unknown legible.</h2>
                <p class="home-section-copy">
                  DARSH converts narrative complexity into structure while staying locally runnable and zero-API-cost when paired with local models. It extracts entities and relationships, builds a knowledge graph, simulates multiple actor types, tracks belief movement, and brings everything back into a decision-grade review layer.
                </p>
              </div>

              <div class="home-intro-pill-row">
                <span v-for="pill in homeIntroPills" :key="pill" class="hero-pill">{{ pill }}</span>
              </div>

              <div class="home-intro-grid">
                <article
                  v-for="(card, index) in homeIntroductionCards"
                  :key="card.title"
                  class="home-feature-card home-reveal"
                  :style="{ '--home-reveal-delay': `${80 + index * 55}ms` }"
                >
                  <strong>{{ card.title }}</strong>
                  <span>{{ card.copy }}</span>
                </article>
              </div>
            </div>
          </section>

          <section id="home-moves" class="home-panel home-section-panel home-reveal">
            <div class="home-panel-shell">
              <div class="home-section-head">
                <div class="home-section-kicker">Five Deliberate Moves</div>
                <h2 class="home-section-title">A guided path from raw event context to a final outcome review.</h2>
                <p class="home-section-copy">
                  The original app is designed as a deliberate workflow. Each step adds structure, visibility, and reasoning depth instead of jumping straight to an answer.
                </p>
              </div>

              <div class="home-walkthrough-grid">
                <article
                  v-for="(step, index) in homeDeliberateMoves"
                  :key="step.title"
                  class="home-walkthrough-card home-reveal"
                  :style="{ '--home-reveal-delay': `${100 + index * 65}ms` }"
                >
                  <span class="walkthrough-number">{{ String(index + 1).padStart(2, '0') }}</span>
                  <strong>{{ step.title }}</strong>
                  <p>{{ step.copy }}</p>
                </article>
              </div>
            </div>
          </section>

          <section id="home-about" class="home-panel home-section-panel home-reveal">
            <div class="home-panel-shell">
              <div class="home-section-head">
                <div class="home-section-kicker">About Us</div>
                <h2 class="home-section-title">Making collective reasoning visible enough to trust before decisions are made.</h2>
                <p class="home-section-copy">
                  DARSH is built around the idea that better prediction needs visible reasoning. We care about how a conclusion forms, which actors move it, where disagreement remains, and what evidence is actually supporting the outcome.
                </p>
              </div>

              <div class="home-about-grid">
                <article
                  v-for="(card, index) in homeAboutCards"
                  :key="card.title"
                  class="home-about-card home-reveal"
                  :style="{ '--home-reveal-delay': `${90 + index * 70}ms` }"
                >
                  <h3>{{ card.title }}</h3>
                  <p>{{ card.copy }}</p>
                </article>
              </div>
              <div class="home-about-foot home-reveal" style="--home-reveal-delay: 420ms">
                <div class="home-social-links">
                  <a class="home-social-pill" href="https://www.linkedin.com/in/indra-mandal007" target="_blank" rel="noreferrer">
                    <span class="social-icon" aria-hidden="true">
                      <svg viewBox="0 0 24 24" role="presentation">
                        <path d="M6.94 8.5A1.56 1.56 0 1 1 6.93 5.4a1.56 1.56 0 0 1 0 3.1ZM5.62 10h2.63v8.4H5.62V10Zm4.28 0h2.52v1.15h.04c.35-.66 1.22-1.35 2.51-1.35 2.69 0 3.18 1.77 3.18 4.08v4.52h-2.63v-4c0-.95-.02-2.18-1.33-2.18-1.33 0-1.53 1.04-1.53 2.11v4.07H9.9V10Z"/>
                      </svg>
                    </span>
                    LinkedIn
                  </a>
                  <a class="home-social-pill" href="https://github.com/indramandal85/DARSH-The-Multi-Agent-Reasoning-Based-Prediction-System." target="_blank" rel="noreferrer">
                    <span class="social-icon" aria-hidden="true">
                      <svg viewBox="0 0 24 24" role="presentation">
                        <path d="M12 .5a12 12 0 0 0-3.79 23.39c.6.1.82-.26.82-.58l-.01-2.03c-3.34.73-4.04-1.42-4.04-1.42-.55-1.38-1.33-1.75-1.33-1.75-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.22 1.84 1.22 1.08 1.82 2.82 1.3 3.5.99.11-.77.42-1.3.76-1.6-2.67-.3-5.48-1.32-5.48-5.9 0-1.3.47-2.36 1.23-3.19-.12-.3-.53-1.53.12-3.18 0 0 1-.32 3.3 1.22a11.6 11.6 0 0 1 6 0c2.3-1.54 3.3-1.22 3.3-1.22.65 1.65.24 2.88.12 3.18.76.83 1.23 1.9 1.23 3.19 0 4.6-2.81 5.59-5.49 5.89.43.37.81 1.1.81 2.22l-.01 3.29c0 .32.22.69.83.57A12 12 0 0 0 12 .5Z"/>
                      </svg>
                    </span>
                    GitHub
                  </a>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>

    <!-- ════════════════════════════════════════════════════
         MAIN APP
    ════════════════════════════════════════════════════ -->
    <div v-else class="main-app">
      <div class="app-bg" aria-hidden="true"></div>

      <!-- ── Topbar ── -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="logo-btn" @click="returnHome">
            <img class="topbar-logo-mark" src="/darsh-mark.svg" alt="DARSH logo" />
            <span class="logo">DARSH</span>
          </button>
        </div>
        <div class="topbar-center">
          <nav class="steps">
            <div v-for="(label, i) in stepLabels" :key="i" class="step"
                 :class="{ active: currentStep === i, done: currentStep > i, disabled: currentStep < i }"
                 @click="currentStep > i ? currentStep = i : null">
              <span class="step-num">{{ currentStep > i ? '✓' : i + 1 }}</span>
              <span class="step-label">{{ label }}</span>
            </div>
          </nav>
        </div>
        <div class="topbar-right">
          <span class="status-dot" :class="apiOk ? 'green' : 'red'"></span>
          <span class="status-label">{{ apiOk ? 'API connected' : 'API offline' }}</span>
        </div>
      </header>

      <!-- ── Phase 4 toolbar ── -->
      <div v-if="(graphResult || graphName) && currentStep <= 1" class="p4-toolbar">
        <button class="p4-btn" :class="{ active: showGraphViewer }" @click="toggleGraphViewer">
          🕸 Knowledge Graph
        </button>
        <button class="p4-btn" :class="{ active: showHistory }" @click="toggleHistory">
          📋 History
        </button>
        <button class="p4-btn" :class="{ active: showMerge }" @click="toggleMerge">
          🔗 Merge Graphs
        </button>
      </div>

      <!-- ── Graph viewer panel ── -->
      <transition name="panel-drop">
        <div v-if="currentStep <= 1 && showGraphViewer && graphViewerName" class="p4-panel">
          <div class="p4-panel-header">
            <span>Knowledge Graph — {{ graphViewerName }}</span>
            <button class="panel-close-btn" @click="showGraphViewer = false">✕</button>
          </div>
          <GraphViewer :graphName="graphViewerName" />
        </div>
      </transition>

      <!-- ── History panel ── -->
      <transition name="panel-drop">
        <div v-if="currentStep <= 1 && showHistory" class="p4-panel">
          <div class="p4-panel-header">
            <span>Simulation History</span>
            <button class="panel-close-btn" @click="showHistory = false">✕</button>
          </div>
          <div v-if="!selectedHistorySim" class="history-list">
            <div v-if="historyList.length === 0" class="hist-empty">No simulation history yet. Run a simulation first.</div>
            <div v-for="sim in historyList" :key="sim.simulation_id"
                 class="history-item" @click="selectHistorySim(sim)">
              <span class="hist-id">{{ sim.simulation_id }}</span>
              <span class="hist-meta">{{ sim.agent_count }} agents · {{ sim.round_count }} rounds</span>
              <span class="hist-action">{{ (sim.dominant_action || '').slice(0, 28) }}</span>
            </div>
          </div>
          <div v-else class="history-detail">
            <button class="btn-ghost small" @click="selectedHistorySim = null">← All simulations</button>
            <div class="hist-detail-title">{{ selectedHistorySim.simulation_id }}</div>
            <div class="round-scrubber">
              <span class="scrubber-label">Round</span>
              <input type="range" :min="1" :max="selectedHistorySim.round_count"
                     v-model.number="historyRound" @input="loadHistoryRound" class="field-slider"
                     :style="sliderProgressStyle(historyRound, 1, selectedHistorySim?.round_count || 1)" />
              <span class="slider-val">{{ historyRound }}</span>
            </div>
            <div v-if="historyRoundData" class="round-data">
              <div class="round-world-state">
                <div class="rd-label">
                  {{ historyRoundData.world_state?.round_label || `Round ${historyRound}` }}
                  <span v-if="historyRoundData.world_state?.time_window" class="rd-time">
                    · {{ historyRoundData.world_state.time_window }}
                  </span>
                </div>
                <p class="rd-text">{{ (historyRoundData.world_state?.text || '').slice(0, 220) }}...</p>
                <div class="rd-meta">
                  <span>Dominant: {{ historyRoundData.world_state?.dominant }}</span>
                  <span>Conf: {{ ((historyRoundData.world_state?.confidence || 0) * 100).toFixed(0) }}%</span>
                </div>
              </div>
              <div v-for="agent in historyRoundData.agents" :key="agent.name" class="agent-snapshot">
                <div class="snap-header">
                  <span class="snap-type" :class="'type-' + (agent.type || '').toLowerCase()">{{ agent.type }}</span>
                  <span class="snap-name">{{ agent.name }}</span>
                  <span v-if="agent.market_role" class="snap-role">{{ formatLabel(agent.market_role) }}</span>
                  <span class="snap-action">{{ (agent.action || '').slice(0, 24) }}</span>
                </div>
                <p class="snap-thought">{{ (agent.thought || '').slice(0, 130) }}...</p>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- ── Merge panel ── -->
      <transition name="panel-drop">
        <div v-if="currentStep <= 1 && showMerge" class="p4-panel">
          <div class="p4-panel-header">
            <span>Merge Knowledge Graphs</span>
            <button class="panel-close-btn" @click="showMerge = false">✕</button>
          </div>
          <p class="merge-hint">Select 2+ graphs to combine into one richer world model.</p>
          <div v-if="availableGraphs.length === 0" class="hist-empty">No graphs found. Build a knowledge graph first.</div>
          <div class="merge-graph-list">
            <label v-for="g in availableGraphs" :key="g.name" class="merge-check-item">
              <input type="checkbox" :value="g.name" v-model="mergeList" />
              <span class="merge-graph-name">{{ g.name }}</span>
              <span v-if="g.has_causal" class="merge-causal-badge">+ causal</span>
            </label>
          </div>
          <div style="padding: 0 16px 14px;">
            <button class="btn-secondary" @click="mergeSelectedGraphs"
                    :disabled="mergeList.length < 2 || merging">
              {{ merging ? 'Merging...' : `Merge ${mergeList.length} graph${mergeList.length !== 1 ? 's' : ''} →` }}
            </button>
            <div v-if="mergeResult" class="status-pill" :class="mergeResult.error ? 'pill-red' : 'pill-green'"
                 style="margin-top: 10px;">
              {{ mergeResult.error || mergeResult.message }}
            </div>
          </div>
        </div>
      </transition>

      <!-- ════════════════════════════════════════════════════
           SCREEN 0 — Document Input
      ════════════════════════════════════════════════════ -->
      <main v-if="currentStep === 0" class="screen">
        <h1 class="screen-title">Choose Input Source</h1>
        <p class="screen-sub">Upload a document, fetch live news, load a historical event, or start from a guided market event template.</p>

        <div class="mode-tabs">
          <button v-for="m in modes" :key="m.id" class="mode-tab"
                  :class="{ active: inputMode === m.id }" @click="switchMode(m.id)">
            <span class="tab-icon">{{ m.icon }}</span>{{ m.label }}
          </button>
        </div>

        <!-- Tab A: Manual Upload -->
        <div v-if="inputMode === 'upload'" class="mode-body">
          <p class="mode-desc">Upload a <code>.txt</code>, <code>.md</code>, or <code>.pdf</code> document. The system normalizes the source safely, builds a knowledge graph, and runs multi-agent simulation without mutating your original file.</p>
          <div class="dropzone" :class="{ 'dropzone-ready': uploadedFilename }"
               @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
            <div v-if="!uploadedFilename" class="dropzone-empty">
              <div class="drop-arrow">↑</div>
              <p>Click or drag a <strong>.txt / .md / .pdf</strong> file here</p>
              <span class="drop-hint">Markdown and PDF inputs are normalized to clean text before graph building</span>
            </div>
            <div v-else class="dropzone-done">
              <span class="check-big">✓</span>
              <p>{{ uploadedDisplayFilename || uploadedFilename }}</p>
              <span class="drop-hint">{{ uploadedWordCount }} words loaded · source: {{ uploadedSourceFormat || 'txt' }}</span>
            </div>
          </div>
          <input ref="fileInput" type="file" accept=".txt,.md,.pdf" style="display:none" @change="handleFileUpload" />
        </div>

        <!-- Tab B: Live News -->
        <div v-if="inputMode === 'live'" class="mode-body">
          <div class="info-banner info-blue">
            <strong>Forward prediction mode.</strong>
            Fetches today's real news from BBC, Reuters, Economic Times and Moneycontrol.
            Use this to predict what will happen next — not to test past accuracy.
          </div>
          <div class="field-group">
            <label class="field-label">Topics <span class="field-hint">(comma-separated keywords)</span></label>
            <input v-model="liveTopics" type="text" class="field-input"
                   placeholder="RBI, interest rate, India inflation, 2025" @keyup.enter="fetchLiveNews" />
            <p class="field-note">Be specific. "RBI interest rate India 2025" works better than just "rates".</p>
          </div>
          <button class="btn-secondary" @click="fetchLiveNews" :disabled="!liveTopics.trim() || fetchLoading">
            {{ fetchLoading ? 'Fetching RSS feeds...' : 'Fetch Live News' }}
          </button>
          <div v-if="fetchMessage" class="status-pill" :class="fetchError ? 'pill-red' : 'pill-green'">{{ fetchMessage }}</div>
        </div>

        <!-- Tab C: Historical Backtest -->
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
              <option v-for="ev in historicalEvents" :key="ev.event_id" :value="ev.event_id">
                {{ ev.date }} — {{ ev.description.slice(0, 65) }}...
              </option>
            </select>
          </div>
          <div v-if="selectedEventId && selectedEventMeta" class="event-card">
            <div class="event-row"><span class="event-key">Domain</span><span class="event-val">{{ selectedEventMeta.domain }}</span></div>
            <div class="event-row"><span class="event-key">Date</span><span class="event-val">{{ selectedEventMeta.date }}</span></div>
            <div class="event-row"><span class="event-key">Actual outcome</span><span class="event-val hidden-outcome">Hidden until after simulation ✦</span></div>
          </div>
          <button class="btn-secondary" @click="loadHistorical" :disabled="!selectedEventId || fetchLoading">
            {{ fetchLoading ? 'Loading document...' : 'Load Historical Document' }}
          </button>
          <div v-if="fetchMessage" class="status-pill" :class="fetchError ? 'pill-red' : 'pill-green'">{{ fetchMessage }}</div>
        </div>

        <!-- Tab D: Market Event Template -->
        <div v-if="inputMode === 'template'" class="mode-body">
          <div class="info-banner info-purple">
            <strong>Guided market-event mode.</strong>
            Pick a reusable India market template, fill in the headline numbers, and generate a ready-to-run pre-market scenario.
          </div>

          <div class="template-grid">
            <div class="field-group">
              <label class="field-label">Event template</label>
              <select v-model="selectedTemplateId" class="field-select" @change="loadTemplateDetail">
                <option value="" disabled>Choose a template...</option>
                <option v-for="template in eventTemplates" :key="template.template_id" :value="template.template_id">
                  {{ template.display_name }}
                </option>
              </select>
              <p class="field-note">Start with the event type you want to simulate before market participants react to it.</p>
            </div>

            <div v-if="selectedTemplate" class="template-card">
              <div class="template-card-top">
                <div>
                  <div class="template-eyebrow">{{ formatLabel(selectedTemplate.category) }}</div>
                  <div class="template-title">{{ selectedTemplate.display_name }}</div>
                </div>
                <div class="template-chip">{{ selectedTemplate.required_inputs?.length || 0 }} inputs</div>
              </div>
              <p class="template-desc">{{ selectedTemplate.description }}</p>
            </div>
          </div>

          <div v-if="selectedTemplate" class="template-form">
            <div v-for="field in selectedTemplate.required_inputs || []" :key="field.key" class="template-field">
              <div v-if="field.type === 'boolean'" class="template-toggle">
                <label class="toggle-row">
                  <span class="toggle-copy">
                    <span class="field-label">{{ field.label }}</span>
                    <span class="field-note">Use this when the event had an exceptional or clearly signalled policy angle.</span>
                  </span>
                  <input v-model="templateInputs[field.key]" type="checkbox" class="toggle-input" />
                </label>
              </div>
              <div v-else class="field-group">
                <label class="field-label">{{ field.label }}</label>
                <input
                  v-model="templateInputs[field.key]"
                  :type="field.type === 'number' ? 'number' : 'text'"
                  class="field-input"
                  :placeholder="field.placeholder || ''"
                  :step="field.type === 'number' ? 'any' : undefined"
                />
              </div>
            </div>
          </div>

          <div v-if="selectedTemplate" class="template-actions">
            <button class="btn-primary" @click="generateTemplateScenario" :disabled="templateLoading">
              {{ templateLoading ? 'Generating Scenario...' : 'Generate Scenario →' }}
            </button>
            <div v-if="templateMessage" class="status-pill" :class="templateError ? 'pill-red' : 'pill-green'">
              {{ templateMessage }}
            </div>
          </div>
        </div>

        <!-- Document ready -->
        <transition name="slide-up">
          <div v-if="uploadedFilename" class="build-section">
            <div class="file-badge">
              <span class="file-icon">📄</span>
              <span class="file-name">{{ uploadedDisplayFilename || uploadedFilename }}</span>
              <span class="file-words">{{ uploadedWordCount }} words · {{ (uploadedSourceFormat || 'txt').toUpperCase() }}</span>
            </div>
            <button class="btn-primary" @click="buildGraph" :disabled="isBuilding">
              {{ isBuilding ? 'Building knowledge graph...' : 'Build Knowledge Graph →' }}
            </button>
            <div v-if="graphMessage" class="status-pill" :class="graphError ? 'pill-red' : 'pill-green'">{{ graphMessage }}</div>
            <div v-if="isBuilding" class="progress-bar"><div class="progress-fill indeterminate"></div></div>
            <div v-if="graphResult" class="graph-result">
              <div class="graph-stat"><span class="stat-num">{{ graphResult.entity_count }}</span><span class="stat-lbl">entities</span></div>
              <div class="graph-divider"></div>
              <div class="graph-stat"><span class="stat-num">{{ graphResult.edge_count }}</span><span class="stat-lbl">relationships</span></div>
            </div>
          </div>
        </transition>
      </main>

      <!-- ════════════════════════════════════════════════════
           SCREEN 1 — Configure
      ════════════════════════════════════════════════════ -->
      <main v-if="currentStep === 1" class="screen">
        <h1 class="screen-title">Configure Simulation</h1>
        <p class="screen-sub">Define the scenario. The multi-agent society will reason about this situation across parallel branches.</p>

        <div class="config-grid">
          <div v-if="config.eventType !== 'general'" class="config-context-card">
            <span class="config-context-label">Scenario type</span>
            <span class="config-context-value">{{ formatLabel(config.eventType) }}</span>
            <span class="config-context-detail">{{ config.actions?.length || 0 }} default action prompts loaded for this event</span>
          </div>
          <div class="field-group">
            <label class="field-label">Prediction topic</label>
            <input v-model="config.topic" type="text" class="field-input" placeholder="RBI emergency rate hike impact on Indian economy" />
          </div>
          <div class="field-group">
            <label class="field-label">Initial situation</label>
            <textarea v-model="config.situation" class="field-textarea" rows="3" placeholder="Describe the current world state..."></textarea>
          </div>
          <div class="field-group">
            <label class="field-label">Events per round <span class="field-hint">(one per line, up to 3)</span></label>
            <textarea v-model="config.eventsRaw" class="field-textarea" rows="3"
                      placeholder="Round 1: Economists warn of recession risk&#10;Round 2: Banks announce EMI increases&#10;Round 3: Government responds"></textarea>
          </div>
          <div class="config-row">
            <div class="field-group half">
              <label class="field-label">Agents per branch</label>
              <div class="slider-wrap">
                <input type="range" v-model.number="config.numAgents" min="3" max="24" step="1" class="field-slider"
                       :style="sliderProgressStyle(config.numAgents, 3, 24)" />
                <span class="slider-val">{{ config.numAgents }}</span>
              </div>
            </div>
            <div class="field-group half">
              <label class="field-label">Parallel branches / worlds</label>
              <div class="slider-wrap">
                <input type="range" v-model.number="config.numBranches" min="1" max="8" step="1" class="field-slider"
                       :style="sliderProgressStyle(config.numBranches, 1, 8)" />
                <span class="slider-val">{{ config.numBranches }}</span>
              </div>
            </div>
          </div>
          <div class="field-group">
            <label class="field-label">Simulation rounds</label>
            <div class="slider-wrap">
              <input type="range" v-model.number="config.numRounds" min="2" max="8" step="1" class="field-slider"
                     :style="sliderProgressStyle(config.numRounds, 2, 8)" />
              <span class="slider-val">{{ config.numRounds }}</span>
            </div>
          </div>
        </div>

        <div class="estimate-card">
          <span class="estimate-label">Estimated runtime</span>
          <span class="estimate-time">~{{ estimatedMinutes }} minutes</span>
          <span class="estimate-detail">
            {{ config.numBranches }} branches × {{ config.numAgents }} agents × {{ config.numRounds }} rounds
            = {{ config.numBranches * config.numAgents * config.numRounds * 3 }} LLM calls
          </span>
        </div>

        <button class="btn-primary" @click="runSimulation">Run Simulation →</button>
      </main>

      <!-- ════════════════════════════════════════════════════
           SCREEN 2 — Running
      ════════════════════════════════════════════════════ -->
      <main v-if="currentStep === 2" class="ops-screen">
        <div class="ops-hero">
          <div>
            <div class="ops-eyebrow">DARSH Control Room</div>
            <h1 class="ops-title">Live Simulation Operations</h1>
            <p class="ops-copy">
              The workbench is tracking branch execution, agent-field motion, and report assembly in one view.
            </p>
          </div>
          <div class="ops-badges">
            <span class="meta-chip">{{ config.numBranches }} branches</span>
            <span class="meta-chip">{{ config.numAgents }} agents</span>
            <span class="meta-chip">{{ config.numRounds }} rounds</span>
            <span v-if="inputMode === 'historical'" class="meta-chip chip-amber">Backtest mode</span>
            <span v-if="inputMode === 'live'" class="meta-chip chip-blue">Live news mode</span>
          </div>
        </div>

        <div class="ops-stage-grid">
          <div v-for="card in runningOpsCards" :key="card.key" class="ops-stage-card" :class="{ done: card.done }">
            <span class="ops-stage-dot"></span>
            <span>{{ card.label }}</span>
          </div>
        </div>

        <div class="ops-workbench">
          <section class="ops-pane ops-pane-wide ops-surface-pane">
            <div class="ops-surface-toolbar">
              <div class="workspace-tabs">
                <button class="workspace-tab" :class="{ active: runningSurfaceTab === 'swarm' }" @click="runningSurfaceTab = 'swarm'">
                  Live Agent Field
                </button>
                <button class="workspace-tab" :class="{ active: runningSurfaceTab === 'graph' }" @click="runningSurfaceTab = 'graph'">
                  Knowledge Graph
                </button>
              </div>
              <div class="ops-surface-toolbar-meta">
                <span class="meta-chip chip-blue">{{ runningGraphAvailable ? 'Graph linked' : 'Graph optional' }}</span>
              </div>
            </div>

            <div class="ops-surface-layout single-surface">
              <div v-if="runningSurfaceTab === 'swarm'" class="ops-surface-main">
                <SwarmCanvas
                  :config="config"
                  :running-step="runningStep"
                  :live-focus="liveFocus"
                  :active="currentStep === 2 && runningSurfaceTab === 'swarm'"
                  mode="running"
                />
              </div>

              <transition name="panel-fade" mode="out-in">
                <div v-if="runningSurfaceTab === 'graph'" key="running-graph-surface" class="ops-graph-stage">
                  <div v-if="runningGraphAvailable" class="ops-graph-frame">
                    <GraphViewer
                      :graphName="graphViewerName || graphName"
                      :canvas-height="900"
                      :dense-mode="true"
                      :live-focus="liveFocus"
                    />
                  </div>
                  <div v-else class="workspace-empty-state running-empty-state">
                    Build or load a knowledge graph to open the running-time graph explorer.
                  </div>
                </div>
              </transition>
            </div>

          </section>

          <section class="ops-pane ops-pane-rail">
            <div class="ops-pane-header">
              <div>
                <div class="ops-pane-label">Realtime Status</div>
                <div class="ops-pane-title">Execution Feed</div>
              </div>
              <span class="ops-pulse">{{ activityPulse }}</span>
            </div>

            <div class="ops-highlight-card">
              <div class="ops-highlight-label">Current backend stage</div>
              <div class="ops-highlight-copy">{{ runningStep || 'Initialising agents...' }}</div>
            </div>

            <div v-if="runningStep && runningStep.includes('report')" class="ops-note-card">
              Report generation is active. Each report section is assembled after the branch simulation finishes.
            </div>

            <div class="progress-bar wide"><div class="progress-fill indeterminate"></div></div>

            <div class="ops-signal-card">
              <div class="ops-highlight-label">Live signal stack</div>
              <div class="ops-signal-chips">
                <span v-for="signal in runningSignalChips" :key="signal" class="ops-signal-chip">{{ signal }}</span>
              </div>
            </div>

            <div class="ops-surface-card ops-feed-card">
              <div class="ops-highlight-label">Live execution notes</div>
              <div class="ops-feed ops-feed-compact">
                <div v-for="item in liveActivityFeed" :key="item" class="ops-feed-item">
                  <span class="ops-feed-dot"></span>
                  <span>{{ item }}</span>
                </div>
              </div>
            </div>

            <div class="ops-trace-panel">
              <div class="ops-highlight-label">Cohort trace window</div>
              <div class="ops-trace-cards">
                <div v-for="card in runningCohortCards.slice(0, 3)" :key="card.role" class="ops-trace-card">
                  <div class="ops-trace-top">
                    <span class="ops-trace-role">{{ card.role }}</span>
                    <span class="ops-trace-tone">{{ card.tone }}</span>
                  </div>
                  <p>{{ card.summary }}</p>
                </div>
              </div>
            </div>

            <div class="ops-metric-grid">
              <div class="ops-mini-card">
                <span class="ops-mini-label">Runtime</span>
                <span class="ops-mini-value">~{{ estimatedMinutes }}–{{ estimatedMinutes + 5 }} min</span>
              </div>
              <div class="ops-mini-card">
                <span class="ops-mini-label">LLM load</span>
                <span class="ops-mini-value">{{ config.numBranches * config.numAgents * config.numRounds * 3 }} calls</span>
              </div>
            </div>

            <div class="ops-console-card">
              <div class="ops-console-head">
                <span>System Dashboard</span>
                <span>{{ runJobId || 'session_live' }}</span>
              </div>
              <div class="ops-console-body">
                <div v-for="line in runningConsoleFeed" :key="line" class="ops-console-line">{{ line }}</div>
              </div>
            </div>
          </section>
        </div>
      </main>

      <!-- ════════════════════════════════════════════════════
           SCREEN 3 — Results
      ════════════════════════════════════════════════════ -->
      <main v-if="currentStep === 3" class="studio-screen">
        <div class="studio-hero">
          <div>
            <div class="ops-eyebrow">Prediction Workbench</div>
            <h1 class="studio-title">{{ simResult.topic || config.topic || 'Market Event Workbench' }}</h1>
            <p class="studio-copy">{{ simResult.prediction }}</p>
          </div>
          <div class="studio-badges">
            <span class="market-badge regime">{{ simResult.num_branches }} branches</span>
            <span class="market-badge volatility">{{ formatLabel(simResult.event_type) }}</span>
            <span v-if="marketImpact" class="market-badge regime">{{ formatLabel(marketImpact.market_regime) }}</span>
          </div>
        </div>

        <div class="results-shell">
          <aside class="results-rail">
            <div class="results-rail-top">
              <div class="results-rail-kicker">Final Workbench</div>
              <div class="results-rail-title">Outcome Review</div>
              <p class="results-rail-copy">
                Move between the final results dashboard, the visual inspection workspace, and the interactive report console.
              </p>
            </div>

            <div class="results-rail-nav">
              <button
                class="results-rail-btn"
                :class="{ active: finalPageTab === 'results' }"
                @click="finalPageTab = 'results'"
              >
                <span class="results-rail-btn-title">Results</span>
                <span class="results-rail-btn-copy">Forecast, report, backtest scoring, and decision readouts</span>
              </button>
              <button
                class="results-rail-btn"
                :class="{ active: finalPageTab === 'visualization' }"
                @click="finalPageTab = 'visualization'"
              >
                <span class="results-rail-btn-title">Visualization</span>
                <span class="results-rail-btn-copy">Knowledge graph and live-agent swarm in one visual workspace</span>
              </button>
              <button
                class="results-rail-btn"
                :class="{ active: finalPageTab === 'interactive' }"
                @click="finalPageTab = 'interactive'"
              >
                <span class="results-rail-btn-title">Interactive Tools</span>
                <span class="results-rail-btn-copy">Ask sectors, cohorts, counterfactuals, and change-trigger questions</span>
              </button>
            </div>

            <div class="results-rail-meta">
              <span class="results-rail-chip">{{ simResult.num_branches }} branches</span>
              <span class="results-rail-chip">{{ formatLabel(simResult.event_type) }}</span>
              <span v-if="marketImpact" class="results-rail-chip">{{ formatLabel(marketImpact.market_regime) }}</span>
            </div>

            <button class="btn-ghost results-rail-reset" @click="resetAll">Start New Prediction</button>
          </aside>

          <section class="results-stage">
            <div v-if="finalPageTab === 'results'" class="results-dashboard">
              <div class="results-main-column">
                <div class="outcome-card studio-summary-card result-card-elevated">
                  <div class="outcome-header">
                    <span>Outcome probability distribution</span>
                    <span class="branch-count">{{ simResult.num_branches }} branches</span>
                  </div>
                  <button
                    v-for="(prob, outcome) in sortedOutcomes"
                    :key="outcome"
                    class="outcome-row outcome-row-button"
                    :class="{ active: resolvedFocusedOutcomeKey === outcome }"
                    @click="focusOutcome(outcome)"
                  >
                    <span class="outcome-label">{{ outcome }}</span>
                    <div class="outcome-bar-bg">
                      <div class="outcome-bar-fill" :class="outcomeColor(outcome)" :style="{ width: animateBars ? prob + '%' : '0%' }"></div>
                    </div>
                    <span class="outcome-pct">{{ prob.toFixed(1) }}%</span>
                  </button>
                </div>

                <div class="result-focus-card">
                  <div class="result-focus-top">
                    <div>
                      <div class="ops-pane-label">Focused Read</div>
                      <div class="ops-pane-title">{{ formatLabel(resolvedFocusedOutcomeKey) }} Outlook</div>
                    </div>
                    <span class="result-focus-chip">{{ focusedOutcomeProbability.toFixed(1) }}%</span>
                  </div>
                  <p class="result-focus-copy">{{ focusedOutcomeNarrative }}</p>
                  <div class="result-focus-grid">
                    <div class="result-focus-box">
                      <span class="result-focus-label">Market Regime</span>
                      <strong>{{ marketImpact ? formatLabel(marketImpact.market_regime) : 'n/a' }}</strong>
                    </div>
                    <div class="result-focus-box">
                      <span class="result-focus-label">Population Read</span>
                      <strong>{{ populationModel ? formatLabel(populationModel.dominant_population_outcome) : 'n/a' }}</strong>
                    </div>
                    <div class="result-focus-box">
                      <span class="result-focus-label">Volatility</span>
                      <strong>{{ marketImpact ? formatLabel(marketImpact.volatility_expectation) : 'n/a' }}</strong>
                    </div>
                  </div>
                  <ul class="result-focus-list">
                    <li v-for="item in focusedOutcomeSupport" :key="item">{{ item }}</li>
                  </ul>
                </div>

                <div class="report-studio-card">
                  <div class="report-studio-header">
                    <div>
                      <div class="ops-pane-label">Analysis Studio</div>
                      <div class="ops-pane-title">Report, Market, and Population Views</div>
                    </div>
                    <div class="report-actions studio-tabs">
                      <button class="workspace-tab" :class="{ active: studioCenterTab === 'report' }" @click="studioCenterTab = 'report'">Report</button>
                      <button class="workspace-tab" :class="{ active: studioCenterTab === 'market' }" @click="studioCenterTab = 'market'">Market</button>
                      <button class="workspace-tab" :class="{ active: studioCenterTab === 'population' }" @click="studioCenterTab = 'population'">Population</button>
                      <button class="btn-secondary small" @click="downloadReport">Download MD</button>
                      <button class="btn-secondary small" @click="downloadReportPdf">Download PDF</button>
                      <button class="btn-ghost small" @click="showReport = !showReport">{{ showReport ? 'Collapse' : 'Expand Full Text' }}</button>
                    </div>
                  </div>

                  <div v-if="studioCenterTab === 'report'" class="report-studio-grid">
                    <div class="report-overview-card report-overview-span">
                      <div class="report-overview-main">
                        <div class="report-overview-chart">
                          <div class="report-donut" :style="{ background: reportOutcomeChartStyle }">
                            <div class="report-donut-hole">
                              <span class="report-donut-label">Dominant</span>
                              <strong>{{ formatLabel(dominantOutcomeLabel) }}</strong>
                            </div>
                          </div>
                          <div class="report-donut-legend">
                            <button
                              v-for="(prob, outcome) in sortedOutcomes"
                              :key="`report-legend-${outcome}`"
                              class="report-donut-row report-donut-row-button"
                              :class="{ active: resolvedFocusedOutcomeKey === outcome }"
                              @click="focusOutcome(outcome)"
                            >
                              <span class="report-donut-dot" :class="outcomeColor(outcome)"></span>
                              <span>{{ formatLabel(outcome) }}</span>
                              <strong>{{ prob.toFixed(1) }}%</strong>
                            </button>
                          </div>
                        </div>

                        <div class="report-overview-metrics">
                          <div v-for="card in reportSummaryCards" :key="card.label" class="report-overview-metric">
                            <span class="report-overview-label">{{ card.label }}</span>
                            <strong class="report-overview-value">{{ card.value }}</strong>
                            <span class="report-overview-sub">{{ card.sub }}</span>
                          </div>
                        </div>
                      </div>

                      <div class="report-trend-strip">
                        <div class="report-trend-title">Interactive Report Charts</div>
                        <div class="report-mini-atlas">
                          <button
                            v-for="card in resultsInsightCards"
                            :key="`report-chart-${card.key}`"
                            class="report-mini-chart-card"
                            :class="{ active: activeResultsInsightCard?.key === card.key }"
                            @click="selectResultsInsight(card.key, card.target)"
                          >
                            <div class="report-mini-chart-head">
                              <span>{{ card.title }}</span>
                              <strong>{{ card.valueLabel }}</strong>
                            </div>
                            <div v-if="card.kind === 'progress'" class="report-mini-progress">
                              <div class="progress-circle report-mini-circle" :style="{ '--progress': `${card.value}` }">
                                <div class="progress-circle-inner report-mini-circle-inner">
                                  <strong>{{ card.valueLabel }}</strong>
                                </div>
                              </div>
                            </div>
                            <div v-else-if="card.kind === 'bars'" class="report-mini-bars">
                              <div v-for="bar in card.bars.slice(0, 3)" :key="bar.label" class="report-mini-bar-row">
                                <span>{{ bar.label }}</span>
                                <div class="report-mini-bar-track">
                                  <div class="report-mini-bar-fill" :class="bar.tone" :style="{ width: `${bar.value}%` }"></div>
                                </div>
                              </div>
                            </div>
                            <div v-else class="report-mini-sunburst">
                              <div class="sunburst-chart report-mini-sunburst-chart" :style="{ background: card.chartStyle }">
                                <div class="sunburst-chart-inner report-mini-circle-inner">
                                  <strong>{{ card.valueLabel }}</strong>
                                </div>
                              </div>
                            </div>
                          </button>
                        </div>

                        <div class="report-trend-title">Sector Trend Snapshot</div>
                        <div class="report-trend-grid">
                          <button
                            v-for="sector in reportTrendSectors"
                            :key="`trend-${sector.sector}`"
                            class="report-trend-card report-trend-card-button"
                            @click="studioCenterTab = 'market'"
                          >
                            <div class="report-trend-head">
                              <span>{{ formatLabel(sector.sector) }}</span>
                              <span :class="sectorDirectionClass(sector.direction)">{{ formatLabel(sector.direction) }}</span>
                            </div>
                            <div class="report-trend-bar">
                              <div class="report-trend-fill" :class="sectorDirectionClass(sector.direction)" :style="{ width: `${Math.max(10, (sector.confidence || 0) * 100)}%` }"></div>
                            </div>
                            <p>{{ sector.reasoning }}</p>
                          </button>
                        </div>
                      </div>
                    </div>

                    <aside class="report-nav">
                      <button
                        v-for="(section, index) in reportSections"
                        :key="section.title + index"
                        class="report-nav-item"
                        :class="{ active: activeReportSectionIndex === index }"
                        @click="activeReportSectionIndex = index"
                      >
                        <span class="report-nav-index">{{ String(index + 1).padStart(2, '0') }}</span>
                        <span class="report-nav-title">{{ section.title }}</span>
                      </button>
                    </aside>

                    <div class="report-viewer">
                      <div v-if="activeReportSection" class="report-section-card">
                        <div class="report-section-title">{{ activeReportSection.title }}</div>
                        <pre class="report-section-body">{{ activeReportSection.body }}</pre>
                      </div>

                      <div v-if="showReport" class="report-raw-card">
                        <div class="report-section-title">Full Report Output</div>
                        <pre class="report-text">{{ simResult.report }}</pre>
                      </div>
                    </div>
                  </div>

                  <div v-else-if="studioCenterTab === 'market' && marketImpact" class="studio-focus-panel">
                    <div class="market-intel-card">
                      <div class="market-intel-header">
                        <div>
                          <div class="market-intel-eyebrow">Market Intelligence</div>
                          <h2 class="market-intel-title">Pre-Market Impact View</h2>
                        </div>
                        <div class="market-intel-badges">
                          <span class="market-badge regime">{{ formatLabel(marketImpact.market_regime) }}</span>
                          <span class="market-badge volatility">{{ formatLabel(marketImpact.volatility_expectation) }} volatility</span>
                        </div>
                      </div>
                      <div class="market-confidence-row">
                        <div class="market-confidence-box">
                          <span class="market-confidence-label">Regime confidence</span>
                          <span class="market-confidence-value">{{ ((marketImpact.regime_confidence || 0) * 100).toFixed(0) }}%</span>
                        </div>
                        <div class="market-confidence-box">
                          <span class="market-confidence-label">Price discovery</span>
                          <span class="market-confidence-value">{{ marketImpact.expected_price_discovery_hours }}h</span>
                        </div>
                        <div class="market-confidence-box">
                          <span class="market-confidence-label">VIX direction</span>
                          <span class="market-confidence-value">{{ formatLabel(marketImpact.vix_direction) }}</span>
                        </div>
                      </div>
                      <div class="section-chart-atlas">
                        <button
                          v-for="card in marketInsightCards"
                          :key="card.key"
                          class="report-mini-chart-card section-chart-card"
                          :class="{ active: activeMarketInsightCard?.key === card.key }"
                          @click="activeMarketInsightKey = card.key"
                        >
                          <div class="report-mini-chart-head">
                            <span>{{ card.title }}</span>
                            <strong>{{ card.valueLabel }}</strong>
                          </div>
                          <div v-if="card.kind === 'progress'" class="report-mini-progress">
                            <div class="progress-circle report-mini-circle" :style="{ '--progress': `${card.value}` }">
                              <div class="progress-circle-inner report-mini-circle-inner">
                                <strong>{{ card.valueLabel }}</strong>
                              </div>
                            </div>
                          </div>
                          <div v-else-if="card.kind === 'bars'" class="report-mini-bars">
                            <div v-for="bar in card.bars" :key="bar.label" class="report-mini-bar-row">
                              <span>{{ bar.label }}</span>
                              <div class="report-mini-bar-track">
                                <div class="report-mini-bar-fill" :class="bar.tone" :style="{ width: `${bar.value}%` }"></div>
                              </div>
                            </div>
                          </div>
                          <div v-else class="report-mini-sunburst">
                            <div class="sunburst-chart report-mini-sunburst-chart" :style="{ background: card.chartStyle }">
                              <div class="sunburst-chart-inner report-mini-circle-inner">
                                <strong>{{ card.valueLabel }}</strong>
                              </div>
                            </div>
                          </div>
                        </button>
                      </div>
                      <div v-if="activeMarketInsightCard" class="section-chart-note">
                        <div class="trigger-heading">{{ activeMarketInsightCard.title }}</div>
                        <p>{{ activeMarketInsightCard.detail }}</p>
                      </div>
                      <div class="sector-impact-grid">
                        <div v-for="sector in displayedSectorImpacts" :key="sector.sector" class="sector-impact-card">
                          <div class="sector-impact-top">
                            <span class="sector-name">{{ formatLabel(sector.sector) }}</span>
                            <span class="sector-direction" :class="sectorDirectionClass(sector.direction)">{{ formatLabel(sector.direction) }}</span>
                          </div>
                          <div class="sector-confidence-bar">
                            <div class="sector-confidence-fill" :class="sectorDirectionClass(sector.direction)" :style="{ width: `${Math.max(10, (sector.confidence || 0) * 100)}%` }"></div>
                          </div>
                          <p class="sector-reasoning">{{ sector.reasoning }}</p>
                          <p class="sector-stocks">{{ (sector.representative_stocks || []).slice(0, 3).join(' · ') }}</p>
                        </div>
                      </div>
                      <div class="watchlist-grid">
                        <div class="watchlist-column">
                          <div class="watchlist-heading">Likely Laggards</div>
                          <div v-for="item in marketImpact.likely_laggards || []" :key="item.sector" class="watchlist-item">
                            <span>{{ item.sector }}</span>
                            <span>{{ ((item.confidence || 0) * 100).toFixed(0) }}%</span>
                          </div>
                        </div>
                        <div class="watchlist-column">
                          <div class="watchlist-heading">Likely Resilient</div>
                          <div v-for="item in marketImpact.likely_resilient || []" :key="item.sector" class="watchlist-item">
                            <span>{{ item.sector }}</span>
                            <span>{{ ((item.confidence || 0) * 100).toFixed(0) }}%</span>
                          </div>
                        </div>
                        <div class="watchlist-column">
                          <div class="watchlist-heading">Likely Beneficiaries</div>
                          <div v-for="item in marketImpact.likely_beneficiaries || []" :key="item.sector" class="watchlist-item">
                            <span>{{ item.sector }}</span>
                            <span>{{ ((item.confidence || 0) * 100).toFixed(0) }}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-else-if="studioCenterTab === 'population' && populationModel" class="studio-focus-panel">
                    <div class="population-card">
                      <div class="population-card-header">
                        <div>
                          <div class="market-intel-eyebrow">Population Model</div>
                          <h2 class="market-intel-title">Weighted Cohort Read</h2>
                        </div>
                        <div class="market-intel-badges">
                          <span class="market-badge regime">{{ formatLabel(populationModel.blended_market_regime) }}</span>
                          <span class="market-badge volatility">{{ formatLabel(populationModel.dominant_population_outcome) }}</span>
                        </div>
                      </div>
                      <div class="population-metric-grid">
                        <div class="population-metric-box">
                          <span class="market-confidence-label">Agents</span>
                          <span class="market-confidence-value">{{ populationModel.sampled_agent_count }}</span>
                        </div>
                        <div class="population-metric-box">
                          <span class="market-confidence-label">Cohorts</span>
                          <span class="market-confidence-value">{{ populationModel.sampled_cohort_count }}</span>
                        </div>
                        <div class="population-metric-box">
                          <span class="market-confidence-label">Base</span>
                          <span class="market-confidence-value">{{ formatPopulation(populationModel.represented_population) }}</span>
                        </div>
                        <div class="population-metric-box">
                          <span class="market-confidence-label">Coverage</span>
                          <span class="market-confidence-value">{{ ((populationModel.coverage_ratio || 0) * 100).toFixed(0) }}%</span>
                        </div>
                      </div>
                      <div class="section-chart-atlas">
                        <button
                          v-for="card in populationInsightCards"
                          :key="card.key"
                          class="report-mini-chart-card section-chart-card"
                          :class="{ active: activePopulationInsightCard?.key === card.key }"
                          @click="activePopulationInsightKey = card.key"
                        >
                          <div class="report-mini-chart-head">
                            <span>{{ card.title }}</span>
                            <strong>{{ card.valueLabel }}</strong>
                          </div>
                          <div v-if="card.kind === 'progress'" class="report-mini-progress">
                            <div class="progress-circle report-mini-circle" :style="{ '--progress': `${card.value}` }">
                              <div class="progress-circle-inner report-mini-circle-inner">
                                <strong>{{ card.valueLabel }}</strong>
                              </div>
                            </div>
                          </div>
                          <div v-else-if="card.kind === 'bars'" class="report-mini-bars">
                            <div v-for="bar in card.bars" :key="bar.label" class="report-mini-bar-row">
                              <span>{{ bar.label }}</span>
                              <div class="report-mini-bar-track">
                                <div class="report-mini-bar-fill" :class="bar.tone" :style="{ width: `${bar.value}%` }"></div>
                              </div>
                            </div>
                          </div>
                          <div v-else class="report-mini-sunburst">
                            <div class="sunburst-chart report-mini-sunburst-chart" :style="{ background: card.chartStyle }">
                              <div class="sunburst-chart-inner report-mini-circle-inner">
                                <strong>{{ card.valueLabel }}</strong>
                              </div>
                            </div>
                          </div>
                        </button>
                      </div>
                      <div v-if="activePopulationInsightCard" class="section-chart-note population-chart-note">
                        <div class="trigger-heading">{{ activePopulationInsightCard.title }}</div>
                        <p>{{ activePopulationInsightCard.detail }}</p>
                      </div>
                      <div class="population-lens-grid">
                        <div v-for="lens in populationLensCards" :key="lens.key" class="population-lens-card">
                          <div class="population-lens-title">{{ lens.label }}</div>
                          <div class="population-lens-outcome">{{ formatLabel(lens.data.dominant_outcome) }}</div>
                          <div class="population-lens-regime">{{ formatLabel(lens.data.market_regime) }}</div>
                          <div class="population-lens-prob">{{ ((lens.data.distribution?.[lens.data.dominant_outcome] || 0) * 100).toFixed(0) }}%</div>
                        </div>
                      </div>
                      <div class="population-cohort-list">
                        <div class="population-section-title">Top Weighted Cohorts</div>
                        <div v-for="cohort in displayedPopulationCohorts" :key="cohort.role_key" class="population-cohort-row">
                          <div class="population-cohort-main">
                            <span class="population-cohort-name">{{ cohort.label }}</span>
                            <span class="population-cohort-role">{{ cohort.sampled_agents }} sampled agents</span>
                          </div>
                          <div class="population-cohort-meta">
                            <span>{{ formatLabel(cohort.dominant_outcome) }}</span>
                            <span>{{ formatPopulation(cohort.represented_population) }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="marketImpact" class="trigger-rail-card trigger-inline-card">
                  <div class="backtest-title">Market Triggers</div>
                  <div class="trigger-rail-group">
                    <div class="trigger-heading">Strengthens</div>
                    <ul class="trigger-list">
                      <li v-for="item in displayedStrengthenTriggers" :key="item">{{ item }}</li>
                      <li v-if="displayedStrengthenTriggers.length === 0" class="trigger-fallback">
                        No strengthening triggers were generated for this run yet.
                      </li>
                    </ul>
                  </div>
                  <div class="trigger-rail-group">
                    <div class="trigger-heading">Weakens</div>
                    <ul class="trigger-list">
                      <li v-for="item in displayedWeakenTriggers" :key="item">{{ item }}</li>
                      <li v-if="displayedWeakenTriggers.length === 0" class="trigger-fallback">
                        No weakening triggers were generated for this run yet.
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <aside class="results-side-column">
                <div class="result-side-card">
                  <div class="backtest-title">Downloads & Snapshot</div>
                  <div class="result-side-actions">
                    <button class="btn-secondary" @click="downloadReport">Download MD</button>
                    <button class="btn-secondary" @click="downloadReportPdf">Download PDF</button>
                  </div>
                  <div class="result-side-stats">
                    <div class="result-side-stat">
                      <span class="result-side-label">Forecast</span>
                      <strong>{{ formatLabel(dominantOutcomeLabel) }}</strong>
                    </div>
                    <div class="result-side-stat">
                      <span class="result-side-label">Avg confidence</span>
                      <strong>{{ averageConfidenceLabel }}</strong>
                    </div>
                    <div class="result-side-stat">
                      <span class="result-side-label">Regime</span>
                      <strong>{{ marketImpact ? formatLabel(marketImpact.market_regime) : 'n/a' }}</strong>
                    </div>
                    <div class="result-side-stat">
                      <span class="result-side-label">Population read</span>
                      <strong>{{ populationModel ? formatLabel(populationModel.dominant_population_outcome) : 'n/a' }}</strong>
                    </div>
                  </div>
                </div>

                <div class="result-side-card">
                  <div class="backtest-title">Strengths & Weaknesses</div>
                  <div class="results-strength-grid">
                    <div class="results-strength-column">
                      <div class="trigger-heading">Strengthens</div>
                      <ul class="trigger-list compact-list">
                        <li v-for="item in displayedStrengthenTriggers" :key="`s-${item}`">{{ item }}</li>
                      </ul>
                    </div>
                    <div class="results-strength-column">
                      <div class="trigger-heading">Weakens</div>
                      <ul class="trigger-list compact-list">
                        <li v-for="item in displayedWeakenTriggers" :key="`w-${item}`">{{ item }}</li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div class="result-side-card">
                  <div class="backtest-title">Run Footprint</div>
                  <div class="result-side-stats result-side-stats-compact">
                    <div v-for="card in resultFootprintCards" :key="card.label" class="result-side-stat">
                      <span class="result-side-label">{{ card.label }}</span>
                      <strong>{{ card.value }}</strong>
                      <span class="result-side-note">{{ card.note }}</span>
                    </div>
                  </div>
                </div>

                <div class="result-side-card">
                  <div class="backtest-title">Priority Watchpoints</div>
                  <div class="result-watch-list">
                    <div v-for="item in resultWatchCards" :key="item.label" class="result-watch-card">
                      <span class="result-watch-label">{{ item.label }}</span>
                      <strong class="result-watch-value">{{ item.value }}</strong>
                      <p class="result-watch-note">{{ item.note }}</p>
                    </div>
                  </div>
                </div>

                <div v-if="inputMode === 'historical' && actualOutcome" class="backtest-panel compact">
                  <div class="backtest-title">Historical Backtest Scoring</div>
                  <div v-if="!brierResult" class="backtest-reveal">
                    <p class="backtest-hint">The simulation ran without seeing the actual outcome. Reveal it now to score the final forecast.</p>
                    <button class="btn-secondary" @click="scorePrediction">Reveal Actual Outcome & Score →</button>
                  </div>
                  <div v-else class="brier-table">
                    <div class="brier-row"><span class="brier-key">Predicted</span><span class="brier-val">{{ brierResult.dominant_predicted }}</span></div>
                    <div class="brier-row"><span class="brier-key">Actual outcome</span><span class="brier-val" :class="brierResult.correct ? 'val-correct' : 'val-wrong'">{{ brierResult.actual_outcome }}</span></div>
                    <div class="brier-row"><span class="brier-key">Brier score</span><span class="brier-val">{{ brierResult.brier_score }}</span></div>
                  </div>
                </div>
              </aside>
            </div>

            <div v-else-if="finalPageTab === 'visualization'" class="visualization-workspace">
              <section class="visualization-card visualization-card-primary">
                <div class="visualization-card-head">
                  <div>
                    <div class="ops-pane-label">Visualization</div>
                    <div class="ops-pane-title">Knowledge Graph Explorer</div>
                  </div>
                  <span class="market-badge">{{ graphViewerName || graphName || 'No graph loaded' }}</span>
                </div>
                <div v-if="graphViewerName || graphName" class="visualization-canvas-wrap">
                  <GraphViewer :graphName="graphViewerName || graphName" :dense-mode="true" :canvas-height="760" />
                </div>
                <div v-else class="workspace-empty-state">
                  Build or load a knowledge graph first to open the full graph explorer.
                </div>
                <div class="visualization-support-grid">
                  <div v-for="item in visualizationGraphStats" :key="item.label" class="visualization-support-card">
                    <span class="visualization-support-label">{{ item.label }}</span>
                    <strong class="visualization-support-value">{{ item.value }}</strong>
                    <span class="visualization-support-note">{{ item.note }}</span>
                  </div>
                </div>
              </section>

              <section class="visualization-card visualization-card-secondary">
                <div class="visualization-card-head">
                  <div>
                    <div class="ops-pane-label">Visualization</div>
                    <div class="ops-pane-title">Population-Weighted Cohort Field</div>
                  </div>
                  <span class="market-badge">{{ populationModel ? formatLabel(populationModel.dominant_population_outcome) : 'Simulation field' }}</span>
                </div>
                <div class="visualization-canvas-wrap visualization-canvas-wrap-swarm">
                  <SwarmCanvas
                    :population-model="populationModel"
                    :config="resultsSwarmVisualizationConfig"
                    :running-step="runningStep"
                    :active="currentStep === 3 && finalPageTab === 'visualization'"
                    mode="results"
                  />
                </div>
                <div class="visualization-support-grid">
                  <div v-for="item in visualizationSwarmStats" :key="item.label" class="visualization-support-card">
                    <span class="visualization-support-label">{{ item.label }}</span>
                    <strong class="visualization-support-value">{{ item.value }}</strong>
                    <span class="visualization-support-note">{{ item.note }}</span>
                  </div>
                </div>
              </section>
            </div>

            <div v-else class="interactive-workspace">
              <div class="interactive-side-column">
                <aside class="interactive-nav-card">
                  <div class="market-intel-eyebrow">Interactive Tools</div>
                  <h2 class="market-intel-title">Report Agent Chats</h2>
                  <p class="interactive-nav-copy">
                    Ask focused follow-ups grounded in the simulation, sector map, and cohort behavior.
                  </p>

                  <div class="tool-card-grid interactive-tool-grid">
                    <button
                      v-for="tool in workbenchToolCards"
                      :key="tool.key"
                      class="tool-card"
                      :class="{ active: chatMode === tool.key }"
                      @click="chatMode = tool.key"
                    >
                      <span class="tool-card-title">{{ tool.title }}</span>
                      <span class="tool-card-copy">{{ tool.desc }}</span>
                    </button>
                  </div>

                  <div class="interactive-nav-facts">
                    <span class="results-rail-chip">{{ simResult.simulation_ids?.length || 0 }} sim traces</span>
                    <span class="results-rail-chip">{{ chatSectorOptions.length }} sectors</span>
                    <span class="results-rail-chip">{{ chatCohortOptions.length }} cohorts</span>
                  </div>
                </aside>

                <section class="interactive-support-card">
                  <div class="market-intel-eyebrow">Context Snapshot</div>
                  <div class="ops-pane-title">Grounded conversation frame</div>
                  <div class="interactive-context-grid">
                    <div v-for="item in interactiveSnapshotCards" :key="item.label" class="interactive-context-item">
                      <span class="interactive-context-label">{{ item.label }}</span>
                      <strong class="interactive-context-value">{{ item.value }}</strong>
                      <span class="interactive-context-note">{{ item.note }}</span>
                    </div>
                  </div>
                </section>

                <section class="interactive-support-card">
                  <div class="market-intel-eyebrow">Suggested Angles</div>
                  <div class="ops-pane-title">Best next questions</div>
                  <div class="interactive-suggestion-list">
                    <div v-for="item in interactivePromptSuggestions" :key="item.title" class="interactive-suggestion-item">
                      <span class="interactive-suggestion-title">{{ item.title }}</span>
                      <p class="interactive-suggestion-copy">{{ item.copy }}</p>
                    </div>
                  </div>
                </section>
              </div>

              <div class="interactive-main-column">
                <section class="interactive-console-card">
                  <div class="chat-card premium-chat interactive-chat-shell">
                    <div class="chat-card-header">
                      <div>
                        <div class="market-intel-eyebrow">Chat Console</div>
                        <h2 class="market-intel-title">{{ activeToolCard.title }}</h2>
                        <p class="interactive-console-copy">{{ activeToolCard.desc }}</p>
                      </div>
                    </div>

                    <div v-if="chatMode === 'ask_sector'" class="chat-form-grid">
                      <div class="field-group">
                        <label class="field-label">Sector</label>
                        <select v-model="chatSector" class="field-select">
                          <option value="" disabled>Choose a sector...</option>
                          <option v-for="sector in chatSectorOptions" :key="sector.key" :value="sector.key">{{ sector.label }}</option>
                        </select>
                      </div>
                      <div class="field-group">
                        <label class="field-label">Question</label>
                        <textarea v-model="chatQuestion" class="field-textarea" rows="4" placeholder="Why is this sector likely to outperform or lag in the current scenario?"></textarea>
                      </div>
                    </div>

                    <div v-else-if="chatMode === 'ask_cohort'" class="chat-form-grid">
                      <div class="field-group">
                        <label class="field-label">Cohort</label>
                        <select v-model="chatCohort" class="field-select">
                          <option value="" disabled>Choose a cohort...</option>
                          <option v-for="cohort in chatCohortOptions" :key="cohort.key" :value="cohort.key">{{ cohort.label }}</option>
                        </select>
                      </div>
                      <div class="field-group">
                        <label class="field-label">Question</label>
                        <textarea v-model="chatQuestion" class="field-textarea" rows="4" placeholder="How is this cohort interpreting the event right now?"></textarea>
                      </div>
                    </div>

                    <div v-else-if="chatMode === 'counterfactual'" class="chat-form-grid">
                      <div class="field-group">
                        <label class="field-label">Counterfactual target</label>
                        <input v-model="chatCounterfactualTarget" type="text" class="field-input" placeholder="RBI, inflation, Brent crude, budget capex" />
                      </div>
                      <div class="field-group">
                        <label class="field-label">Question</label>
                        <textarea v-model="chatQuestion" class="field-textarea" rows="4" placeholder="What if this driver had not happened or had been much weaker?"></textarea>
                      </div>
                    </div>

                    <div v-else class="field-group">
                      <label class="field-label">Question</label>
                      <textarea v-model="chatQuestion" class="field-textarea" rows="4" placeholder="What would change this forecast before the market open?"></textarea>
                    </div>

                    <div class="interactive-actions-row">
                      <button class="btn-secondary" @click="runSimulationChat" :disabled="chatActionDisabled">
                        {{ chatLoading ? 'Analyzing...' : chatActionLabel }}
                      </button>
                      <span class="interactive-helper-text">Answers are grounded in the current simulation output and mapped evidence.</span>
                    </div>

                    <div v-if="chatMessage" class="status-pill" :class="chatError ? 'pill-red' : 'pill-green'">{{ chatMessage }}</div>

                    <div v-if="chatResponse" class="chat-response-card premium-response interactive-response-card">
                      <div class="interactive-response-head thread-head">
                        <div>
                          <div class="chat-response-title">{{ chatResponse.title }}</div>
                          <div class="interactive-response-subtitle">Simulation-grounded response</div>
                        </div>
                        <div class="thread-head-chips">
                          <span class="results-rail-chip">{{ activeToolCard.title }}</span>
                          <span class="results-rail-chip">{{ activeChatContext }}</span>
                        </div>
                      </div>

                      <div class="interactive-chat-thread">
                        <div class="thread-row thread-row-user">
                          <div class="thread-avatar">You</div>
                          <div class="thread-bubble thread-bubble-user">
                            <div class="thread-meta-row">
                              <div class="thread-meta">Question</div>
                              <div class="thread-time">{{ chatQuestionTimestamp || 'Just now' }}</div>
                            </div>
                            <p class="thread-text">{{ activeChatPrompt }}</p>
                          </div>
                        </div>

                        <div class="thread-row thread-row-ai">
                          <div class="thread-avatar thread-avatar-ai">NS</div>
                          <div class="thread-bubble thread-bubble-ai">
                            <div class="thread-meta-row">
                              <div class="thread-meta">Answer</div>
                              <div class="thread-time">{{ chatAnswerTimestamp || 'Now' }}</div>
                            </div>
                            <div class="thread-answer-stack">
                              <p v-for="(line, index) in chatResponseParagraphs" :key="`chat-line-${index}`" class="chat-response-answer">
                                {{ line }}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div v-if="(chatResponse.supporting_points || []).length" class="interactive-reference-card pinned-evidence-card">
                        <div class="interactive-reference-head">
                          <div>
                            <div class="trigger-heading">Pinned Evidence</div>
                            <div class="interactive-reference-subtitle">Grounded references and cohort thinking pulled from this simulation run.</div>
                          </div>
                          <span class="interactive-reference-chip">{{ (chatResponse.supporting_points || []).length }} refs</span>
                        </div>
                        <div class="interactive-reference-grid">
                          <div v-for="item in chatResponse.supporting_points" :key="item" class="interactive-reference-item">
                            <span class="interactive-reference-pin">Pinned</span>
                            <span class="interactive-reference-copy">{{ item }}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div v-else class="interactive-empty-state">
                      <div class="interactive-empty-title">Ask a focused question</div>
                      <p>
                        The console will return a concise answer plus simulation-grounded supporting points so you can see which evidence or cohort logic drove the answer.
                      </p>
                    </div>
                  </div>
                </section>

                <section class="interactive-support-card interactive-support-card-wide">
                  <div class="market-intel-eyebrow">Grounding Snapshot</div>
                  <div class="ops-pane-title">What the console can cite right now</div>
                  <div class="interactive-context-grid">
                    <div v-for="item in interactiveGroundingCards" :key="item.label" class="interactive-context-item">
                      <span class="interactive-context-label">{{ item.label }}</span>
                      <strong class="interactive-context-value">{{ item.value }}</strong>
                      <span class="interactive-context-note">{{ item.note }}</span>
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </section>
        </div>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import axios from 'axios'
import GraphViewer from '../GraphViewer.vue'
import SwarmCanvas from '../SwarmCanvas.vue'

const API = 'http://localhost:5001'

// ── App state ─────────────────────────────────────────────────────────────────
const showHome    = ref(true)
const currentStep = ref(0)
const stepLabels  = ['Input', 'Configure', 'Running', 'Results']
const apiOk       = ref(false)

// ── Home screen data ──────────────────────────────────────────────────────────
const homeHeroPills = [
  'Runs locally on your machine',
  'Zero API cost',
  'Graph-native memory',
  'Explainable result review',
]

const homeIntroPills = [
  'Runs locally',
  'Zero API cost',
  'Causal-aware',
  'Calibration-minded',
]

const homeIntroductionCards = [
  {
    title: 'Graph-grounded memory',
    copy: 'Entity and relationship structure keeps the system anchored to visible context instead of prompt fog.',
  },
  {
    title: 'Heterogeneous agent society',
    copy: 'Different mandates, speeds, memory, and network roles create divergence instead of collapsing everyone into one voice.',
  },
  {
    title: 'Belief tracking',
    copy: 'Outcomes evolve through weighted belief distributions so confidence and disagreement stay inspectable.',
  },
  {
    title: 'Local-first execution',
    copy: 'Run the full workbench on your machine so sensitive scenarios stay close and iteration stays fast.',
  },
  {
    title: 'Zero API cost workflow',
    copy: 'When paired with local models, repeated experimentation stays practical without paid API usage stacking up.',
  },
  {
    title: 'Visible reasoning surfaces',
    copy: 'Knowledge graphs, swarm maps, and report cards make the reasoning process easier to follow and challenge.',
  },
]

const homeDeliberateMoves = [
  {
    title: 'Ingest the scenario',
    copy: 'Start from a document, live news, a historical event, or a guided market template.',
  },
  {
    title: 'Build graph memory',
    copy: 'Extract entities, relationships, and context cues into an inspectable knowledge graph.',
  },
  {
    title: 'Configure the simulation',
    copy: 'Set the agent count, rounds, branches, and event framing before running the world forward.',
  },
  {
    title: 'Watch the swarm react',
    copy: 'Track live cohort behavior, attention spread, and belief movement during the run.',
  },
  {
    title: 'Review the outcome',
    copy: 'Land on results, visual inspection, and interactive follow-up tools in one final workbench.',
  },
]

const homeAboutCards = [
  {
    title: 'Our vision',
    copy: 'To make reaction intelligence inspectable enough for real decision-making, not just impressive demos.',
  },
  {
    title: 'Why DARSH exists',
    copy: 'Most systems stop at answers. We care about the full path: context, memory, agents, disagreement, and explainable outcomes.',
  },
  {
    title: 'What makes it different',
    copy: 'It blends graph memory, agent asymmetry, probabilistic beliefs, local-first execution, and low-cost experimentation into one coherent workflow.',
  },
  {
    title: 'How we build',
    copy: 'Locally runnable by design, grounded in visible structure, careful about uncertainty, and built to avoid unnecessary API cost.',
  },
]

const homeNodes = Array.from({ length: 12 }, (_, i) => ({
  id: i,
  x: 5 + Math.random() * 90,
  y: 5 + Math.random() * 90,
  size: 6 + Math.random() * 12,
  delay: Math.random() * 4
}))

function gridCellStyle() {
  return {
    animationDelay   : (Math.random() * 8) + 's',
    animationDuration: (Math.random() * 8 + 6) + 's',
  }
}

function homeBotStyle(index) {
  const hues = [25, 42, 88, 142, 212, 254]
  const hue = hues[index % hues.length]
  const left = (index * 8.7) % 94
  const top = (index * 11.3) % 108
  const size = 24 + (index % 5) * 5.5
  const opacity = 0.16 + (index % 5) * 0.035
  const duration = 18 + (index % 8) * 1.9
  return {
    '--bot-hue': `${hue}`,
    '--bot-size': `${size}px`,
    '--bot-opacity': `${opacity}`,
    left: `${left}%`,
    top: `${top}%`,
    animationDelay: `${(index % 10) * -1.6}s`,
    animationDuration: `${duration}s`,
  }
}

function scrollHomeSection(id) {
  if (typeof document === 'undefined') return
  const target = document.getElementById(id)
  if (!target) return
  target.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function previewDemoLiveRun() {}

function enterApp() {
  showHome.value = false
  if (typeof window !== 'undefined') {
    window.scrollTo(0, 0)
  }
  checkApi()
  loadHistoricalList()
  loadEventTemplates()
  loadTrackRecordSummary()
}

function returnHome() {
  showHome.value = true
  if (typeof window !== 'undefined') {
    window.scrollTo(0, 0)
  }
}

let homeRevealObserver = null

function setupHomeRevealObserver() {
  if (typeof window === 'undefined' || homeRevealObserver || !showHome.value) return

  homeRevealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
        homeRevealObserver?.unobserve(entry.target)
      }
    })
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -10% 0px',
  })

  document.querySelectorAll('.home-reveal').forEach((node) => {
    homeRevealObserver?.observe(node)
  })
}

function resetHomeRevealObserver() {
  homeRevealObserver?.disconnect()
  homeRevealObserver = null
}

// ── Input mode ────────────────────────────────────────────────────────────────
const modes = [
  { id: 'upload',     label: 'Manual Upload',      icon: '📄' },
  { id: 'live',       label: 'Live News',           icon: '📡' },
  { id: 'historical', label: 'Historical Backtest', icon: '🔍' },
  { id: 'template',   label: 'Market Event Template', icon: '📊' }
]
const inputMode = ref('upload')

// ── Upload state ──────────────────────────────────────────────────────────────
const uploadedFilename  = ref('')
const uploadedDisplayFilename = ref('')
const uploadedSourceFormat = ref('')
const uploadedWordCount = ref(0)

// ── Live news state ───────────────────────────────────────────────────────────
const liveTopics   = ref('')
const fetchLoading = ref(false)
const fetchMessage = ref('')
const fetchError   = ref(false)

// ── Historical state ──────────────────────────────────────────────────────────
const historicalEvents  = ref([])
const selectedEventId   = ref('')
const actualOutcome     = ref('')
const brierResult       = ref(null)
const selectedEventMeta = computed(() =>
  historicalEvents.value.find(e => e.event_id === selectedEventId.value) || null
)

// ── Template state ────────────────────────────────────────────────────────────
const eventTemplates    = ref([])
const selectedTemplateId = ref('')
const selectedTemplate  = ref(null)
const templateInputs    = ref({})
const templateLoading   = ref(false)
const templateMessage   = ref('')
const templateError     = ref(false)

// ── Graph build ───────────────────────────────────────────────────────────────
const isBuilding   = ref(false)
const graphMessage = ref('')
const graphError   = ref(false)
const graphResult  = ref(null)
const graphJobId   = ref(null)
const graphName    = ref('')

// ── Simulation config ─────────────────────────────────────────────────────────
const defaultSimulationActions = [
  'wait and observe before acting',
  'immediately revise plans',
  'research historical data before deciding',
  'spread information to network',
  'consult an expert or advisor',
  'take immediate protective action'
]

const marketCohortKeys = [
  'RETAIL_TRADER',
  'DOMESTIC_MUTUAL_FUND',
  'FII_ANALYST',
  'HEDGE_FUND_PM',
  'PRIVATE_BANK_TREASURY',
  'PSU_BANK_DESK',
  'BROKER_RESEARCH_DESK',
  'FINANCIAL_MEDIA_EDITOR',
  'REGULATOR_POLICY_DESK',
  'MINISTRY_POLICY_TEAM',
  'CORPORATE_TREASURY',
  'SECTOR_OPERATING_FIRM'
]

function createDefaultConfig() {
  return {
    topic: '',
    situation: '',
    eventsRaw: '',
    eventType: 'general',
    actions: [],
    numAgents: 5,
    numBranches: 3,
    numRounds: 3
  }
}

function createEmptyLiveFocus() {
  return {
    kind: '',
    branch_id: '',
    round_number: 0,
    round_label: '',
    market_role: '',
    agent_name: '',
    focus_terms: [],
    pulse: 0,
  }
}

function sliderProgressStyle(value, min, max) {
  const numericValue = Number(value)
  const start = Number(min)
  const end = Number(max)
  const range = Math.max(end - start, 1)
  const clamped = Math.min(Math.max(numericValue, start), end)
  const progress = ((clamped - start) / range) * 100
  return {
    '--slider-progress': `${progress}%`,
  }
}

const config = ref(createDefaultConfig())

// ── Running state ─────────────────────────────────────────────────────────────
const runJobId    = ref(null)
const runningStep = ref('')
const runningSurfaceTab = ref('swarm')
const liveFocus   = ref(createEmptyLiveFocus())
let   runPoller   = null

// ── Results state ─────────────────────────────────────────────────────────────
const simResult   = ref({})
const showReport  = ref(false)
const animateBars = ref(false)
const trackRecordSummary = ref({
  total_predictions: 0,
  accuracy: 0,
  average_brier_score: null,
  sector_direction_accuracy: null,
  track_record_markdown: ''
})
const chatMode    = ref('ask_sector')
const chatQuestion = ref('')
const chatSector   = ref('')
const chatCohort   = ref('')
const chatCounterfactualTarget = ref('')
const chatLoading  = ref(false)
const chatMessage  = ref('')
const chatError    = ref(false)
const chatResponse = ref(null)
const chatQuestionTimestamp = ref('')
const chatAnswerTimestamp = ref('')
const finalPageTab = ref('results')
const focusedOutcomeKey = ref('')
const resultsInsightKey = ref('market_confidence')
const workbenchTab = ref('swarm')
const workspaceDrawerOpen = ref(false)
const studioCenterTab = ref('report')
const activeReportSectionIndex = ref(0)
const activityPulse = ref(0)
const activeMarketInsightKey = ref('market_confidence')
const activePopulationInsightKey = ref('population_coverage')

// ── Phase 4: Graph viewer ─────────────────────────────────────────────────────
const showGraphViewer = ref(false)
const graphViewerName = ref('')

// ── Phase 4: History ──────────────────────────────────────────────────────────
const showHistory        = ref(false)
const historyList        = ref([])
const selectedHistorySim = ref(null)
const historyRound       = ref(1)
const historyRoundData   = ref(null)

// ── Phase 4: Merge ────────────────────────────────────────────────────────────
const showMerge       = ref(false)
const availableGraphs = ref([])
const mergeList       = ref([])
const mergeResult     = ref(null)
const merging         = ref(false)

// ── Computed ──────────────────────────────────────────────────────────────────
const estimatedMinutes = computed(() => {
  const calls = config.value.numBranches * config.value.numAgents * config.value.numRounds * 3
  return Math.max(4, Math.round(calls * 0.08))
})

const sortedOutcomes = computed(() => {
  const probs = simResult.value.outcome_probs || {}
  return Object.fromEntries(Object.entries(probs).sort((a, b) => b[1] - a[1]))
})

const marketImpact = computed(() => simResult.value.market_impact || null)
const populationModel = computed(() => simResult.value.population_model || null)
const runningGraphAvailable = computed(() => Boolean(graphViewerName.value || graphName.value))

const displayedSectorImpacts = computed(() => {
  const impacts = marketImpact.value?.sector_impacts || {}
  return Object.values(impacts)
    .sort((a, b) => (b.confidence || 0) - (a.confidence || 0))
    .slice(0, 8)
})

const displayedPopulationCohorts = computed(() => {
  const cohorts = populationModel.value?.cohort_breakdown || []
  return cohorts.slice(0, 6)
})

const displayedStrengthenTriggers = computed(() => {
  if (!marketImpact.value) return []
  const direct = Array.isArray(marketImpact.value.triggers_that_strengthen)
    ? marketImpact.value.triggers_that_strengthen.filter(Boolean)
    : []
  if (direct.length) return direct
  const signals = Array.isArray(marketImpact.value.monitoring_signals)
    ? marketImpact.value.monitoring_signals.filter(Boolean)
    : []
  const narratives = [
    marketImpact.value.institutional_narrative,
    marketImpact.value.media_narrative,
  ].filter(Boolean)
  return [...signals, ...narratives].slice(0, 3)
})

const displayedWeakenTriggers = computed(() => {
  if (!marketImpact.value) return []
  const direct = Array.isArray(marketImpact.value.triggers_that_weaken)
    ? marketImpact.value.triggers_that_weaken.filter(Boolean)
    : []
  if (direct.length) return direct
  const narratives = [
    marketImpact.value.retail_narrative,
    marketImpact.value.media_narrative,
  ].filter(Boolean)
  const signals = Array.isArray(marketImpact.value.monitoring_signals)
    ? marketImpact.value.monitoring_signals.filter(Boolean)
    : []
  return [...narratives, ...signals].slice(0, 3)
})

const populationLensCards = computed(() => {
  const lensViews = populationModel.value?.lens_views || {}
  return [
    { key: 'participation', label: 'Participation Lens', data: lensViews.participation || {} },
    { key: 'capital', label: 'Capital Lens', data: lensViews.capital || {} },
    { key: 'velocity', label: 'Narrative Velocity', data: lensViews.velocity || {} }
  ]
})

const reportSections = computed(() => {
  const raw = (simResult.value.report || '').trim()
  if (!raw) return []

  const parts = raw.split(/\n(?=##\s+)/g).filter(Boolean)
  if (parts.length <= 1 && !raw.startsWith('## ')) {
    return [{ title: 'Prediction Report', body: raw }]
  }

  return parts.map((part, index) => {
    const lines = part.trim().split('\n')
    const first = lines[0] || `Section ${index + 1}`
    const title = first.replace(/^##\s+/, '').trim()
    return {
      title: title || `Section ${index + 1}`,
      body: lines.slice(1).join('\n').trim()
    }
  })
})

const activeReportSection = computed(() => {
  if (!reportSections.value.length) return null
  return reportSections.value[Math.min(activeReportSectionIndex.value, reportSections.value.length - 1)]
})

const dominantOutcomeLabel = computed(() => {
  const entries = Object.entries(simResult.value.outcome_probs || {})
  if (!entries.length) return 'n/a'
  return entries.sort((a, b) => b[1] - a[1])[0][0]
})

const resolvedFocusedOutcomeKey = computed(() => {
  const available = Object.keys(simResult.value.outcome_probs || {})
  if (focusedOutcomeKey.value && available.includes(focusedOutcomeKey.value)) {
    return focusedOutcomeKey.value
  }
  return available[0] || dominantOutcomeLabel.value || 'cautious'
})

const focusedOutcomeProbability = computed(() => {
  const probs = simResult.value.outcome_probs || {}
  return Number(probs[resolvedFocusedOutcomeKey.value] || 0)
})

const averageConfidenceLabel = computed(() => {
  const predictionText = simResult.value.prediction || ''
  const match = predictionText.match(/Average agent confidence:\s*([0-9.]+)%/i)
  if (match) return `${Number(match[1]).toFixed(0)}%`

  const marketConfidence = marketImpact.value?.regime_confidence
  if (marketConfidence != null && Number.isFinite(Number(marketConfidence))) {
    return `${Math.round(Number(marketConfidence) * 100)}%`
  }

  const dominant = focusedOutcomeProbability.value
  if (Number.isFinite(dominant) && dominant > 0) return `${Math.round(dominant)}%`
  return 'n/a'
})

const focusedOutcomeNarrative = computed(() => {
  const outcome = resolvedFocusedOutcomeKey.value
  const regime = marketImpact.value?.market_regime ? formatLabel(marketImpact.value.market_regime) : 'the current regime'
  const populationRead = populationModel.value?.dominant_population_outcome
    ? formatLabel(populationModel.value.dominant_population_outcome)
    : 'the sampled population'
  const topSector = displayedSectorImpacts.value[0]
  const sectorRead = topSector
    ? `${formatLabel(topSector.sector)} is the clearest transmission channel right now`
    : 'sector dispersion is still forming'

  if (outcome === 'optimistic') {
    return `The market is leaning constructive, with ${regime} conditions and ${populationRead} reinforcing a more positive read. ${sectorRead}.`
  }
  if (outcome === 'panic') {
    return `The market is pricing a sharp downside reaction, with ${regime} conditions deteriorating and ${populationRead} pointing to defensive positioning. ${sectorRead}.`
  }
  if (outcome === 'divided') {
    return `The simulation shows a split market where conviction is fragmented. ${populationRead} is not yet aligned, and ${sectorRead}.`
  }
  if (outcome === 'confident') {
    return `Participants are converging quickly on a firmer directional read. ${populationRead} is aligned with ${regime}, and ${sectorRead}.`
  }
  return `The dominant read is still cautious: participants see a plausible path forward, but they want more confirmation before committing aggressively. ${populationRead} remains the anchor, and ${sectorRead}.`
})

const focusedOutcomeSupport = computed(() => {
  const supports = []
  const regime = marketImpact.value?.market_regime
  const volatility = marketImpact.value?.volatility_expectation
  const leadingSector = displayedSectorImpacts.value[0]
  const leadingCohort = displayedPopulationCohorts.value[0]

  if (regime) supports.push(`Market regime currently maps to ${formatLabel(regime)}.`)
  if (volatility) supports.push(`Expected volatility remains ${formatLabel(volatility)} into the next price-discovery window.`)
  if (leadingSector) {
    supports.push(`${formatLabel(leadingSector.sector)} shows the strongest visible sector signal at ${Math.round((leadingSector.confidence || 0) * 100)}% confidence.`)
  }
  if (leadingCohort) {
    supports.push(`${leadingCohort.label} is the heaviest weighted cohort and currently reads the event as ${formatLabel(leadingCohort.dominant_outcome)}.`)
  }

  const triggerPool = [
    ...displayedStrengthenTriggers.value,
    ...displayedWeakenTriggers.value,
  ].filter(Boolean)

  if (triggerPool.length) {
    supports.push(`Key trigger to watch: ${triggerPool[0]}.`)
  }

  return supports.slice(0, 4)
})

const reportOutcomeChartStyle = computed(() => {
  const probs = simResult.value.outcome_probs || {}
  const entries = Object.entries(probs).sort((a, b) => b[1] - a[1])
  if (!entries.length) return 'conic-gradient(#e8e0d8 0deg 360deg)'

  const colorMap = {
    cautious: '#f3b256',
    optimistic: '#2ca88a',
    panic: '#e56a76',
    divided: '#8d71df',
    confident: '#4e8fff',
  }

  let start = 0
  const segments = entries.map(([outcome, value]) => {
    const end = start + (Number(value) || 0) * 3.6
    const segment = `${colorMap[outcome] || '#d3c8bf'} ${start}deg ${end}deg`
    start = end
    return segment
  })

  if (start < 360) segments.push(`#efe6dc ${start}deg 360deg`)
  return `conic-gradient(${segments.join(', ')})`
})

const reportSummaryCards = computed(() => {
  const regime = marketImpact.value?.market_regime ? formatLabel(marketImpact.value.market_regime) : 'n/a'
  const volatility = marketImpact.value?.volatility_expectation ? formatLabel(marketImpact.value.volatility_expectation) : 'n/a'
  const confidence = marketImpact.value?.regime_confidence != null
    ? `${Math.round(Number(marketImpact.value.regime_confidence) * 100)}%`
    : 'n/a'
  const populationRead = populationModel.value?.dominant_population_outcome
    ? formatLabel(populationModel.value.dominant_population_outcome)
    : 'n/a'

  return [
    { label: 'Market Regime', value: regime, sub: `Confidence ${confidence}` },
    { label: 'Volatility', value: volatility, sub: `${marketImpact.value?.expected_price_discovery_hours || 'n/a'}h discovery window` },
    { label: 'Population Read', value: populationRead, sub: `${populationModel.value?.sampled_agent_count || simResult.value.num_agents || 0} agents sampled` },
    { label: 'Branch Spread', value: `${simResult.value.num_branches || 0} branches`, sub: `${Object.keys(simResult.value.outcome_probs || {}).length || 0} tracked outcomes` },
  ]
})

const reportTrendSectors = computed(() => displayedSectorImpacts.value.slice(0, 4))

function buildConicGradient(segments, fallbackColor = '#efe6dc') {
  if (!segments.length) return `conic-gradient(${fallbackColor} 0deg 360deg)`
  const totalWeight = segments.reduce((sum, segment) => sum + Number(segment.weight || 0), 0) || 1
  let start = 0
  const gradientSegments = segments.map(segment => {
    const sweep = Math.max(14, (Number(segment.weight || 0) / totalWeight) * 360)
    const entry = `${segment.color} ${start}deg ${start + sweep}deg`
    start += sweep
    return entry
  })
  if (start < 360) gradientSegments.push(`${fallbackColor} ${start}deg 360deg`)
  return `conic-gradient(${gradientSegments.join(', ')})`
}

function outcomeBarFillClass(outcome) {
  const normalized = String(outcome || '').toLowerCase()
  if (normalized === 'optimistic' || normalized === 'risk_on') return 'sector-green-fill'
  if (normalized === 'panic' || normalized === 'risk_off') return 'sector-red-fill'
  if (normalized === 'divided') return 'sector-blue-fill'
  return 'sector-amber-fill'
}

const resultsInsightCards = computed(() => {
  const regimeConfidence = Math.round(Number(marketImpact.value?.regime_confidence || focusedOutcomeProbability.value / 100 || 0) * 100)
  const sectorBars = displayedSectorImpacts.value.slice(0, 4).map(sector => ({
    label: formatLabel(sector.sector).slice(0, 14),
    value: Math.max(12, Math.round((sector.confidence || 0) * 100)),
    tone: sectorDirectionFillClass(sector.direction),
  }))

  const topCohorts = displayedPopulationCohorts.value.slice(0, 4)
  const totalPopulation = topCohorts.reduce((sum, cohort) => sum + Number(cohort.represented_population || 0), 0) || topCohorts.length || 1
  const populationPalette = ['#4e8fff', '#2ca88a', '#8d71df', '#f3b256', '#e56a76']
  let currentAngle = 0
  const populationLegend = topCohorts.map((cohort, index) => {
    const share = Number(cohort.represented_population || 0) / totalPopulation
    const angle = Math.max(18, share * 360)
    const color = populationPalette[index % populationPalette.length]
    const segment = `${color} ${currentAngle}deg ${currentAngle + angle}deg`
    currentAngle += angle
    return {
      label: cohort.label,
      color,
      segment,
    }
  })
  const populationChartStyle = populationLegend.length
    ? `conic-gradient(${populationLegend.map(item => item.segment).join(', ')})`
    : 'conic-gradient(#e8e0d8 0deg 360deg)'

  return [
    {
      key: 'market_confidence',
      title: 'Progress Circle',
      subtitle: 'Regime conviction',
      kind: 'progress',
      value: Math.max(8, Math.min(100, regimeConfidence)),
      valueLabel: `${Math.max(8, Math.min(100, regimeConfidence))}%`,
      centerLabel: formatLabel(marketImpact.value?.market_regime || dominantOutcomeLabel.value),
      detail: `This chart tracks how strongly the simulation is aligned on the current regime. Right now the forecast is anchored by ${formatLabel(marketImpact.value?.market_regime || 'the current market regime')} with ${averageConfidenceLabel.value} average confidence across agents.`,
      target: 'market',
      targetLabel: 'Open Market View',
    },
    {
      key: 'sector_plot',
      title: 'Bar Plot',
      subtitle: 'Sector momentum',
      kind: 'bars',
      bars: sectorBars,
      valueLabel: sectorBars[0] ? `${sectorBars[0].value}%` : 'n/a',
      detail: sectorBars.length
        ? `${formatLabel(displayedSectorImpacts.value[0].sector)} is the strongest visible sector expression right now. Use the Market view to inspect sector reasoning, stock watchlists, and second-order effects in more detail.`
        : 'No sector signals are available yet for this run.',
      target: 'market',
      targetLabel: 'Open Market View',
    },
    {
      key: 'population_sunburst',
      title: 'Sunburst',
      subtitle: 'Population concentration',
      kind: 'sunburst',
      chartStyle: populationChartStyle,
      legend: populationLegend,
      valueLabel: populationModel.value ? `${displayedPopulationCohorts.value.length}` : '0',
      centerLabel: populationModel.value ? 'cohorts' : 'n/a',
      detail: displayedPopulationCohorts.value.length
        ? `${displayedPopulationCohorts.value[0].label} is carrying the heaviest weighted share in the current population model. Open the Population view to inspect each cohort’s represented base and dominant read.`
        : 'Population weighting is not available for this run yet.',
      target: 'population',
      targetLabel: 'Open Population',
    },
  ]
})

const activeResultsInsightCard = computed(() => {
  return resultsInsightCards.value.find(card => card.key === resultsInsightKey.value) || resultsInsightCards.value[0] || null
})

const marketInsightCards = computed(() => {
  const regimeConfidence = Math.max(8, Math.min(100, Math.round(Number(marketImpact.value?.regime_confidence || 0) * 100)))
  const sectorBars = displayedSectorImpacts.value.slice(0, 4).map(sector => ({
    label: formatLabel(sector.sector).slice(0, 14),
    value: Math.max(12, Math.round((sector.confidence || 0) * 100)),
    tone: sectorDirectionFillClass(sector.direction),
  }))

  const watchlistSegments = [
    { label: 'Beneficiaries', weight: (marketImpact.value?.likely_beneficiaries || []).length, color: '#2ca88a' },
    { label: 'Resilient', weight: (marketImpact.value?.likely_resilient || []).length, color: '#4e8fff' },
    { label: 'Laggards', weight: (marketImpact.value?.likely_laggards || []).length, color: '#e56a76' },
  ].filter(item => item.weight > 0)

  return [
    {
      key: 'market_confidence',
      title: 'Regime Circle',
      kind: 'progress',
      value: regimeConfidence,
      valueLabel: `${regimeConfidence}%`,
      detail: `The regime read is currently ${formatLabel(marketImpact.value?.market_regime || dominantOutcomeLabel.value)} with ${averageConfidenceLabel.value} average agent conviction.`
    },
    {
      key: 'market_sectors',
      title: 'Sector Bars',
      kind: 'bars',
      bars: sectorBars,
      valueLabel: sectorBars[0] ? `${sectorBars[0].value}%` : 'n/a',
      detail: sectorBars.length
        ? `${formatLabel(displayedSectorImpacts.value[0].sector)} is the strongest visible sector channel. The chart compares how clearly each top sector is expressing this scenario.`
        : 'No sector ranking is available for this run yet.'
    },
    {
      key: 'market_watchlist',
      title: 'Watchlist Mix',
      kind: 'sunburst',
      chartStyle: buildConicGradient(watchlistSegments),
      valueLabel: `${watchlistSegments.reduce((sum, item) => sum + item.weight, 0) || 0}`,
      detail: watchlistSegments.length
        ? `This chart shows how the watchlist is distributed across likely beneficiaries, resilient names, and laggards.`
        : 'No watchlist composition is available yet.'
    },
  ]
})

const activeMarketInsightCard = computed(() => {
  return marketInsightCards.value.find(card => card.key === activeMarketInsightKey.value) || marketInsightCards.value[0] || null
})

const populationInsightCards = computed(() => {
  const coverageValue = Math.max(8, Math.min(100, Math.round(Number(populationModel.value?.coverage_ratio || 0) * 100)))
  const lensBars = populationLensCards.value.map(lens => ({
    label: lens.label.replace(' Lens', '').replace('Narrative Velocity', 'Velocity').slice(0, 14),
    value: Math.max(12, Math.round(((lens.data.distribution?.[lens.data.dominant_outcome] || 0) * 100))),
    tone: outcomeBarFillClass(lens.data.dominant_outcome),
  }))

  const topCohorts = displayedPopulationCohorts.value.slice(0, 4)
  const totalPopulation = topCohorts.reduce((sum, cohort) => sum + Number(cohort.represented_population || 0), 0) || 1
  const cohortSegments = topCohorts.map((cohort, index) => ({
    label: cohort.label,
    weight: Number(cohort.represented_population || 0) / totalPopulation,
    color: ['#4e8fff', '#2ca88a', '#8d71df', '#f3b256'][index % 4],
  }))

  return [
    {
      key: 'population_coverage',
      title: 'Coverage Circle',
      kind: 'progress',
      value: coverageValue,
      valueLabel: `${coverageValue}%`,
      detail: `Population coverage indicates how much of the represented market base is being explained by the weighted cohort model in this run.`
    },
    {
      key: 'population_lenses',
      title: 'Lens Bars',
      kind: 'bars',
      bars: lensBars,
      valueLabel: lensBars[0] ? `${lensBars[0].value}%` : 'n/a',
      detail: lensBars.length
        ? `This compares the dominant conviction level across participation, capital, and narrative velocity lenses.`
        : 'Population lens views are not available for this run yet.'
    },
    {
      key: 'population_mix',
      title: 'Cohort Mix',
      kind: 'sunburst',
      chartStyle: buildConicGradient(cohortSegments),
      valueLabel: `${topCohorts.length}`,
      detail: topCohorts.length
        ? `${topCohorts[0].label} carries the biggest represented share in the current weighted model.`
        : 'No weighted cohort composition is available yet.'
    },
  ]
})

const activePopulationInsightCard = computed(() => {
  return populationInsightCards.value.find(card => card.key === activePopulationInsightKey.value) || populationInsightCards.value[0] || null
})

const resultsSwarmVisualizationConfig = computed(() => ({
  ...config.value,
  swarmBoardWidth: 940,
  swarmBoardHeight: 660,
  swarmCenterOnLoad: true,
}))

const resultFootprintCards = computed(() => [
  {
    label: 'Graph Nodes',
    value: graphResult.value?.entity_count ?? 'n/a',
    note: graphResult.value?.entity_count ? 'mapped entities' : 'linked graph',
  },
  {
    label: 'Relationships',
    value: graphResult.value?.edge_count ?? 'n/a',
    note: graphResult.value?.edge_count ? 'tracked edges' : 'loaded on demand',
  },
  {
    label: 'Agent Sample',
    value: populationModel.value?.sampled_agent_count || simResult.value.num_agents || config.value.numAgents,
    note: 'active simulated agents',
  },
  {
    label: 'Sim Traces',
    value: simResult.value.simulation_ids?.length || simResult.value.num_branches || config.value.numBranches,
    note: 'parallel world outputs',
  },
])

const resultWatchCards = computed(() => {
  const topSector = displayedSectorImpacts.value[0]
  const topCohort = displayedPopulationCohorts.value[0]
  const strengthen = displayedStrengthenTriggers.value[0]
  const weaken = displayedWeakenTriggers.value[0]

  return [
    {
      label: 'Top Sector',
      value: topSector ? formatLabel(topSector.sector) : 'n/a',
      note: topSector
        ? `${Math.round((topSector.confidence || 0) * 100)}% confidence with ${formatLabel(topSector.direction)} drift.`
        : 'No sector leader is mapped for this run yet.',
    },
    {
      label: 'Top Cohort',
      value: topCohort?.label || 'n/a',
      note: topCohort
        ? `${formatLabel(topCohort.dominant_outcome)} read across ${topCohort.sampled_agents} sampled agents.`
        : 'No weighted cohort lead is available yet.',
    },
    {
      label: 'Strengthen Trigger',
      value: strengthen || 'n/a',
      note: strengthen ? 'If this develops further, the forecast likely firms up.' : 'No strengthening trigger surfaced.',
    },
    {
      label: 'Weaken Trigger',
      value: weaken || 'n/a',
      note: weaken ? 'If this dominates, the current read gets challenged first.' : 'No weakening trigger surfaced.',
    },
  ]
})

const visualizationGraphStats = computed(() => [
  {
    label: 'Nodes',
    value: graphResult.value?.entity_count ?? 'n/a',
    note: 'entities currently mapped',
  },
  {
    label: 'Edges',
    value: graphResult.value?.edge_count ?? 'n/a',
    note: 'relationships currently linked',
  },
  {
    label: 'Lead Outcome',
    value: formatLabel(dominantOutcomeLabel.value),
    note: `${averageConfidenceLabel.value} average confidence`,
  },
  {
    label: 'Graph Source',
    value: graphViewerName.value || graphName.value || 'n/a',
    note: 'active graph explorer source',
  },
])

const visualizationSwarmStats = computed(() => [
  {
    label: 'Cohorts',
    value: populationModel.value?.sampled_cohort_count || displayedPopulationCohorts.value.length || 'n/a',
    note: 'weighted participant groups',
  },
  {
    label: 'Represented Base',
    value: populationModel.value ? formatPopulation(populationModel.value.represented_population) : 'n/a',
    note: 'population-scale exposure',
  },
  {
    label: 'Coverage',
    value: populationModel.value ? `${Math.round(Number(populationModel.value.coverage_ratio || 0) * 100)}%` : 'n/a',
    note: 'of the weighted model',
  },
  {
    label: 'Dominant Read',
    value: populationModel.value?.dominant_population_outcome ? formatLabel(populationModel.value.dominant_population_outcome) : 'n/a',
    note: populationModel.value?.blended_market_regime ? `${formatLabel(populationModel.value.blended_market_regime)} regime` : 'awaiting population model',
  },
])

const runningOpsCards = computed(() => {
  const step = (runningStep.value || '').toLowerCase()
  const checks = [
    { key: 'ingest', label: 'Scenario Loaded', done: Boolean(config.value.topic || config.value.situation) },
    { key: 'branches', label: 'Branches Spinning', done: step.includes('branch') || currentStep.value > 2 },
    { key: 'agents', label: 'Agent Reasoning', done: step.includes('agent') || step.includes('round') || currentStep.value > 2 },
    { key: 'report', label: 'Report Assembly', done: step.includes('report') || currentStep.value > 2 },
  ]
  return checks
})

const liveActivityFeed = computed(() => {
  const base = [
    `Branch mesh prepared for ${config.value.numBranches} scenario paths.`,
    `${config.value.numAgents} representative agents are being expanded into a denser swarm field.`,
    `Current event track: ${(config.value.eventType || 'general').replaceAll('_', ' ')}.`,
    runningStep.value || 'Waiting for the next backend status update.',
    `Round architecture: ${config.value.numRounds} propagation stages.`,
  ]
  return base.filter(Boolean)
})

const runningSignalChips = computed(() => [
  formatLabel(config.value.eventType || 'general'),
  `${config.value.numAgents} cohorts`,
  `${config.value.numBranches} branches`,
  `${config.value.numRounds} stages`,
])

const runningCohortCards = computed(() => {
  const tones = ['cautious', 'cautious', 'risk off', 'divided', 'optimistic', 'cautious']
  const summaries = [
    'Retail flow is reacting first, testing whether the opening narrative becomes a broader positioning wave.',
    'Domestic funds are comparing valuation support against policy or liquidity pressure before adding size.',
    'Foreign desks are measuring downside protection, currency sensitivity, and whether the move is already crowded.',
    'Media desks are amplifying the loudest signals and shaping how quickly the headline diffuses across cohorts.',
    'Broker research is scanning for second-order beneficiaries and early dispersion within sectors.',
    'Treasury and operating desks are focusing on funding pressure, balance-sheet impact, and risk transfer.',
  ]

  return marketCohortKeys
    .slice(0, Math.max(4, config.value.numAgents))
    .map((role, index) => ({
      role: formatLabel(role),
      tone: tones[index % tones.length],
      summary: summaries[index % summaries.length],
    }))
})

const runningConsoleFeed = computed(() => [
  `[${new Date().toLocaleTimeString('en-GB', { hour12: false })}] Booted ${config.value.numBranches} scenario branches`,
  `[${new Date().toLocaleTimeString('en-GB', { hour12: false })}] Expanded ${config.value.numAgents} representative cohorts into dense field nodes`,
  `[${new Date().toLocaleTimeString('en-GB', { hour12: false })}] Event track → ${formatLabel(config.value.eventType || 'general')}`,
  `[${new Date().toLocaleTimeString('en-GB', { hour12: false })}] ${runningStep.value || 'Waiting for backend stage update...'}`,
  `[${new Date().toLocaleTimeString('en-GB', { hour12: false })}] Runtime envelope ~${estimatedMinutes.value}-${estimatedMinutes.value + 5} min`,
])

const workbenchToolCards = computed(() => [
  { key: 'ask_sector', title: 'Sector Lens', desc: 'Ask why one sector is strong, weak, or resilient.' },
  { key: 'what_would_change', title: 'Change Triggers', desc: 'See what could strengthen or weaken the forecast before the open.' },
  { key: 'ask_cohort', title: 'Cohort View', desc: 'Inspect how one participant cluster is reading the event.' },
  { key: 'counterfactual', title: 'Counterfactual', desc: 'Test how the scenario changes if a core driver weakens.' },
])

const interactiveSnapshotCards = computed(() => [
  {
    label: 'Active Tool',
    value: activeToolCard.value.title,
    note: activeToolCard.value.desc,
  },
  {
    label: 'Lead Outcome',
    value: formatLabel(dominantOutcomeLabel.value),
    note: `${averageConfidenceLabel.value} average confidence`,
  },
  {
    label: 'Sectors Indexed',
    value: `${chatSectorOptions.value.length}`,
    note: 'sector answers currently available',
  },
  {
    label: 'Cohorts Indexed',
    value: `${chatCohortOptions.value.length}`,
    note: 'cohort reads currently available',
  },
])

const interactivePromptSuggestions = computed(() => {
  const topSector = displayedSectorImpacts.value[0]
  const topCohort = displayedPopulationCohorts.value[0]

  if (chatMode.value === 'ask_sector') {
    const sectorLabel = topSector ? formatLabel(topSector.sector) : 'the leading sector'
    return [
      { title: 'Transmission', copy: `Why is ${sectorLabel} carrying the strongest visible market expression right now?` },
      { title: 'Watchlist', copy: `What would need to change for ${sectorLabel} to lose leadership before the open?` },
      { title: 'Second-order', copy: `Which adjacent sectors would be the next to react if ${sectorLabel} accelerates?` },
    ]
  }

  if (chatMode.value === 'ask_cohort') {
    const cohortLabel = topCohort?.label || 'the leading cohort'
    return [
      { title: 'Interpretation', copy: `How is ${cohortLabel} reading the event versus the broader population model?` },
      { title: 'Conviction', copy: `What would increase or reduce ${cohortLabel}'s conviction first?` },
      { title: 'Spillover', copy: `Which other cohorts are most likely to follow ${cohortLabel}'s move?` },
    ]
  }

  if (chatMode.value === 'counterfactual') {
    return [
      { title: 'Driver Removal', copy: 'What if the main policy or liquidity driver becomes materially weaker?' },
      { title: 'Regime Flip', copy: 'Which regime is most likely if the current dominant driver disappears?' },
      { title: 'Fastest Change', copy: 'Which sector or cohort would react first under the counterfactual path?' },
    ]
  }

  return [
    { title: 'Forecast Breaker', copy: 'What is the single fastest way this forecast could flip before the open?' },
    { title: 'Confirmation', copy: 'Which incoming signal would most strongly confirm the current read?' },
    { title: 'Weak Point', copy: 'Where is the highest uncertainty still sitting inside the current forecast?' },
  ]
})

const interactiveGroundingCards = computed(() => {
  const topSector = displayedSectorImpacts.value[0]
  const topCohort = displayedPopulationCohorts.value[0]
  const strengthen = displayedStrengthenTriggers.value[0]
  const weaken = displayedWeakenTriggers.value[0]

  return [
    {
      label: 'Current Regime',
      value: marketImpact.value?.market_regime ? formatLabel(marketImpact.value.market_regime) : formatLabel(dominantOutcomeLabel.value),
      note: marketImpact.value?.volatility_expectation ? `${formatLabel(marketImpact.value.volatility_expectation)} volatility` : 'regime fallback to forecast outcome',
    },
    {
      label: 'Lead Sector',
      value: topSector ? formatLabel(topSector.sector) : 'n/a',
      note: topSector ? `${Math.round((topSector.confidence || 0) * 100)}% confidence` : 'no sector leader yet',
    },
    {
      label: 'Lead Cohort',
      value: topCohort?.label || 'n/a',
      note: topCohort ? `${formatPopulation(topCohort.represented_population)} represented` : 'no cohort weighting yet',
    },
    {
      label: 'Live Trigger',
      value: strengthen || weaken || 'n/a',
      note: strengthen ? 'strengthening path' : weaken ? 'weakening path' : 'no active trigger surfaced',
    },
  ]
})

const activeToolCard = computed(() => {
  return workbenchToolCards.value.find(tool => tool.key === chatMode.value) || workbenchToolCards.value[0]
})

const activeChatContext = computed(() => {
  if (chatMode.value === 'ask_sector') return chatSectorOptions.value.find(item => item.key === chatSector.value)?.label || 'Sector'
  if (chatMode.value === 'ask_cohort') return chatCohortOptions.value.find(item => item.key === chatCohort.value)?.label || 'Cohort'
  if (chatMode.value === 'counterfactual') return chatCounterfactualTarget.value || 'Counterfactual'
  return 'Forecast'
})

const activeChatPrompt = computed(() => {
  if (chatQuestion.value?.trim()) return chatQuestion.value.trim()
  if (chatMode.value === 'ask_sector') return `Why is ${activeChatContext.value} likely to move this way in the current scenario?`
  if (chatMode.value === 'ask_cohort') return `How is ${activeChatContext.value} interpreting the event right now?`
  if (chatMode.value === 'counterfactual') return `What changes if ${activeChatContext.value} becomes much weaker or disappears?`
  return 'What would change this forecast before the market open?'
})

const chatResponseParagraphs = computed(() => {
  const answer = (chatResponse.value?.answer || '').trim()
  if (!answer) return []
  return answer
    .split(/(?<=[.!?])\s+/)
    .map(line => line.trim())
    .filter(Boolean)
})

function formatThreadTimestamp(date = new Date()) {
  return new Intl.DateTimeFormat('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date)
}

const chatSectorOptions = computed(() => {
  const impacts = marketImpact.value?.sector_impacts || {}
  return Object.keys(impacts)
    .map(key => ({ key, label: formatLabel(key) }))
    .sort((a, b) => a.label.localeCompare(b.label))
})

const chatCohortOptions = computed(() => {
  return marketCohortKeys
    .map(key => ({ key, label: formatLabel(key) }))
    .sort((a, b) => a.label.localeCompare(b.label))
})

const chatActionDisabled = computed(() => {
  if (chatLoading.value) return true
  if (chatMode.value === 'ask_sector') return !chatSector.value
  if (chatMode.value === 'ask_cohort') return !chatCohort.value
  return false
})

const chatActionLabel = computed(() => {
  if (chatMode.value === 'ask_sector') return 'Ask Sector →'
  if (chatMode.value === 'what_would_change') return 'Analyze Forecast Change →'
  if (chatMode.value === 'ask_cohort') return 'Ask Cohort →'
  if (chatMode.value === 'counterfactual') return 'Run Counterfactual →'
  return 'Analyze →'
})

// ── Lifecycle ─────────────────────────────────────────────────────────────────
let pulseTimer = null

onMounted(() => {
  checkApi()
  loadTrackRecordSummary()
  nextTick(() => {
    if (showHome.value) setupHomeRevealObserver()
  })
  pulseTimer = setInterval(() => {
    activityPulse.value = (activityPulse.value + 1) % 1000
  }, 1600)
})

onUnmounted(() => {
  if (pulseTimer) clearInterval(pulseTimer)
  resetHomeRevealObserver()
})

watch(() => simResult.value.report, () => {
  activeReportSectionIndex.value = 0
})

watch(showHome, async (value) => {
  if (value) {
    await nextTick()
    resetHomeRevealObserver()
    setupHomeRevealObserver()
    return
  }
  resetHomeRevealObserver()
})

watch(dominantOutcomeLabel, (value) => {
  const available = Object.keys(simResult.value.outcome_probs || {})
  if (!available.length) {
    focusedOutcomeKey.value = ''
    return
  }
  if (!focusedOutcomeKey.value || !available.includes(focusedOutcomeKey.value)) {
    focusedOutcomeKey.value = value !== 'n/a' ? value : available[0]
  }
})

// ── API health ────────────────────────────────────────────────────────────────
async function checkApi() {
  try { await axios.get(`${API}/api/health`); apiOk.value = true }
  catch { apiOk.value = false }
}

async function loadTrackRecordSummary() {
  try {
    const res = await axios.get(`${API}/api/prediction-track-record`)
    trackRecordSummary.value = {
      total_predictions: res.data.total_predictions || 0,
      accuracy: res.data.accuracy || 0,
      average_brier_score: res.data.average_brier_score ?? null,
      sector_direction_accuracy: res.data.sector_direction_accuracy ?? null,
      track_record_markdown: res.data.track_record_markdown || ''
    }
  } catch {
    trackRecordSummary.value = {
      total_predictions: 0,
      accuracy: 0,
      average_brier_score: null,
      sector_direction_accuracy: null,
      track_record_markdown: ''
    }
  }
}

// ── Mode switch ───────────────────────────────────────────────────────────────
function switchMode(mode) {
  inputMode.value = mode
  uploadedFilename.value = ''
  uploadedDisplayFilename.value = ''
  uploadedSourceFormat.value = ''
  uploadedWordCount.value = 0
  fetchMessage.value = ''
  fetchError.value = false
  graphMessage.value = ''
  graphError.value = false
  graphResult.value = null
  actualOutcome.value = ''
  brierResult.value = null
  templateMessage.value = ''
  templateError.value = false

  if (mode === 'template' && !eventTemplates.value.length) {
    loadEventTemplates()
  }
}

// ── Upload ────────────────────────────────────────────────────────────────────
function handleDrop(e) { const f = e.dataTransfer.files[0]; if (f) uploadFile(f) }
function handleFileUpload(e) { const f = e.target.files[0]; if (f) uploadFile(f) }

async function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await axios.post(`${API}/api/upload`, form)
    setUploadedDocument(res.data)
  } catch (e) {
    graphMessage.value = 'Upload failed: ' + (e.response?.data?.error || e.message)
    graphError.value = true
  }
}

function setUploadedDocument(meta) {
  uploadedFilename.value = meta.filename || ''
  uploadedDisplayFilename.value = meta.display_filename || meta.filename || ''
  uploadedSourceFormat.value = meta.source_format || ((meta.filename || '').split('.').pop() || 'txt')
  uploadedWordCount.value = meta.word_count || 0
}

// ── Live news ─────────────────────────────────────────────────────────────────
async function fetchLiveNews() {
  const topics = liveTopics.value.split(',').map(t => t.trim()).filter(Boolean)
  if (!topics.length) return
  fetchLoading.value = true
  fetchMessage.value = 'Connecting to RSS feeds...'
  fetchError.value = false
  try {
    const res  = await axios.post(`${API}/api/fetch-news`, { topics })
    const poll = setInterval(async () => {
      const s = await axios.get(`${API}/api/status/${res.data.job_id}`)
      const d = s.data
      if (d.status === 'complete') {
        clearInterval(poll)
        fetchLoading.value = false
        setUploadedDocument(d)
        fetchMessage.value = d.message || `✓ ${d.article_count} articles fetched`
        if (d.warning) fetchMessage.value += ' ⚠ ' + d.warning
      } else if (d.status === 'error') {
        clearInterval(poll); fetchLoading.value = false
        fetchMessage.value = 'Error: ' + d.error; fetchError.value = true
      } else { fetchMessage.value = d.step || 'Fetching...' }
    }, 2000)
  } catch (e) {
    fetchLoading.value = false
    fetchMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    fetchError.value = true
  }
}

// ── Historical ────────────────────────────────────────────────────────────────
async function loadHistoricalList() {
  try {
    const res = await axios.get(`${API}/api/historical-events`)
    historicalEvents.value = res.data.events || []
  } catch { historicalEvents.value = [] }
}

async function loadHistorical() {
  if (!selectedEventId.value) return
  fetchLoading.value = true
  fetchMessage.value = 'Loading historical document...'
  fetchError.value = false
  try {
    const res = await axios.post(`${API}/api/load-historical`, { event_id: selectedEventId.value })
    const d = res.data
    fetchLoading.value = false
    setUploadedDocument(d)
    actualOutcome.value = d.actual_outcome
    config.value.topic = d.description || selectedEventMeta.value?.description || config.value.topic
    config.value.situation = d.description || config.value.situation
    config.value.eventType = mapHistoricalEventType(d.event_id, d.domain)
    fetchMessage.value = '✓ ' + d.message
  } catch (e) {
    fetchLoading.value = false
    fetchMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    fetchError.value = true
  }
}

// ── Event templates ───────────────────────────────────────────────────────────
async function loadEventTemplates() {
  try {
    const res = await axios.get(`${API}/api/event-templates`)
    eventTemplates.value = res.data.templates || []
    if (!selectedTemplateId.value && eventTemplates.value.length) {
      selectedTemplateId.value = eventTemplates.value[0].template_id
      await loadTemplateDetail()
    }
  } catch {
    eventTemplates.value = []
  }
}

async function loadTemplateDetail() {
  if (!selectedTemplateId.value) return

  templateLoading.value = true
  templateMessage.value = 'Loading template details...'
  templateError.value = false

  try {
    const res = await axios.get(`${API}/api/event-templates/${selectedTemplateId.value}`)
    selectedTemplate.value = res.data
    templateInputs.value = Object.fromEntries(
      (res.data.required_inputs || []).map(field => [field.key, field.default ?? ''])
    )
    templateMessage.value = 'Template ready. Fill the inputs to generate a simulation scenario.'
  } catch (e) {
    selectedTemplate.value = null
    templateInputs.value = {}
    templateMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    templateError.value = true
  } finally {
    templateLoading.value = false
  }
}

async function generateTemplateScenario() {
  if (!selectedTemplateId.value) return

  templateLoading.value = true
  templateMessage.value = 'Generating market scenario...'
  templateError.value = false

  try {
    const res = await axios.post(`${API}/api/event-templates/render`, {
      template_id: selectedTemplateId.value,
      inputs: templateInputs.value
    })

    const rendered = res.data
    config.value.topic = rendered.topic || ''
    config.value.situation = rendered.situation || ''
    config.value.eventsRaw = (rendered.round_events || []).join('\n')
    config.value.eventType = rendered.event_type || 'general'
    config.value.actions = rendered.default_actions || []

    graphName.value = ''
    graphViewerName.value = ''
    graphResult.value = null
    uploadedFilename.value = ''
    uploadedDisplayFilename.value = ''
    uploadedSourceFormat.value = ''
    uploadedWordCount.value = 0

    templateMessage.value = 'Scenario generated. Review it on the next screen before running the simulation.'
    currentStep.value = 1
  } catch (e) {
    templateMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    templateError.value = true
  } finally {
    templateLoading.value = false
  }
}

// ── Build graph ───────────────────────────────────────────────────────────────
async function buildGraph() {
  if (!uploadedFilename.value) return
  isBuilding.value = true
  graphMessage.value = 'Extracting entities and building graph...'
  graphError.value = false
  graphResult.value = null
  graphName.value = uploadedFilename.value.replace(/\.[^.]+$/, '')
  try {
    const res = await axios.post(`${API}/api/build-graph`, { filename: uploadedFilename.value })
    const poll = setInterval(async () => {
      const s = await axios.get(`${API}/api/status/${res.data.job_id}`)
      const d = s.data
      if (d.status === 'complete') {
        clearInterval(poll)
        isBuilding.value = false
        graphMessage.value = `✓ Graph built — ${d.entity_count} entities, ${d.edge_count} relationships`
        graphResult.value = d
        graphViewerName.value = graphName.value
        if (!config.value.topic && graphName.value)
          config.value.topic = graphName.value.replace(/_/g, ' ')
        setTimeout(() => { currentStep.value = 1 }, 1200)
      } else if (d.status === 'error') {
        clearInterval(poll); isBuilding.value = false
        graphMessage.value = 'Error: ' + d.error; graphError.value = true
      } else { graphMessage.value = d.step || 'Building...' }
    }, 3000)
  } catch (e) {
    isBuilding.value = false
    graphMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    graphError.value = true
  }
}

// ── Run simulation ────────────────────────────────────────────────────────────
async function runSimulation() {
  const events = config.value.eventsRaw.split('\n').map(l => l.trim()).filter(Boolean)
  if (!config.value.topic.trim()) { alert('Please enter a prediction topic.'); return }
  currentStep.value = 2
  runningStep.value = 'Starting simulation branches...'
  liveFocus.value = createEmptyLiveFocus()
  try {
    const res = await axios.post(`${API}/api/run-simulation`, {
      topic       : config.value.topic,
      situation   : config.value.situation || 'An event has occurred. Agents will reason about its implications.',
      events      : events.length ? events : buildDefaultRoundEvents(),
      actions     : config.value.actions?.length ? config.value.actions : defaultSimulationActions,
      event_type  : config.value.eventType || 'general',
      graph_name  : graphName.value || '',
      num_agents  : config.value.numAgents,
      num_branches: config.value.numBranches,
      num_rounds  : config.value.numRounds
    })
    runJobId.value = res.data.job_id
    runPoller = setInterval(async () => {
      const s = await axios.get(`${API}/api/status/${runJobId.value}`)
      const d = s.data
      if (d.status === 'complete') {
        clearInterval(runPoller); simResult.value = d
        liveFocus.value = createEmptyLiveFocus()
        finalPageTab.value = 'results'
        focusedOutcomeKey.value = Object.entries(d.outcome_probs || {}).sort((a, b) => b[1] - a[1])[0]?.[0] || ''
        resultsInsightKey.value = 'market_confidence'
        activeMarketInsightKey.value = 'market_confidence'
        activePopulationInsightKey.value = 'population_coverage'
        workbenchTab.value = d.graph_name ? 'graph' : 'swarm'
        workspaceDrawerOpen.value = false
        studioCenterTab.value = 'report'
        chatMode.value = 'ask_sector'
        chatQuestion.value = ''
        chatSector.value = Object.keys(d.market_impact?.sector_impacts || {})[0] || ''
        chatCohort.value = marketCohortKeys[0]
        chatCounterfactualTarget.value = ''
        chatLoading.value = false
        chatMessage.value = ''
        chatError.value = false
        chatResponse.value = null
        chatQuestionTimestamp.value = ''
        chatAnswerTimestamp.value = ''
        currentStep.value = 3
        ensureHistoryLoaded()
        ensureAvailableGraphs()
        await nextTick()
        setTimeout(() => { animateBars.value = true }, 100)
      } else if (d.status === 'error') {
        clearInterval(runPoller); runningStep.value = 'Error: ' + d.error
        liveFocus.value = createEmptyLiveFocus()
      } else {
        runningStep.value = d.step || 'Agents reasoning...'
        liveFocus.value = d.live_focus
          ? {
              kind: d.live_focus.kind || '',
              branch_id: d.live_focus.branch_id || '',
              round_number: d.live_focus.round_number || 0,
              round_label: d.live_focus.round_label || '',
              market_role: d.live_focus.market_role || '',
              agent_name: d.live_focus.agent_name || '',
              focus_terms: Array.isArray(d.live_focus.focus_terms) ? d.live_focus.focus_terms : [],
              pulse: d.live_focus.pulse || 0,
            }
          : createEmptyLiveFocus()
      }
    }, 2000)
  } catch (e) {
    runningStep.value = 'Error: ' + (e.response?.data?.error || e.message)
    liveFocus.value = createEmptyLiveFocus()
  }
}

function buildDefaultRoundEvents() {
  const topic = config.value.topic?.trim() || 'the current event'
  const eventLabel = formatLabel(config.value.eventType || 'general').toLowerCase()
  const defaults = [
    `Headline shock forms as ${topic} is first priced across desks and sectors.`,
    `Broker notes and institutional interpretation emerge around ${topic}, shifting positioning across ${eventLabel}.`,
    `Media framing and cross-cohort discussion widen as participants reassess ${topic}.`,
    `Sector rotation and risk transfer become more visible as ${topic} moves from headline reaction to portfolio action.`,
    `Second-order effects and policy transmission of ${topic} become clearer through balance-sheet, earnings, and macro debate.`,
    `Follow-through positioning tests whether the first move around ${topic} was underpriced, overdone, or correctly framed.`,
    `Participants compare confirmation signals against contrarian warnings as ${topic} settles into broader market expectations.`,
    `Late-stage interpretation focuses on durability, execution credibility, and whether ${topic} changes medium-term allocations.`,
  ]
  return defaults.slice(0, Math.max(2, config.value.numRounds || 3))
}

function mapHistoricalEventType(eventId, domain) {
  const eventMap = {
    rbi_rate_hike_2022: 'rbi_rate_hike',
    india_ukraine_oil_2022: 'oil_price_spike',
    india_corporate_tax_cut_2019: 'budget_fiscal_expansion',
  }

  if (eventMap[eventId]) return eventMap[eventId]

  const domainMap = {
    monetary_policy: 'rbi_rate_hike',
    fiscal_policy: 'budget_fiscal_expansion',
    geopolitical: 'oil_price_spike',
  }

  return domainMap[domain] || 'general'
}

// ── Score backtest ────────────────────────────────────────────────────────────
async function scorePrediction() {
  if (!actualOutcome.value || !simResult.value.outcome_probs) return
  try {
    const res = await axios.post(`${API}/api/score-prediction`, {
      predicted_probs: simResult.value.outcome_probs,
      actual_outcome : actualOutcome.value,
      event_id       : selectedEventId.value || 'unknown',
      topic          : simResult.value.topic || config.value.topic || selectedEventMeta.value?.description || selectedEventId.value || 'Historical event',
      event_type     : simResult.value.event_type || config.value.eventType || 'general',
      event_date     : selectedEventMeta.value?.date || '',
      domain         : selectedEventMeta.value?.domain || '',
      model_version  : 'v3',
      phase_config   : ['phase1', 'phase2', 'phase4', 'phase3', 'phase6_partial', 'phase7', 'phase6_full', 'phase5'],
      branch_count   : simResult.value.num_branches || config.value.numBranches,
      agent_count    : simResult.value.num_agents || config.value.numAgents,
      used_market_roles: true,
      market_impact  : simResult.value.market_impact || {}
    })
    brierResult.value = res.data
    if (res.data.track_record_summary) {
      trackRecordSummary.value = res.data.track_record_summary
    } else {
      await loadTrackRecordSummary()
    }
  } catch (e) { console.error('Scoring failed:', e) }
}

// ── Phase 6 partial: interactive analysis ───────────────────────────────────
async function runSimulationChat() {
  if (!marketImpact.value) return
  if (chatMode.value === 'ask_sector' && !chatSector.value) return

  chatLoading.value = true
  chatMessage.value = 'Running interactive analysis...'
  chatError.value = false
  chatResponse.value = null
  chatQuestionTimestamp.value = formatThreadTimestamp()
  chatAnswerTimestamp.value = ''

  try {
    const res = await axios.post(`${API}/api/simulation-chat`, {
      mode: chatMode.value,
      question: chatQuestion.value,
      sector: chatSector.value,
      cohort: chatCohort.value,
      counterfactual_target: chatCounterfactualTarget.value,
      topic: config.value.topic || simResult.value.topic || 'Current market scenario',
      market_impact: marketImpact.value,
      simulation_ids: simResult.value.simulation_ids || [],
      causal_dag_path: simResult.value.causal_dag_path || ''
    })
    chatResponse.value = res.data
    chatMessage.value = 'Interactive analysis ready.'
    chatAnswerTimestamp.value = formatThreadTimestamp()
  } catch (e) {
    chatMessage.value = 'Error: ' + (e.response?.data?.error || e.message)
    chatError.value = true
  } finally {
    chatLoading.value = false
  }
}

// ── Download report ───────────────────────────────────────────────────────────
function downloadReport() {
  const content = simResult.value.report || 'No report available.'
  const blob = new Blob([content], { type: 'text/markdown' })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href = url; a.download = `darsh_report_${Date.now()}.md`; a.click()
  URL.revokeObjectURL(url)
}

async function downloadReportPdf() {
  if (!simResult.value.report) return
  try {
    const res = await axios.post(
      `${API}/api/export-report-pdf`,
      {
        topic: simResult.value.topic || config.value.topic || 'DARSH Prediction',
        report: simResult.value.report,
        outcome_probs: simResult.value.outcome_probs || {},
        market_impact: simResult.value.market_impact || {},
        population_model: simResult.value.population_model || {},
      },
      { responseType: 'blob' }
    )
    const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `darsh_report_${Date.now()}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    chatMessage.value = 'PDF export failed: ' + (e.response?.data?.error || e.message)
    chatError.value = true
  }
}

// ── Reset ─────────────────────────────────────────────────────────────────────
function resetAll() {
  currentStep.value = 0; inputMode.value = 'upload'
  uploadedFilename.value = ''; uploadedDisplayFilename.value = ''; uploadedSourceFormat.value = ''; uploadedWordCount.value = 0
  liveTopics.value = ''; fetchMessage.value = ''; fetchError.value = false; fetchLoading.value = false
  selectedEventId.value = ''; actualOutcome.value = ''; brierResult.value = null
  graphMessage.value = ''; graphError.value = false; graphResult.value = null; isBuilding.value = false
  runningStep.value = ''; simResult.value = {}; animateBars.value = false; showReport.value = false
  liveFocus.value = createEmptyLiveFocus()
  finalPageTab.value = 'results'
  focusedOutcomeKey.value = ''
  resultsInsightKey.value = 'market_confidence'
  activeMarketInsightKey.value = 'market_confidence'
  activePopulationInsightKey.value = 'population_coverage'
  chatMode.value = 'ask_sector'; chatQuestion.value = ''; chatSector.value = ''
  workbenchTab.value = 'swarm'
  workspaceDrawerOpen.value = false
  studioCenterTab.value = 'report'
  activeReportSectionIndex.value = 0
  chatCohort.value = ''; chatCounterfactualTarget.value = ''
  chatLoading.value = false; chatMessage.value = ''; chatError.value = false; chatResponse.value = null
  chatQuestionTimestamp.value = ''; chatAnswerTimestamp.value = ''
  showGraphViewer.value = false; showHistory.value = false; showMerge.value = false
  mergeList.value = []; mergeResult.value = null
  selectedTemplateId.value = ''
  selectedTemplate.value = null
  templateInputs.value = {}
  templateLoading.value = false
  templateMessage.value = ''
  templateError.value = false
  config.value = createDefaultConfig()
  if (runPoller) clearInterval(runPoller)
  loadTrackRecordSummary()
}

function focusOutcome(outcome) {
  focusedOutcomeKey.value = outcome
}

function selectResultsInsight(key, target = '') {
  resultsInsightKey.value = key
  if (target) studioCenterTab.value = target
}

async function ensureHistoryLoaded() {
  if (historyList.value.length) return
  try {
    const res = await axios.get(`${API}/api/simulations/history`)
    historyList.value = res.data.simulations || []
  } catch {
    historyList.value = []
  }
}

async function ensureAvailableGraphs() {
  if (availableGraphs.value.length) return
  try {
    const res = await axios.get(`${API}/api/graphs`)
    availableGraphs.value = res.data.graphs || []
  } catch {
    availableGraphs.value = []
  }
}

async function openWorkbenchTab(tab) {
  workspaceDrawerOpen.value = true
  workbenchTab.value = tab
  if (tab === 'history') await ensureHistoryLoaded()
  if (tab === 'merge') await ensureAvailableGraphs()
}

async function toggleResultsWorkspace(tab) {
  if (workspaceDrawerOpen.value && workbenchTab.value === tab) {
    workspaceDrawerOpen.value = false
    return
  }
  await openWorkbenchTab(tab)
}

// ── Phase 4: Graph viewer ─────────────────────────────────────────────────────
function toggleGraphViewer() {
  showGraphViewer.value = !showGraphViewer.value
  if (showGraphViewer.value) { showHistory.value = false; showMerge.value = false }
}

// ── Phase 4: History ──────────────────────────────────────────────────────────
async function toggleHistory() {
  showHistory.value = !showHistory.value
  if (showHistory.value) {
    showGraphViewer.value = false; showMerge.value = false
    if (!historyList.value.length) {
      try {
        const res = await axios.get(`${API}/api/simulations/history`)
        historyList.value = res.data.simulations || []
      } catch { historyList.value = [] }
    }
  }
}

async function selectHistorySim(sim) {
  selectedHistorySim.value = sim; historyRound.value = 1
  await loadHistoryRound()
}

async function loadHistoryRound() {
  if (!selectedHistorySim.value) return
  try {
    const res = await axios.get(
      `${API}/api/simulations/${selectedHistorySim.value.simulation_id}/round/${historyRound.value}`)
    historyRoundData.value = res.data
  } catch { historyRoundData.value = null }
}

// ── Phase 4: Merge ────────────────────────────────────────────────────────────
async function toggleMerge() {
  showMerge.value = !showMerge.value
  if (showMerge.value) {
    showGraphViewer.value = false; showHistory.value = false
    mergeResult.value = null; mergeList.value = []
    try {
      const res = await axios.get(`${API}/api/graphs`)
      availableGraphs.value = res.data.graphs || []
    } catch { availableGraphs.value = [] }
  }
}

async function mergeSelectedGraphs() {
  if (mergeList.value.length < 2) return
  merging.value = true
  try {
    const res = await axios.post(`${API}/api/merge-graphs`, { graph_names: mergeList.value })
    mergeResult.value = res.data
  } catch (e) {
    mergeResult.value = { error: e.response?.data?.error || e.message }
  } finally { merging.value = false }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function outcomeColor(outcome) {
  const map = { panic: 'bar-red', cautious: 'bar-amber', optimistic: 'bar-green', divided: 'bar-blue' }
  return map[outcome?.toLowerCase()] || 'bar-blue'
}

function formatLabel(value) {
  return (value || '').replaceAll('_', ' ')
}

function formatPopulation(value) {
  const numeric = Number(value || 0)
  if (!Number.isFinite(numeric)) return '0'
  if (numeric >= 10000000) return `${(numeric / 10000000).toFixed(1)}Cr`
  if (numeric >= 100000) return `${(numeric / 100000).toFixed(1)}L`
  return numeric.toLocaleString('en-IN')
}

function sectorDirectionClass(direction) {
  if ((direction || '').includes('negative')) return 'sector-red'
  if ((direction || '').includes('positive')) return 'sector-green'
  return 'sector-amber'
}

function sectorDirectionFillClass(direction) {
  if ((direction || '').includes('negative')) return 'sector-red-fill'
  if ((direction || '').includes('positive')) return 'sector-green-fill'
  return 'sector-amber-fill'
}
</script>

<style>
/* ── Design tokens ───────────────────────────────────────────────────────── */
:root {
  --bg       : #f7f9ff;
  --bg-grad  : #dee6ff;
  --surface  : rgba(255, 255, 255, 0.84);
  --surface2 : rgba(243, 247, 255, 0.95);
  --border   : rgba(131, 148, 214, 0.18);
  --border2  : rgba(131, 148, 214, 0.34);
  --text     : #24324f;
  --muted    : #6f7a98;
  --accent   : #8a74ff;
  --green    : #61d9d5;
  --amber    : #77cfff;
  --red      : #f078c4;
  --purple   : #b58fff;
  --blue     : #62bbff;
  --radius   : 10px;
  --radius-sm: 6px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 75% 55% at 10% -10%, rgba(111, 215, 255, 0.24) 0%, transparent 62%),
    radial-gradient(ellipse 58% 48% at 100% 0%, rgba(178, 144, 255, 0.18) 0%, transparent 65%),
    radial-gradient(ellipse 65% 52% at 55% 110%, rgba(104, 221, 214, 0.12) 0%, transparent 68%);
  color: var(--text);
  font-family: 'Avenir Next', 'Segoe UI', 'Trebuchet MS', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
}

/* ── HOME ────────────────────────────────────────────────────────────────── */
.home {
  position: relative;
  min-height: 100vh;
  background:
    radial-gradient(circle at 18% 18%, rgba(111, 215, 255, 0.16), transparent 26%),
    radial-gradient(circle at 82% 12%, rgba(178, 144, 255, 0.12), transparent 22%),
    radial-gradient(circle at 52% 86%, rgba(104, 221, 214, 0.08), transparent 24%),
    linear-gradient(180deg, #fcfdff 0%, #f7f9ff 44%, #eff4ff 100%);
  overflow-x: hidden;
  z-index: 100;
}

.home-grid {
  position: fixed;
  inset: 0;
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  grid-template-rows: repeat(8, 1fr);
  pointer-events: none;
}

.grid-cell {
  border: 0.5px solid rgba(209, 122, 62, 0.07);
  animation: grid-pulse 8s ease-in-out infinite;
}

@keyframes grid-pulse {
  0%, 100% { background: transparent; }
  50%       { background: rgba(239, 107, 74, 0.05); }
}

.home-agent-rain {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.92), rgba(0, 0, 0, 0.56));
}

.landing-bot {
  position: absolute;
  width: var(--bot-size);
  height: calc(var(--bot-size) * 0.72);
  border-radius: calc(var(--bot-size) * 0.22);
  background:
    linear-gradient(180deg, hsla(var(--bot-hue), 90%, 78%, 0.92), hsla(var(--bot-hue), 76%, 60%, 0.8));
  opacity: var(--bot-opacity);
  filter: blur(0.03px);
  box-shadow:
    0 0 0 1px hsla(var(--bot-hue), 78%, 78%, 0.24),
    0 12px 28px hsla(var(--bot-hue), 88%, 58%, 0.18);
  animation: landingBotRain linear infinite;
  transform: translate3d(0, 0, 0);
}

.landing-bot::before,
.landing-bot::after {
  content: '';
  position: absolute;
  top: 27%;
  width: calc(var(--bot-size) * 0.12);
  height: calc(var(--bot-size) * 0.12);
  border-radius: 50%;
  background: rgba(245, 255, 255, 0.9);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.22);
}

.landing-bot::before {
  left: 28%;
}

.landing-bot::after {
  right: 28%;
}

@keyframes landingBotRain {
  0% {
    transform: translate3d(0, -9vh, 0) rotate(0.001deg) scale(0.98);
  }
  50% {
    transform: translate3d(8px, 48vh, 0) rotate(0.001deg) scale(1);
  }
  100% {
    transform: translate3d(-6px, 112vh, 0) rotate(0.001deg) scale(1.02);
  }
}

.home-nodes {
  position: fixed;
  inset: 0;
  pointer-events: none;
}

.home-node {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(239, 107, 74, 0.22) 0%, rgba(47, 127, 232, 0.1) 45%, transparent 72%);
  animation: node-float 6s ease-in-out infinite;
  transform: translate(-50%, -50%);
}

@keyframes node-float {
  0%, 100% { transform: translate(-50%, -50%) scale(1);   opacity: 0.35; }
  50%       { transform: translate(-50%, -58%) scale(1.3); opacity: 0.65; }
}

.home-topbar {
  position: sticky;
  top: 0;
  z-index: 30;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(232, 210, 188, 0.72);
  background: rgba(255, 249, 241, 0.88);
  backdrop-filter: blur(16px);
}

.home-brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  color: #2d211a;
  cursor: pointer;
  justify-self: start;
}

.brand-mark-img {
  display: block;
  width: 34px;
  height: 34px;
  object-fit: contain;
  filter: drop-shadow(0 10px 24px rgba(138, 116, 255, 0.2));
}

.home-brand-mark {
  font-size: 28px;
}

.home-marketing-nav {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  justify-self: center;
}

.home-marketing-link {
  border: 0;
  background: transparent;
  color: #7a6354;
  font: inherit;
  font-weight: 600;
  padding: 10px 12px;
  cursor: pointer;
  transition: color 180ms ease, transform 180ms ease;
}

.home-marketing-link:hover,
.home-marketing-link:focus-visible {
  color: #2d211a;
  transform: translateY(-1px);
}

.home-topbar-actions {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  justify-self: end;
}

.home-topbar-demo,
.home-topbar-secondary,
.home-topbar-primary {
  border-radius: 16px;
  padding: 12px 16px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 180ms ease,
    background 180ms ease,
    border-color 180ms ease,
    box-shadow 240ms ease,
    color 180ms ease;
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

.home-topbar-demo {
  border: 1px solid rgba(109, 161, 255, 0.28);
  background: rgba(245, 249, 255, 0.9);
  color: #49678f;
  box-shadow: 0 10px 24px rgba(92, 133, 205, 0.08);
}

.home-topbar-secondary {
  border: 1px solid rgba(232, 210, 188, 0.82);
  background: rgba(255, 255, 255, 0.8);
  color: #6f4f3d;
}

.home-topbar-primary {
  border: 1px solid rgba(239, 196, 147, 0.4);
  background: linear-gradient(135deg, rgba(255, 235, 217, 0.96), rgba(237, 247, 255, 0.96));
  color: #2d211a;
  box-shadow: 0 16px 36px rgba(188, 129, 81, 0.18);
}

.home-topbar-demo::before,
.home-topbar-secondary::before,
.home-topbar-primary::before,
.home-cta::before,
.home-ghost-cta::before {
  content: '';
  position: absolute;
  inset: -20% auto -20% -22%;
  width: 36%;
  background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.42), transparent);
  transform: translateX(-180%) skewX(-18deg);
  transition:
    transform 620ms cubic-bezier(0.22, 1, 0.36, 1),
    opacity 260ms ease;
  opacity: 0;
  pointer-events: none;
}

.home-topbar-demo:hover::before,
.home-topbar-secondary:hover::before,
.home-topbar-primary:hover::before,
.home-cta:hover::before,
.home-ghost-cta:hover::before,
.home-topbar-demo:focus-visible::before,
.home-topbar-secondary:focus-visible::before,
.home-topbar-primary:focus-visible::before,
.home-cta:focus-visible::before,
.home-ghost-cta:focus-visible::before {
  opacity: 1;
  transform: translateX(420%) skewX(-18deg);
}

.home-topbar-demo:hover,
.home-topbar-secondary:hover,
.home-topbar-primary:hover,
.home-topbar-demo:focus-visible,
.home-topbar-secondary:focus-visible,
.home-topbar-primary:focus-visible {
  transform: translateY(-1px) scale(1.01);
}

.home-topbar-demo:hover,
.home-topbar-demo:focus-visible {
  border-color: rgba(95, 146, 239, 0.42);
  box-shadow: 0 14px 28px rgba(92, 133, 205, 0.14);
}

.home-scroll {
  position: relative;
  z-index: 2;
}

.home-stage {
  position: relative;
  width: min(1380px, calc(100vw - 40px));
  margin: 0 auto;
  padding: 18px 0 36px;
}

.home-panel {
  position: relative;
  z-index: 2;
  min-height: calc(100vh - 88px);
  display: grid;
  align-content: center;
  padding: 16px 0;
  scroll-margin-top: 100px;
}

.home-reveal {
  opacity: 0;
  transform: translateY(26px) scale(0.985);
  transition:
    opacity 760ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 860ms cubic-bezier(0.22, 1, 0.36, 1);
  transition-delay: var(--home-reveal-delay, 0ms);
  will-change: opacity, transform;
}

.home-reveal.is-visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.home-panel-shell {
  width: min(1180px, 100%);
  margin: 0 auto;
  padding: 0;
}

.home-section-panel .home-panel-shell {
  display: grid;
  gap: 20px;
  align-content: center;
  justify-items: center;
}

.home-hero-panel {
  text-align: center;
}

.home-eyebrow {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #9b6a43;
  margin-bottom: 14px;
}

.home-hero-strip,
.home-intro-pill-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 22px;
}

.hero-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  border-radius: 999px;
  border: 1px solid rgba(233, 210, 187, 0.82);
  background: rgba(255, 247, 239, 0.94);
  color: #8c6143;
  font-size: 13px;
  font-weight: 700;
}

.home-hero-visual {
  position: relative;
  width: min(860px, 100%);
  height: 286px;
  margin: 22px auto 18px;
  padding-inline: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  isolation: isolate;
}

.hero-visual-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(224, 195, 169, 0.68);
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.16), transparent 68%);
  animation: heroOrbitFloat 10s ease-in-out infinite;
}

.hero-visual-ring.ring-one {
  width: 210px;
  height: 210px;
  border-color: rgba(248, 179, 102, 0.42);
}

.hero-visual-ring.ring-two {
  width: 320px;
  height: 320px;
  border-style: dashed;
  border-color: rgba(100, 170, 255, 0.28);
  animation-delay: -2s;
}

.hero-visual-ring.ring-three {
  width: 430px;
  height: 430px;
  border-color: rgba(110, 211, 194, 0.22);
  animation-delay: -4s;
}

.hero-visual-core {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
  min-width: 0;
  width: fit-content;
  max-width: min(360px, calc(100% - 220px));
  padding: 18px 22px 16px;
  border-radius: 24px;
  border: 1px solid rgba(229, 207, 186, 0.72);
  background: linear-gradient(160deg, rgba(255, 252, 247, 0.92), rgba(244, 249, 255, 0.84));
  box-shadow:
    0 18px 42px rgba(156, 108, 72, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(14px);
}

.hero-visual-logo {
  width: 94px;
  height: 94px;
  margin-bottom: 2px;
  object-fit: contain;
  filter: drop-shadow(0 14px 30px rgba(138, 116, 255, 0.24));
}

.hero-visual-core-title {
  font-size: 34px;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.05em;
  color: #2f2119;
}

.hero-visual-core-subtitle {
  margin-top: 0;
  max-width: 18ch;
  color: #7b6557;
  font-size: 11.5px;
  line-height: 1.32;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  text-wrap: balance;
}

.hero-visual-chip {
  position: absolute;
  z-index: 3;
  padding: 9px 15px;
  border-radius: 999px;
  border: 1px solid rgba(231, 206, 182, 0.8);
  background: rgba(255, 252, 247, 0.86);
  box-shadow: 0 14px 30px rgba(170, 120, 78, 0.12);
  color: #6f5344;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  animation: heroChipFloat 7s ease-in-out infinite;
}

.hero-visual-chip.chip-a { top: 24px; left: 0; }
.hero-visual-chip.chip-b { top: 34px; right: 0; animation-delay: -1.5s; }
.hero-visual-chip.chip-c { bottom: 22px; left: 4%; animation-delay: -3s; }
.hero-visual-chip.chip-d { bottom: 10px; right: 4%; animation-delay: -4.2s; }

@keyframes heroOrbitFloat {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-8px) scale(1.02); }
}

@keyframes heroChipFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}

.home-title {
  margin: 0;
  font-size: clamp(46px, 6vw, 88px);
  line-height: 0.95;
  font-weight: 900;
  letter-spacing: -0.05em;
  color: #2b2019;
}

.title-brand {
  color: transparent;
  background: linear-gradient(135deg, #24324f 0%, #6eb4ff 24%, #8a74ff 58%, #b58fff 78%, #61d9d5 100%);
  -webkit-background-clip: text;
  background-clip: text;
}

.title-neuro { color: var(--text); }

.title-swarm {
  color: transparent;
  background: linear-gradient(135deg, var(--accent) 0%, #ff9d5c 34%, var(--purple) 68%, var(--green) 100%);
  -webkit-background-clip: text; background-clip: text;
}

.home-tagline {
  margin: 18px auto 0;
  font-size: 16px;
  line-height: 1.62;
  color: #6d5648;
  max-width: 920px;
}

.home-supporting-copy {
  max-width: 760px;
  margin: 12px auto 0;
  color: #8c715f;
  font-size: 14px;
  line-height: 1.62;
}

.home-hero-cta-row {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.home-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 34px 0 18px;
  flex-wrap: wrap;
}

.home-stat { display: flex; flex-direction: column; align-items: center; gap: 3px; }
.hstat-num { font-size: 20px; font-weight: 700; color: #c35436; }
.hstat-lbl { font-size: 10px; color: #7a5d4d; text-transform: uppercase; letter-spacing: 0.08em; }
.hstat-sep { width: 1px; height: 32px; background: rgba(209, 122, 62, 0.22); }

.home-cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 40px;
  background: linear-gradient(135deg, #ef6b4a 0%, #f49f39 100%);
  border: none;
  border-radius: 999px;
  color: #fff;
  font-family: inherit;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 16px 38px rgba(239, 107, 74, 0.28);
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

.home-cta:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 18px 42px rgba(239, 107, 74, 0.38);
}
.cta-arrow { font-size: 18px; transition: transform 0.2s; }
.home-cta:hover .cta-arrow { transform: translateX(4px); }

.home-ghost-cta {
  border-radius: 999px;
  border: 1px solid rgba(232, 210, 188, 0.86);
  background: rgba(255, 255, 255, 0.82);
  color: #75533d;
  padding: 16px 22px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35);
  position: relative;
  overflow: hidden;
  isolation: isolate;
  transition:
    transform 180ms ease,
    border-color 180ms ease,
    box-shadow 220ms ease,
    background 180ms ease;
}

.home-ghost-cta:hover,
.home-ghost-cta:focus-visible {
  transform: translateY(-1px) scale(1.01);
  border-color: rgba(214, 176, 146, 0.9);
  box-shadow:
    0 14px 28px rgba(170, 120, 78, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.45);
}

.home-cta:active,
.home-ghost-cta:active,
.home-topbar-demo:active,
.home-topbar-secondary:active,
.home-topbar-primary:active {
  transform: translateY(0px) scale(0.985);
}

.home-capabilities {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  color: #735748;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.cap-dot { opacity: 0.3; }

.home-tech { font-size: 11px; color: rgba(104, 77, 63, 0.58); letter-spacing: 0.03em; }

.home-section-head {
  max-width: 920px;
  margin: 0 auto;
  display: grid;
  justify-items: center;
  text-align: center;
}

.home-section-kicker {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #9b6a43;
  margin-bottom: 14px;
}

.home-section-title {
  margin: 0;
  font-size: clamp(28px, 3.4vw, 44px);
  line-height: 1.02;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: transparent;
  background: linear-gradient(135deg, #24324f 0%, #5d8dff 24%, #7d7cff 54%, #ab8fff 78%, #66d6ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow: 0 14px 34px rgba(125, 124, 255, 0.1);
}

.home-section-copy {
  margin: 16px auto 0;
  max-width: 860px;
  color: #705a4b;
  font-size: 16px;
  line-height: 1.72;
}

.home-intro-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.home-feature-card,
.home-about-card,
.home-walkthrough-card {
  padding: 18px;
  border-radius: 24px;
  border: 1px solid rgba(233, 210, 187, 0.76);
  background: rgba(255, 255, 255, 0.76);
  box-shadow: 0 18px 38px rgba(170, 120, 78, 0.08);
  transition:
    transform 240ms ease,
    box-shadow 260ms ease,
    border-color 220ms ease;
}

.home-feature-card:hover,
.home-about-card:hover,
.home-walkthrough-card:hover {
  transform: translateY(-4px);
  border-color: rgba(225, 192, 158, 0.95);
  box-shadow: 0 22px 44px rgba(170, 120, 78, 0.12);
}

.home-feature-card strong,
.home-walkthrough-card strong {
  display: block;
  color: #31231b;
  font-size: 16px;
  line-height: 1.22;
}

.home-feature-card span,
.home-walkthrough-card p,
.home-about-card p {
  display: block;
  margin-top: 10px;
  color: #775f50;
  line-height: 1.68;
  font-size: 14px;
}

.home-walkthrough-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}

.walkthrough-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 34px;
  padding: 0 10px;
  border-radius: 999px;
  background: rgba(243, 178, 86, 0.16);
  color: #b16e38;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.home-walkthrough-card strong {
  margin-top: 12px;
}

.home-about-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.home-about-foot {
  display: grid;
  justify-items: center;
  gap: 12px;
  margin-top: 18px;
}

.home-social-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.home-social-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border-radius: 999px;
  border: 1px solid rgba(233, 210, 187, 0.86);
  background: rgba(255, 255, 255, 0.86);
  padding: 11px 15px;
  color: #654838;
  font: inherit;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease, opacity 180ms ease;
}

.home-social-pill:hover,
.home-social-pill:focus-visible {
  transform: translateY(-1px);
  border-color: rgba(197, 158, 125, 0.92);
  box-shadow: 0 14px 30px rgba(171, 121, 79, 0.12);
}

.home-social-pill.is-disabled {
  cursor: default;
  opacity: 0.7;
}

.home-social-pill.is-disabled:hover,
.home-social-pill.is-disabled:focus-visible {
  transform: none;
  border-color: rgba(233, 210, 187, 0.86);
  box-shadow: none;
}

.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 999px;
  background: rgba(243, 178, 86, 0.15);
  color: #b06c37;
}

.social-icon svg {
  width: 14px;
  height: 14px;
  fill: currentColor;
}

.home-about-card h3 {
  margin: 0;
  color: #2d211a;
  font-size: 20px;
  line-height: 1.18;
}

@media (max-width: 1180px) {
  .home-topbar {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .home-marketing-nav,
  .home-topbar-actions {
    justify-content: center;
    justify-self: center;
  }

  .home-brand {
    justify-self: center;
  }

  .home-stage {
    width: min(100vw - 32px, 1380px);
  }

  .home-intro-grid,
  .home-about-grid,
  .home-walkthrough-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 760px) {
  .home-panel {
    min-height: auto;
    padding: 26px 0;
  }

  .home-brand-mark {
    font-size: 24px;
  }

  .home-title {
    font-size: clamp(40px, 14vw, 64px);
  }

  .home-tagline,
  .home-section-copy {
    font-size: 15px;
  }

  .home-hero-visual {
    width: min(100%, 760px);
    height: 248px;
    padding-inline: 4px;
  }

  .hero-visual-ring.ring-one {
    width: 170px;
    height: 170px;
  }

  .hero-visual-ring.ring-two {
    width: 250px;
    height: 250px;
  }

  .hero-visual-ring.ring-three {
    width: 330px;
    height: 330px;
  }

  .hero-visual-chip {
    font-size: 10px;
    padding: 8px 12px;
    max-width: 42%;
    text-align: center;
  }

  .hero-visual-core {
    max-width: min(290px, calc(100% - 44px));
    padding: 14px 16px 13px;
    gap: 6px;
  }

  .hero-visual-logo {
    width: 78px;
    height: 78px;
  }

  .hero-visual-core-title {
    font-size: 30px;
  }

  .hero-visual-core-subtitle {
    max-width: 16ch;
    font-size: 9.5px;
    letter-spacing: 0.11em;
  }

  .hero-visual-chip.chip-a { top: 18px; left: 0; }
  .hero-visual-chip.chip-b { top: 24px; right: 0; }
  .hero-visual-chip.chip-c { bottom: 16px; left: 1%; }
  .hero-visual-chip.chip-d { bottom: 6px; right: 1%; }

  .home-intro-grid,
  .home-about-grid,
  .home-walkthrough-grid {
    grid-template-columns: 1fr;
  }

  .home-feature-card,
  .home-about-card,
  .home-walkthrough-card {
    padding: 16px;
  }

  .home-hero-cta-row {
    flex-direction: column;
    align-items: center;
  }

  .home-cta,
  .home-ghost-cta {
    width: min(320px, 100%);
    justify-content: center;
  }
}

/* ── MAIN APP ────────────────────────────────────────────────────────────── */
.main-app { position: relative; min-height: 100vh; }

.app-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image:
    radial-gradient(circle, rgba(239, 107, 74, 0.08) 1px, transparent 1px),
    radial-gradient(circle, rgba(47, 127, 232, 0.05) 1px, transparent 1px);
  background-size: 32px 32px, 96px 96px;
  background-position: 0 0, 16px 16px;
  z-index: 0;
  animation: bg-drift 30s linear infinite;
}

@keyframes bg-drift {
  0%   { background-position: 0 0, 16px 16px; }
  100% { background-position: 32px 32px, 48px 48px; }
}

.main-app > * { position: relative; z-index: 1; }

/* ── Topbar ──────────────────────────────────────────────────────────────── */
.topbar {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid var(--border);
  background: rgba(255, 248, 239, 0.78);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: sticky;
  top: 0;
  z-index: 50;
  gap: 20px;
}

.topbar-left   { flex-shrink: 0; }
.topbar-center { flex: 1; display: flex; justify-content: center; }
.topbar-right  { flex-shrink: 0; display: flex; align-items: center; gap: 7px; font-size: 12px; color: var(--muted); }

.logo-btn { background: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; padding: 0; }
.logo     { font-size: 15px; font-weight: 600; letter-spacing: -0.02em; color: var(--text); }
.topbar-logo-mark {
  width: 26px;
  height: 26px;
  object-fit: contain;
  filter: drop-shadow(0 8px 18px rgba(138, 116, 255, 0.18));
}

.status-dot { width: 7px; height: 7px; border-radius: 50%; }
.status-dot.green { background: var(--green); box-shadow: 0 0 6px rgba(45,212,160,0.5); }
.status-dot.red   { background: var(--red); }

/* ── Steps ───────────────────────────────────────────────────────────────── */
.steps { display: flex; gap: 3px; }

.step {
  display: flex; align-items: center; gap: 6px; padding: 6px 12px;
  border-radius: var(--radius-sm); font-size: 12px; color: var(--muted);
  border: 1px solid transparent; transition: all 0.2s;
}

.step.active  { background: rgba(255, 255, 255, 0.75); border-color: var(--border2); color: var(--text); box-shadow: 0 12px 26px rgba(206, 127, 79, 0.08); }
.step.done    { color: var(--green); cursor: pointer; }
.step.done:hover { background: rgba(255, 255, 255, 0.55); }

.step-num {
  font-size: 10px; width: 18px; height: 18px; border-radius: 50%;
  background: rgba(255, 255, 255, 0.78); display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

.step.active .step-num { background: var(--accent); color: #fff; }
.step.done .step-num   { background: var(--green);  color: #fff; }

/* ── P4 toolbar ──────────────────────────────────────────────────────────── */
.p4-toolbar {
  display: flex; gap: 8px; flex-wrap: wrap; padding: 9px 20px;
  background: rgba(255, 243, 231, 0.72); border-bottom: 1px solid var(--border); backdrop-filter: blur(8px);
}

.p4-btn {
  padding: 6px 14px; background: rgba(255, 255, 255, 0.7); border: 1px solid var(--border);
  border-radius: var(--radius-sm); color: var(--muted); font-family: inherit;
  font-size: 12px; cursor: pointer; transition: all 0.15s;
}

.p4-btn:hover  { color: var(--text); border-color: var(--border2); }
.p4-btn.active { color: var(--accent); border-color: rgba(239, 107, 74, 0.38); background: rgba(255, 237, 221, 0.96); }

/* ── P4 panel ────────────────────────────────────────────────────────────── */
.p4-panel {
  margin: 0 20px 10px; background: rgba(255, 252, 247, 0.92); border: 1px solid var(--border2);
  border-radius: var(--radius); overflow: hidden;
  box-shadow: 0 22px 44px rgba(160, 106, 69, 0.12);
}

.p4-panel-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 16px; background: var(--surface2);
  border-bottom: 1px solid var(--border); font-size: 12px; font-weight: 500; color: var(--text);
}

.panel-close-btn {
  background: none; border: none; color: var(--muted);
  cursor: pointer; font-size: 12px; padding: 2px 6px; border-radius: 4px; transition: color 0.15s;
}

.panel-close-btn:hover { color: var(--text); }

/* ── History ─────────────────────────────────────────────────────────────── */
.history-list { padding: 4px 0; max-height: 320px; overflow-y: auto; }

.history-item {
  display: grid; grid-template-columns: 1.2fr 1fr 2fr; gap: 12px;
  padding: 9px 16px; border-bottom: 1px solid var(--border);
  cursor: pointer; font-size: 11px; transition: background 0.15s;
}

.history-item:hover { background: var(--surface2); }
.hist-id     { color: var(--text); font-weight: 500; }
.hist-meta   { color: var(--muted); }
.hist-action { color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hist-empty  { padding: 20px; font-size: 12px; color: var(--muted); text-align: center; }

.history-detail { padding: 14px 16px; }
.hist-detail-title { font-size: 15px; font-weight: 600; margin: 10px 0; }

.round-scrubber {
  display: flex; align-items: center; gap: 10px; padding: 9px 12px;
  background: rgba(255, 245, 234, 0.92); border-radius: var(--radius-sm); margin: 12px 0;
}

.scrubber-label { font-size: 11px; color: var(--muted); white-space: nowrap; }

.round-data { display: flex; flex-direction: column; gap: 8px; max-height: 400px; overflow-y: auto; }

.round-world-state { background: rgba(255, 247, 238, 0.92); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px; }
.rd-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px; }
.rd-time { color: var(--accent); text-transform: none; letter-spacing: 0; }
.rd-text  { font-size: 12px; color: var(--muted); line-height: 1.6; }
.rd-meta  { display: flex; gap: 16px; font-size: 11px; color: var(--accent); margin-top: 8px; }

.agent-snapshot { background: rgba(255, 248, 240, 0.92); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 9px 12px; }

.snap-header { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }

.snap-type {
  font-size: 9px; padding: 2px 7px; border-radius: 3px;
  text-transform: uppercase; letter-spacing: 0.04em; flex-shrink: 0;
}

.type-rational      { background: rgba(47,127,232,0.14); color: #2f7fe8; }
.type-emotional     { background: rgba(213,77,89,0.14);  color: #d54d59; }
.type-tribal        { background: rgba(242,169,59,0.18); color: #bf7d14; }
.type-contrarian    { background: rgba(142,99,215,0.14); color: #8e63d7; }
.type-institutional { background: rgba(27,154,131,0.14); color: #1b9a83; }

.snap-name   { font-size: 12px; font-weight: 500; flex: 1; }
.snap-role   { font-size: 9px; color: var(--purple); background: rgba(142,99,215,0.12); border-radius: 999px; padding: 3px 7px; }
.snap-action { font-size: 10px; color: var(--muted); }
.snap-thought { font-size: 11px; color: var(--muted); line-height: 1.6; }

/* ── Merge ───────────────────────────────────────────────────────────────── */
.merge-hint { font-size: 12px; color: var(--muted); padding: 12px 16px 8px; }
.merge-graph-list { display: flex; flex-direction: column; gap: 6px; padding: 0 16px 10px; max-height: 200px; overflow-y: auto; }

.merge-check-item {
  display: flex; align-items: center; gap: 10px; font-size: 12px;
  cursor: pointer; padding: 7px 10px; border: 1px solid var(--border);
  border-radius: var(--radius-sm); transition: border-color 0.15s;
}

.merge-check-item:hover { border-color: var(--accent); }
.merge-check-item input { accent-color: var(--accent); }
.merge-graph-name  { flex: 1; }
.merge-causal-badge { font-size: 10px; color: var(--amber); padding: 2px 7px; background: rgba(232,160,32,0.1); border-radius: 3px; }

/* ── Screen ──────────────────────────────────────────────────────────────── */
.screen { max-width: 720px; margin: 0 auto; padding: 32px 20px 60px; animation: fadeIn 0.25s ease; }
.screen-center { display: flex; flex-direction: column; align-items: center; text-align: center; padding-top: 60px; }
.ops-screen,
.studio-screen {
  width: min(1580px, calc(100vw - 36px));
  max-width: none;
  margin: 0 auto;
  padding: 26px 0 42px;
  animation: fadeIn 0.25s ease;
}

.ops-hero,
.studio-hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.ops-eyebrow {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  margin-bottom: 6px;
}

.ops-title,
.studio-title {
  font-size: 30px;
  line-height: 1.08;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--text);
}

.ops-copy,
.studio-copy {
  margin-top: 10px;
  color: var(--muted);
  max-width: 760px;
  line-height: 1.7;
  font-size: 13px;
}

.ops-badges,
.studio-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.ops-stage-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.ops-stage-card {
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(255, 252, 247, 0.82);
  border: 1px solid var(--border);
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.ops-stage-card.done {
  border-color: rgba(27, 154, 131, 0.26);
  color: var(--text);
  background: rgba(244, 252, 249, 0.92);
}

.ops-stage-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: rgba(242, 169, 59, 0.9);
  box-shadow: 0 0 0 4px rgba(242, 169, 59, 0.12);
}

.ops-stage-card.done .ops-stage-dot {
  background: var(--green);
  box-shadow: 0 0 0 4px rgba(27, 154, 131, 0.12);
}

.ops-workbench {
  display: grid;
  grid-template-columns: minmax(0, 1.72fr) minmax(370px, 0.94fr);
  gap: 16px;
  align-items: stretch;
}

.ops-pane,
.studio-pane {
  background: rgba(255, 252, 247, 0.82);
  border: 1px solid var(--border2);
  border-radius: 20px;
  box-shadow: 0 22px 44px rgba(160, 106, 69, 0.09);
}

.ops-pane {
  padding: 18px;
}

.ops-pane-wide {
  overflow: hidden;
}

.ops-surface-pane {
  padding: 16px;
}

.ops-surface-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.ops-surface-toolbar-meta {
  display: flex;
  gap: 8px;
  align-items: center;
}

.ops-surface-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 14px;
  min-height: 0;
}

.ops-surface-main {
  min-width: 0;
}

.ops-surface-layout.single-surface {
  min-height: 0;
}

.ops-surface-card {
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.76);
}

.ops-graph-stage {
  min-width: 0;
}

.ops-graph-frame {
  min-height: 860px;
}

.running-empty-state {
  min-height: 860px;
}

.ops-pane-header,
.studio-pane-header,
.report-studio-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.ops-pane-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  margin-bottom: 5px;
}

.ops-pane-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}

.ops-highlight-card,
.ops-note-card {
  padding: 14px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid var(--border);
  margin-bottom: 12px;
}

.ops-highlight-label {
  font-size: 10px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}

.ops-highlight-copy,
.ops-note-card {
  color: var(--text);
  line-height: 1.6;
  font-size: 13px;
}

.ops-feed {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 14px 0;
}

.ops-feed-compact {
  margin: 4px 0 0;
}

.ops-pane-rail {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ops-feed-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
}

.ops-feed-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 6px;
  background: var(--blue);
  flex-shrink: 0;
}

.ops-metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.ops-mini-card {
  padding: 12px;
  border-radius: 14px;
  background: rgba(247, 251, 255, 0.88);
  border: 1px solid rgba(47, 127, 232, 0.12);
}

.ops-signal-card,
.ops-trace-panel {
  padding: 14px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.76);
}

.ops-signal-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 6px;
}

.ops-signal-chip {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 244, 237, 0.92);
  border: 1px solid rgba(242, 169, 59, 0.24);
  color: #7b5844;
  font-size: 12px;
}

.ops-trace-cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

.ops-trace-card {
  padding: 12px;
  border-radius: 14px;
  background: rgba(252, 252, 252, 0.9);
  border: 1px solid rgba(221, 212, 202, 0.74);
}

.ops-trace-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.ops-trace-role {
  font-size: 12px;
  font-weight: 700;
  color: var(--text);
}

.ops-trace-tone {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--green);
}

.ops-trace-card p {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--muted);
}

.ops-console-card {
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(21, 25, 35, 0.9);
  background: #0f141b;
  color: #d6e5ff;
  box-shadow: 0 18px 34px rgba(15, 20, 27, 0.22);
}

.ops-console-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.04);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.ops-console-body {
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-family: 'SFMono-Regular', 'Consolas', monospace;
  font-size: 11px;
  line-height: 1.6;
  max-height: 132px;
  overflow: auto;
}

.ops-console-line {
  color: rgba(214, 229, 255, 0.88);
}

.ops-mini-label {
  display: block;
  font-size: 10px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}

.ops-mini-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
}

.ops-pulse {
  font-size: 11px;
  color: var(--blue);
  border: 1px solid rgba(47, 127, 232, 0.18);
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(47, 127, 232, 0.08);
}

.studio-grid {
  display: grid;
  grid-template-columns: minmax(410px, 1fr) minmax(520px, 1.28fr) minmax(360px, 0.92fr);
  gap: 16px;
  align-items: start;
}

.studio-grid.workspace-collapsed {
  grid-template-columns: 92px minmax(620px, 1.42fr) minmax(360px, 0.92fr);
}

.studio-left-pane,
.studio-center-pane,
.studio-right-pane {
  padding: 16px;
}

.studio-right-pane {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.studio-left-pane.collapsed {
  padding: 12px;
}

.workspace-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.workspace-header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

.workspace-tab {
  padding: 7px 11px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.68);
  color: var(--muted);
  font-family: inherit;
  font-size: 11px;
  cursor: pointer;
}

.workspace-tab.active {
  color: var(--blue);
  border-color: rgba(47, 127, 232, 0.28);
  background: rgba(47, 127, 232, 0.08);
}

.workspace-collapse-btn {
  width: 34px;
  height: 34px;
  padding: 0;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.72);
  color: var(--muted);
  font-family: inherit;
  font-size: 15px;
  line-height: 1;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.workspace-launcher-rail {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.workspace-launcher-btn {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-start;
  width: 100%;
  padding: 12px 10px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.7);
  color: var(--text);
  font-family: inherit;
  cursor: pointer;
  min-height: 110px;
}

.workspace-launcher-btn.active {
  border-color: rgba(47, 127, 232, 0.28);
  background: rgba(47, 127, 232, 0.08);
}

.workspace-launcher-title {
  font-size: 12px;
  font-weight: 700;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  letter-spacing: 0.04em;
}

.workspace-launcher-copy {
  font-size: 10px;
  color: var(--muted);
  writing-mode: vertical-rl;
  transform: rotate(180deg);
}

.workspace-panel-body,
.workspace-graph-wrap {
  min-height: 760px;
  display: flex;
  flex-direction: column;
}

.workspace-panel-body > * ,
.workspace-graph-wrap > * {
  flex: 1;
}

.workspace-empty-state {
  min-height: 420px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--muted);
  padding: 24px;
  border: 1px dashed var(--border2);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.58);
}

.studio-summary-card {
  margin-bottom: 16px;
}

.compact {
  margin-bottom: 0;
}

.compact-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.studio-focus-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.report-studio-card {
  background: rgba(255, 252, 247, 0.94);
  border: 1px solid var(--border2);
  border-radius: 20px;
  padding: 18px;
  box-shadow: 0 18px 36px rgba(160, 106, 69, 0.08);
}

.report-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.studio-tabs {
  align-items: center;
}

.report-studio-grid {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: 16px;
}

.report-overview-span {
  grid-column: 1 / -1;
}

.report-overview-card {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.report-overview-main {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 16px;
}

.report-overview-chart {
  display: flex;
  gap: 16px;
  align-items: center;
}

.report-donut {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.84), 0 18px 30px rgba(160, 106, 69, 0.08);
}

.report-donut-hole {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: rgba(255, 252, 247, 0.97);
  border: 1px solid rgba(230, 217, 206, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  text-align: center;
  padding: 10px;
}

.report-donut-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.report-donut-hole strong {
  font-size: 14px;
  line-height: 1.2;
  color: var(--text);
}

.report-donut-legend {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.report-donut-row {
  display: grid;
  grid-template-columns: 10px 1fr auto;
  gap: 8px;
  align-items: center;
  font-size: 12px;
  color: var(--muted);
}

.report-donut-row strong {
  color: var(--text);
}

.report-donut-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.report-overview-metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.report-overview-metric {
  padding: 14px 15px;
  border-radius: 14px;
  background: rgba(255, 251, 246, 0.92);
  border: 1px solid rgba(232, 206, 182, 0.64);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.report-overview-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.report-overview-value {
  font-size: 18px;
  line-height: 1.2;
  color: var(--text);
}

.report-overview-sub {
  font-size: 11px;
  line-height: 1.5;
  color: var(--muted);
}

.report-trend-strip {
  border-top: 1px solid rgba(232, 206, 182, 0.58);
  padding-top: 16px;
}

.report-trend-title {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 10px;
}

.report-trend-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.report-trend-card {
  border-radius: 14px;
  border: 1px solid rgba(232, 206, 182, 0.62);
  background: rgba(255, 251, 246, 0.92);
  padding: 12px;
  min-width: 0;
}

.report-trend-head {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  color: var(--text);
  margin-bottom: 8px;
}

.report-trend-bar {
  height: 6px;
  border-radius: 999px;
  background: rgba(223, 214, 204, 0.44);
  overflow: hidden;
  margin-bottom: 8px;
}

.report-trend-fill {
  height: 100%;
  border-radius: inherit;
}

.report-trend-card p {
  margin: 0;
  font-size: 11px;
  line-height: 1.55;
  color: var(--muted);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.report-chart-atlas-card {
  padding: 18px;
  border-radius: 20px;
  background: rgba(255, 252, 247, 0.9);
  border: 1px solid var(--border2);
  box-shadow: 0 20px 36px rgba(160, 106, 69, 0.08);
}

.report-chart-atlas-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.report-chart-atlas-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.report-insight-card {
  text-align: left;
  padding: 14px;
  border-radius: 16px;
  border: 1px solid rgba(226, 214, 203, 0.78);
  background: rgba(255, 255, 255, 0.82);
  color: var(--text);
  font-family: inherit;
  cursor: pointer;
  transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
  min-width: 0;
}

.report-insight-card:hover,
.report-insight-card.active {
  transform: translateY(-1px);
  border-color: rgba(47, 127, 232, 0.18);
  box-shadow: 0 14px 22px rgba(47, 127, 232, 0.08);
}

.report-insight-head {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: flex-start;
  margin-bottom: 12px;
}

.report-insight-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
}

.report-insight-subtitle,
.report-insight-link {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.55;
}

.report-insight-link {
  white-space: nowrap;
}

.report-insight-progress,
.report-insight-sunburst {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 170px;
}

.progress-circle,
.sunburst-chart {
  width: 138px;
  height: 138px;
  border-radius: 50%;
  display: grid;
  place-items: center;
}

.progress-circle {
  background:
    radial-gradient(circle at center, rgba(255, 252, 247, 0.98) 0 54px, transparent 55px),
    conic-gradient(#4e8fff calc(var(--progress, 50) * 1%), rgba(233, 227, 220, 0.9) 0);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.8), 0 16px 26px rgba(160, 106, 69, 0.08);
}

.progress-circle-inner,
.sunburst-chart-inner {
  width: 82px;
  height: 82px;
  border-radius: 50%;
  background: rgba(255, 252, 247, 0.98);
  border: 1px solid rgba(230, 217, 206, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  text-align: center;
  padding: 10px;
}

.progress-circle-inner strong,
.sunburst-chart-inner strong {
  font-size: 20px;
  line-height: 1;
  color: var(--text);
}

.progress-circle-inner span,
.sunburst-chart-inner span {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.report-insight-bars {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 170px;
  justify-content: center;
}

.report-insight-bar-row {
  display: grid;
  grid-template-columns: 68px minmax(0, 1fr) 42px;
  gap: 8px;
  align-items: center;
}

.report-insight-bar-label,
.report-insight-bar-value {
  font-size: 11px;
  color: var(--muted);
}

.report-insight-bar-track {
  height: 10px;
  border-radius: 999px;
  background: rgba(224, 216, 206, 0.54);
  overflow: hidden;
}

.report-insight-bar-fill {
  height: 100%;
  border-radius: inherit;
}

.sector-red-fill {
  background: linear-gradient(90deg, rgba(213, 77, 89, 0.96), rgba(235, 127, 138, 0.96));
}

.sector-green-fill {
  background: linear-gradient(90deg, rgba(27, 154, 131, 0.96), rgba(76, 198, 176, 0.96));
}

.sector-amber-fill {
  background: linear-gradient(90deg, rgba(242, 169, 59, 0.96), rgba(245, 196, 94, 0.96));
}

.sector-blue-fill {
  background: linear-gradient(90deg, rgba(95, 132, 235, 0.96), rgba(139, 114, 223, 0.96));
}

.sunburst-legend {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-left: 14px;
}

.sunburst-legend-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--muted);
}

.sunburst-legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.report-chart-note {
  margin-top: 14px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(226, 214, 203, 0.78);
}

.report-chart-note p {
  font-size: 12px;
  line-height: 1.7;
  color: var(--muted);
  margin-top: 6px;
}

.section-chart-atlas {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.section-chart-card {
  min-height: 178px;
}

.section-chart-note {
  margin-bottom: 16px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(226, 214, 203, 0.78);
}

.section-chart-note p {
  margin: 6px 0 0;
  font-size: 12px;
  line-height: 1.7;
  color: var(--muted);
}

.population-chart-note {
  background: rgba(247, 251, 255, 0.9);
  border-color: rgba(47, 127, 232, 0.12);
}

.report-mini-atlas {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.report-mini-chart-card {
  padding: 12px;
  border-radius: 14px;
  border: 1px solid rgba(226, 214, 203, 0.74);
  background: rgba(255, 255, 255, 0.8);
  color: var(--text);
  font-family: inherit;
  cursor: pointer;
  text-align: left;
}

.report-mini-chart-card.active {
  border-color: rgba(47, 127, 232, 0.22);
  background: rgba(246, 250, 255, 0.96);
}

.report-mini-chart-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 11px;
}

.report-mini-progress,
.report-mini-sunburst {
  display: flex;
  justify-content: center;
}

.report-mini-circle,
.report-mini-sunburst-chart {
  width: 92px;
  height: 92px;
}

.report-mini-circle-inner {
  width: 56px;
  height: 56px;
}

.report-mini-circle-inner strong {
  font-size: 13px;
}

.report-mini-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.report-mini-bar-row {
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr);
  gap: 8px;
  align-items: center;
  font-size: 10px;
  color: var(--muted);
}

.report-mini-bar-track {
  height: 8px;
  border-radius: 999px;
  background: rgba(224, 216, 206, 0.54);
  overflow: hidden;
}

.report-mini-bar-fill {
  height: 100%;
  border-radius: inherit;
}

.report-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.report-nav-item {
  width: 100%;
  text-align: left;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.72);
  color: var(--muted);
  font-family: inherit;
  cursor: pointer;
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.report-nav-item.active {
  border-color: rgba(27, 154, 131, 0.26);
  background: rgba(243, 251, 249, 0.96);
  color: var(--text);
}

.report-nav-index {
  font-size: 10px;
  color: var(--green);
  margin-top: 2px;
}

.report-nav-title {
  font-size: 12px;
  line-height: 1.5;
}

.report-viewer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.report-section-card,
.report-raw-card {
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
}

.report-section-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 10px;
}

.report-section-body {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 12px;
  color: var(--muted);
  line-height: 1.8;
}

.premium-chat {
  margin-bottom: 16px;
}

.tool-card-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.tool-card {
  text-align: left;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.76);
  cursor: pointer;
  font-family: inherit;
  color: var(--text);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tool-card.active {
  border-color: rgba(47, 127, 232, 0.25);
  background: rgba(246, 250, 255, 0.96);
}

.tool-card-title {
  font-size: 13px;
  font-weight: 700;
}

.tool-card-copy {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.6;
}

.premium-response {
  background: rgba(250, 252, 255, 0.98);
}

.trigger-rail-card {
  background: rgba(255, 252, 247, 0.94);
  border: 1px solid rgba(242, 169, 59, 0.18);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
}

.trigger-inline-card {
  margin-top: 16px;
}

.trigger-rail-group + .trigger-rail-group {
  margin-top: 12px;
}

.trigger-fallback {
  color: var(--muted);
  font-style: italic;
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

.screen-title { font-size: 22px; font-weight: 600; letter-spacing: -0.03em; margin-bottom: 8px; }
.screen-sub   { color: var(--muted); font-size: 13px; margin-bottom: 28px; line-height: 1.7; }

/* ── Mode tabs ───────────────────────────────────────────────────────────── */
.mode-tabs { display: flex; gap: 6px; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--border); flex-wrap: wrap; }

.mode-tab {
  display: flex; align-items: center; gap: 6px; padding: 8px 16px;
  border: 1px solid var(--border); background: transparent; color: var(--muted);
  border-radius: var(--radius-sm); cursor: pointer; font-size: 12px;
  font-family: inherit; transition: all 0.15s;
}

.mode-tab:hover { color: var(--text); border-color: var(--border2); }
.mode-tab.active { background: var(--surface2); border-color: var(--accent); color: var(--accent); }

.tab-icon  { font-size: 13px; }
.mode-body { padding: 4px 0; }
.mode-desc { font-size: 13px; color: var(--muted); margin-bottom: 20px; line-height: 1.7; }

/* ── Banners ─────────────────────────────────────────────────────────────── */
.info-banner {
  padding: 12px 14px; border-radius: var(--radius-sm); font-size: 12px;
  line-height: 1.6; margin-bottom: 20px; border-left: 3px solid;
}

.info-blue  { background: rgba(47, 127, 232, 0.09); border-color: var(--blue); color: #315d9d; }
.info-amber { background: rgba(242, 169, 59, 0.12);  border-color: var(--amber);  color: #8d5e12; }
.info-purple { background: rgba(142, 99, 215, 0.1); border-color: var(--purple); color: #6c4cb1; }

/* ── Template mode ──────────────────────────────────────────────────────── */
.template-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 16px;
  align-items: start;
  margin-bottom: 18px;
}

.template-card {
  background: rgba(255, 251, 246, 0.9);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
}

.template-card-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 10px;
}

.template-eyebrow,
.config-context-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.template-title,
.config-context-value {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
}

.template-chip {
  font-size: 11px;
  color: var(--purple);
  background: rgba(142, 99, 215, 0.12);
  border: 1px solid rgba(142, 99, 215, 0.2);
  border-radius: 999px;
  padding: 5px 10px;
  white-space: nowrap;
}

.template-desc,
.config-context-detail {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.7;
}

.template-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px 18px;
  margin-bottom: 18px;
}

.template-field {
  min-width: 0;
}

.template-toggle {
  height: 100%;
}

.toggle-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  min-height: 100%;
  background: rgba(255, 252, 247, 0.92);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}

.toggle-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.toggle-copy .field-label {
  margin-bottom: 4px;
}

.toggle-copy .field-note {
  margin-top: 0;
}

.toggle-input {
  width: 18px;
  height: 18px;
  accent-color: var(--purple);
  flex-shrink: 0;
}

.template-actions {
  display: flex;
  flex-direction: column;
}

/* ── Dropzone ────────────────────────────────────────────────────────────── */
.dropzone {
  border: 1.5px dashed var(--border2); border-radius: var(--radius);
  padding: 40px 24px; text-align: center; cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  background: rgba(255, 251, 246, 0.7);
}

.dropzone:hover    { border-color: var(--accent); background: rgba(255, 236, 219, 0.58); }
.dropzone-ready    { border-color: var(--green); background: rgba(219, 247, 241, 0.72); }
.dropzone-empty    { color: var(--muted); }
.drop-arrow        { font-size: 28px; margin-bottom: 10px; color: rgba(209, 122, 62, 0.56); }
.drop-hint         { font-size: 11px; color: var(--muted); display: block; margin-top: 6px; }
.dropzone-done     { color: var(--green); }
.check-big         { font-size: 28px; display: block; margin-bottom: 8px; }

/* ── Fields ──────────────────────────────────────────────────────────────── */
.field-group { margin-bottom: 18px; }

.field-label {
  display: block; font-size: 11px; font-weight: 500; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--muted); margin-bottom: 7px;
}

.field-hint { text-transform: none; letter-spacing: 0; font-weight: 400; }
.field-note { font-size: 11px; color: var(--muted); margin-top: 5px; }

.field-input,
.field-textarea,
.field-select {
  width: 100%; background: rgba(255, 255, 255, 0.78); border: 1px solid var(--border);
  border-radius: var(--radius-sm); color: var(--text); font-family: inherit;
  font-size: 13px; padding: 10px 12px; transition: border-color 0.15s; outline: none;
}

.field-input:focus,
.field-textarea:focus,
.field-select:focus { border-color: var(--accent); box-shadow: 0 0 0 4px rgba(239, 107, 74, 0.12); }

.field-textarea { resize: vertical; }

/* ── Sliders ─────────────────────────────────────────────────────────────── */
.slider-wrap { display: flex; align-items: center; gap: 12px; }
.field-slider { flex: 1; accent-color: var(--accent); }
.slider-val   { font-size: 18px; font-weight: 600; color: var(--accent); min-width: 28px; text-align: center; }

/* ── Event card ──────────────────────────────────────────────────────────── */
.event-card { background: rgba(255, 252, 247, 0.88); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px 14px; margin: 12px 0; display: flex; flex-direction: column; gap: 8px; }
.event-row   { display: flex; justify-content: space-between; font-size: 12px; }
.event-key   { color: var(--muted); }
.event-val   { color: var(--text); }
.hidden-outcome { color: var(--amber); }

/* ── Build section ───────────────────────────────────────────────────────── */
.build-section { margin-top: 24px; padding-top: 22px; border-top: 1px solid var(--border); }

.file-badge { display: flex; align-items: center; gap: 8px; background: rgba(255, 252, 247, 0.9); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 9px 13px; margin-bottom: 14px; font-size: 12px; }
.file-icon  { font-size: 14px; }
.file-name  { flex: 1; color: var(--text); }
.file-words { color: var(--muted); font-size: 11px; }

.graph-result { display: flex; align-items: center; gap: 16px; margin-top: 14px; padding: 14px 18px; background: rgba(255, 242, 231, 0.96); border-radius: var(--radius-sm); border: 1px solid var(--border); }
.graph-stat   { display: flex; flex-direction: column; align-items: center; }
.stat-num     { font-size: 28px; font-weight: 700; color: var(--accent); }
.stat-lbl     { font-size: 11px; color: var(--muted); }
.graph-divider { width: 1px; height: 36px; background: var(--border); }

/* ── Config ──────────────────────────────────────────────────────────────── */
.config-grid { display: flex; flex-direction: column; gap: 4px; margin-bottom: 24px; }
.config-row  { display: flex; gap: 20px; }
.half        { flex: 1; }

.config-context-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: rgba(255, 248, 238, 0.92);
  border: 1px solid rgba(142, 99, 215, 0.18);
  border-radius: var(--radius);
  padding: 14px 16px;
  margin-bottom: 6px;
}

.estimate-card { background: rgba(255, 251, 246, 0.92); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px 16px; margin-bottom: 20px; display: flex; flex-direction: column; gap: 4px; box-shadow: 0 16px 30px rgba(185, 123, 83, 0.08); }
.estimate-label  { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
.estimate-time   { font-size: 22px; font-weight: 700; color: var(--amber); }
.estimate-detail { font-size: 11px; color: var(--muted); }

/* ── Running ─────────────────────────────────────────────────────────────── */
.running-indicator { position: relative; width: 64px; height: 64px; margin-bottom: 28px; }

.pulse-ring { position: absolute; inset: 0; border-radius: 50%; border: 1.5px solid var(--amber); animation: pulse-out 1.8s ease-out infinite; }
.ring2      { animation-delay: 0.6s; }

.pulse-core { position: absolute; inset: 16px; border-radius: 50%; background: var(--amber); opacity: 0.9; box-shadow: 0 0 16px rgba(232,160,32,0.5); }

@keyframes pulse-out {
  0%   { transform: scale(1); opacity: 0.7; }
  100% { transform: scale(2.4); opacity: 0; }
}

.running-step  { color: var(--muted); font-size: 13px; margin: 10px 0 16px; }
.running-hint  { color: var(--muted); font-size: 12px; margin-top: 20px; max-width: 380px; }
.running-meta  { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-top: 12px; }
.meta-chip     { font-size: 11px; padding: 4px 10px; border-radius: 20px; background: rgba(255, 248, 240, 0.88); border: 1px solid var(--border); color: var(--muted); }
.chip-amber    { border-color: var(--amber); color: var(--amber); }
.chip-blue     { border-color: var(--accent); color: var(--accent); }

.report-progress-hint { font-size: 11px; color: var(--muted); margin-top: 6px; opacity: 0.7; }

/* ── Progress bar ────────────────────────────────────────────────────────── */
.progress-bar { height: 2px; background: var(--surface2); border-radius: 2px; overflow: hidden; margin-top: 8px; width: 100%; }
.progress-bar.wide { width: 320px; max-width: 100%; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 2px; }

.progress-fill.indeterminate {
  width: 40% !important;
  animation: slide-right 1.6s ease-in-out infinite;
}

@keyframes slide-right {
  0%   { transform: translateX(-150%); }
  100% { transform: translateX(400%); }
}

/* ── Results ─────────────────────────────────────────────────────────────── */
.outcome-card {
  background: rgba(255, 252, 247, 0.92);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: 0 18px 36px rgba(185, 123, 83, 0.1);
}

.outcome-header { display: flex; justify-content: space-between; font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; }

.outcome-row   { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.outcome-label { font-size: 12px; width: 80px; flex-shrink: 0; color: var(--muted); }
.outcome-pct   { font-size: 13px; font-weight: 600; width: 48px; text-align: right; }

.outcome-bar-bg   { flex: 1; height: 7px; background: rgba(238, 222, 205, 0.72); border-radius: 4px; overflow: hidden; }
.outcome-bar-fill { height: 100%; border-radius: 4px; transition: width 0.9s cubic-bezier(0.34, 1.56, 0.64, 1); }

.bar-red    { background: var(--red); }
.bar-amber  { background: var(--amber); }
.bar-green  { background: var(--green); }
.bar-blue   { background: var(--accent); }

.dominant-badge { display: flex; align-items: center; gap: 12px; padding: 14px 18px; border-radius: var(--radius-sm); margin-bottom: 16px; border: 1px solid; }
.dominant-badge.bar-red   { color: var(--red);   background: rgba(217,79,79,0.07);   border-color: rgba(217,79,79,0.25); }
.dominant-badge.bar-amber { color: var(--amber); background: rgba(232,160,32,0.07);  border-color: rgba(232,160,32,0.25); }
.dominant-badge.bar-green { color: var(--green); background: rgba(45,212,160,0.07);  border-color: rgba(45,212,160,0.25); }
.dominant-badge.bar-blue  { color: var(--accent); background: rgba(67,145,245,0.07); border-color: rgba(67,145,245,0.25); }

.badge-label   { font-size: 11px; opacity: 0.7; }
.badge-outcome { font-size: 18px; font-weight: 700; flex: 1; }
.badge-prob    { font-size: 12px; opacity: 0.8; }

.prediction-summary { background: rgba(255, 252, 247, 0.92); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px 16px; font-size: 13px; color: var(--muted); line-height: 1.7; margin-bottom: 16px; }

.market-intel-card {
  background: rgba(255, 252, 247, 0.94);
  border: 1px solid var(--border2);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: 0 18px 36px rgba(185, 123, 83, 0.1);
}

.market-intel-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.market-intel-eyebrow {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 4px;
}

.market-intel-title {
  font-size: 20px;
  line-height: 1.2;
}

.market-intel-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.market-badge {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 11px;
  border: 1px solid var(--border);
  background: rgba(255, 244, 229, 0.9);
  color: var(--text);
}

.market-confidence-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}

.market-confidence-box {
  background: rgba(255, 245, 234, 0.92);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
}

.market-confidence-label {
  display: block;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-bottom: 6px;
}

.market-confidence-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}

.sector-impact-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.sector-impact-card {
  background: rgba(255, 248, 240, 0.92);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px;
}

.sector-impact-top {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}

.sector-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.sector-direction {
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
}

.sector-confidence-bar {
  height: 7px;
  background: rgba(238, 222, 205, 0.72);
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 8px;
}

.sector-confidence-fill {
  height: 100%;
  border-radius: 999px;
}

.sector-red {
  color: var(--red);
  background: linear-gradient(90deg, rgba(213, 77, 89, 0.95), rgba(231, 120, 125, 0.95));
}

.sector-green {
  color: var(--green);
  background: linear-gradient(90deg, rgba(27, 154, 131, 0.95), rgba(76, 198, 176, 0.95));
}

.sector-amber {
  color: #b87812;
  background: linear-gradient(90deg, rgba(242, 169, 59, 0.95), rgba(245, 196, 94, 0.95));
}

.sector-reasoning {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 8px;
}

.sector-stocks {
  font-size: 11px;
  color: var(--text);
}

.watchlist-grid,
.trigger-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 14px;
}

.watchlist-column,
.trigger-column {
  background: rgba(255, 248, 240, 0.92);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px;
}

.watchlist-heading,
.trigger-heading {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-bottom: 10px;
}

.watchlist-item {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(209, 122, 62, 0.12);
}

.watchlist-item:last-child {
  border-bottom: none;
}

.watchlist-empty {
  font-size: 12px;
  color: var(--muted);
}

.population-card {
  background: rgba(245, 251, 255, 0.96);
  border: 1px solid rgba(47, 127, 232, 0.18);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: 0 18px 36px rgba(60, 112, 184, 0.1);
}

.population-card-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.population-metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.population-metric-box,
.population-lens-card {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(47, 127, 232, 0.12);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
}

.population-lens-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.population-lens-title {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-bottom: 6px;
}

.population-lens-outcome {
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}

.population-lens-regime {
  font-size: 12px;
  color: var(--muted);
  margin-top: 4px;
}

.population-lens-prob {
  margin-top: 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--blue);
}

.population-section-title {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-bottom: 10px;
}

.population-cohort-list,
.population-takeaway-block {
  margin-top: 14px;
}

.population-cohort-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 9px 0;
  border-bottom: 1px solid rgba(47, 127, 232, 0.1);
}

.population-cohort-row:last-child {
  border-bottom: none;
}

.population-cohort-main,
.population-cohort-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.population-cohort-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}

.population-cohort-role,
.population-cohort-meta {
  font-size: 11px;
  color: var(--muted);
}

.chat-card {
  background: rgba(255, 252, 247, 0.94);
  border: 1px solid rgba(47, 127, 232, 0.16);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: 0 18px 36px rgba(60, 112, 184, 0.09);
}

.chat-card-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.chat-mode-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.chat-mode-tab {
  padding: 7px 11px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255, 245, 234, 0.85);
  color: var(--muted);
  font-family: inherit;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.chat-mode-tab.active {
  background: rgba(47, 127, 232, 0.12);
  color: var(--blue);
  border-color: rgba(47, 127, 232, 0.25);
}

.chat-form-grid {
  display: grid;
  grid-template-columns: 0.85fr 1.15fr;
  gap: 16px;
}

.chat-response-card {
  margin-top: 14px;
  background: rgba(246, 250, 255, 0.92);
  border: 1px solid rgba(47, 127, 232, 0.18);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
}

.chat-response-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.chat-response-answer {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.7;
}

.chat-support-list {
  margin-top: 10px;
  padding-left: 18px;
  font-size: 12px;
  color: var(--muted);
  line-height: 1.7;
}

.chat-support-list li + li {
  margin-top: 5px;
}

.trigger-list {
  padding-left: 18px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.7;
}

.trigger-list li + li {
  margin-top: 6px;
}

/* ── Final results revamp ───────────────────────────────────────────────── */
.results-shell {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}

.results-rail {
  position: sticky;
  top: 92px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 18px;
  border-radius: 20px;
  background: rgba(255, 252, 247, 0.9);
  border: 1px solid var(--border2);
  box-shadow: 0 22px 40px rgba(160, 106, 69, 0.09);
}

.results-rail-top {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.results-rail-kicker {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
}

.results-rail-title {
  font-size: 26px;
  line-height: 1.02;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--text);
}

.results-rail-copy {
  font-size: 12px;
  line-height: 1.7;
  color: var(--muted);
}

.results-rail-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.results-rail-btn {
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px;
  border-radius: 18px;
  border: 1px solid rgba(221, 209, 198, 0.82);
  background: rgba(255, 255, 255, 0.76);
  color: var(--text);
  font-family: inherit;
  cursor: pointer;
  transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease, background 0.16s ease;
}

.results-rail-btn:hover {
  transform: translateY(-1px);
  border-color: rgba(47, 127, 232, 0.18);
}

.results-rail-btn.active {
  border-color: rgba(47, 127, 232, 0.26);
  background: rgba(241, 247, 255, 0.95);
  box-shadow: 0 14px 24px rgba(47, 127, 232, 0.08);
}

.results-rail-btn-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
}

.results-rail-btn-copy {
  font-size: 11px;
  line-height: 1.65;
  color: var(--muted);
}

.results-rail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.results-rail-chip {
  display: inline-flex;
  align-items: center;
  padding: 7px 11px;
  border-radius: 999px;
  background: rgba(255, 244, 237, 0.92);
  border: 1px solid rgba(242, 169, 59, 0.22);
  color: #7b5844;
  font-size: 11px;
}

.results-rail-reset {
  width: 100%;
}

.results-stage {
  min-width: 0;
}

.results-dashboard {
  display: grid;
  grid-template-columns: minmax(0, 1.46fr) minmax(340px, 0.8fr);
  gap: 16px;
  align-items: start;
}

.results-main-column,
.results-side-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.result-card-elevated,
.result-focus-card,
.result-side-card,
.visualization-card,
.interactive-nav-card,
.interactive-support-card,
.interactive-console-card,
.trigger-inline-card {
  background: rgba(255, 252, 247, 0.9);
  border: 1px solid var(--border2);
  border-radius: 20px;
  box-shadow: 0 20px 36px rgba(160, 106, 69, 0.08);
}

.result-focus-card,
.result-side-card,
.interactive-nav-card,
.interactive-support-card,
.interactive-console-card {
  padding: 18px;
}

.outcome-row-button {
  width: 100%;
  border-radius: 14px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: background 0.16s ease, border-color 0.16s ease, transform 0.16s ease;
}

.outcome-row-button:hover {
  background: rgba(255, 255, 255, 0.62);
}

.outcome-row-button.active {
  background: rgba(255, 255, 255, 0.84);
  border-color: rgba(47, 127, 232, 0.18);
  transform: translateX(2px);
}

.result-focus-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 12px;
}

.result-focus-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  border-radius: 999px;
  background: rgba(255, 245, 234, 0.98);
  border: 1px solid rgba(242, 169, 59, 0.24);
  color: #80573f;
  font-size: 13px;
  font-weight: 700;
}

.result-focus-copy {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
  margin-bottom: 14px;
}

.result-focus-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}

.result-focus-box {
  padding: 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(225, 214, 203, 0.78);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.result-focus-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.result-focus-box strong {
  font-size: 14px;
  color: var(--text);
}

.result-focus-list {
  padding-left: 18px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.7;
}

.result-focus-list li + li {
  margin-top: 6px;
}

.report-donut-row-button {
  width: 100%;
  padding: 6px 8px;
  border-radius: 12px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: background 0.16s ease, border-color 0.16s ease;
}

.report-donut-row-button:hover,
.report-donut-row-button.active {
  background: rgba(255, 255, 255, 0.82);
  border-color: rgba(47, 127, 232, 0.14);
}

.report-trend-card-button {
  text-align: left;
  border: 1px solid rgba(225, 214, 203, 0.7);
  background: rgba(255, 255, 255, 0.78);
  border-radius: 14px;
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.16s ease;
}

.report-trend-card-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 24px rgba(160, 106, 69, 0.08);
}

.result-side-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.result-side-stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.result-side-stats-compact .result-side-stat {
  min-height: 92px;
}

.result-side-stat {
  padding: 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(226, 214, 203, 0.72);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.result-side-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.result-side-note {
  font-size: 11px;
  line-height: 1.5;
  color: var(--muted);
}

.results-strength-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.results-strength-column {
  min-width: 0;
}

.compact-list {
  margin-top: 4px;
}

.compact-list li + li {
  margin-top: 5px;
}

.trigger-inline-card {
  padding: 18px;
}

.result-watch-list {
  display: grid;
  gap: 10px;
}

.result-watch-card {
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(225, 214, 203, 0.72);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.result-watch-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.result-watch-value {
  font-size: 14px;
  color: var(--text);
}

.result-watch-note {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--muted);
}

.trigger-fallback {
  color: rgba(122, 93, 77, 0.7);
  list-style: none;
  margin-left: -18px;
}

.visualization-workspace {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  align-items: stretch;
}

.visualization-card {
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.visualization-card-primary {
  min-width: 0;
}

.visualization-card-secondary {
  min-width: 0;
}

.visualization-card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  flex-wrap: wrap;
}

.visualization-canvas-wrap {
  min-height: 760px;
  height: 760px;
  display: flex;
}

.visualization-canvas-wrap > * {
  min-height: 760px;
  height: 100%;
  width: 100%;
  flex: 1;
}

.visualization-canvas-wrap-swarm {
  align-items: stretch;
}

.visualization-support-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.visualization-support-card {
  padding: 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(225, 214, 203, 0.72);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.visualization-support-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.visualization-support-value {
  font-size: 14px;
  color: var(--text);
}

.visualization-support-note {
  font-size: 11px;
  line-height: 1.5;
  color: var(--muted);
}

.visualization-canvas-wrap-swarm .mode-results .swarm-board {
  min-height: 660px;
}

.visualization-canvas-wrap-swarm .swarm-shell {
  min-height: 760px;
}

.visualization-canvas-wrap-swarm .swarm-legend-overlay.results-overlay {
  left: 12px;
  right: 12px;
  bottom: 12px;
  width: auto;
  grid-template-columns: 1fr;
  gap: 8px;
}

.visualization-canvas-wrap-swarm .mode-results .legend-pills-cohorts {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px 7px;
}

.visualization-canvas-wrap-swarm .mode-results .legend-pills-status {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 7px;
}

.visualization-canvas-wrap-swarm .legend-section-compact {
  padding: 8px 9px;
}

.visualization-canvas-wrap-swarm .legend-title {
  margin-bottom: 6px;
  font-size: 9px;
}

.visualization-canvas-wrap-swarm .legend-pill {
  min-height: 34px;
  padding: 5px 8px;
  font-size: 10px;
  line-height: 1.35;
}

.interactive-workspace {
  display: grid;
  grid-template-columns: minmax(340px, 0.88fr) minmax(0, 1.22fr);
  gap: 16px;
  align-items: start;
}

.interactive-side-column,
.interactive-main-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.interactive-nav-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.interactive-nav-copy {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
}

.interactive-tool-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.interactive-nav-facts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.interactive-console-card {
  min-width: 0;
}

.interactive-support-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.interactive-chat-shell {
  min-height: 760px;
}

.interactive-console-copy {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
  margin-top: 6px;
}

.interactive-actions-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.interactive-helper-text {
  color: var(--muted);
  font-size: 11px;
}

.interactive-response-card {
  margin-top: 16px;
}

.interactive-response-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.thread-head {
  margin-bottom: 16px;
}

.thread-head-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.interactive-response-subtitle {
  font-size: 11px;
  color: var(--muted);
  margin-top: 3px;
}

.interactive-chat-thread {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.thread-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.thread-row-user {
  justify-content: flex-end;
}

.thread-row-ai {
  justify-content: flex-start;
}

.thread-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: rgba(255, 240, 226, 0.96);
  border: 1px solid rgba(239, 107, 74, 0.2);
  color: var(--accent);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.thread-avatar-ai {
  background: rgba(241, 247, 255, 0.96);
  border-color: rgba(47, 127, 232, 0.22);
  color: var(--blue);
}

.thread-bubble {
  max-width: min(680px, 100%);
  padding: 14px 16px;
  border-radius: 18px;
  border: 1px solid rgba(221, 210, 201, 0.8);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 14px 22px rgba(160, 106, 69, 0.06);
}

.thread-bubble-user {
  background: rgba(255, 245, 235, 0.96);
}

.thread-bubble-ai {
  background: rgba(248, 251, 255, 0.98);
}

.thread-meta {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 7px;
}

.thread-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 7px;
}

.thread-meta-row .thread-meta {
  margin-bottom: 0;
}

.thread-time {
  font-size: 10px;
  color: rgba(111, 92, 81, 0.72);
  letter-spacing: 0.04em;
  white-space: nowrap;
}

.thread-text {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text);
}

.thread-answer-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.interactive-reference-card {
  margin-top: 14px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 250, 244, 0.84);
  border: 1px solid rgba(230, 212, 198, 0.82);
}

.interactive-reference-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  flex-wrap: wrap;
}

.interactive-reference-subtitle {
  font-size: 11px;
  line-height: 1.65;
  color: var(--muted);
  margin-top: 4px;
}

.interactive-reference-chip {
  display: inline-flex;
  align-items: center;
  padding: 7px 11px;
  border-radius: 999px;
  background: rgba(255, 244, 237, 0.92);
  border: 1px solid rgba(47, 127, 232, 0.16);
  color: #46658d;
  font-size: 11px;
  white-space: nowrap;
}

.pinned-evidence-card {
  background: linear-gradient(180deg, rgba(255, 251, 246, 0.96), rgba(248, 250, 255, 0.92));
}

.interactive-support-list {
  margin-top: 8px;
}

.interactive-reference-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 8px;
}

.interactive-reference-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(226, 214, 203, 0.74);
}

.interactive-reference-pin {
  display: inline-flex;
  align-self: flex-start;
  padding: 5px 9px;
  border-radius: 999px;
  background: rgba(47, 127, 232, 0.08);
  border: 1px solid rgba(47, 127, 232, 0.14);
  color: var(--blue);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.interactive-reference-copy {
  font-size: 12px;
  color: var(--muted);
  line-height: 1.65;
}

.interactive-empty-state {
  min-height: 240px;
  border: 1px dashed rgba(209, 122, 62, 0.24);
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.56);
  color: var(--muted);
}

.interactive-empty-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}

.interactive-context-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.interactive-context-item {
  padding: 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(225, 214, 203, 0.72);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.interactive-context-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
}

.interactive-context-value {
  font-size: 14px;
  color: var(--text);
}

.interactive-context-note {
  font-size: 11px;
  line-height: 1.5;
  color: var(--muted);
}

.interactive-suggestion-list {
  display: grid;
  gap: 10px;
}

.interactive-suggestion-item {
  padding: 13px 14px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(225, 214, 203, 0.72);
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.interactive-suggestion-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text);
}

.interactive-suggestion-copy {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--muted);
}

/* ── Backtest ────────────────────────────────────────────────────────────── */
.backtest-panel { background: rgba(255, 250, 242, 0.96); border: 1px solid rgba(242,169,59,0.34); border-radius: var(--radius); padding: 18px 20px; margin-bottom: 16px; }
.backtest-title { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--amber); margin-bottom: 14px; }
.backtest-hint  { font-size: 12px; color: var(--muted); margin-bottom: 14px; line-height: 1.6; }

.brier-table { display: flex; flex-direction: column; gap: 10px; }
.brier-row   { display: flex; justify-content: space-between; font-size: 13px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.brier-row:last-child { border-bottom: none; padding-bottom: 0; }
.brier-key   { color: var(--muted); }
.brier-val   { font-weight: 500; }
.val-correct { color: var(--green); }
.val-wrong   { color: var(--red); }

.track-record-card {
  background: rgba(255, 252, 247, 0.94);
  border: 1px solid rgba(27, 154, 131, 0.18);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
}

.track-record-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.track-metric {
  background: rgba(243, 251, 249, 0.94);
  border: 1px solid rgba(27, 154, 131, 0.14);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
}

.track-metric-label {
  display: block;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-bottom: 6px;
}

.track-metric-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}

.track-record-table-wrap {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  overflow: auto;
}

.track-record-table {
  margin: 0;
  padding: 14px;
  font-size: 12px;
  line-height: 1.8;
  color: var(--muted);
  white-space: pre-wrap;
  word-break: break-word;
}

/* ── Report ──────────────────────────────────────────────────────────────── */
.report-section { margin-bottom: 16px; }
.report-body    { margin-top: 12px; }

.report-text { background: rgba(255, 252, 247, 0.92); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 16px; font-family: inherit; font-size: 12px; line-height: 1.8; color: var(--muted); white-space: pre-wrap; word-break: break-word; max-height: 480px; overflow-y: auto; }

/* ── Actions ─────────────────────────────────────────────────────────────── */
.actions-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
.actions-row.vertical { flex-direction: column; }

.studio-right-pane .chat-card,
.studio-right-pane .backtest-panel,
.studio-right-pane .actions-row {
  margin-bottom: 0;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.btn-primary {
  width: 100%; padding: 13px 20px; background: linear-gradient(135deg, #ef6b4a 0%, #f2a93b 100%); border: none;
  border-radius: var(--radius-sm); color: #fff; font-family: inherit;
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: opacity 0.15s, transform 0.1s;
  box-shadow: 0 12px 24px rgba(239, 107, 74, 0.22);
}

.btn-primary:hover:not(:disabled)  { opacity: 0.92; box-shadow: 0 16px 30px rgba(239, 107, 74, 0.3); }
.btn-primary:active:not(:disabled) { transform: scale(0.99); }
.btn-primary:disabled { opacity: 0.3; cursor: not-allowed; box-shadow: none; }

.btn-secondary {
  padding: 10px 18px; background: rgba(255, 255, 255, 0.72); border: 1px solid var(--border2);
  border-radius: var(--radius-sm); color: var(--text); font-family: inherit;
  font-size: 13px; cursor: pointer; transition: border-color 0.15s;
}

.btn-secondary:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.btn-secondary:disabled { opacity: 0.35; cursor: not-allowed; }
.btn-secondary.small { padding: 7px 11px; font-size: 11px; }

.btn-ghost {
  padding: 10px 18px; background: transparent; border: 1px solid var(--border);
  border-radius: var(--radius-sm); color: var(--muted); font-family: inherit;
  font-size: 13px; cursor: pointer; transition: color 0.15s, border-color 0.15s;
}

.btn-ghost:hover { color: var(--text); border-color: var(--border2); }
.btn-ghost.small { padding: 6px 10px; font-size: 11px; margin-bottom: 12px; }

/* ── Status pill ─────────────────────────────────────────────────────────── */
.status-pill { margin-top: 10px; padding: 8px 12px; border-radius: var(--radius-sm); font-size: 12px; border: 1px solid var(--border); background: rgba(255, 252, 247, 0.88); color: var(--muted); }
.pill-green  { border-color: rgba(45,212,160,0.4); color: var(--green); }
.pill-red    { border-color: rgba(217,79,79,0.4);  color: var(--red); }

/* ── Transitions ─────────────────────────────────────────────────────────── */
.slide-up-enter-active   { animation: slideUp 0.3s ease; }
@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

.panel-drop-enter-active { animation: panel-drop-in 0.2s ease; }
.panel-drop-leave-active { animation: panel-drop-in 0.15s ease reverse; }
@keyframes panel-drop-in { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: none; } }

.panel-fade-enter-active,
.panel-fade-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
}

.panel-fade-enter-from,
.panel-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* ── Misc ────────────────────────────────────────────────────────────────── */
code { background: rgba(255, 241, 227, 0.9); padding: 2px 6px; border-radius: 3px; font-family: inherit; font-size: 12px; color: var(--accent); }

@media (max-width: 720px) {
  .ops-screen,
  .studio-screen {
    width: calc(100vw - 20px);
  }

  .template-grid,
  .template-form,
  .config-row,
  .chat-form-grid,
  .results-shell,
  .results-dashboard,
  .visualization-workspace,
  .interactive-workspace,
  .market-confidence-row,
  .population-metric-grid,
  .population-lens-grid,
  .sector-impact-grid,
  .report-overview-main,
  .report-trend-grid,
  .ops-stage-grid,
  .ops-surface-layout,
  .ops-surface-footer,
  .ops-workbench,
  .studio-grid,
  .insight-duo,
  .report-studio-grid,
  .tool-card-grid,
  .track-record-grid,
  .watchlist-grid,
  .trigger-grid {
    grid-template-columns: 1fr;
  }

  .template-grid,
  .template-form,
  .config-row,
  .chat-form-grid,
  .results-shell,
  .results-dashboard,
  .visualization-workspace,
  .interactive-workspace,
  .population-metric-grid,
  .population-lens-grid,
  .report-overview-main,
  .report-overview-metrics,
  .report-trend-grid,
  .ops-surface-layout,
  .ops-workbench,
  .studio-grid,
  .insight-duo,
  .report-studio-grid,
  .tool-card-grid,
  .track-record-grid {
    display: flex;
    flex-direction: column;
  }

  .ops-hero,
  .studio-hero,
  .studio-pane-header,
  .report-studio-header,
  .chat-card-header,
  .market-intel-header,
  .population-card-header {
    flex-direction: column;
  }

  .workspace-tabs,
  .tool-card-grid {
    width: 100%;
  }

  .report-overview-chart {
    flex-direction: column;
    align-items: flex-start;
  }

  .report-chart-atlas-grid,
  .report-mini-atlas,
  .section-chart-atlas,
  .results-strength-grid,
  .result-side-actions,
  .result-side-stats,
  .visualization-support-grid,
  .interactive-context-grid,
  .interactive-reference-grid,
  .report-overview-metrics {
    grid-template-columns: 1fr;
  }

  .visualization-workspace {
    grid-template-columns: 1fr;
  }

  .results-rail {
    position: static;
  }

  .results-main-column,
  .results-side-column {
    width: 100%;
  }

  .result-focus-grid,
  .interactive-tool-grid {
    grid-template-columns: 1fr;
  }

  .ops-graph-frame,
  .running-empty-state {
    min-height: 520px;
  }

  .visualization-canvas-wrap,
  .visualization-canvas-wrap > * {
    min-height: 520px;
  }
}

/* ── Theme Refresh ─────────────────────────────────────────────────────── */
@keyframes grid-pulse {
  0%, 100% { background: transparent; }
  50%       { background: rgba(138, 116, 255, 0.05); }
}

.home-grid .grid-cell {
  border-color: rgba(145, 163, 226, 0.1);
}

.home-node {
  background: radial-gradient(circle, rgba(111, 215, 255, 0.18) 0%, rgba(138, 116, 255, 0.12) 48%, transparent 74%);
}

.home-topbar {
  border-bottom-color: rgba(145, 163, 226, 0.24);
  background: rgba(249, 251, 255, 0.9);
}

.home-brand,
.home-brand-mark,
.results-rail-title,
.badge-outcome,
.market-intel-title {
  color: #253252;
}

.home-section-title {
  color: transparent;
  background: linear-gradient(135deg, #24324f 0%, #5d8dff 24%, #7d7cff 54%, #ab8fff 78%, #66d6ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow: 0 16px 38px rgba(125, 124, 255, 0.1);
}

.title-brand {
  text-shadow: 0 18px 42px rgba(121, 117, 255, 0.12);
}

.home-eyebrow,
.home-section-kicker {
  color: #7d7cff;
  border-color: rgba(178, 144, 255, 0.24);
}

.home-marketing-link,
.home-counts,
.home-tagline,
.home-supporting-copy,
.home-section-copy,
.home-capabilities,
.home-tech,
.results-rail-copy,
.result-focus-copy,
.interactive-nav-copy,
.interactive-console-copy,
.thread-time {
  color: #6f7a98;
}

.home-topbar-demo,
.home-topbar-secondary,
.home-ghost-cta,
.home-social-pill {
  border-color: rgba(145, 163, 226, 0.22);
  background: rgba(255, 255, 255, 0.88);
  color: #5f6d94;
}

.home-topbar-actions {
  gap: 10px;
}

.home-topbar-primary,
.home-cta,
.btn-primary {
  background: linear-gradient(135deg, #69cbff 0%, #8a74ff 52%, #c194ff 100%);
  box-shadow: 0 18px 38px rgba(124, 116, 255, 0.22);
}

.home-cta:hover,
.btn-primary:hover:not(:disabled) {
  box-shadow: 0 22px 44px rgba(124, 116, 255, 0.28);
}

.hero-pill,
.hero-visual-chip,
.results-rail-chip,
.result-focus-chip,
.interactive-reference-chip,
.meta-chip,
.market-badge,
.chat-mode-tab,
.status-pill,
.thread-avatar,
.thread-bubble-user,
.interactive-reference-card,
.interactive-reference-item,
.report-donut-row-button:hover,
.report-donut-row-button.active {
  border-color: rgba(145, 163, 226, 0.2);
  background: rgba(255, 255, 255, 0.88);
  color: #5f6d94;
}

.hero-visual-ring {
  border-color: rgba(152, 172, 235, 0.48);
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.28), transparent 68%);
}

.hero-visual-ring.ring-one { border-color: rgba(105, 203, 255, 0.44); }
.hero-visual-ring.ring-two { border-color: rgba(138, 116, 255, 0.28); }
.hero-visual-ring.ring-three { border-color: rgba(178, 144, 255, 0.2); }

.hero-visual-core,
.home-feature-card,
.home-about-card,
.home-walkthrough-card,
.p4-panel,
.round-scrubber,
.round-world-state,
.agent-snapshot,
.event-card,
.file-badge,
.graph-result,
.estimate-card,
.outcome-card,
.prediction-summary,
.market-intel-card,
.sector-impact-card,
.watchlist-column,
.trigger-column,
.chat-card,
.chat-response-card,
.outcome-card,
.population-card,
.backtest-panel,
.track-record-card,
.report-text,
.results-rail,
.result-card-elevated,
.result-focus-card,
.result-side-card,
.visualization-card,
.interactive-nav-card,
.interactive-console-card,
.trigger-inline-card,
.thread-bubble,
.track-record-table-wrap {
  border-color: rgba(145, 163, 226, 0.22);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.94), rgba(243, 247, 255, 0.9));
  box-shadow: 0 22px 44px rgba(95, 112, 180, 0.1);
}

.hero-visual-core {
  box-shadow:
    0 24px 56px rgba(95, 112, 180, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.62);
}

.hero-visual-core-title,
.panel-head,
.panel-name,
.thread-text,
.result-focus-box strong,
.result-side-stat,
.market-confidence-value,
.population-lens-outcome,
.track-metric-value,
.stat-num {
  color: #253252;
}

.hero-visual-core-subtitle,
.hero-visual-chip,
.field-note,
.event-key,
.file-words,
.estimate-label,
.estimate-detail,
.outcome-header,
.outcome-label,
.sector-reasoning,
.watchlist-heading,
.trigger-heading,
.results-rail-kicker,
.results-rail-btn-copy,
.result-focus-label,
.result-side-label,
.interactive-helper-text,
.interactive-response-subtitle,
.interactive-reference-subtitle,
.interactive-reference-copy,
.track-metric-label,
.report-overview-copy {
  color: #6f7a98;
}

.title-swarm {
  background: linear-gradient(135deg, #63c8ff 0%, #8a74ff 46%, #c194ff 74%, #68ddd6 100%);
  -webkit-background-clip: text;
  background-clip: text;
}

.hstat-lbl,
.field-label,
.rd-label,
.results-rail-kicker,
.results-rail-chip,
.thread-meta,
.code,
code {
  color: #7d7cff;
}

.hstat-num,
.slider-val,
.stat-num,
.estimate-time,
.result-focus-chip,
.interactive-reference-pin {
  color: #8a74ff;
}

.field-slider {
  --slider-progress: 50%;
  -webkit-appearance: none;
  appearance: none;
  height: 14px;
  background: transparent;
}

.field-slider::-webkit-slider-runnable-track {
  height: 10px;
  border-radius: 999px;
  border: 1px solid rgba(145, 163, 226, 0.22);
  background:
    linear-gradient(90deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%) 0 / var(--slider-progress) 100% no-repeat,
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(241, 245, 255, 0.94));
  box-shadow: inset 0 1px 2px rgba(124, 138, 191, 0.12);
}

.field-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  margin-top: -5px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.96);
  background: linear-gradient(135deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%);
  box-shadow: 0 8px 18px rgba(124, 116, 255, 0.22);
}

.field-slider::-moz-range-track {
  height: 10px;
  border-radius: 999px;
  border: 1px solid rgba(145, 163, 226, 0.22);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(241, 245, 255, 0.94));
  box-shadow: inset 0 1px 2px rgba(124, 138, 191, 0.12);
}

.field-slider::-moz-range-progress {
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(90deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%);
}

.field-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.96);
  background: linear-gradient(135deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%);
  box-shadow: 0 8px 18px rgba(124, 116, 255, 0.22);
}

.progress-bar {
  height: 8px;
  border-radius: 999px;
  border: 1px solid rgba(145, 163, 226, 0.18);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(241, 245, 255, 0.92));
  box-shadow: inset 0 1px 2px rgba(124, 138, 191, 0.12);
}

.progress-fill {
  background: linear-gradient(90deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%);
  box-shadow: 0 0 14px rgba(124, 116, 255, 0.18);
}

.progress-fill.indeterminate {
  background:
    linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.22) 22%, rgba(255,255,255,0.08) 100%),
    linear-gradient(90deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%);
}

.progress-circle {
  background:
    radial-gradient(circle at center, rgba(255, 255, 255, 0.99) 0 54px, transparent 55px),
    conic-gradient(#69cbff 0%, #8a74ff calc(var(--progress, 50) * 0.72%), #c194ff calc(var(--progress, 50) * 1%), rgba(214, 223, 246, 0.92) 0);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.84), 0 18px 28px rgba(95, 112, 180, 0.1);
}

.progress-circle-inner,
.sunburst-chart-inner {
  background: rgba(255, 255, 255, 0.98);
  border-color: rgba(145, 163, 226, 0.2);
}

.report-insight-bar-track,
.report-mini-bar-track {
  background: rgba(215, 224, 246, 0.56);
}

.report-insight-bar-fill,
.report-mini-bar-fill {
  box-shadow: 0 0 10px rgba(124, 116, 255, 0.12);
}

.main-app {
  --workflow-box-bg: linear-gradient(160deg, rgba(255, 255, 255, 0.95), rgba(244, 241, 255, 0.9));
  --workflow-box-bg-soft: linear-gradient(160deg, rgba(255, 255, 255, 0.92), rgba(246, 249, 255, 0.88));
  --workflow-box-border: rgba(145, 163, 226, 0.22);
  --workflow-box-shadow: 0 20px 40px rgba(95, 112, 180, 0.1);
}

.main-app :is(
  [class*="-card"],
  [class*="-panel"],
  [class*="-pane"],
  .dropzone,
  .build-section,
  .file-badge,
  .graph-result,
  .round-scrubber,
  .round-world-state,
  .agent-snapshot,
  .results-rail,
  .studio-focus-panel,
  .visual-panel,
  .population-metric-box,
  .result-focus-box,
  .result-side-stat,
  .market-confidence-box,
  .population-cohort-row,
  .track-metric,
  .report-chart-note,
  .section-chart-note,
  .report-nav-item,
  .interactive-context-item,
  .interactive-suggestion-item,
  .meta-chip,
  .results-rail-chip,
  .market-badge,
  .status-pill
) {
  background: var(--workflow-box-bg);
  border-color: var(--workflow-box-border);
  box-shadow: var(--workflow-box-shadow);
}

.main-app :is(
  .report-chart-note,
  .section-chart-note,
  .visual-panel,
  .report-nav-item,
  .result-focus-box,
  .result-side-stat,
  .market-confidence-box,
  .population-metric-box,
  .population-cohort-row,
  .track-metric,
  .interactive-context-item,
  .interactive-suggestion-item,
  .meta-chip,
  .results-rail-chip,
  .market-badge,
  .status-pill
) {
  background: var(--workflow-box-bg-soft);
}

.hstat-sep,
.graph-divider,
.watchlist-item,
.conn-item,
.brier-row {
  background: rgba(145, 163, 226, 0.16);
  border-bottom-color: rgba(145, 163, 226, 0.16);
}

.walkthrough-number,
.social-icon,
.status-dot.green {
  background: rgba(138, 116, 255, 0.14);
  color: #7d7cff;
}

.app-bg {
  background-image:
    radial-gradient(circle, rgba(111, 215, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle, rgba(178, 144, 255, 0.08) 1px, transparent 1px);
}

.topbar,
.p4-toolbar {
  background: rgba(248, 250, 255, 0.84);
}

.p4-btn.active,
.mode-tab.active,
.results-rail-btn.active,
.chat-mode-tab.active {
  background: rgba(244, 241, 255, 0.96);
  border-color: rgba(138, 116, 255, 0.28);
  color: #8a74ff;
}

.dropzone {
  background: rgba(252, 253, 255, 0.72);
}

.dropzone:hover,
.drop-arrow,
.interactive-empty-state {
  border-color: rgba(138, 116, 255, 0.26);
  background: rgba(244, 241, 255, 0.62);
  color: #6f7a98;
}

.field-input:focus,
.field-textarea:focus,
.field-select:focus {
  box-shadow: 0 0 0 4px rgba(138, 116, 255, 0.12);
}

.btn-secondary,
.btn-ghost,
.results-rail-btn,
.result-side-stat,
.result-focus-box,
.interactive-context-item,
.interactive-suggestion-item,
.report-trend-card-button,
.thread-bubble,
.interactive-reference-item {
  border-color: rgba(145, 163, 226, 0.2);
  background: rgba(255, 255, 255, 0.84);
}

.btn-secondary:hover:not(:disabled),
.btn-ghost:hover {
  border-color: rgba(138, 116, 255, 0.3);
  color: #8a74ff;
}

.thread-avatar {
  border-color: rgba(138, 116, 255, 0.2);
  color: #8a74ff;
}

.thread-avatar-ai {
  background: rgba(241, 247, 255, 0.96);
  border-color: rgba(98, 187, 255, 0.22);
  color: #62bbff;
}

code {
  background: rgba(244, 241, 255, 0.86);
  color: #7d7cff;
}

.main-app {
  --workflow-pill-bg: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(243, 247, 255, 0.94));
  --workflow-pill-bg-strong: linear-gradient(160deg, rgba(245, 248, 255, 0.98), rgba(244, 241, 255, 0.94));
  --workflow-pill-border: rgba(145, 163, 226, 0.24);
  --workflow-pill-border-strong: rgba(138, 116, 255, 0.34);
  --workflow-pill-text: #5f6d94;
  --workflow-pill-title: #253252;
  --workflow-pill-accent: #7d7cff;
}

.main-app :is(
  .step,
  .p4-btn,
  .mode-tab,
  .meta-chip,
  .ops-signal-chip,
  .workspace-tab,
  .workspace-collapse-btn,
  .chat-mode-tab,
  .results-rail-chip,
  .market-badge,
  .result-focus-chip,
  .interactive-reference-chip,
  .template-chip,
  .merge-causal-badge
) {
  background: var(--workflow-pill-bg);
  border-color: var(--workflow-pill-border);
  color: var(--workflow-pill-text);
  box-shadow: 0 12px 24px rgba(95, 112, 180, 0.08);
}

.main-app :is(
  .step.active,
  .p4-btn.active,
  .mode-tab.active,
  .workspace-tab.active,
  .chat-mode-tab.active,
  .results-rail-btn.active
) {
  background: var(--workflow-pill-bg-strong);
  border-color: var(--workflow-pill-border-strong);
  color: var(--workflow-pill-title);
  box-shadow: 0 14px 28px rgba(95, 112, 180, 0.12);
}

.main-app :is(
  .step-num,
  .tab-icon,
  .mode-tab .tab-icon
) {
  background: rgba(138, 116, 255, 0.12);
  color: var(--workflow-pill-accent);
  border: 1px solid rgba(138, 116, 255, 0.16);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.82);
}

.main-app :is(
  .info-banner,
  .backtest-panel,
  .track-record-card,
  .report-text,
  .chat-response-card,
  .interactive-reference-card,
  .interactive-empty-state
) {
  background: var(--workflow-box-bg-soft);
  border-color: var(--workflow-box-border);
  box-shadow: var(--workflow-box-shadow);
}

.main-app :is(
  .ops-eyebrow,
  .ops-pane-label,
  .ops-highlight-label,
  .results-rail-kicker,
  .template-eyebrow,
  .config-context-label,
  .market-intel-eyebrow,
  .watchlist-heading,
  .trigger-heading,
  .population-section-title,
  .population-lens-title,
  .report-overview-label,
  .report-trend-title,
  .result-focus-label,
  .market-confidence-label,
  .track-metric-label,
  .backtest-title,
  .interactive-reference-pin
) {
  color: var(--workflow-pill-accent);
}

.main-app :is(
  .template-title,
  .config-context-value,
  .ops-pane-title,
  .results-rail-title,
  .market-intel-title,
  .result-focus-box strong,
  .result-side-stat strong,
  .track-metric-value,
  .market-confidence-value,
  .report-overview-value
) {
  color: var(--workflow-pill-title);
}

.main-app :is(
  .mode-desc,
  .info-banner,
  .config-context-detail,
  .ops-copy,
  .ops-highlight-copy,
  .ops-note-card,
  .report-overview-sub,
  .results-rail-copy,
  .interactive-reference-copy,
  .interactive-empty-state,
  .backtest-hint
) {
  color: #6e7a99;
}

.main-app :is(
  .p4-toolbar,
  .p4-panel-header
) {
  background: rgba(248, 250, 255, 0.9);
  border-bottom-color: var(--workflow-pill-border);
}
</style>
