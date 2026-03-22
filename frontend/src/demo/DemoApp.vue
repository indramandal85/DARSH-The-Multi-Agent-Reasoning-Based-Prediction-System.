<template>
  <div class="demo-app" :class="{ 'home-mode': currentScreen === 'home' }">
    <div class="demo-bg" aria-hidden="true"></div>

    <header class="demo-topbar" :class="{ 'home-nav-mode': currentScreen === 'home' }">
      <div class="demo-brand" role="button" tabindex="0" aria-label="Go to demo home" @click="currentScreen = 'home'" @keydown.enter="currentScreen = 'home'" @keydown.space.prevent="currentScreen = 'home'">
        <img class="brand-mark-img demo-brand-icon" src="/darsh-mark.svg" alt="DARSH logo" />
      </div>
      <template v-if="currentScreen === 'home'">
        <nav class="demo-marketing-nav">
          <button class="demo-marketing-link" @click="scrollHomeSection('demo-hero')">Get Started</button>
          <button class="demo-marketing-link" @click="scrollHomeSection('demo-introduction')">Introduction</button>
          <button class="demo-marketing-link" @click="scrollHomeSection('demo-about')">About Us</button>
        </nav>
        <div class="demo-home-topbar-actions">
          <button class="demo-topbar-secondary" @click="scrollHomeSection('demo-waitlist')">Join Wishlist</button>
          <button class="demo-topbar-primary" @click="goToInput">Try Live Demo</button>
        </div>
      </template>
      <template v-else>
        <nav class="demo-steps">
          <button
            v-for="(label, index) in demoSteps"
            :key="label"
            class="demo-step"
            :class="{ active: stepIndex === index, done: stepIndex > index }"
            :disabled="stepIndex < index"
            @click="jumpToStep(index)"
          >
            <span class="demo-step-num">{{ stepIndex > index ? '✓' : index + 1 }}</span>
            <span>{{ label }}</span>
          </button>
        </nav>
        <div class="demo-topbar-state">Preset walkthrough · zero API cost</div>
      </template>
    </header>

    <main class="demo-shell">
      <section v-if="currentScreen === 'home'" class="demo-home">
        <div class="demo-home-stage">
          <div class="demo-home-agent-rain" aria-hidden="true">
            <span
              v-for="index in 132"
              :key="`landing-bot-${index}`"
              class="landing-bot"
              :style="landingBotStyle(index)"
            ></span>
          </div>

          <section id="demo-hero" class="demo-hero-panel demo-home-panel reveal-on-scroll">
            <div class="demo-eyebrow reveal-on-scroll">Local-first multi-agent reasoning for reactions, narratives, institutions, and markets</div>
            <div class="demo-hero-strip reveal-on-scroll">
              <span class="hero-pill">Runs locally on your machine</span>
              <span class="hero-pill">Zero API cost</span>
              <span class="hero-pill">Belief scoring + Bayesian-style evidence updates</span>
              <span class="hero-pill">Graph memory, backtests, and explainable outputs</span>
            </div>
            <div class="demo-hero-visual reveal-on-scroll" aria-hidden="true">
              <div class="hero-visual-ring ring-one"></div>
              <div class="hero-visual-ring ring-two"></div>
              <div class="hero-visual-ring ring-three"></div>
              <div class="hero-visual-core">
                <img class="hero-visual-logo" src="/darsh-mark.svg" alt="DARSH neural mark" />
                <div class="hero-visual-core-title">DARSH</div>
                <div class="hero-visual-core-subtitle">Pre-Decision Behavioral Intelligence</div>
              </div>
              <span class="hero-visual-chip chip-a">Graph Memory</span>
              <span class="hero-visual-chip chip-b">Belief Motion</span>
              <span class="hero-visual-chip chip-c">Cohort Signals</span>
              <span class="hero-visual-chip chip-d">Calibrated Outcomes</span>
            </div>
            <h1 class="demo-home-title">Turn uncertainty into opportunity.</h1>
            <p class="demo-home-subtitle">
              DARSH transforms messy human context into structured, inspectable intelligence. It is locally runnable, can operate with zero API cost when paired with local models, and combines graph-native memory, asymmetric multi-agent reasoning, probabilistic belief motion, Bayesian-style evidence weighting, and calibration-aware reporting.
            </p>
            <p class="demo-home-supporting-copy">
              Built for analysts, operators, researchers, strategists, and builders who want to rehearse real-world reactions locally instead of guessing through them.
            </p>
            <div class="demo-hero-cta-row">
              <button class="demo-cta" @click="goToInput">Try Live Demo</button>
              <button class="demo-ghost-cta" @click="scrollHomeSection('demo-introduction')">See How It Works</button>
            </div>
            <div id="demo-waitlist" class="demo-waitlist-card">
              <div class="demo-waitlist-copy">
                <div class="waitlist-title">Join the launch circle</div>
                <p>Get notified when the full DARSH workbench opens with deeper simulations, cleaner calibration, richer visual intelligence surfaces, and production-grade local reasoning workflows.</p>
              </div>
              <div class="demo-waitlist-form">
                <input
                  v-model="waitlistEmail"
                  type="email"
                  class="demo-waitlist-input"
                  placeholder="Enter your email"
                />
                <button class="demo-waitlist-btn" @click="joinWaitlist">
                  {{ waitlistJoined ? 'Joined' : 'Notify Me' }}
                </button>
              </div>
            </div>

            <div class="demo-home-get-started reveal-on-scroll">
              <div class="card-kicker">Get Started</div>
              <h2 class="demo-home-section-title demo-home-section-title-compact">From raw context to an explainable forecast in five deliberate moves.</h2>
              <div class="demo-walkthrough-grid">
                <article class="demo-walkthrough-card reveal-on-scroll">
                  <span class="walkthrough-number">01</span>
                  <strong>Ingest the scenario</strong>
                  <p>Start from a document, report, event, or narrative signal and convert it into structured context.</p>
                </article>
                <article class="demo-walkthrough-card reveal-on-scroll">
                  <span class="walkthrough-number">02</span>
                  <strong>Build graph memory</strong>
                  <p>Extract entities, links, and shared cues so reasoning stays grounded in interpretable structure.</p>
                </article>
                <article class="demo-walkthrough-card reveal-on-scroll">
                  <span class="walkthrough-number">03</span>
                  <strong>Simulate heterogeneous actors</strong>
                  <p>Run agents with different mandates, speeds, memory, and influence across rounds and alternate worlds.</p>
                </article>
                <article class="demo-walkthrough-card reveal-on-scroll">
                  <span class="walkthrough-number">04</span>
                  <strong>Track belief motion</strong>
                  <p>Watch cautious, panic, optimistic, and divided conviction evolve with confidence and spillover.</p>
                </article>
                <article class="demo-walkthrough-card reveal-on-scroll">
                  <span class="walkthrough-number">05</span>
                  <strong>Review the workbench</strong>
                  <p>Land on a calibrated final read with visual explanations, market views, cohort reasoning, and backtest scoring.</p>
                </article>
              </div>
            </div>
          </section>

          <section id="demo-introduction" class="demo-home-panel demo-home-panel-intro reveal-on-scroll">
            <div class="demo-home-panel-shell">
              <div class="card-kicker">Introduction</div>
              <div class="demo-section-head centered reveal-on-scroll">
                <h2 class="demo-home-section-title">Turn raw context into structured foresight, not just another summary.</h2>
                <p class="demo-home-section-copy">
                  DARSH turns narrative input into a live reasoning environment that can run locally with zero API cost when driven by local models: extract entities, organize graph memory, simulate heterogeneous actors, trace belief movement, and resolve the situation into explainable probabilities, calibrated confidence, and action-ready readouts.
                </p>
                <p class="demo-home-section-copy compact">
                  It is built to show not just what might happen, but why conviction forms, where disagreement remains, which cohorts move the outcome, and where uncertainty is still worth respecting.
                </p>
              </div>

              <div class="demo-intro-pill-row reveal-on-scroll">
                <span class="demo-intro-pill">Runs locally</span>
                <span class="demo-intro-pill">Zero API cost</span>
                <span class="demo-intro-pill">Probabilistic beliefs</span>
                <span class="demo-intro-pill">Calibration-aware reporting</span>
              </div>

              <div class="demo-intro-grid">
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Graph-grounded memory</strong>
                  <span>Dense entity and relationship memory keeps every conclusion tied to visible structure instead of disappearing into prompt fog.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Asymmetric agent society</strong>
                  <span>Agents do not collapse into one voice. Mandates, reaction speeds, network influence, and memory produce real behavioural divergence.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Probabilistic reasoning</strong>
                  <span>Belief distributions, confidence scores, and Bayesian-style evidence weighting keep the forecast updateable, auditable, and more honest.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Explainable operating surface</strong>
                  <span>Knowledge graphs, swarm maps, confidence distributions, and cohort traces make the reasoning process visible instead of hidden behind one answer box.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Real-time decision flow</strong>
                  <span>Watch agents think, react, post, hesitate, and reposition in sequence so decision-making feels alive instead of synthetic.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Deep analysis outputs</strong>
                  <span>Final reports combine outcomes, drivers, dissent, market structure, and weighted population reads into one coherent review layer.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Evidence-backed interaction</strong>
                  <span>Interactive follow-ups stay grounded in the simulation, letting users question sectors, cohorts, and scenarios with traceable evidence.</span>
                </article>
                <article class="demo-highlight-card demo-intro-feature-card reveal-on-scroll">
                  <strong>Decision-grade calibration</strong>
                  <span>Backtests, confidence scoring, and structured review loops help transform impressive visuals into more trustworthy decision support.</span>
                </article>
              </div>
            </div>
          </section>

          <section id="demo-about" class="demo-home-panel demo-home-panel-about reveal-on-scroll">
            <div class="demo-home-panel-shell demo-home-panel-about-shell">
              <div class="card-kicker">About Us</div>
              <div class="demo-about-hero reveal-on-scroll">
                <h2 class="demo-home-section-title">Building explainable intelligence systems, not black boxes.</h2>
                <p class="demo-home-section-copy">
                  We believe the future of prediction is not a single mysterious answer. It is a transparent system that shows what it knows, how beliefs evolve, which actors disagree, and where uncertainty still deserves respect.
                </p>
                <p class="demo-home-section-copy compact">
                  DARSH exists to make high-trust local-first simulation feel rigorous, readable, and useful enough for real-world thinking, not just spectacular enough for a demo.
                </p>
                <p class="demo-home-section-copy compact">
                  Our aim is to help teams reason through complexity with more structure, more humility, and more clarity than a single-shot assistant can offer.
                </p>
              </div>

              <div class="demo-about-grid">
                <article class="demo-about-card reveal-on-scroll">
                  <h3>Our vision</h3>
                  <p>To make reaction intelligence as inspectable as analytics: a system where narratives, institutions, people, and networks can be simulated, challenged, and understood before decisions are made.</p>
                </article>
                <article class="demo-about-card reveal-on-scroll">
                  <h3>Why DARSH exists</h3>
                  <p>Because most prediction tools stop at answers. We care about the full path: graph memory, agent asymmetry, belief movement, calibration, and visually readable reasoning.</p>
                </article>
                <article class="demo-about-card reveal-on-scroll">
                  <h3>What makes it different</h3>
                  <p>It blends graph memory, multi-agent reasoning, probability distributions, calibration, and premium visual explanation into one coherent operating surface.</p>
                </article>
                <article class="demo-about-card reveal-on-scroll">
                  <h3>How we build</h3>
                  <ul class="demo-about-list">
                    <li>Locally runnable by design</li>
                    <li>Zero API cost when paired with local models</li>
                    <li>Graph-native memory instead of context fog</li>
                    <li>Probabilistic output instead of fake certainty</li>
                    <li>Professional visual explanation at every stage</li>
                  </ul>
                </article>
              </div>

              <div class="demo-about-foot reveal-on-scroll">
                <div class="demo-about-tags">
                  <span class="hero-pill">Local-first</span>
                  <span class="hero-pill">Explainable</span>
                  <span class="hero-pill">Graph-native</span>
                  <span class="hero-pill">Premium visualization</span>
                  <span class="hero-pill">Calibration aware</span>
                </div>
                <div class="demo-social-links">
                  <a class="demo-social-pill" href="https://www.linkedin.com/in/indra-mandal007" target="_blank" rel="noreferrer">
                    <span class="social-icon" aria-hidden="true">
                      <svg viewBox="0 0 24 24" role="presentation">
                        <path d="M6.94 8.5A1.56 1.56 0 1 1 6.93 5.4a1.56 1.56 0 0 1 0 3.1ZM5.62 10h2.63v8.4H5.62V10Zm4.28 0h2.52v1.15h.04c.35-.66 1.22-1.35 2.51-1.35 2.69 0 3.18 1.77 3.18 4.08v4.52h-2.63v-4c0-.95-.02-2.18-1.33-2.18-1.33 0-1.53 1.04-1.53 2.11v4.07H9.9V10Z"/>
                      </svg>
                    </span>
                    LinkedIn
                  </a>
                  <a class="demo-social-pill" href="https://github.com/indramandal85" target="_blank" rel="noreferrer">
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
      </section>

      <section v-else-if="currentScreen === 'input'" class="demo-stage">
        <div class="demo-stage-head">
          <div>
            <div class="demo-stage-kicker">Step 1 / 4</div>
            <h1 class="demo-stage-title">Build the knowledge graph</h1>
            <p class="demo-stage-subtitle">
              In the full platform you can upload a document, fetch live news, use a historical event,
              or start from a guided market template. In this demo, the graph is pre-scripted and ready to build.
            </p>
          </div>
        </div>

        <div class="demo-input-grid">
          <article class="demo-input-card">
            <div class="input-card-icon">↑</div>
            <div class="input-card-title">Upload Document</div>
            <p>TXT, MD, or PDF ingestion with safe normalization before graph extraction.</p>
            <span class="input-card-chip">Disabled in demo</span>
          </article>
          <article class="demo-input-card">
            <div class="input-card-icon">RSS</div>
            <div class="input-card-title">Live News</div>
            <p>Bring in current coverage to forecast near-term market behavior.</p>
            <span class="input-card-chip">Preset scenario only</span>
          </article>
          <article class="demo-input-card">
            <div class="input-card-icon">⏱</div>
            <div class="input-card-title">Historical Event</div>
            <p>Backtest the system against known events without leaking the answer.</p>
            <span class="input-card-chip">Demo scenario loaded</span>
          </article>
          <article class="demo-input-card">
            <div class="input-card-icon">◎</div>
            <div class="input-card-title">Market Template</div>
            <p>Generate a structured scenario from a guided market-event template.</p>
            <span class="input-card-chip">Observation only</span>
          </article>
        </div>

        <div class="demo-progress-card">
          <div class="demo-progress-head">
            <span>{{ buildInProgress ? buildStatusLabel : 'Preset dense graph ready for generation' }}</span>
            <strong>{{ buildInProgress ? `${Math.round(buildProgress * 100)}%` : 'Ready' }}</strong>
          </div>
          <div class="demo-progress-track">
            <div class="demo-progress-fill" :style="{ width: `${buildProgress * 100}%` }"></div>
          </div>
          <div class="demo-mini-steps">
            <span v-for="(label, index) in buildSteps" :key="label" class="demo-mini-step" :class="{ done: buildStepIndex > index, active: buildStepIndex === index && buildInProgress }">
              {{ label }}
            </span>
          </div>
        </div>

        <button class="demo-primary-btn" :disabled="buildInProgress" @click="startBuild">
          {{ buildInProgress ? 'Building knowledge graph...' : 'Build the Knowledge Graph' }}
        </button>
      </section>

      <section v-else-if="currentScreen === 'configure'" class="demo-stage">
        <div class="demo-stage-head">
          <div>
            <div class="demo-stage-kicker">Step 2 / 4</div>
            <h1 class="demo-stage-title">Review the preset simulation configuration</h1>
            <p class="demo-stage-subtitle">
              In the full platform you can tune branch count, round depth, and agent population.
              The demo locks these controls at a high-density preset to show the full visual system.
            </p>
          </div>
        </div>

        <div class="demo-config-grid">
          <div class="demo-config-card">
            <span class="demo-config-label">Scenario</span>
            <strong class="demo-config-value">{{ DEMO_SCENARIO.title }}</strong>
            <p>{{ DEMO_SCENARIO.subtitle }}</p>
          </div>
          <div class="demo-config-card">
            <span class="demo-config-label">Knowledge graph</span>
            <strong class="demo-config-value">{{ demoGraphStats.entities }} nodes · {{ demoGraphStats.relationships }} edges</strong>
            <p>Prebuilt dense graph memory for the walkthrough.</p>
          </div>
          <div class="demo-config-card">
            <span class="demo-config-label">Preset</span>
            <strong class="demo-config-value">max visibility mode</strong>
            <p>Agent, branch, and round controls are fixed for demo consistency.</p>
          </div>
        </div>

        <div class="demo-slider-grid">
          <div class="demo-slider-card">
            <div class="demo-slider-top">
              <span>Agents per branch</span>
              <strong>{{ DEMO_CONFIG_PRESET.numAgents }}</strong>
            </div>
            <div class="demo-slider">
              <div class="demo-slider-fill" style="width: 100%"></div>
            </div>
          </div>
          <div class="demo-slider-card">
            <div class="demo-slider-top">
              <span>Rounds</span>
              <strong>{{ DEMO_CONFIG_PRESET.numRounds }}</strong>
            </div>
            <div class="demo-slider">
              <div class="demo-slider-fill" style="width: 100%"></div>
            </div>
          </div>
          <div class="demo-slider-card">
            <div class="demo-slider-top">
              <span>Branches / worlds</span>
              <strong>{{ DEMO_CONFIG_PRESET.numBranches }}</strong>
            </div>
            <div class="demo-slider">
              <div class="demo-slider-fill" style="width: 100%"></div>
            </div>
          </div>
        </div>

        <button class="demo-primary-btn" @click="startSimulation">Run Simulation</button>
      </section>

      <section v-else-if="currentScreen === 'running'" class="demo-running">
        <div class="demo-stage-head running-head">
          <div>
            <div class="demo-stage-kicker">Step 3 / 4</div>
            <h1 class="demo-stage-title">Live operating run</h1>
            <p class="demo-stage-subtitle">
              This scripted walkthrough shows how the full product looks at high density while the system builds a read,
              propagates it through the swarm, and then writes the report.
            </p>
          </div>
          <div class="demo-run-badges">
            <span class="demo-badge">{{ DEMO_CONFIG_PRESET.numBranches }} branches</span>
            <span class="demo-badge">{{ DEMO_CONFIG_PRESET.numRounds }} rounds</span>
            <span class="demo-badge">{{ DEMO_GRAPH_DATA.node_count }} entities</span>
          </div>
        </div>

        <div class="demo-running-grid">
          <div class="demo-running-main">
            <div class="demo-running-graph">
              <GraphViewer
                :graph-name="DEMO_GRAPH_NAME"
                :graph-data="DEMO_GRAPH_DATA"
                :dense-mode="true"
                :canvas-height="520"
                dense-preset="mirofish"
                :node-scale="0.34"
                :edge-length-scale="0.48"
                :dense-compact-factor="0.76"
                :dense-zoom-multiplier="3.34"
                :dense-min-scale="2.02"
                :dense-max-scale="2.94"
                :dense-center-on-load="true"
                :show-edge-labels="true"
                :live-focus="currentLiveFocus"
              />
            </div>

            <div class="demo-running-swarm">
              <SwarmCanvas
                :population-model="DEMO_POPULATION"
                :config="demoRunningSwarmConfig"
                :running-step="currentRunningStep"
                mode="running"
                :active="currentScreen === 'running'"
                :live-focus="currentLiveFocus"
              />
            </div>
          </div>

          <aside class="demo-running-rail">
            <div class="demo-status-card">
              <div class="demo-status-label">Current backend stage</div>
              <div class="demo-status-title">{{ currentRunningTitle }}</div>
              <div class="demo-status-subtitle">{{ currentRunningStep }}</div>
              <div class="demo-progress-track large">
                <div class="demo-progress-fill" :style="{ width: `${runningProgress * 100}%` }"></div>
              </div>
              <div class="demo-status-meta">{{ runningPhaseLabel }}</div>
            </div>

            <div class="demo-rail-card">
              <div class="rail-card-title">Live signal stack</div>
              <div class="rail-chip-grid">
                <span class="rail-chip">{{ DEMO_SCENARIO.modeTag }}</span>
                <span class="rail-chip">{{ DEMO_CONFIG_PRESET.numAgents }} agents</span>
                <span class="rail-chip">{{ DEMO_CONFIG_PRESET.numRounds }} rounds</span>
                <span class="rail-chip">{{ DEMO_CONFIG_PRESET.numBranches }} branches</span>
              </div>
            </div>

            <div class="demo-rail-card">
              <div class="rail-card-title">Execution notes</div>
              <ul class="rail-note-list">
                <li v-for="note in runningNotes" :key="note">{{ note }}</li>
              </ul>
            </div>

            <div class="demo-rail-card demo-report-action-card">
              <div class="rail-card-title">Report handoff</div>
              <p class="demo-rail-copy">
                Explore the dense scripted run as long as you want. Trigger the report when you are ready to move into the final analyst workbench.
              </p>
              <button
                class="demo-primary-btn demo-inline-action"
                :disabled="reportRequested"
                @click="beginReportGeneration"
              >
                {{ reportRequested ? 'Generating report...' : 'Generate Report' }}
              </button>
            </div>

            <div class="demo-rail-card">
              <div class="rail-card-title">Report generation</div>
              <div class="demo-report-stage-note">
                {{ reportRequested ? `Step ${Math.min(reportStepIndex + 1, DEMO_REPORT_STEPS.length)}/${DEMO_REPORT_STEPS.length} is active.` : 'Waiting for your trigger.' }}
              </div>
              <div class="report-step-list">
                <div v-for="(step, index) in DEMO_REPORT_STEPS" :key="step" class="report-step-row" :class="{ done: reportStepIndex > index, active: reportStepIndex === index && isReportPhase }">
                  <span class="report-step-index">{{ String(index + 1).padStart(2, '0') }}</span>
                  <span>{{ step }}</span>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </section>

      <section v-else class="demo-final">
        <aside class="demo-final-rail">
          <div class="demo-rail-head">
            <div class="demo-stage-kicker">Final Workbench</div>
            <h2>Outcome Review</h2>
            <p>Move between the result dashboard, the visual inspection workspace, and the preview console.</p>
          </div>

          <button class="demo-nav-card" :class="{ active: finalSection === 'results' }" @click="finalSection = 'results'">
            <strong>Results</strong>
            <span>Forecast, report, and backtest review</span>
          </button>
          <button class="demo-nav-card" :class="{ active: finalSection === 'visualization' }" @click="finalSection = 'visualization'">
            <strong>Visualization</strong>
            <span>Knowledge graph and agent swarm workspace</span>
          </button>
          <button class="demo-nav-card" :class="{ active: finalSection === 'tools' }" @click="finalSection = 'tools'">
            <strong>Interactive Tools</strong>
            <span>Read-only preview of the report console</span>
          </button>

          <button class="demo-secondary-btn" @click="resetDemo">Start the Demo Again</button>
        </aside>

        <div class="demo-final-main">
          <div class="demo-stage-head final-head">
            <div>
              <div class="demo-stage-kicker">Step 4 / 4</div>
              <h1 class="demo-stage-title">{{ DEMO_SCENARIO.title }}</h1>
              <p class="demo-stage-subtitle">
                Across {{ DEMO_CONFIG_PRESET.numBranches }} scripted worlds, the model resolves to a cautious lead with meaningful panic and divided tails still visible.
              </p>
            </div>
          </div>

          <div v-if="finalSection === 'results'" class="demo-results-grid">
            <section class="demo-card outcome-card">
              <div class="card-head">
                <div>
                  <div class="card-kicker">Outcome probability distribution</div>
                  <div class="card-title">Forecast snapshot</div>
                </div>
                <div class="donut-wrap">
                  <div class="donut-chart" :style="{ background: outcomeConic }"></div>
                </div>
              </div>
              <div class="outcome-bars">
                <div v-for="row in outcomeRows" :key="row.key" class="outcome-row">
                  <span>{{ row.label }}</span>
                  <div class="outcome-track">
                    <div class="outcome-fill" :style="{ width: `${row.percent}%`, background: row.color }"></div>
                  </div>
                  <strong>{{ row.percent }}%</strong>
                </div>
              </div>
              <div class="forecast-support-grid">
                <article v-for="item in forecastSupportCards" :key="item.label" class="forecast-support-card">
                  <span>{{ item.label }}</span>
                  <strong>{{ item.value }}</strong>
                  <p>{{ item.note }}</p>
                </article>
              </div>
            </section>

            <section class="demo-card summary-card">
              <div class="card-head">
                <div>
                  <div class="card-kicker">Decision snapshot</div>
                  <div class="card-title">Market readout</div>
                </div>
              </div>
              <div class="summary-metric-grid">
                <div class="summary-metric">
                  <span>Regime</span>
                  <strong>{{ formatLabel(DEMO_SCENARIO.market.regime) }}</strong>
                </div>
                <div class="summary-metric">
                  <span>Volatility</span>
                  <strong>{{ formatLabel(DEMO_SCENARIO.market.volatility) }}</strong>
                </div>
                <div class="summary-metric">
                  <span>Discovery</span>
                  <strong>{{ DEMO_SCENARIO.market.discoveryWindow }}</strong>
                </div>
                <div class="summary-metric">
                  <span>Brier</span>
                  <strong>{{ DEMO_SCENARIO.historicalBacktest.brier }}</strong>
                </div>
              </div>
              <div class="summary-callout">
                <div class="summary-callout-title">Why the read holds</div>
                <p>Domestic benchmark capital slows the downside, while foreign desks and media-linked channels keep caution elevated instead of allowing a clean risk-on reversal.</p>
              </div>
            </section>

            <section class="demo-card analysis-card">
              <div class="card-head">
                <div>
                  <div class="card-kicker">Analysis studio</div>
                  <div class="card-title">Report, market, and population views</div>
                </div>
                <div class="analysis-head-actions">
                  <div class="analysis-tabs">
                    <button v-for="tab in analysisTabs" :key="tab" class="analysis-tab" :class="{ active: analysisTab === tab }" @click="analysisTab = tab">
                      {{ formatLabel(tab) }}
                    </button>
                  </div>
                  <div class="analysis-download-actions">
                    <button class="analysis-download-btn" @click="downloadDemoReportMarkdown">Download Report (.md)</button>
                    <button class="analysis-download-btn secondary" @click="downloadDemoReportPdf">Download Report (.pdf)</button>
                  </div>
                </div>
              </div>

              <div v-if="analysisTab === 'report'" class="analysis-view">
                <div class="analysis-chart-card">
                  <div class="mini-chart-title">Forecast weight</div>
                  <div class="mini-donut" :style="{ background: outcomeConic }"></div>
                  <div class="mini-donut-legend">
                    <div v-for="row in reportLegendRows" :key="row.key" class="mini-legend-row">
                      <span class="mini-legend-swatch" :style="{ background: row.color }"></span>
                      <div class="mini-legend-copy">
                        <span>{{ row.label }}</span>
                        <small>{{ row.note }}</small>
                      </div>
                      <strong>{{ row.percent }}%</strong>
                    </div>
                  </div>
                  <div class="analysis-foot-note">Branch-weighted outcome split across the scripted demo worlds.</div>
                </div>
                <div class="analysis-copy-card">
                  <h3>Executive read</h3>
                  <p>The demo leans cautious because slower benchmark-aware capital remains measured even while fast media and foreign-flow channels keep downside vigilance elevated.</p>
                  <ul>
                    <li>Domestic flows prevent the scenario from collapsing into pure panic.</li>
                    <li>Foreign and media-linked channels keep the panic and divided tails alive.</li>
                    <li>The closing regime is uncertainty-hold, not risk-on recovery.</li>
                  </ul>
                </div>
              </div>

              <div v-else-if="analysisTab === 'market'" class="analysis-view">
                <div class="analysis-chart-card wide">
                  <div class="mini-chart-title">Sector balance</div>
                  <div class="sector-bars">
                    <div v-for="sector in DEMO_SCENARIO.market.sectors" :key="sector.id" class="sector-row">
                      <span>{{ sector.label }}</span>
                      <div class="sector-track">
                        <div class="sector-fill" :style="{ width: `${Math.round(sector.score * 100)}%` }"></div>
                      </div>
                      <strong>{{ Math.round(sector.score * 100) }}</strong>
                    </div>
                  </div>
                </div>
                <div class="analysis-copy-card">
                  <h3>Market intelligence</h3>
                  <p><strong>Regime:</strong> {{ DEMO_SCENARIO.market.regime }} · <strong>Volatility:</strong> {{ DEMO_SCENARIO.market.volatility }}</p>
                  <ul>
                    <li v-for="sector in DEMO_SCENARIO.market.sectors.slice(0, 3)" :key="sector.id">{{ sector.note }}</li>
                  </ul>
                </div>
              </div>

              <div v-else class="analysis-view">
                <div class="analysis-chart-card">
                  <div class="mini-chart-title">Population weighting</div>
                  <div class="sunburst-sim">
                    <div v-for="(slice, index) in populationSlices" :key="slice.label" class="sunburst-ring" :style="populationSliceStyle(slice, index)"></div>
                    <div class="sunburst-core">Population</div>
                  </div>
                  <div class="population-legend">
                    <div v-for="row in populationLegendRows" :key="row.label" class="population-legend-row">
                      <span class="population-ring-swatch" :style="{ borderColor: row.color }"></span>
                      <div class="population-legend-copy">
                        <span>{{ row.label }}</span>
                        <small>{{ row.population }} represented · {{ row.confidence }}% confidence · {{ row.velocity }}% velocity</small>
                      </div>
                      <strong>{{ row.percent }}%</strong>
                    </div>
                  </div>
                  <div class="analysis-foot-note">Weighted by represented population and cohort influence velocity, not just raw agent count.</div>
                </div>
                <div class="analysis-copy-card">
                  <h3>Population model</h3>
                  <p>The weighted population view remains cautious because domestic benchmark capital stays measured, while retail and media-linked cohorts keep the path noisy and fast.</p>
                  <ul>
                    <li v-for="slice in populationSlices.slice(0, 3)" :key="slice.label">{{ slice.label }} anchors {{ slice.percent }}% of the weighted read.</li>
                  </ul>
                </div>
              </div>
            </section>

            <section class="demo-card backtest-card">
              <div class="card-kicker">Historical backtest scoring</div>
              <div class="score-grid">
                <div class="score-item">
                  <span>Predicted</span>
                  <strong>{{ formatLabel(DEMO_SCENARIO.historicalBacktest.predicted) }}</strong>
                </div>
                <div class="score-item">
                  <span>Actual</span>
                  <strong>{{ formatLabel(DEMO_SCENARIO.historicalBacktest.actual) }}</strong>
                </div>
                <div class="score-item">
                  <span>Brier score</span>
                  <strong>{{ DEMO_SCENARIO.historicalBacktest.brier }}</strong>
                </div>
              </div>
            </section>

            <section class="demo-card strengths-card">
              <div class="card-kicker">Strengths and weaknesses</div>
              <div class="strength-grid">
                <div>
                  <h3>Strengthens</h3>
                  <ul>
                    <li v-for="item in DEMO_SCENARIO.market.triggers.strengthens" :key="item">{{ item }}</li>
                  </ul>
                </div>
                <div>
                  <h3>Weakens</h3>
                  <ul>
                    <li v-for="item in DEMO_SCENARIO.market.triggers.weakens" :key="item">{{ item }}</li>
                  </ul>
                </div>
              </div>
            </section>
          </div>

          <div v-else-if="finalSection === 'visualization'" class="demo-visual-grid">
            <section class="demo-card visual-card">
              <div class="card-head">
                <div>
                  <div class="card-kicker">Visualization</div>
                  <div class="card-title">Knowledge Graph Explorer</div>
                </div>
                <div class="visual-meta">{{ DEMO_GRAPH_DATA.node_count }} nodes · {{ DEMO_GRAPH_DATA.link_count }} links</div>
              </div>
              <div class="visual-graph-shell">
                <GraphViewer
                  :graph-name="DEMO_GRAPH_NAME"
                  :graph-data="DEMO_GRAPH_DATA"
                  :dense-mode="true"
                  :canvas-height="720"
                  dense-preset="mirofish"
                  :node-scale="0.32"
                  :edge-length-scale="0.5"
                  :dense-compact-factor="0.74"
                  :dense-zoom-multiplier="3.26"
                  :dense-min-scale="1.94"
                  :dense-max-scale="2.82"
                  :dense-center-on-load="true"
                  :show-edge-labels="true"
                />
              </div>
            </section>

            <section class="demo-card visual-card">
              <div class="card-head">
                <div>
                  <div class="card-kicker">Visualization</div>
                  <div class="card-title">Population-Weighted Cohort Field</div>
                </div>
                <div class="visual-meta">{{ DEMO_POPULATION.cohort_breakdown.length }} cohorts</div>
              </div>
              <div class="visual-swarm-shell">
                <SwarmCanvas
                  :population-model="DEMO_POPULATION"
                  :config="demoResultsSwarmConfig"
                  mode="results"
                  :active="true"
                />
              </div>
            </section>
          </div>

          <div v-else class="demo-tools-grid">
            <section class="demo-card tools-card">
              <div class="card-head">
                <div>
                  <div class="card-kicker">Interactive tools</div>
                  <div class="card-title">Report-agent console preview</div>
                </div>
                <div class="preview-lock">Preview only</div>
              </div>

              <div class="thread-list">
                <article v-for="(thread, index) in DEMO_SCENARIO.toolPreview" :key="thread.tool" class="thread-card">
                  <div class="thread-head">
                    <span class="thread-tool">{{ thread.tool }}</span>
                    <span class="thread-time">12:0{{ index + 3 }}:4{{ index }}</span>
                  </div>
                  <div class="thread-bubble user">
                    <div class="thread-role">Analyst</div>
                    <p>{{ thread.question }}</p>
                  </div>
                  <div class="thread-bubble assistant">
                    <div class="thread-role">Report Agent</div>
                    <p>{{ thread.answer }}</p>
                    <div class="pinned-evidence">
                      <div class="pinned-evidence-title">Pinned evidence</div>
                      <div v-for="item in thread.evidence" :key="item" class="evidence-pill">{{ item }}</div>
                    </div>
                  </div>
                </article>
              </div>

              <div class="thread-input-disabled">
                <span>Interactive Q&A is locked in the demo. Open the full platform to ask follow-up questions.</span>
              </div>
            </section>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import GraphViewer from '../GraphViewer.vue'
import SwarmCanvas from '../SwarmCanvas.vue'
import {
  DEMO_CONFIG_PRESET,
  DEMO_GRAPH_DATA,
  DEMO_GRAPH_NAME,
  DEMO_POPULATION,
  DEMO_REPORT_MARKDOWN,
  DEMO_REPORT_STEPS,
  DEMO_RUNNING_SCRIPT,
  DEMO_SCENARIO,
} from './demo-data'

const demoSteps = ['Welcome', 'Build Graph', 'Configure', 'Run', 'Results']
const currentScreen = ref('home')
const buildInProgress = ref(false)
const buildProgress = ref(0)
const buildStepIndex = ref(0)
const analysisTab = ref('report')
const finalSection = ref('results')
const runningElapsed = ref(0)
const reportRequested = ref(false)
const reportElapsed = ref(0)
const waitlistEmail = ref('')
const waitlistJoined = ref(false)

let buildTimer = null
let runTimer = null
let revealObserver = null

const SIMULATION_LOOP_MS = 21000
const REPORT_DURATION_MS = 10000
const outcomePalette = {
  cautious: '#7fcfff',
  panic: '#f07cc6',
  divided: '#b290ff',
  optimistic: '#68ddd6',
}
const outcomeLegendNotes = {
  cautious: 'Domestic benchmark capital stays measured and slows a full risk-off break.',
  panic: 'Offshore stress and fast headline channels keep the downside tail alive.',
  divided: 'Disagreement persists across fast-money, media, and options-linked cohorts.',
  optimistic: 'A relief path exists, but it needs stronger absorption from benchmark buyers.',
}
const populationPalette = ['#7fcfff', '#5c96ff', '#68ddd6', '#b290ff', '#f07cc6']

const buildSteps = [
  'Extracting entities',
  'Linking relations',
  'Compressing memory',
  'Preparing dense layout',
]

const stepIndex = computed(() => {
  if (currentScreen.value === 'home') return 0
  if (currentScreen.value === 'input') return 1
  if (currentScreen.value === 'configure') return 2
  if (currentScreen.value === 'running') return 3
  return 4
})

const buildStatusLabel = computed(() => buildSteps[Math.min(buildStepIndex.value, buildSteps.length - 1)] || 'Preparing')

const runningPhase = computed(() => (reportRequested.value ? 'report' : 'simulation'))
const runningProgress = computed(() => (
  reportRequested.value
    ? Math.min(reportElapsed.value / REPORT_DURATION_MS, 1)
    : ((runningElapsed.value % SIMULATION_LOOP_MS) / SIMULATION_LOOP_MS)
))
const isReportPhase = computed(() => runningPhase.value === 'report')
const reportStepIndex = computed(() => {
  if (!isReportPhase.value) return -1
  return Math.min(
    DEMO_REPORT_STEPS.length,
    Math.floor((reportElapsed.value / REPORT_DURATION_MS) * DEMO_REPORT_STEPS.length)
  )
})

const currentMoment = computed(() => {
  if (isReportPhase.value) return null
  const time = runningElapsed.value % SIMULATION_LOOP_MS
  return [...DEMO_RUNNING_SCRIPT]
    .reverse()
    .find(moment => time >= moment.at) || DEMO_RUNNING_SCRIPT[0]
})

const currentRunningTitle = computed(() => {
  if (isReportPhase.value) return `Generating report ${Math.min(reportStepIndex.value + 1, DEMO_REPORT_STEPS.length)}/${DEMO_REPORT_STEPS.length}`
  return currentMoment.value?.title || 'Scripted simulation active'
})

const currentRunningStep = computed(() => {
  if (isReportPhase.value) {
    const step = DEMO_REPORT_STEPS[Math.min(reportStepIndex.value, DEMO_REPORT_STEPS.length - 1)] || 'Finalizing report'
    return `${step}...`
  }
  return currentMoment.value?.step || 'Simulation is initializing...'
})

const runningPhaseLabel = computed(() => (
  isReportPhase.value
    ? 'Report writing window · scripted completion'
    : 'Live simulation window · explore freely, then trigger report generation'
))

const currentLiveFocus = computed(() => {
  if (isReportPhase.value) {
    return {
      market_role: 'FINANCIAL_MEDIA_EDITOR',
      focus_terms: ['Financial Media', 'Risk Narrative', 'Sentiment Loop'],
    }
  }
  return {
    market_role: currentMoment.value?.market_role || 'RETAIL_TRADER',
    focus_terms: currentMoment.value?.focus_terms || [],
  }
})

const demoRunningSwarmConfig = computed(() => ({
  ...DEMO_CONFIG_PRESET,
  swarmDefaultZoom: 2.38,
  swarmZoomMultiplier: 1.66,
  swarmMinZoom: 2.22,
  swarmMaxZoom: 2.96,
  swarmCenterOnLoad: true,
}))

const demoResultsSwarmConfig = computed(() => ({
  ...DEMO_CONFIG_PRESET,
  swarmBoardWidth: 920,
  swarmBoardHeight: 660,
  swarmCenterOnLoad: true,
}))

const runningNotes = computed(() => {
  if (isReportPhase.value) {
    return [
      'Simulation branches closed and aggregated.',
      `Report section ${Math.min(reportStepIndex.value + 1, DEMO_REPORT_STEPS.length)}/${DEMO_REPORT_STEPS.length} is being written.`,
      'Knowledge graph grounding remains visible while the final read is composed.',
      'Outcome calibration stays cautious with panic and divided tails still active.',
    ]
  }
  return [
    'Branch mesh prepared for 8 dense scenario paths.',
    'Preset graph memory is feeding entity-level cues into the swarm.',
    currentMoment.value?.step || 'Live swarm is processing the scenario...',
    `Current stage: ${currentMoment.value?.stage || 'Opening headline shock'}.`,
  ]
})

const outcomeRows = computed(() => {
  return Object.entries(DEMO_SCENARIO.outcomeProbs).map(([key, value]) => ({
    key,
    label: formatLabel(key),
    percent: Math.round(value * 100),
    color: outcomePalette[key],
  }))
})

const outcomeConic = computed(() => {
  let cursor = 0
  const segments = outcomeRows.value.map(row => {
    const start = cursor
    cursor += row.percent
    return `${outcomePalette[row.key]} ${start}% ${cursor}%`
  })
  return `conic-gradient(${segments.join(', ')})`
})

const forecastSupportCards = computed(() => {
  const ranked = [...outcomeRows.value].sort((a, b) => b.percent - a.percent)
  const lead = ranked[0] || { label: 'Lead', percent: 0 }
  const runnerUp = ranked[1] || { label: 'Secondary', percent: 0 }
  const topTwo = ranked.slice(0, 2).reduce((sum, row) => sum + row.percent, 0)
  const residual = Math.max(0, 100 - topTwo)

  return [
    {
      label: 'Lead path',
      value: `${lead.label} ${lead.percent}%`,
      note: 'Domestic funds and treasury desks keep this as the weighted base case.',
    },
    {
      label: 'Stress tail',
      value: `${runnerUp.label} ${runnerUp.percent}%`,
      note: 'Fast narrative and offshore channels stop the outlook from becoming cleanly constructive.',
    },
    {
      label: 'Top-two share',
      value: `${topTwo}%`,
      note: 'Most branch-weight sits inside the two most plausible endings rather than scattering evenly.',
    },
    {
      label: 'Residual dispersion',
      value: `${residual}%`,
      note: 'Relief and disagreement remain visible, but they are not driving the close.',
    },
  ]
})

const reportLegendRows = computed(() => {
  return outcomeRows.value.map(row => ({
    ...row,
    note: outcomeLegendNotes[row.key] || 'Weighted scenario share across the scripted run.',
  }))
})

const analysisTabs = ['report', 'market', 'population']

const demoGraphStats = computed(() => ({
  entities: DEMO_GRAPH_DATA.node_count,
  relationships: DEMO_GRAPH_DATA.link_count,
}))

const populationSlices = computed(() => {
  const total = DEMO_POPULATION.cohort_breakdown.reduce((sum, cohort) => sum + cohort.represented_population, 0)
  return DEMO_POPULATION.cohort_breakdown
    .slice(0, 5)
    .map((cohort, index) => ({
      label: cohort.label,
      percent: Math.round((cohort.represented_population / total) * 100),
      color: populationPalette[index],
    }))
})

const populationLegendRows = computed(() => {
  const total = DEMO_POPULATION.cohort_breakdown.reduce((sum, cohort) => sum + cohort.represented_population, 0)
  return DEMO_POPULATION.cohort_breakdown
    .slice(0, 5)
    .map((cohort, index) => ({
      label: cohort.label,
      percent: Math.round((cohort.represented_population / total) * 100),
      color: populationPalette[index],
      population: formatPopulationCount(cohort.represented_population),
      confidence: Math.round(cohort.avg_decision_confidence * 100),
      velocity: Math.round(cohort.velocity_influence * 100),
    }))
})

function populationSliceStyle(slice, index) {
  return {
    width: `${160 - index * 24}px`,
    height: `${160 - index * 24}px`,
    borderColor: slice.color,
    opacity: `${0.9 - index * 0.1}`,
  }
}

function goToInput() {
  stopTimers()
  currentScreen.value = 'input'
}

function scrollHomeSection(id) {
  if (typeof document === 'undefined') return
  const target = document.getElementById(id)
  if (!target) return
  target.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function joinWaitlist() {
  const email = waitlistEmail.value.trim()
  if (!email || !email.includes('@')) return
  waitlistJoined.value = true
  if (typeof window !== 'undefined') {
    const subject = encodeURIComponent('DARSH Waitlist Request')
    const body = encodeURIComponent(`Please add me to the DARSH waitlist.\n\nEmail: ${email}\n\nInterest: Demo + launch updates`)
    window.location.href = `mailto:?subject=${subject}&body=${body}`
  }
}

function jumpToStep(index) {
  if (index === 0) {
    resetDemo()
  } else if (index === 1) {
    goToInput()
  } else if (index === 2) {
    currentScreen.value = 'configure'
  } else if (index === 3) {
    startSimulation()
  } else if (index === 4) {
    currentScreen.value = 'final'
  }
}

function startBuild() {
  stopTimers()
  buildInProgress.value = true
  buildProgress.value = 0
  buildStepIndex.value = 0
  const start = Date.now()

  buildTimer = setInterval(() => {
    const elapsed = Date.now() - start
    buildProgress.value = Math.min(elapsed / 5000, 1)
    buildStepIndex.value = Math.min(
      buildSteps.length - 1,
      Math.floor(buildProgress.value * buildSteps.length)
    )

    if (elapsed >= 5000) {
      clearInterval(buildTimer)
      buildTimer = null
      buildInProgress.value = false
      currentScreen.value = 'configure'
    }
  }, 120)
}

function startSimulation() {
  stopTimers()
  currentScreen.value = 'running'
  runningElapsed.value = 0
  reportElapsed.value = 0
  reportRequested.value = false
  finalSection.value = 'results'
  analysisTab.value = 'report'

  runTimer = setInterval(() => {
    if (reportRequested.value) {
      reportElapsed.value = Math.min(reportElapsed.value + 220, REPORT_DURATION_MS)
      if (reportElapsed.value >= REPORT_DURATION_MS) {
        clearInterval(runTimer)
        runTimer = null
        currentScreen.value = 'final'
      }
      return
    }
    runningElapsed.value += 220
  }, 220)
}

function beginReportGeneration() {
  if (reportRequested.value) return
  reportRequested.value = true
  reportElapsed.value = 0
}

function stopTimers() {
  if (buildTimer) {
    clearInterval(buildTimer)
    buildTimer = null
  }
  if (runTimer) {
    clearInterval(runTimer)
    runTimer = null
  }
}

function resetDemo() {
  stopTimers()
  currentScreen.value = 'home'
  buildInProgress.value = false
  buildProgress.value = 0
  buildStepIndex.value = 0
  runningElapsed.value = 0
  reportElapsed.value = 0
  reportRequested.value = false
  finalSection.value = 'results'
  analysisTab.value = 'report'
}

function formatLabel(value) {
  return String(value || '')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, char => char.toUpperCase())
}

function formatPopulationCount(value) {
  if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(1)}B`
  if (value >= 10_000_000) return `${Math.round(value / 1_000_000)}M`
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`
  if (value >= 1000) return `${Math.round(value / 1000)}K`
  return String(value)
}

function downloadDemoReportMarkdown() {
  downloadBlob(
    new Blob([DEMO_REPORT_MARKDOWN], { type: 'text/markdown;charset=utf-8' }),
    `${demoReportFilenameBase()}.md`
  )
}

function downloadDemoReportPdf() {
  const pdfBlob = buildDemoReportPdf(DEMO_REPORT_MARKDOWN)
  downloadBlob(pdfBlob, `${demoReportFilenameBase()}.pdf`)
}

function demoReportFilenameBase() {
  return (DEMO_SCENARIO.title || 'darsh-demo-report')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  window.setTimeout(() => URL.revokeObjectURL(url), 0)
}

function buildDemoReportPdf(markdown) {
  const pageWidth = 612
  const pageHeight = 792
  const marginLeft = 54
  const marginTop = 62
  const marginBottom = 58
  const lineHeight = 16
  const titleLineHeight = 22
  const maxChars = 82
  const maxLinesPerPage = Math.floor((pageHeight - marginTop - marginBottom) / lineHeight)
  const regularFontObject = 3
  const boldFontObject = 4

  const tokens = markdownToPdfTokens(markdown, maxChars)
  const pages = []
  let currentPage = []
  let currentLineCount = 0

  tokens.forEach((token) => {
    const tokenLineCost = token.size === 18 ? Math.max(1, Math.ceil(titleLineHeight / lineHeight)) : 1
    if (currentLineCount + tokenLineCost > maxLinesPerPage && currentPage.length) {
      pages.push(currentPage)
      currentPage = []
      currentLineCount = 0
    }
    currentPage.push(token)
    currentLineCount += tokenLineCost
  })

  if (currentPage.length) {
    pages.push(currentPage)
  }

  const objects = []
  const pageObjectNumbers = []
  const contentObjectNumbers = []
  let nextObjectNumber = 5

  pages.forEach((page) => {
    pageObjectNumbers.push(nextObjectNumber)
    contentObjectNumbers.push(nextObjectNumber + 1)
    nextObjectNumber += 2
    objects.push(null, null)
  })

  const pageObjects = pages.map((page, pageIndex) => {
    const pageObjectNumber = pageObjectNumbers[pageIndex]
    const contentObjectNumber = contentObjectNumbers[pageIndex]
    const contentStream = pageTokensToPdfStream(page, {
      pageHeight,
      marginLeft,
      marginTop,
      lineHeight,
      titleLineHeight,
    })
    const contentBytes = new TextEncoder().encode(contentStream)

    const pageObject = `${pageObjectNumber} 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageWidth} ${pageHeight}] /Resources << /Font << /F1 ${regularFontObject} 0 R /F2 ${boldFontObject} 0 R >> >> /Contents ${contentObjectNumber} 0 R >>
endobj
`
    const contentObject = `${contentObjectNumber} 0 obj
<< /Length ${contentBytes.length} >>
stream
${contentStream}
endstream
endobj
`
    return { pageObject, contentObject }
  })

  const pageKids = pageObjectNumbers.map(number => `${number} 0 R`).join(' ')
  const catalogObject = `1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
`
  const pagesObject = `2 0 obj
<< /Type /Pages /Count ${pages.length} /Kids [${pageKids}] >>
endobj
`
  const fontObjectRegular = `3 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
`
  const fontObjectBold = `4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>
endobj
`

  const allObjects = [
    catalogObject,
    pagesObject,
    fontObjectRegular,
    fontObjectBold,
  ]

  pageObjects.forEach((item) => {
    allObjects.push(item.pageObject, item.contentObject)
  })

  let pdf = '%PDF-1.4\n'
  const offsets = [0]

  allObjects.forEach((objectText) => {
    offsets.push(pdf.length)
    pdf += objectText
  })

  const xrefStart = pdf.length
  pdf += `xref
0 ${allObjects.length + 1}
0000000000 65535 f 
`

  for (let index = 1; index <= allObjects.length; index += 1) {
    pdf += `${String(offsets[index]).padStart(10, '0')} 00000 n 
`
  }

  pdf += `trailer
<< /Size ${allObjects.length + 1} /Root 1 0 R >>
startxref
${xrefStart}
%%EOF`

  return new Blob([pdf], { type: 'application/pdf' })
}

function markdownToPdfTokens(markdown, maxChars) {
  const lines = String(markdown || '')
    .replace(/\r/g, '')
    .split('\n')

  const tokens = []

  lines.forEach((line) => {
    const trimmed = line.trim()
    if (!trimmed) {
      tokens.push({ text: '', size: 12, font: 'F1' })
      return
    }

    const headingMatch = trimmed.match(/^(#{1,6})\s+(.*)$/)
    if (headingMatch) {
      const level = headingMatch[1].length
      const headingText = headingMatch[2].trim()
      const size = level === 1 ? 18 : 14
      wrapPdfLine(headingText, level === 1 ? 42 : 58).forEach(text => {
        tokens.push({ text, size, font: 'F2' })
      })
      tokens.push({ text: '', size: 12, font: 'F1' })
      return
    }

    const bulletText = normalizeMarkdownText(trimmed.replace(/^- /, '- '))
    wrapPdfLine(bulletText, maxChars).forEach(text => {
      tokens.push({ text, size: 12, font: 'F1' })
    })
  })

  return tokens
}

function wrapPdfLine(text, limit) {
  const words = String(text || '').split(/\s+/).filter(Boolean)
  if (!words.length) return ['']

  const lines = []
  let current = words[0]

  for (let index = 1; index < words.length; index += 1) {
    const next = `${current} ${words[index]}`
    if (next.length <= limit) {
      current = next
    } else {
      lines.push(current)
      current = words[index]
    }
  }

  lines.push(current)
  return lines
}

function pageTokensToPdfStream(tokens, layout) {
  const commands = []
  let y = layout.pageHeight - layout.marginTop

  tokens.forEach((token) => {
    if (!token.text) {
      y -= layout.lineHeight
      return
    }

    commands.push('BT')
    commands.push(`/${token.font} ${token.size} Tf`)
    commands.push(`1 0 0 1 ${layout.marginLeft} ${y} Tm`)
    commands.push(`(${escapePdfText(token.text)}) Tj`)
    commands.push('ET')

    y -= token.size === 18 ? layout.titleLineHeight : layout.lineHeight
  })

  return commands.join('\n')
}

function escapePdfText(text) {
  return String(text || '')
    .replace(/\\/g, '\\\\')
    .replace(/\(/g, '\\(')
    .replace(/\)/g, '\\)')
}

function normalizeMarkdownText(text) {
  return String(text || '')
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/__(.*?)__/g, '$1')
    .replace(/`([^`]*)`/g, '$1')
}

function landingBotStyle(index) {
  const hues = [25, 42, 88, 142, 212, 254]
  const hue = hues[index % hues.length]
  const left = (index * 8.7) % 94
  const top = (index * 11.3) % 108
  const size = 24 + (index % 5) * 5.5
  const opacity = 0.19 + (index % 5) * 0.04
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

function setupRevealObserver() {
  if (typeof window === 'undefined' || revealObserver) return
  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
        revealObserver?.unobserve(entry.target)
      }
    })
  }, {
    threshold: 0.14,
    rootMargin: '0px 0px -8% 0px',
  })

  document.querySelectorAll('.reveal-on-scroll').forEach((node) => {
    revealObserver?.observe(node)
  })
}

onMounted(() => {
  nextTick(() => {
    setupRevealObserver()
  })
})

watch(currentScreen, async (value) => {
  if (value === 'home') {
    await nextTick()
    revealObserver?.disconnect()
    revealObserver = null
    setupRevealObserver()
  }
})

onBeforeUnmount(stopTimers)
onBeforeUnmount(() => {
  revealObserver?.disconnect()
  revealObserver = null
})
</script>

<style scoped>
.demo-app {
  min-height: 100vh;
  background:
    radial-gradient(circle at 16% 18%, rgba(247, 190, 96, 0.16), transparent 28%),
    radial-gradient(circle at 82% 12%, rgba(136, 205, 255, 0.12), transparent 24%),
    radial-gradient(circle at 54% 86%, rgba(166, 128, 255, 0.08), transparent 26%),
    #fffaf4;
  color: #3a2921;
  font-family: "Avenir Next", "Helvetica Neue", Arial, sans-serif;
}

.demo-bg {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(circle, rgba(192, 183, 174, 0.16) 1.1px, transparent 1.2px),
    transparent;
  background-size: 30px 30px;
  pointer-events: none;
  opacity: 0.44;
}

.demo-topbar {
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

.demo-brand {
  width: 54px;
  height: 54px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  border-radius: 18px;
  border: 1px solid rgba(145, 163, 226, 0.22);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.96), rgba(243, 247, 255, 0.92));
  box-shadow:
    0 16px 32px rgba(95, 112, 180, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.76);
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.brand-mark-img {
  display: block;
  width: 40px;
  height: 40px;
  object-fit: contain;
  filter: drop-shadow(0 10px 24px rgba(138, 116, 255, 0.2));
}

.demo-brand:hover,
.demo-brand:focus-visible {
  transform: translateY(-1px) scale(1.02);
  border-color: rgba(138, 116, 255, 0.34);
  box-shadow:
    0 20px 38px rgba(124, 116, 255, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.82);
}

.demo-brand:focus-visible {
  outline: none;
}

.demo-steps {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.demo-step {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  border: 1px solid rgba(232, 210, 188, 0.82);
  background: rgba(255, 255, 255, 0.74);
  color: #7b6251;
  padding: 10px 14px;
  font: inherit;
}

.demo-step.active,
.demo-step.done {
  color: #2d211a;
  border-color: rgba(242, 162, 86, 0.86);
  background: rgba(255, 246, 236, 0.96);
}

.demo-step-num {
  width: 24px;
  height: 24px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(244, 166, 91, 0.18);
  font-size: 12px;
  font-weight: 800;
}

.demo-topbar-state {
  justify-self: end;
  color: #8b6f5a;
  font-size: 13px;
}

.demo-shell {
  padding: 28px 24px 34px;
}

.demo-stage,
.demo-card,
.demo-final-rail {
  border-radius: 28px;
  border: 1px solid rgba(233, 210, 187, 0.82);
  background: rgba(255, 252, 247, 0.92);
  box-shadow: 0 30px 54px rgba(153, 102, 67, 0.1);
}

.demo-app.home-mode {
  background:
    radial-gradient(circle at 22% 24%, rgba(78, 143, 255, 0.14), transparent 20%),
    radial-gradient(circle at 78% 18%, rgba(55, 193, 177, 0.1), transparent 18%),
    radial-gradient(circle at 52% 78%, rgba(255, 174, 79, 0.1), transparent 22%),
    #fffaf4;
  color: #3a2921;
}

.demo-app.home-mode .demo-bg {
  background:
    radial-gradient(circle, rgba(192, 183, 174, 0.18) 1px, transparent 1.2px),
    transparent;
  background-size: 36px 36px;
  opacity: 0.52;
}

.demo-app.home-mode .demo-shell {
  padding: 0;
}

.demo-app.home-mode .demo-topbar {
  border-bottom: 1px solid rgba(232, 210, 188, 0.72);
  background: rgba(255, 249, 241, 0.88);
  backdrop-filter: blur(18px);
}

.demo-app.home-mode .demo-marketing-link {
  color: #2d211a;
}

.home-nav-mode {
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
}

.home-nav-mode .demo-brand {
  justify-self: start;
}

.home-nav-mode .demo-marketing-nav {
  justify-self: center;
}

.home-nav-mode .demo-home-topbar-actions {
  justify-self: end;
}

.demo-marketing-nav {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}

.demo-marketing-link {
  border: 0;
  background: transparent;
  color: #7a6354;
  font: inherit;
  font-weight: 600;
  padding: 10px 12px;
  cursor: pointer;
  transition: color 180ms ease, transform 180ms ease;
}

.demo-marketing-link:hover,
.demo-marketing-link:focus-visible {
  color: #2d211a;
  transform: translateY(-1px);
}

.demo-home-topbar-actions {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.demo-topbar-secondary,
.demo-topbar-primary {
  border-radius: 16px;
  padding: 12px 16px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  transition: transform 180ms ease, background 180ms ease, border-color 180ms ease;
}

.demo-topbar-secondary {
  border: 1px solid rgba(232, 210, 188, 0.82);
  background: rgba(255, 255, 255, 0.8);
  color: #6f4f3d;
}

.demo-topbar-primary {
  border: 1px solid rgba(239, 196, 147, 0.4);
  background: linear-gradient(135deg, rgba(255, 235, 217, 0.96), rgba(237, 247, 255, 0.96));
  color: #2d211a;
  box-shadow: 0 16px 36px rgba(188, 129, 81, 0.18);
}

.demo-topbar-secondary:hover,
.demo-topbar-primary:hover,
.demo-topbar-secondary:focus-visible,
.demo-topbar-primary:focus-visible {
  transform: translateY(-1px);
}

.demo-home {
  position: relative;
  min-height: calc(100vh - 90px);
  overflow: hidden;
}

.demo-home-stage {
  position: relative;
  width: min(1380px, calc(100vw - 40px));
  margin: 0 auto;
  padding: 18px 0 26px;
}

.demo-home-agent-rain {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.92), rgba(0, 0, 0, 0.54));
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

.demo-home-panel {
  position: relative;
  z-index: 2;
  min-height: calc(100vh - 88px);
  display: grid;
  align-content: center;
  padding: 12px 0;
}

.reveal-on-scroll {
  opacity: 0;
  transform: translateY(26px) scale(0.985);
  transition:
    opacity 720ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 820ms cubic-bezier(0.22, 1, 0.36, 1);
}

.reveal-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.demo-hero-panel {
  text-align: center;
}

.demo-home-panel-shell {
  width: min(1180px, 100%);
  margin: 0 auto;
  padding: 10px 0;
}

.demo-home-panel-intro .demo-home-panel-shell,
.demo-home-panel-about .demo-home-panel-shell {
  display: grid;
  gap: 18px;
  align-content: center;
}

.demo-hero-strip {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 22px;
}

.demo-hero-visual {
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
  display: inline-block;
  background:
    linear-gradient(135deg, #253252 0%, #356fca 26%, #69cbff 48%, #7f6dff 74%, #b785ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow:
    0 10px 28px rgba(124, 116, 255, 0.14),
    0 0 20px rgba(105, 203, 255, 0.1);
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

.demo-eyebrow,
.demo-stage-kicker,
.card-kicker {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #9b6a43;
  margin-bottom: 14px;
}

.demo-home-title,
.demo-stage-title {
  margin: 0;
  font-size: clamp(46px, 6vw, 88px);
  line-height: 0.95;
  font-weight: 900;
  letter-spacing: -0.05em;
  color: transparent;
  background: linear-gradient(135deg, #24324f 0%, #5d8dff 22%, #7d7cff 52%, #ab8fff 78%, #66d6ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow: 0 16px 38px rgba(121, 117, 255, 0.1);
}

.demo-stage-title {
  font-size: clamp(36px, 5vw, 58px);
  letter-spacing: normal;
}

.demo-home-subtitle,
.demo-stage-subtitle {
  margin: 18px auto 0;
  font-size: 16px;
  line-height: 1.62;
  color: #6d5648;
  max-width: 920px;
}

.demo-stage-subtitle {
  margin-left: 0;
  color: #6d5648;
  max-width: 760px;
}

.demo-hero-cta-row {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.demo-home-supporting-copy {
  max-width: 760px;
  margin: 12px auto 0;
  color: #8c715f;
  font-size: 14px;
  line-height: 1.62;
}

.demo-cta,
.demo-primary-btn,
.demo-secondary-btn {
  margin-top: 24px;
  border: 0;
  border-radius: 18px;
  background: linear-gradient(135deg, #f2a55c, #ef7d61);
  color: #fff;
  padding: 16px 22px;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 18px 30px rgba(239, 125, 97, 0.24);
}

.demo-ghost-cta {
  margin-top: 24px;
  border-radius: 18px;
  border: 1px solid rgba(232, 210, 188, 0.86);
  background: rgba(255, 255, 255, 0.82);
  color: #75533d;
  padding: 16px 22px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

.demo-secondary-btn {
  width: 100%;
  margin-top: 18px;
  background: rgba(255, 255, 255, 0.88);
  color: #714d3a;
  border: 1px solid rgba(232, 210, 188, 0.88);
  box-shadow: none;
}

.demo-waitlist-card {
  width: min(920px, 100%);
  margin: 18px auto 0;
  padding: 20px 22px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 18px;
  align-items: center;
  border-radius: 28px;
  border: 1px solid rgba(233, 210, 187, 0.82);
  background: linear-gradient(145deg, rgba(255, 249, 242, 0.96), rgba(247, 251, 255, 0.94));
  box-shadow: 0 28px 70px rgba(173, 121, 78, 0.12);
}

.demo-waitlist-copy p {
  margin: 10px 0 0;
  color: #7a6456;
  line-height: 1.68;
}

.waitlist-title {
  font-size: 24px;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #2c211a;
}

.demo-waitlist-form {
  display: flex;
  gap: 12px;
  align-items: center;
}

.demo-waitlist-input {
  width: 320px;
  padding: 16px 18px;
  border-radius: 16px;
  border: 1px solid rgba(228, 206, 187, 0.86);
  background: rgba(255, 255, 255, 0.86);
  color: #2e221a;
  font: inherit;
  outline: none;
}

.demo-waitlist-input::placeholder {
  color: #a18a79;
}

.demo-waitlist-btn {
  border: 0;
  border-radius: 16px;
  padding: 16px 18px;
  background: linear-gradient(135deg, #8da5ff, #64dbc2);
  color: #08111c;
  font: inherit;
  font-weight: 900;
  cursor: pointer;
}

.demo-home-intro-header {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(340px, 0.72fr);
  gap: 18px;
  align-items: stretch;
}

.demo-home-get-started {
  width: min(1180px, 100%);
  margin: 18px auto 0;
  padding: 20px;
  border-radius: 28px;
  border: 1px solid rgba(233, 210, 187, 0.82);
  background: linear-gradient(155deg, rgba(255, 252, 247, 0.92), rgba(247, 251, 255, 0.88));
  box-shadow: 0 22px 56px rgba(173, 121, 78, 0.1);
}

.demo-home-section-title-compact {
  font-size: clamp(24px, 2.4vw, 33px);
  margin-top: 2px;
}

.demo-walkthrough-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.demo-walkthrough-card {
  padding: 15px;
  border-radius: 22px;
  border: 1px solid rgba(233, 210, 187, 0.76);
  background: rgba(255, 255, 255, 0.74);
  min-height: 156px;
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

.demo-walkthrough-card strong {
  display: block;
  margin-top: 12px;
  color: #31231b;
  font-size: 15px;
  line-height: 1.2;
}

.demo-walkthrough-card p {
  margin: 8px 0 0;
  color: #775f50;
  line-height: 1.5;
  font-size: 12.5px;
}

.demo-section-head {
  display: grid;
  gap: 14px;
}

.demo-section-head.centered {
  max-width: 980px;
  margin: 0 auto;
  text-align: center;
}

.demo-home-intro-copy,
.demo-home-intro-callout,
.demo-about-hero,
.demo-about-card {
  padding: 26px;
  border-radius: 30px;
  border: 1px solid rgba(233, 210, 187, 0.82);
  background: linear-gradient(160deg, rgba(255, 252, 247, 0.94), rgba(252, 247, 240, 0.9));
  box-shadow: 0 26px 70px rgba(173, 121, 78, 0.12);
}

.intro-callout-kicker {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #a1714a;
  margin-bottom: 10px;
}

.demo-home-intro-callout h3 {
  margin: 0;
  font-size: 24px;
  color: #31231b;
  line-height: 1.14;
}

.demo-home-section-title {
  margin: 0;
  font-size: clamp(24px, 2.5vw, 34px);
  line-height: 1.04;
  letter-spacing: -0.035em;
  color: transparent;
  background: linear-gradient(135deg, #24324f 0%, #5d8dff 24%, #7d7cff 54%, #ab8fff 78%, #66d6ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow: 0 14px 34px rgba(125, 124, 255, 0.1);
}

.demo-home-section-copy {
  margin: 0;
  color: #765f51;
  line-height: 1.62;
  font-size: 14px;
}

.demo-home-section-copy.compact {
  font-size: 13.5px;
}

.demo-intro-pill-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.demo-intro-pill {
  display: inline-flex;
  align-items: center;
  padding: 9px 14px;
  border-radius: 999px;
  border: 1px solid rgba(227, 205, 183, 0.82);
  background: rgba(255, 255, 255, 0.82);
  color: #7b5d4a;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.demo-intro-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}

.demo-highlight-card {
  padding: 18px;
  border-radius: 18px;
  border: 1px solid rgba(233, 210, 187, 0.78);
  background: rgba(255, 255, 255, 0.74);
  backdrop-filter: blur(8px);
}

.demo-highlight-card strong {
  display: block;
  font-size: 16px;
  color: #34251c;
  line-height: 1.22;
}

.demo-highlight-card span {
  display: block;
  margin-top: 8px;
  color: #775f50;
  line-height: 1.54;
  font-size: 13px;
}

.demo-intro-feature-card {
  min-height: 196px;
}

.demo-about-hero {
  text-align: center;
  max-width: 980px;
  margin: 0 auto;
}

.demo-about-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.demo-about-card h3 {
  margin: 0 0 12px;
  font-size: 22px;
  color: #2e221a;
}

.demo-about-card p,
.demo-about-list {
  margin: 0;
  color: #755f51;
  line-height: 1.64;
}

.demo-about-list {
  padding-left: 18px;
}

.demo-about-foot {
  display: grid;
  gap: 12px;
  justify-items: center;
}

.demo-about-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 4px;
}

.demo-social-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.demo-social-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border-radius: 999px;
  border: 1px solid rgba(233, 210, 187, 0.86);
  background: rgba(255, 255, 255, 0.86);
  padding: 10px 14px;
  color: #654838;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
  transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}

.demo-social-pill:hover,
.demo-social-pill:focus-visible {
  transform: translateY(-1px);
  border-color: rgba(197, 158, 125, 0.92);
  box-shadow: 0 14px 30px rgba(171, 121, 79, 0.12);
}

.demo-social-pill.is-disabled {
  cursor: default;
  opacity: 0.7;
}

.demo-social-pill.is-disabled:hover,
.demo-social-pill.is-disabled:focus-visible {
  transform: none;
  border-color: rgba(233, 210, 187, 0.86);
  box-shadow: none;
}

.demo-social-pill .social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 999px;
  background: rgba(243, 178, 86, 0.15);
  color: #b06c37;
}

.demo-social-pill .social-icon svg {
  width: 14px;
  height: 14px;
  fill: currentColor;
}

@keyframes heroOrbitFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-8px) scale(1.015); }
}

@keyframes heroChipFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-7px); }
}

.demo-stage,
.demo-running,
.demo-final {
  display: grid;
  gap: 22px;
}

.demo-stage {
  padding: 28px;
}

.demo-stage-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}

.demo-input-grid,
.demo-config-grid,
.demo-slider-grid {
  display: grid;
  gap: 16px;
}

.demo-input-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.demo-config-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.demo-slider-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.demo-input-card,
.demo-config-card,
.demo-slider-card,
.demo-progress-card,
.demo-status-card,
.demo-rail-card {
  border-radius: 24px;
  border: 1px solid rgba(233, 210, 187, 0.8);
  background: rgba(255, 255, 255, 0.8);
  padding: 20px;
}

.demo-config-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-config-value {
  display: block;
  font-size: 22px;
  line-height: 1.22;
  color: #2f231b;
}

.input-card-icon {
  width: 46px;
  height: 46px;
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(243, 178, 86, 0.18);
  color: #b56c2a;
  font-weight: 800;
}

.input-card-title,
.card-title {
  margin-top: 12px;
  font-size: 28px;
  font-weight: 900;
  color: #2f231b;
}

.demo-input-card p,
.demo-config-card p {
  color: #7a6354;
  line-height: 1.65;
}

.input-card-chip,
.demo-badge,
.rail-chip,
.preview-lock {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 999px;
  border: 1px solid rgba(235, 206, 177, 0.88);
  background: rgba(255, 250, 243, 0.96);
  color: #8c6143;
  padding: 9px 13px;
  font-size: 13px;
}

.demo-progress-head,
.demo-slider-top,
.card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.demo-progress-track {
  position: relative;
  height: 11px;
  margin-top: 14px;
  border-radius: 999px;
  background: rgba(241, 229, 216, 0.92);
  overflow: hidden;
}

.demo-progress-track.large {
  height: 13px;
  margin-top: 18px;
}

.demo-progress-fill,
.demo-slider-fill {
  position: absolute;
  inset: 0 auto 0 0;
  border-radius: inherit;
  background: linear-gradient(90deg, #f3b256, #ef7d61);
}

.demo-mini-steps {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 14px;
}

.demo-mini-step {
  padding: 8px 10px;
  border-radius: 999px;
  background: rgba(255, 250, 243, 0.9);
  border: 1px solid rgba(233, 210, 187, 0.76);
  color: #8b6f5c;
  font-size: 12px;
}

.demo-mini-step.active,
.demo-mini-step.done {
  color: #3a2a21;
  border-color: rgba(243, 178, 86, 0.86);
}

.demo-slider {
  position: relative;
  height: 10px;
  margin-top: 16px;
  border-radius: 999px;
  background: rgba(237, 229, 220, 0.94);
  overflow: hidden;
}

.demo-running-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.34fr) minmax(340px, 0.6fr);
  gap: 16px;
}

.demo-running-main {
  display: grid;
  gap: 0;
}

.demo-running-graph,
.demo-running-swarm,
.visual-graph-shell,
.visual-swarm-shell {
  border-radius: 28px;
  overflow: hidden;
}

.demo-running-graph {
  min-height: 520px;
}

.demo-running-swarm {
  min-height: 560px;
  margin-top: -10px;
}

.demo-running-graph :deep(.graph-viewer.dense-mode),
.demo-running-graph :deep(.graph-viewer.dense-mode .gv-canvas) {
  min-height: 520px;
  height: 520px;
}

.demo-running-rail {
  display: grid;
  align-content: start;
  gap: 18px;
}

.demo-status-title {
  margin-top: 8px;
  font-size: 24px;
  font-weight: 900;
  color: #32241b;
}

.demo-status-subtitle,
.rail-note-list,
.demo-rail-head p,
.score-item span,
.analysis-copy-card p,
.analysis-copy-card li,
.strength-grid li,
.thread-bubble p {
  color: #755f50;
  line-height: 1.65;
}

.demo-status-meta {
  margin-top: 12px;
  font-size: 13px;
  color: #8d705d;
}

.demo-report-action-card {
  display: grid;
  gap: 14px;
}

.demo-rail-copy,
.demo-report-stage-note {
  color: #7a6354;
  line-height: 1.6;
  font-size: 14px;
}

.demo-inline-action {
  width: 100%;
  margin-top: 0;
}

.rail-card-title {
  font-size: 14px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a1714a;
  margin-bottom: 12px;
}

.rail-chip-grid {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.rail-note-list {
  margin: 0;
  padding-left: 18px;
}

.report-step-list {
  display: grid;
  gap: 10px;
}

.report-step-row {
  display: grid;
  grid-template-columns: 34px 1fr;
  gap: 12px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 16px;
  background: rgba(255, 248, 240, 0.9);
  border: 1px solid rgba(233, 210, 187, 0.72);
  color: #8f6d55;
}

.report-step-row.active,
.report-step-row.done {
  color: #3a2a21;
  border-color: rgba(243, 178, 86, 0.9);
}

.report-step-index {
  font-weight: 800;
  color: #b57643;
}

.demo-final {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.demo-final-rail {
  position: sticky;
  top: 102px;
  align-self: start;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 28px;
}

.demo-rail-head h2 {
  margin: 0;
  font-size: 48px;
  line-height: 0.96;
  color: #2f221a;
}

.demo-nav-card {
  width: 100%;
  display: grid;
  gap: 8px;
  margin-top: 16px;
  padding: 18px 20px;
  border-radius: 22px;
  border: 1px solid rgba(232, 210, 188, 0.82);
  background: rgba(255, 255, 255, 0.76);
  text-align: left;
  font: inherit;
  cursor: pointer;
}

.demo-nav-card strong {
  font-size: 18px;
  color: #34251c;
}

.demo-nav-card span {
  color: #7d6656;
  line-height: 1.55;
}

.demo-nav-card.active {
  background: rgba(240, 246, 255, 0.92);
  border-color: rgba(113, 164, 255, 0.42);
}

.demo-final-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 18px;
}

.demo-final-main {
  display: grid;
  gap: 22px;
}

.demo-results-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
  gap: 18px;
}

.demo-card {
  padding: 22px;
}

.outcome-card { grid-column: 1; }
.summary-card { grid-column: 2; }
.analysis-card { grid-column: 1 / -1; }
.backtest-card { grid-column: 1; }
.strengths-card { grid-column: 2; }

.donut-wrap { display: flex; align-items: center; justify-content: center; }

.donut-chart {
  width: 124px;
  height: 124px;
  border-radius: 50%;
  position: relative;
}

.donut-chart::after,
.mini-donut::after {
  content: '';
  position: absolute;
  inset: 24px;
  border-radius: 50%;
  background: rgba(255, 252, 247, 0.98);
}

.outcome-bars,
.sector-bars {
  display: grid;
  gap: 12px;
  margin-top: 18px;
}

.forecast-support-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.forecast-support-card {
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(145deg, rgba(255, 249, 243, 0.96), rgba(242, 247, 255, 0.78));
  border: 1px solid rgba(224, 210, 196, 0.82);
}

.forecast-support-card span {
  display: block;
  color: #8f725e;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.forecast-support-card strong {
  display: block;
  margin-top: 10px;
  color: #302219;
  font-size: 19px;
  line-height: 1.2;
}

.forecast-support-card p {
  margin: 10px 0 0;
  color: #7a6354;
  line-height: 1.6;
  font-size: 13px;
}

.outcome-row,
.sector-row {
  display: grid;
  grid-template-columns: 140px 1fr 48px;
  gap: 12px;
  align-items: center;
}

.outcome-track,
.sector-track {
  height: 11px;
  border-radius: 999px;
  background: rgba(238, 230, 220, 0.92);
  overflow: hidden;
}

.outcome-fill,
.sector-fill {
  height: 100%;
  border-radius: inherit;
}

.sector-fill {
  background: linear-gradient(90deg, #f3b256, #4e8fff);
}

.analysis-head-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.analysis-tabs {
  display: inline-flex;
  gap: 8px;
  flex-wrap: wrap;
}

.analysis-download-actions {
  display: inline-flex;
  gap: 8px;
  flex-wrap: wrap;
}

.analysis-download-btn {
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(94, 146, 238, 0.32);
  background: rgba(241, 247, 255, 0.94);
  color: #345a97;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
}

.analysis-download-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 18px rgba(80, 122, 202, 0.12);
}

.analysis-download-btn.secondary {
  border-color: rgba(229, 181, 90, 0.36);
  background: rgba(255, 249, 240, 0.96);
  color: #9d6a34;
}

.analysis-tab {
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(232, 210, 188, 0.84);
  background: rgba(255, 252, 247, 0.9);
  font: inherit;
  color: #7c6656;
  cursor: pointer;
}

.analysis-tab.active {
  color: #2d2119;
  border-color: rgba(113, 164, 255, 0.42);
  background: rgba(239, 246, 255, 0.92);
}

.analysis-view {
  display: grid;
  grid-template-columns: minmax(240px, 0.92fr) minmax(0, 1.08fr);
  gap: 16px;
  margin-top: 18px;
}

.analysis-chart-card,
.analysis-copy-card {
  min-height: 260px;
  border-radius: 22px;
  border: 1px solid rgba(232, 210, 188, 0.82);
  background: rgba(255, 255, 255, 0.8);
  padding: 18px;
}

.analysis-chart-card.wide { min-height: 280px; }

.mini-chart-title {
  font-size: 13px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9c6d4b;
}

.mini-donut {
  position: relative;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  margin: 20px auto 0;
}

.mini-donut-legend,
.population-legend {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}

.mini-legend-row,
.population-legend-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 10px;
  align-items: start;
  padding: 11px 12px;
  border-radius: 16px;
  background: rgba(255, 248, 240, 0.84);
  border: 1px solid rgba(232, 210, 188, 0.72);
}

.mini-legend-swatch {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 4px;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
}

.population-ring-swatch {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 3px solid;
  background: rgba(255, 255, 255, 0.94);
  margin-top: 4px;
  box-shadow: 0 1px 3px rgba(92, 62, 46, 0.08);
}

.mini-legend-copy,
.population-legend-copy {
  display: grid;
  gap: 4px;
  min-width: 0;
}

.mini-legend-copy span,
.population-legend-copy span {
  color: #32241b;
  font-size: 13px;
  font-weight: 700;
}

.mini-legend-copy small,
.population-legend-copy small {
  color: #8a705c;
  line-height: 1.45;
  font-size: 12px;
}

.mini-legend-row strong,
.population-legend-row strong {
  color: #31231a;
  font-size: 14px;
}

.sunburst-sim {
  position: relative;
  width: 170px;
  height: 170px;
  margin: 24px auto 0;
}

.sunburst-ring {
  position: absolute;
  inset: 0;
  margin: auto;
  border-radius: 50%;
  border: 10px solid;
}

.sunburst-core {
  position: absolute;
  inset: 0;
  width: 78px;
  height: 78px;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 252, 247, 0.96);
  border: 1px solid rgba(232, 210, 188, 0.82);
  font-weight: 800;
  color: #6e5647;
}

.analysis-foot-note {
  margin-top: 14px;
  padding: 12px 14px;
  border-radius: 16px;
  background: rgba(245, 247, 251, 0.82);
  border: 1px dashed rgba(195, 208, 229, 0.82);
  color: #6f7287;
  font-size: 12px;
  line-height: 1.55;
}

.analysis-copy-card h3,
.strength-grid h3 {
  margin: 0 0 12px;
  font-size: 24px;
  color: #2d2119;
}

.summary-metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.summary-metric {
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(255, 248, 240, 0.88);
  border: 1px solid rgba(232, 210, 188, 0.72);
}

.summary-metric span {
  display: block;
  color: #8a6f5d;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.summary-metric strong {
  display: block;
  margin-top: 10px;
  color: #33241b;
  font-size: 22px;
  line-height: 1.18;
}

.summary-callout {
  margin-top: 16px;
  padding: 16px 18px;
  border-radius: 20px;
  background: linear-gradient(145deg, rgba(242, 247, 255, 0.88), rgba(255, 250, 244, 0.92));
  border: 1px solid rgba(205, 217, 236, 0.72);
}

.summary-callout-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #6a83aa;
  margin-bottom: 10px;
}

.summary-callout p {
  margin: 0;
  color: #6f5b4b;
  line-height: 1.65;
}

.score-grid {
  display: grid;
  gap: 12px;
  margin-top: 16px;
}

.score-item {
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 248, 240, 0.88);
  border: 1px solid rgba(232, 210, 188, 0.72);
}

.score-item strong {
  display: block;
  margin-top: 8px;
  font-size: 26px;
  color: #33241b;
}

.strength-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 12px;
}

.demo-visual-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  align-items: stretch;
}

.visual-card {
  display: grid;
  gap: 16px;
  align-content: start;
  height: 100%;
}

.visual-meta {
  color: #8b6e5b;
  font-size: 14px;
}

.visual-graph-shell,
.visual-swarm-shell {
  display: grid;
  min-height: 736px;
  height: 100%;
}

.visual-graph-shell :deep(.graph-viewer.dense-mode) {
  min-height: 720px;
  height: 720px;
}

.visual-swarm-shell :deep(.mode-results .swarm-board) {
  min-height: 660px;
}

.visual-swarm-shell :deep(.swarm-shell) {
  min-height: 660px;
}

.visual-swarm-shell :deep(.swarm-legend-overlay.results-overlay) {
  left: 12px;
  right: 12px;
  bottom: 12px;
  width: auto;
  grid-template-columns: 1fr;
  gap: 8px;
}

.visual-swarm-shell :deep(.mode-results .legend-pills-cohorts) {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 7px;
}

.visual-swarm-shell :deep(.mode-results .legend-pills-status) {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 7px;
}

.visual-swarm-shell :deep(.legend-section-compact) {
  padding: 8px 9px;
}

.visual-swarm-shell :deep(.legend-title) {
  margin-bottom: 6px;
  font-size: 9px;
}

.visual-swarm-shell :deep(.legend-pill) {
  min-height: 34px;
  padding: 5px 8px;
  font-size: 10px;
  line-height: 1.35;
}

.demo-tools-grid {
  display: block;
}

.tools-card {
  min-height: 820px;
}

.thread-list {
  display: grid;
  gap: 18px;
  margin-top: 18px;
}

.thread-card {
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(232, 210, 188, 0.8);
}

.thread-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.thread-tool {
  font-size: 13px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a16d48;
}

.thread-time {
  color: #9b7e6a;
  font-size: 12px;
}

.thread-bubble {
  margin-top: 12px;
  padding: 16px;
  border-radius: 20px;
}

.thread-bubble.user {
  background: rgba(255, 247, 239, 0.92);
  border: 1px solid rgba(239, 210, 182, 0.84);
}

.thread-bubble.assistant {
  background: rgba(242, 247, 255, 0.92);
  border: 1px solid rgba(186, 210, 245, 0.82);
}

.thread-role {
  margin-bottom: 8px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #9a6d49;
}

.pinned-evidence {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid rgba(205, 217, 236, 0.72);
}

.pinned-evidence-title {
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6a83aa;
  margin-bottom: 10px;
}

.evidence-pill {
  display: inline-flex;
  margin: 0 8px 8px 0;
  padding: 8px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(186, 210, 245, 0.82);
  color: #53657f;
  font-size: 13px;
}

.thread-input-disabled {
  margin-top: 20px;
  padding: 18px;
  border-radius: 20px;
  background: rgba(250, 246, 241, 0.92);
  border: 1px dashed rgba(232, 210, 188, 0.88);
  color: #8b6e5b;
}

#demo-hero,
#demo-introduction,
#demo-about,
#demo-waitlist {
  scroll-margin-top: 110px;
}

@media (max-width: 1180px) {
  .demo-home,
  .demo-running-grid,
  .demo-final,
  .demo-results-grid,
  .demo-visual-grid,
  .analysis-view,
  .strength-grid,
  .demo-input-grid,
  .demo-config-grid,
  .demo-slider-grid {
    grid-template-columns: 1fr;
  }

  .demo-topbar {
    grid-template-columns: 1fr;
  }

  .home-nav-mode {
    grid-template-columns: 1fr;
  }

  .demo-topbar-state {
    justify-self: start;
  }

  .demo-marketing-nav,
  .demo-home-topbar-actions {
    justify-content: flex-start;
  }

  .demo-home-stage {
    width: min(100vw - 32px, 1380px);
    padding: 32px 0 48px;
  }

  .demo-home-title {
    font-size: clamp(44px, 10vw, 88px);
  }

  .demo-final-rail {
    position: static;
    top: auto;
  }

  .demo-waitlist-card,
  .demo-walkthrough-grid,
  .demo-about-grid,
  .demo-waitlist-form,
  .summary-metric-grid {
    grid-template-columns: 1fr;
  }

  .demo-intro-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .demo-waitlist-input {
    width: 100%;
  }

  .demo-hero-panel {
    padding-top: 28px;
  }

  .demo-hero-cta-row {
    justify-content: flex-start;
  }

  .demo-home-panel {
    min-height: auto;
    padding: 28px 0;
  }

  .demo-home-panel-shell {
    padding: 16px 0;
  }

  .demo-about-hero,
  .demo-about-card,
  .demo-highlight-card {
    padding: 22px;
  }
}

@media (max-width: 760px) {
  .demo-shell {
    padding: 18px 16px 24px;
  }

  .demo-app.home-mode .demo-shell {
    padding: 0;
  }

  .demo-home-stage {
    width: calc(100vw - 24px);
  }

  .demo-brand-mark {
    font-size: 24px;
  }

  .demo-home-title {
    font-size: clamp(40px, 12vw, 62px);
  }

  .demo-hero-visual {
    width: min(100%, 760px);
    height: 248px;
    padding-inline: 4px;
  }

  .demo-home-subtitle,
  .demo-stage-subtitle {
    font-size: 17px;
  }

  .hero-pill,
  .demo-marketing-link {
    font-size: 12px;
  }

  .demo-home-panel {
    padding: 18px 0;
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

  .hero-visual-chip {
    font-size: 10px;
    padding: 8px 12px;
    max-width: 42%;
    text-align: center;
  }

  .hero-visual-chip.chip-a { top: 18px; left: 0; }
  .hero-visual-chip.chip-b { top: 24px; right: 0; }
  .hero-visual-chip.chip-c { bottom: 16px; left: 1%; }
  .hero-visual-chip.chip-d { bottom: 6px; right: 1%; }

  .demo-home-section-title {
    font-size: 30px;
  }

  .demo-about-card h3,
  .demo-highlight-card strong {
    font-size: 22px;
  }

  .demo-waitlist-card {
    padding: 18px;
  }
}

/* ── Theme Refresh ─────────────────────────────────────────────────────── */
.demo-app {
  background:
    radial-gradient(circle at 16% 18%, rgba(111, 215, 255, 0.16), transparent 28%),
    radial-gradient(circle at 82% 12%, rgba(178, 144, 255, 0.14), transparent 24%),
    radial-gradient(circle at 54% 86%, rgba(104, 221, 214, 0.1), transparent 26%),
    #f8fbff;
  color: #253252;
}

.demo-bg {
  background:
    radial-gradient(circle, rgba(165, 178, 221, 0.18) 1.1px, transparent 1.25px),
    transparent;
}

.demo-app.home-mode {
  background:
    radial-gradient(circle at 22% 24%, rgba(92, 150, 255, 0.14), transparent 20%),
    radial-gradient(circle at 78% 18%, rgba(111, 215, 255, 0.1), transparent 18%),
    radial-gradient(circle at 52% 78%, rgba(178, 144, 255, 0.12), transparent 22%),
    #f8fbff;
  color: #253252;
}

.demo-app.home-mode .demo-bg {
  background:
    radial-gradient(circle, rgba(165, 178, 221, 0.18) 1px, transparent 1.2px),
    transparent;
}

.demo-topbar,
.demo-app.home-mode .demo-topbar {
  border-bottom-color: rgba(145, 163, 226, 0.24);
  background: rgba(249, 251, 255, 0.9);
}

.demo-stage,
.demo-card,
.demo-final-rail,
.demo-about-hero,
.demo-about-card,
.demo-highlight-card,
.demo-home-get-started,
.demo-waitlist-card,
.demo-walkthrough-card,
.demo-input-card,
.demo-config-card,
.demo-nav-card,
.demo-progress-card,
.demo-rail-card,
.demo-report-action-card,
.demo-slider-card,
.demo-status-card {
  border-color: rgba(145, 163, 226, 0.22);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.94), rgba(244, 248, 255, 0.9));
  box-shadow: 0 28px 56px rgba(95, 112, 180, 0.11);
}

.demo-brand,
.demo-app.home-mode .demo-brand,
.demo-app.home-mode .demo-marketing-link,
.demo-app.home-mode .demo-brand-mark,
.demo-about-card h3,
.demo-highlight-card strong,
.waitlist-title {
  color: #253252;
}

.demo-brand-badge,
.demo-app.home-mode .demo-brand-badge,
.demo-eyebrow,
.demo-stage-kicker,
.card-kicker,
.intro-callout-kicker {
  color: #7d7cff;
  border-color: rgba(178, 144, 255, 0.26);
}

.demo-brand-badge,
.demo-app.home-mode .demo-brand-badge {
  background: rgba(255, 255, 255, 0.9);
}

.demo-marketing-link,
.demo-topbar-state,
.demo-home-subtitle,
.demo-stage-subtitle,
.demo-home-supporting-copy,
.demo-home-section-copy,
.demo-highlight-card span,
.demo-walkthrough-card p,
.demo-about-card p,
.demo-about-list,
.demo-waitlist-copy p {
  color: #6e7a99;
}

.demo-step {
  border-color: rgba(145, 163, 226, 0.22);
  background: rgba(255, 255, 255, 0.82);
  color: #6e7a99;
}

.demo-step.active,
.demo-step.done {
  color: #253252;
  border-color: rgba(138, 116, 255, 0.34);
  background: rgba(244, 241, 255, 0.94);
}

.demo-step-num,
.walkthrough-number,
.demo-social-pill .social-icon {
  background: rgba(138, 116, 255, 0.14);
  color: #7d7cff;
}

.demo-progress-head strong,
.demo-slider-top strong {
  color: #8a74ff;
}

.demo-progress-track,
.demo-slider {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(241, 245, 255, 0.94));
  border: 1px solid rgba(145, 163, 226, 0.2);
  box-shadow: inset 0 1px 2px rgba(124, 138, 191, 0.12);
}

.demo-progress-fill,
.demo-slider-fill {
  background: linear-gradient(90deg, #69cbff 0%, #8a74ff 58%, #c194ff 100%);
  box-shadow: 0 0 16px rgba(124, 116, 255, 0.18);
}

.demo-topbar-secondary,
.demo-ghost-cta,
.demo-secondary-btn,
.demo-social-pill,
.demo-waitlist-input,
.demo-intro-pill,
.hero-pill {
  border-color: rgba(145, 163, 226, 0.22);
  background: rgba(255, 255, 255, 0.88);
  color: #5f6d94;
}

.demo-topbar-primary,
.demo-cta,
.demo-primary-btn,
.demo-waitlist-btn {
  background: linear-gradient(135deg, #69cbff 0%, #8a74ff 52%, #c194ff 100%);
  color: #ffffff;
  box-shadow: 0 20px 36px rgba(124, 116, 255, 0.2);
}

.hero-visual-ring {
  border-color: rgba(156, 176, 236, 0.5);
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.3), transparent 68%);
}

.hero-visual-ring.ring-one {
  border-color: rgba(105, 203, 255, 0.48);
}

.hero-visual-ring.ring-two {
  border-color: rgba(138, 116, 255, 0.28);
}

.hero-visual-ring.ring-three {
  border-color: rgba(160, 139, 255, 0.22);
}

.hero-visual-core {
  border-color: rgba(145, 163, 226, 0.22);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.94), rgba(242, 246, 255, 0.9));
  box-shadow:
    0 24px 56px rgba(95, 112, 180, 0.14),
    inset 0 1px 0 rgba(255, 255, 255, 0.62);
}

.hero-visual-core-title {
  background:
    linear-gradient(135deg, #253252 0%, #356fca 26%, #69cbff 48%, #7f6dff 74%, #b785ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow:
    0 10px 28px rgba(124, 116, 255, 0.14),
    0 0 20px rgba(105, 203, 255, 0.1);
}

.hero-visual-core-subtitle,
.hero-visual-chip {
  color: #62719b;
}

.hero-visual-chip {
  border-color: rgba(145, 163, 226, 0.22);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 16px 30px rgba(95, 112, 180, 0.1);
}

.demo-home-title,
.demo-stage-title,
.demo-home-section-title {
  color: transparent;
  background: linear-gradient(135deg, #24324f 0%, #5d8dff 22%, #7d7cff 52%, #ab8fff 78%, #66d6ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
}

.demo-cta,
.demo-primary-btn,
.demo-secondary-btn,
.demo-ghost-cta,
.demo-topbar-primary,
.demo-topbar-secondary {
  transition: transform 180ms ease, box-shadow 220ms ease, border-color 180ms ease, background 180ms ease;
}

.demo-cta:hover,
.demo-primary-btn:hover,
.demo-ghost-cta:hover,
.demo-topbar-primary:hover,
.demo-topbar-secondary:hover {
  transform: translateY(-1px);
}

.demo-app:not(.home-mode) {
  --demo-workflow-box-bg: linear-gradient(160deg, rgba(255, 255, 255, 0.95), rgba(244, 241, 255, 0.9));
  --demo-workflow-box-bg-soft: linear-gradient(160deg, rgba(255, 255, 255, 0.92), rgba(246, 249, 255, 0.88));
  --demo-workflow-box-border: rgba(145, 163, 226, 0.22);
  --demo-workflow-box-shadow: 0 20px 40px rgba(95, 112, 180, 0.1);
}

.demo-app:not(.home-mode) :is(
  [class*="-card"],
  .demo-stage,
  .demo-progress-track,
  .demo-slider,
  .demo-badge,
  .input-card-chip,
  .rail-chip,
  .report-step-row,
  .summary-metric,
  .mini-legend-row,
  .population-legend-row,
  .analysis-foot-note,
  .visual-graph-shell,
  .visual-swarm-shell
) {
  background: var(--demo-workflow-box-bg);
  border-color: var(--demo-workflow-box-border);
  box-shadow: var(--demo-workflow-box-shadow);
}

.demo-app:not(.home-mode) :is(
  .demo-badge,
  .input-card-chip,
  .rail-chip,
  .report-step-row,
  .summary-metric,
  .mini-legend-row,
  .population-legend-row,
  .analysis-foot-note
) {
  background: var(--demo-workflow-box-bg-soft);
}

.demo-app:not(.home-mode) {
  --demo-theme-pill-bg: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(243, 247, 255, 0.94));
  --demo-theme-pill-bg-strong: linear-gradient(160deg, rgba(245, 248, 255, 0.98), rgba(244, 241, 255, 0.94));
  --demo-theme-pill-border: rgba(145, 163, 226, 0.24);
  --demo-theme-pill-border-strong: rgba(138, 116, 255, 0.34);
  --demo-theme-pill-text: #5f6d94;
  --demo-theme-pill-title: #253252;
  --demo-theme-pill-accent: #7d7cff;
}

.demo-app:not(.home-mode) :is(
  .input-card-chip,
  .demo-badge,
  .rail-chip,
  .preview-lock,
  .demo-mini-step,
  .analysis-tab,
  .analysis-download-btn,
  .analysis-download-btn.secondary
) {
  background: var(--demo-theme-pill-bg);
  border-color: var(--demo-theme-pill-border);
  color: var(--demo-theme-pill-text);
  box-shadow: 0 12px 24px rgba(95, 112, 180, 0.08);
}

.demo-app:not(.home-mode) :is(
  .demo-mini-step.active,
  .demo-mini-step.done,
  .report-step-row.active,
  .report-step-row.done,
  .analysis-tab.active
) {
  background: var(--demo-theme-pill-bg-strong);
  border-color: var(--demo-theme-pill-border-strong);
  color: var(--demo-theme-pill-title);
  box-shadow: 0 14px 28px rgba(95, 112, 180, 0.12);
}

.demo-app:not(.home-mode) :is(
  .input-card-icon,
  .report-step-index
) {
  background: rgba(138, 116, 255, 0.12);
  color: var(--demo-theme-pill-accent);
  border: 1px solid rgba(138, 116, 255, 0.18);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.demo-app:not(.home-mode) :is(
  .demo-stage-kicker,
  .card-kicker,
  .demo-config-label,
  .demo-status-label,
  .rail-card-title,
  .mini-chart-title,
  .summary-callout-title,
  .thread-tool,
  .thread-role,
  .pinned-evidence-title
) {
  color: var(--demo-theme-pill-accent);
}

.demo-app:not(.home-mode) :is(
  .demo-config-value,
  .demo-status-title,
  .demo-rail-head h2,
  .score-item strong,
  .analysis-copy-card h3,
  .strength-grid h3,
  .thread-bubble p strong
) {
  color: var(--demo-theme-pill-title);
}

.demo-app:not(.home-mode) :is(
  .demo-input-card p,
  .demo-config-card p,
  .demo-status-subtitle,
  .demo-status-meta,
  .demo-rail-copy,
  .demo-report-stage-note,
  .score-item span,
  .analysis-copy-card p,
  .analysis-copy-card li,
  .strength-grid li,
  .thread-bubble p,
  .thread-time,
  .visual-meta
) {
  color: #6e7a99;
}

.demo-app:not(.home-mode) :is(
  .forecast-support-card,
  .score-item,
  .thread-card,
  .thread-input-disabled,
  .thread-bubble.user,
  .thread-bubble.assistant,
  .summary-callout,
  .evidence-pill
) {
  background: var(--demo-workflow-box-bg-soft);
  border-color: var(--demo-workflow-box-border);
  box-shadow: 0 18px 34px rgba(95, 112, 180, 0.08);
}

.demo-app:not(.home-mode) .analysis-download-btn:hover {
  border-color: var(--demo-theme-pill-border-strong);
  box-shadow: 0 12px 22px rgba(95, 112, 180, 0.12);
}
</style>
