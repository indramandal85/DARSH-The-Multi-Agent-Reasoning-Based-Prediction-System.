// Demo-only seeded graph data for the static walkthrough.
const GRAPH_WIDTH = 980
const GRAPH_HEIGHT = 760
const GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5))

const PERSON_NAMES = [
  'Aarav', 'Ishaan', 'Kabir', 'Aditya', 'Rohan', 'Vikram', 'Arjun', 'Neel',
  'Aman', 'Kunal', 'Rahul', 'Sameer', 'Nikhil', 'Pranav', 'Aditi', 'Mira',
  'Kavya', 'Ananya', 'Ira', 'Rhea', 'Diya', 'Sana', 'Tara', 'Meera',
]

const PLACE_NAMES = [
  'Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune',
  'Ahmedabad', 'Kolkata', 'Singapore', 'Dubai', 'London', 'New York',
]

const CLUSTER_NAMING = {
  policy: {
    people: ['Raghav Menon', 'Ananya Deshpande', 'Vikram Sethi', 'Mira Rao', 'Kunal Bhatia', 'Ishita Sen', 'Dev Khanna'],
    organizations: ['Monetary Strategy Council', 'Fiscal Signalling Forum', 'Sovereign Policy Desk', 'Rates Calibration Board', 'Public Finance Unit', 'Treasury Reform Office', 'Macro Stability Council'],
    events: ['Interim Rate Review', 'Budget Transmission Call', 'Liquidity Corridor Briefing', 'Bond Auction Debrief', 'Treasury Coordination Huddle', 'Policy Messaging Session', 'Inflation Guidance Note'],
    concepts: ['Terminal Rate Path', 'Policy Pass-through Premium', 'Fiscal Credibility Spread', 'Liquidity Absorption Window', 'Inflation Anchor Range', 'Sovereign Funding Balance', 'Transmission Confidence Gauge'],
    places: ['North Block Briefing Room', 'Mint Street Operations Desk', 'Parliament Annexe Policy Bay', 'Central Secretariat Macro Cell', 'Janpath Strategy Suite', 'Nirman Bhavan Fiscal Desk'],
  },
  banking: {
    people: ['Arjun Shah', 'Neha Kulkarni', 'Rohit Vora', 'Pallavi Iyer', 'Samar Ghosh', 'Tanya Jain', 'Harshita Kapoor'],
    organizations: ['Treasury Liquidity Desk', 'Deposit Franchise Office', 'Credit Watch Forum', 'PSU Balance Sheet Cell', 'Funding Cost Board', 'Recovery Analytics Unit', 'Bank Treasury Circle'],
    events: ['Deposit Flow Check', 'Credit Slippage Call', 'Repo Desk Huddle', 'Funding Spread Review', 'Quarterly Treasury Brief', 'Deposit Repricing Note', 'Asset Quality Watch'],
    concepts: ['Deposit Cost Curve', 'Credit Impulse Spread', 'Funding Stability Buffer', 'Loan Growth Pulse', 'Treasury Carry Window', 'Recovery Momentum Gauge', 'Balance Sheet Resilience'],
    places: ['Nariman Point Dealing Room', 'Fort Treasury Floor', 'Lower Parel Credit Hub', 'BKC Banking Desk', 'Dalal Street Bank Bay', 'Churchgate Liquidity Room'],
  },
  markets: {
    people: ['Kabir Mehta', 'Aditi Narang', 'Siddharth Bose', 'Rhea Malhotra', 'Yash Bansal', 'Meera Chopra', 'Nikhil Tandon'],
    organizations: ['Index Flows Desk', 'Derivatives Strategy Cell', 'Market Breadth Forum', 'Volatility Positioning Desk', 'Cash Market Board', 'Cross-Asset Signals Unit', 'Momentum Analytics Circle'],
    events: ['Opening Bell Shock', 'Index Rebalance Watch', 'Options Expiry Sweep', 'Midday Flow Check', 'Closing Auction Pulse', 'Volatility Breakout Alert', 'Block Trade Digest'],
    concepts: ['Index Breadth Momentum', 'Gamma Pressure Band', 'Retail Flow Reflex', 'Intraday Liquidity Pocket', 'Price Discovery Window', 'Volatility Spillover', 'Trend Confirmation Signal'],
    places: ['Dalal Street Market Pod', 'NSE Co-location Bay', 'BKC Derivatives Hub', 'Prabhadevi Execution Desk', 'Bandra Market Room', 'Colaba Trading Floor'],
  },
  industry: {
    people: ['Viren Chawla', 'Sneha Arora', 'Aman Duggal', 'Priya Nair', 'Nitin Bedi', 'Ritika Saran', 'Mohit Bhasin'],
    organizations: ['Corporate Planning Office', 'Capex Strategy Forum', 'Industrial Demand Desk', 'Energy Cost Council', 'Manufacturing Signals Unit', 'Earnings Revision Board', 'Supply Chain Watch'],
    events: ['Management Guidance Cut', 'Capex Approval Review', 'Input Cost Spike', 'Plant Expansion Brief', 'Quarterly Margin Reset', 'Demand Channel Check', 'Procurement Shock Call'],
    concepts: ['Operating Leverage Window', 'Input Cost Pass-through', 'Order Book Visibility', 'Capex Intent Signal', 'Margin Compression Risk', 'Utilization Recovery Path', 'Earnings Revision Drift'],
    places: ['Bengaluru Corporate Cell', 'Pune Industrial Room', 'Gurugram Strategy Bay', 'Chennai Plant Desk', 'Vadodara Operations Hub', 'Noida Supply Suite'],
  },
  media: {
    people: ['Sana Mirza', 'Aditya Talwar', 'Ritika Dutta', 'Karan Makkar', 'Diya Chatterjee', 'Manav Kapur', 'Tara Nanda'],
    organizations: ['Headline Risk Desk', 'Narrative Intelligence Studio', 'Markets Coverage Unit', 'Editorial Signals Team', 'Breaking News Bureau', 'Sentiment Tracking Room', 'Broadcast Analysis Desk'],
    events: ['Prime Time Flash', 'Headline Cascade Watch', 'Anchor Desk Debrief', 'Newsletter Push Alert', 'Breaking Tape Sweep', 'Narrative Pivot Call', 'Morning Brief Release'],
    concepts: ['Narrative Velocity', 'Headline Amplification Loop', 'Attention Rotation Index', 'Sentiment Overshoot Risk', 'Storyline Persistence', 'Retail Mindshare Pulse', 'Signal-to-Noise Ratio'],
    places: ['Noida Broadcast Suite', 'Connaught Place Newsroom', 'Lower Parel Media Desk', 'Film City Editorial Hub', 'Delhi NCR News Bay', 'Worli Studio Floor'],
  },
  global: {
    people: ['Ira Wadhwa', 'Rahul Mistry', 'Leena Sood', 'Varun Kohli', 'Ayesha Thomas', 'Keshav Patel', 'Samaira Gupta'],
    organizations: ['Offshore Macro Desk', 'EM Flows Council', 'FX Strategy Office', 'Cross-Border Risk Unit', 'Global Allocation Forum', 'Dollar Liquidity Desk', 'Asia Signals Board'],
    events: ['Overnight Risk Sweep', 'Asia Open Check', 'FX Basis Review', 'Offshore Allocation Call', 'US Rates Spillover Note', 'Dollar Funding Alert', 'Singapore Morning Brief'],
    concepts: ['Dollar Liquidity Pulse', 'EM Risk Premium', 'FX Basis Stress', 'Offshore Positioning Drift', 'Cross-Market Contagion', 'Carry Trade Pressure', 'Global Macro Impulse'],
    places: ['Singapore Macro Desk', 'Dubai Offshore Hub', 'London EM Room', 'Hong Kong Flow Bay', 'New York Rates Pod', 'Canary Wharf Asia Bridge'],
  },
  macro: {
    people: ['Aarav Subramaniam', 'Isha Mahajan', 'Parth Agarwal', 'Naina Reddy', 'Rishi Bahl', 'Kavya Murthy', 'Soham Lahiri'],
    organizations: ['Inflation Analysis Cell', 'Yield Curve Council', 'Macro Forecast Unit', 'Rates Research Forum', 'Policy Sensitivity Desk', 'Bond Strategy Office', 'Economic Signals Board'],
    events: ['CPI Surprise Note', 'Yield Curve Steepener', 'GDP Revision Call', 'Policy Minutes Review', 'Inflation Print Watch', 'Bond Auction Recap', 'Macro Data Sweep'],
    concepts: ['Real Rate Gap', 'Inflation Persistence', 'Duration Risk Pocket', 'Curve Repricing Window', 'Growth-Inflation Tradeoff', 'Policy Credibility Band', 'Bond Supply Pressure'],
    places: ['Nariman Point Macro Desk', 'Delhi Macro Briefing Room', 'Cuffe Parade Rates Bay', 'Fort Bond Hub', 'Pragati Maidan Data Cell', 'Mumbai Curve Desk'],
  },
  consumer: {
    people: ['Rhea Suri', 'Dhruv Anand', 'Anika Batra', 'Gautam Sehgal', 'Mitali Verma', 'Arnav Sinha', 'Sia Oberoi'],
    organizations: ['Demand Tracking Desk', 'Retail Credit Forum', 'Household Spend Unit', 'Consumer Signals Lab', 'NBFC Distribution Cell', 'Payments Insight Board', 'Affordability Watch Desk'],
    events: ['Festival Demand Pulse', 'Retail Credit Review', 'EMI Stress Check', 'Discretionary Spend Note', 'Vehicle Booking Flash', 'Consumption Trend Call', 'Household Budget Snapshot'],
    concepts: ['Affordability Threshold', 'Consumption Recovery Pulse', 'Credit Uptake Signal', 'Household Stress Index', 'Discretionary Spend Momentum', 'Retail Financing Spread', 'Urban Demand Drift'],
    places: ['Pune Consumer Desk', 'Indiranagar Spend Hub', 'Gurugram Retail Floor', 'Thane Credit Room', 'Ahmedabad Demand Bay', 'Koregaon Park Consumer Suite'],
  },
}

const RELATIONS = [
  'RELATES_TO', 'TRACKS', 'AMPLIFIES', 'MONITORS', 'AFFECTS',
  'INFLUENCES', 'SHAPES', 'RESPONDS_TO', 'USES', 'WATCHES',
]

const CLUSTERS = [
  {
    key: 'policy',
    label: 'Policy',
    center: { x: 532, y: 206 },
    hubs: ['Reserve Bank of India', 'Government of India', 'Policy Transmission', 'Ministry of Finance'],
    focusTerms: ['RBI', 'Policy', 'Transmission', 'Rates', 'Liquidity'],
  },
  {
    key: 'banking',
    label: 'Banking',
    center: { x: 360, y: 314 },
    hubs: ['PSU Banks', 'Credit Growth', 'Liquidity Conditions', 'Mumbai'],
    focusTerms: ['Banks', 'Liquidity', 'Credit', 'Treasury'],
  },
  {
    key: 'markets',
    label: 'Markets',
    center: { x: 678, y: 302 },
    hubs: ['Nifty 50', 'Bank Nifty', 'Retail Traders', 'Rupee'],
    focusTerms: ['Nifty', 'Retail', 'Flows', 'Rupee'],
  },
  {
    key: 'industry',
    label: 'Industry',
    center: { x: 784, y: 474 },
    hubs: ['Corporate India', 'Auto Sector', 'Energy Import Bill', 'Bengaluru'],
    focusTerms: ['Corporate', 'Auto', 'Energy', 'Earnings'],
  },
  {
    key: 'media',
    label: 'Media',
    center: { x: 278, y: 504 },
    hubs: ['Financial Media', 'Risk Narrative', 'Sentiment Loop', 'Delhi'],
    focusTerms: ['Media', 'Narrative', 'Sentiment'],
  },
  {
    key: 'global',
    label: 'Global',
    center: { x: 644, y: 592 },
    hubs: ['Foreign Portfolio Flows', 'Global Risk Desk', 'Dollar Index', 'Singapore Desk'],
    focusTerms: ['Foreign', 'Global', 'Dollar', 'Flows'],
  },
  {
    key: 'macro',
    label: 'Macro',
    center: { x: 510, y: 448 },
    hubs: ['Inflation Path', 'Fiscal Deficit', 'Bond Yields', 'Domestic Mutual Funds'],
    focusTerms: ['Inflation', 'Fiscal', 'Bonds', 'Funds'],
  },
  {
    key: 'consumer',
    label: 'Consumer',
    center: { x: 424, y: 636 },
    hubs: ['Consumer Demand', 'NBFC Basket', 'Private Credit Desk', 'Pune'],
    focusTerms: ['Consumer', 'NBFC', 'Demand', 'Credit'],
  },
]

const CORE_NODES = [
  { id: 'Reserve Bank of India', type: 'ORGANIZATION', description: 'Central monetary authority anchoring rate expectations and liquidity conditions.' },
  { id: 'Government of India', type: 'ORGANIZATION', description: 'Fiscal and policy center shaping taxes, spending, and political signaling.' },
  { id: 'Ministry of Finance', type: 'ORGANIZATION', description: 'Fiscal policy command center coordinating tax, deficit, and expenditure messaging.' },
  { id: 'Nifty 50', type: 'CONCEPT', description: 'Headline equity benchmark reflecting broad Indian market sentiment.' },
  { id: 'Bank Nifty', type: 'CONCEPT', description: 'Bank-heavy equity index that responds quickly to liquidity, rates, and credit narratives.' },
  { id: 'Corporate India', type: 'ORGANIZATION', description: 'Operating companies and CFO networks reacting to policy, demand, and earnings expectations.' },
  { id: 'Domestic Mutual Funds', type: 'ORGANIZATION', description: 'Domestic long-only funds balancing benchmark risk, flows, and conviction sizing.' },
  { id: 'Foreign Portfolio Flows', type: 'CONCEPT', description: 'Cross-border capital impulses influencing risk appetite and market breadth.' },
  { id: 'Retail Traders', type: 'CONCEPT', description: 'Fast-moving retail participation amplifying social narratives and short-term positioning.' },
  { id: 'Policy Transmission', type: 'CONCEPT', description: 'How macro decisions pass through credit, earnings, currency, and consumption channels.' },
  { id: 'Rupee', type: 'CONCEPT', description: 'Currency sensitivity node reacting to growth, inflation, and foreign flow balance.' },
  { id: 'Bond Yields', type: 'CONCEPT', description: 'Rate curve signal for funding costs, valuation pressure, and fiscal credibility.' },
  { id: 'Liquidity Conditions', type: 'CONCEPT', description: 'System-level liquidity affecting funding ease, risk-taking, and market resilience.' },
  { id: 'Inflation Path', type: 'CONCEPT', description: 'Core macro path shaping policy tone, real rates, and sector rotation.' },
  { id: 'Fiscal Deficit', type: 'CONCEPT', description: 'Fiscal balance signal driving sovereign credibility and supply expectations.' },
  { id: 'Credit Growth', type: 'CONCEPT', description: 'Bank lending pulse linked to consumption, capex, and policy confidence.' },
  { id: 'Auto Sector', type: 'ORGANIZATION', description: 'Consumer cyclicals layer reacting to demand, financing, and input-cost shifts.' },
  { id: 'PSU Banks', type: 'ORGANIZATION', description: 'Public sector banking cluster with high policy-transmission sensitivity.' },
  { id: 'NBFC Basket', type: 'ORGANIZATION', description: 'Shadow-lending cluster sensitive to spreads, funding stability, and consumption credit.' },
  { id: 'Energy Import Bill', type: 'EVENT', description: 'External cost shock driver that transmits into inflation, currency, and margins.' },
  { id: 'Financial Media', type: 'ORGANIZATION', description: 'Headline-amplification network shaping public narrative and cross-cohort attention.' },
  { id: 'Risk Narrative', type: 'CONCEPT', description: 'Shared market storyline that compresses complex developments into tradable sentiment.' },
  { id: 'Sentiment Loop', type: 'CONCEPT', description: 'Feedback loop between price action, commentary, and participant conviction.' },
  { id: 'Global Risk Desk', type: 'ORGANIZATION', description: 'Macro desk observing India through global rates, FX, and cross-market positioning.' },
  { id: 'Dollar Index', type: 'CONCEPT', description: 'Global FX strength proxy influencing EM risk allocation.' },
  { id: 'Consumer Demand', type: 'CONCEPT', description: 'Real-economy demand pulse linked to jobs, credit, and discretionary spending.' },
  { id: 'Private Credit Desk', type: 'ORGANIZATION', description: 'Funding and credit-monitoring cohort focused on balance-sheet stability.' },
  { id: 'Mumbai', type: 'PLACE', description: 'Financial market hub anchoring broker, banking, and exchange activity.' },
  { id: 'Delhi', type: 'PLACE', description: 'Policy and political signal center.' },
  { id: 'Bengaluru', type: 'PLACE', description: 'Technology and growth narrative hub.' },
  { id: 'Singapore Desk', type: 'PLACE', description: 'Offshore market lens watching India through FX and cross-asset flow channels.' },
  { id: 'Pune', type: 'PLACE', description: 'Manufacturing and consumption-linked business hub.' },
]

const DEMO_CONFIG = {
  numAgents: 24,
  numRounds: 8,
  numBranches: 8,
  eventType: 'macro_regime_shift',
  swarmNodeScale: 0.3,
  swarmBoardHeight: 460,
  swarmDefaultZoom: 2.06,
  swarmZoomMultiplier: 1.48,
  swarmMinZoom: 1.82,
  swarmMaxZoom: 2.28,
  swarmCenterOnLoad: true,
  animationIntervalMs: 860,
}

const DEMO_POPULATION_MODEL = {
  represented_population: 137000000,
  weighted_regime: 'uncertainty hold',
  weighted_outcome: 'cautious',
  cohort_breakdown: [
    {
      role_key: 'RETAIL_TRADER',
      label: 'Retail Trader',
      dominant_outcome: 'cautious',
      belief_distribution: { cautious: 0.42, panic: 0.16, optimistic: 0.18, divided: 0.24 },
      avg_decision_confidence: 0.57,
      velocity_influence: 0.92,
      represented_population: 54000000,
    },
    {
      role_key: 'DOMESTIC_MUTUAL_FUND',
      label: 'Domestic Mutual Fund Manager',
      dominant_outcome: 'cautious',
      belief_distribution: { cautious: 0.53, panic: 0.11, optimistic: 0.19, divided: 0.17 },
      avg_decision_confidence: 0.66,
      velocity_influence: 0.58,
      represented_population: 31000000,
    },
    {
      role_key: 'FII_ANALYST',
      label: 'Foreign Institutional Analyst',
      dominant_outcome: 'panic',
      belief_distribution: { cautious: 0.28, panic: 0.34, optimistic: 0.14, divided: 0.24 },
      avg_decision_confidence: 0.61,
      velocity_influence: 0.74,
      represented_population: 1400000,
    },
    {
      role_key: 'BROKER_RESEARCH_DESK',
      label: 'Broker Research Desk',
      dominant_outcome: 'optimistic',
      belief_distribution: { cautious: 0.31, panic: 0.11, optimistic: 0.39, divided: 0.19 },
      avg_decision_confidence: 0.63,
      velocity_influence: 0.82,
      represented_population: 95000,
    },
    {
      role_key: 'FINANCIAL_MEDIA_EDITOR',
      label: 'Financial Media Editor',
      dominant_outcome: 'divided',
      belief_distribution: { cautious: 0.25, panic: 0.18, optimistic: 0.18, divided: 0.39 },
      avg_decision_confidence: 0.51,
      velocity_influence: 0.88,
      represented_population: 2800,
    },
    {
      role_key: 'CORPORATE_TREASURY',
      label: 'Corporate Treasury',
      dominant_outcome: 'cautious',
      belief_distribution: { cautious: 0.48, panic: 0.17, optimistic: 0.14, divided: 0.21 },
      avg_decision_confidence: 0.62,
      velocity_influence: 0.52,
      represented_population: 62000,
    },
    {
      role_key: 'PRIVATE_BANK_TREASURY',
      label: 'Private Bank Treasury',
      dominant_outcome: 'cautious',
      belief_distribution: { cautious: 0.46, panic: 0.16, optimistic: 0.18, divided: 0.2 },
      avg_decision_confidence: 0.64,
      velocity_influence: 0.55,
      represented_population: 21000,
    },
    {
      role_key: 'PSU_BANK_DESK',
      label: 'PSU Bank Desk',
      dominant_outcome: 'cautious',
      belief_distribution: { cautious: 0.49, panic: 0.12, optimistic: 0.18, divided: 0.21 },
      avg_decision_confidence: 0.59,
      velocity_influence: 0.57,
      represented_population: 120000,
    },
    {
      role_key: 'SECTOR_OPERATING_FIRM',
      label: 'Sector Operating Firm',
      dominant_outcome: 'optimistic',
      belief_distribution: { cautious: 0.3, panic: 0.12, optimistic: 0.4, divided: 0.18 },
      avg_decision_confidence: 0.6,
      velocity_influence: 0.66,
      represented_population: 43000000,
    },
    {
      role_key: 'OPTIONS_FLOW_DESK',
      label: 'Options Flow Desk',
      dominant_outcome: 'divided',
      belief_distribution: { cautious: 0.28, panic: 0.24, optimistic: 0.12, divided: 0.36 },
      avg_decision_confidence: 0.56,
      velocity_influence: 0.91,
      represented_population: 1800,
    },
  ],
}

export const DEMO_SCENARIO = {
  title: 'India Macro Regime Stress Demo',
  subtitle: 'A scripted walkthrough of the full DARSH flow with zero API cost, dense graph memory, expanded cohort simulation, and report generation.',
  topic: 'macro regime stress demo',
  modeTag: 'demo mode',
  graphStats: { entities: 304, relationships: 598, stages: 6 },
  outcomeProbs: {
    cautious: 0.52,
    panic: 0.21,
    divided: 0.17,
    optimistic: 0.1,
  },
  historicalBacktest: {
    predicted: 'cautious',
    actual: 'divided',
    brier: 0.142,
  },
  strengths: [
    'Captures transmission from policy, funding, sentiment, and sector reaction in one shared view.',
    'Shows why domestic funds stay measured even while faster cohorts lean defensive.',
    'Separates headline impulse from slower benchmark-aware capital allocation.',
  ],
  weaknesses: [
    'Fast retail and media layers can still over-amplify downside noise in the opening phase.',
    'Global flow reactions remain sensitive to the chosen shock framing in the demo.',
    'Small cohort splits can make final confidence look tighter than the underlying disagreement.',
  ],
  market: {
    regime: 'uncertainty hold',
    volatility: 'moderate to elevated',
    discoveryWindow: '36-48h',
    vixDirection: 'rising',
    sectors: [
      { id: 'banks', label: 'Banks', score: 0.74, direction: 'mixed', note: 'Rate transmission and credit visibility keep banks active, but positioning stays selective.' },
      { id: 'nbfc', label: 'NBFCs', score: 0.64, direction: 'weak', note: 'Funding-sensitive lenders wobble as spreads and risk filters tighten.' },
      { id: 'autos', label: 'Autos', score: 0.58, direction: 'mixed', note: 'Demand support exists, but input costs and risk appetite blur the near-term read.' },
      { id: 'it', label: 'IT Exporters', score: 0.42, direction: 'steady', note: 'Defensive quality helps, but the demo scenario is more domestic-risk driven.' },
      { id: 'energy', label: 'Energy Importers', score: 0.31, direction: 'weak', note: 'Import-cost pressure and currency sensitivity weigh on the group.' },
    ],
    triggers: {
      strengthens: [
        'If domestic funds absorb the opening shock and benchmark desks re-risk.',
        'If rupee pressure stabilizes while bond yields stop widening.',
        'If policy messaging shifts from caution to transmission confidence.',
      ],
      weakens: [
        'If offshore desks extend the first selloff through the FX channel.',
        'If financial media amplifies a fiscal-stress narrative into broader retail caution.',
        'If private credit and NBFC desks signal funding strain instead of resilience.',
      ],
    },
  },
  toolPreview: [
    {
      tool: 'Sector Lens',
      question: 'Why does the model keep banks active instead of fully risk-off?',
      answer: 'Banks stay active because policy transmission, deposit franchises, and benchmark positioning still support selective buying. The model does not read the shock as a pure balance-sheet crisis.',
      evidence: ['Domestic Mutual Fund Manager stayed cautious, not panicked.', 'Credit Growth and PSU Banks remained central graph hubs.', 'Rising yields hurt weaker lenders more than deposit-rich banks.'],
    },
    {
      tool: 'Cohort View',
      question: 'What is the domestic-fund take in one sentence?',
      answer: 'Domestic funds want proof that the first risk-off impulse is overdone before they add size.',
      evidence: ['Benchmark-aware posture dominated fund discussion.', 'Caution stayed high but never turned into full panic.', 'Fund confidence held near the mid-60% range in the preset script.'],
    },
    {
      tool: 'Counterfactual',
      question: 'What changes if rupee weakness never appears?',
      answer: 'The model shifts toward cautious-to-constructive. Panic falls because offshore stress and import-cost pressure stop reinforcing each other.',
      evidence: ['Rupee is a shared downstream node across banks, energy, and foreign-flow clusters.', 'Dollar-linked edges lose strength in the counterfactual branch.'],
    },
    {
      tool: 'Change Triggers',
      question: 'What single signal would most improve the outlook?',
      answer: 'A visible rotation by domestic funds into benchmark-heavy cyclicals would tighten the optimistic path fastest.',
      evidence: ['Domestic fund absorption is the strongest stabilizing cohort in the scripted run.', 'It reduces both retail fear and media-induced uncertainty loops.'],
    },
  ],
}

export const DEMO_REPORT_STEPS = [
  'Writing executive summary',
  'Scoring predicted outcome',
  'Mapping causal drivers',
  'Synthesizing agent behavior',
  'Capturing dissenting views',
  'Finalizing confidence assessment',
]

export const DEMO_RUNNING_SCRIPT = [
  {
    at: 0,
    title: 'Round 1/8 - retail reaction sweep',
    stage: 'Opening headline shock',
    step: 'Round 1/8 - Retail Trader (RETAIL_TRADER) is pricing the first headline impulse...',
    market_role: 'RETAIL_TRADER',
    focus_terms: ['Retail Traders', 'Nifty 50', 'Consumer Demand', 'Auto Sector', 'Sentiment Loop'],
  },
  {
    at: 3500,
    title: 'Round 2/8 - broker desks rebalance',
    stage: 'Opening interpretation split',
    step: 'Round 2/8 - Broker Research Desk (BROKER_RESEARCH_DESK) is testing whether the first move is exaggerated...',
    market_role: 'BROKER_RESEARCH_DESK',
    focus_terms: ['Corporate India', 'Policy Transmission', 'Risk Narrative', 'Broker', 'Liquidity Conditions'],
  },
  {
    at: 7000,
    title: 'Round 3/8 - domestic funds stay measured',
    stage: 'Institutional validation',
    step: 'Round 3/8 - Domestic Mutual Fund Manager (DOMESTIC_MUTUAL_FUND) is filtering noise before committing capital...',
    market_role: 'DOMESTIC_MUTUAL_FUND',
    focus_terms: ['Domestic Mutual Funds', 'Bank Nifty', 'Bond Yields', 'Liquidity Conditions', 'Fiscal Deficit'],
  },
  {
    at: 10500,
    title: 'Round 4/8 - foreign desks extend stress checks',
    stage: 'Cross-market spillover',
    step: 'Round 4/8 - Foreign Institutional Analyst (FII_ANALYST) is stress-testing the rupee and offshore flow channel...',
    market_role: 'FII_ANALYST',
    focus_terms: ['Foreign Portfolio Flows', 'Dollar Index', 'Rupee', 'Global Risk Desk', 'Singapore Desk'],
  },
  {
    at: 14000,
    title: 'Round 5/8 - bank desks test transmission',
    stage: 'Funding transmission check',
    step: 'Round 5/8 - PSU Bank Desk (PSU_BANK_DESK) is watching whether credit and deposit confidence hold...',
    market_role: 'PSU_BANK_DESK',
    focus_terms: ['PSU Banks', 'Credit Growth', 'Liquidity Conditions', 'Private Credit Desk', 'Mumbai'],
  },
  {
    at: 17000,
    title: 'Round 6/8 - media layer amplifies uncertainty',
    stage: 'Narrative amplification',
    step: 'Round 6/8 - Financial Media Editor (FINANCIAL_MEDIA_EDITOR) is amplifying competing narratives across fast channels...',
    market_role: 'FINANCIAL_MEDIA_EDITOR',
    focus_terms: ['Financial Media', 'Risk Narrative', 'Sentiment Loop', 'Government of India', 'Nifty 50'],
  },
]

export const DEMO_REPORT_MARKDOWN = `# DARSH Demo Report

## Prediction Snapshot

The scripted demo resolves with a **cautious lead**, supported by a visible secondary layer of **panic risk** and **divided interpretation**. The path is not a collapse signal. It is a transmission-stress scenario in which the faster cohorts react first, the domestic benchmark cohorts slow the downside, and the foreign-flow layer keeps uncertainty elevated.

## Executive Summary

The opening impulse is negative because fast participants interpret the shock through liquidity, currency, and funding sensitivity. Domestic funds do not validate a full risk-off cascade. They stay measured, which keeps the final distribution from tipping into outright panic. Financial media and options-style flows widen disagreement, leaving the final regime in an uncertainty-hold state rather than a clean recovery path.

## Market Intelligence

- Banks remain active but selective because credit transmission still matters more than pure fear.
- NBFCs and import-sensitive groups show the weakest resilience.
- The rupee and bond-yield channel keep the foreign-flow layer defensive.
- If domestic funds absorb the shock and benchmark desks re-risk, the optimistic path strengthens quickly.

## Population Model

Retail and media cohorts react first, but domestic mutual funds and treasury desks moderate the final state. Foreign desks and funding-sensitive credit cohorts keep the panic tail alive. The weighted population view therefore lands in cautious territory with meaningful downside vigilance still present.

## Confidence Assessment

Confidence is moderate. The scripted run produces clear transmission logic, but disagreement across global, retail, and media-linked cohorts remains too visible to call the path decisively constructive.
`

function seeded(seed) {
  let hash = 0
  const text = String(seed)
  for (let index = 0; index < text.length; index += 1) {
    hash = ((hash << 5) - hash) + text.charCodeAt(index)
    hash |= 0
  }
  return Math.abs(Math.sin(hash) * 10000) % 1
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value))
}

function makeLabel(cluster, type, index) {
  const profile = CLUSTER_NAMING[cluster.key]
  if (!profile) {
    if (type === 'PERSON') {
      const name = PERSON_NAMES[(index + cluster.label.length * 3) % PERSON_NAMES.length]
      return `${name} ${cluster.label} Desk ${String(index + 1).padStart(2, '0')}`
    }
    if (type === 'ORGANIZATION') {
      return `${cluster.label} Network ${String(index + 1).padStart(2, '0')}`
    }
    if (type === 'EVENT') {
      return `${cluster.label} Event ${String(index + 1).padStart(2, '0')}`
    }
    if (type === 'CONCEPT') {
      return `${cluster.label} Signal ${String(index + 1).padStart(2, '0')}`
    }
    const place = PLACE_NAMES[(index + cluster.label.length) % PLACE_NAMES.length]
    return `${place} ${cluster.label} Hub ${String(index + 1).padStart(2, '0')}`
  }

  if (type === 'PERSON') {
    return profile.people[index % profile.people.length]
  }
  if (type === 'ORGANIZATION') {
    return profile.organizations[index % profile.organizations.length]
  }
  if (type === 'EVENT') {
    return profile.events[index % profile.events.length]
  }
  if (type === 'CONCEPT') {
    return profile.concepts[index % profile.concepts.length]
  }
  return profile.places[index % profile.places.length]
}

function makeDescription(cluster, type, label) {
  const focus = cluster.focusTerms.join(', ')
  return `${label} sits inside the ${cluster.label.toLowerCase()} layer of the demo graph and routes information through ${focus}.`
}

function coreNodePosition(index) {
  const ring = index < 12 ? 0 : 1
  const ringOffset = ring === 0 ? 46 : 118
  const radialStep = ring === 0 ? 11.5 : 14.5
  const angleJitter = (seeded(`core-${index}-theta`) - 0.5) * 0.42
  const angle = GOLDEN_ANGLE * (index + 1) + angleJitter
  const radius = ringOffset + Math.sqrt((ring === 0 ? index : index - 11) + 1) * radialStep
  const jitterX = (seeded(`core-${index}-jx`) - 0.5) * (ring === 0 ? 10 : 14)
  const jitterY = (seeded(`core-${index}-jy`) - 0.5) * (ring === 0 ? 8 : 12)

  return {
    x: clamp(GRAPH_WIDTH / 2 + Math.cos(angle) * radius * 1.05 + jitterX, 52, GRAPH_WIDTH - 52),
    y: clamp(GRAPH_HEIGHT / 2 + Math.sin(angle) * radius * 0.74 + jitterY, 52, GRAPH_HEIGHT - 52),
  }
}

function clusterNodePosition(cluster, clusterIndex, index) {
  const baseAngle = GOLDEN_ANGLE * (index + 1 + clusterIndex * 1.7)
  const angle = baseAngle + (seeded(`${cluster.key}-${index}-theta`) - 0.5) * 0.58
  const radius = 18 + Math.sqrt(index + 1) * 13.2 + seeded(`${cluster.key}-${index}-radius`) * 9.5
  const ellipseX = 0.92 + (seeded(`${cluster.key}-ellipse-x`) - 0.5) * 0.14
  const ellipseY = 0.8 + (seeded(`${cluster.key}-ellipse-y`) - 0.5) * 0.18
  const localJitterX = (seeded(`${cluster.key}-${index}-jx`) - 0.5) * 8
  const localJitterY = (seeded(`${cluster.key}-${index}-jy`) - 0.5) * 7

  return {
    x: clamp(
      cluster.center.x + Math.cos(angle) * radius * ellipseX + localJitterX,
      46,
      GRAPH_WIDTH - 46
    ),
    y: clamp(
      cluster.center.y + Math.sin(angle) * radius * ellipseY + localJitterY,
      46,
      GRAPH_HEIGHT - 46
    ),
  }
}

function rebalanceDemoGraphNodes(nodes) {
  const coreIds = new Set(CORE_NODES.map(node => node.id))
  const working = nodes.map(node => ({
    ...node,
    anchorX: node.x,
    anchorY: node.y,
    mobility: coreIds.has(node.id) ? 0.34 : 1,
    anchorPull: coreIds.has(node.id) ? 0.1 : 0.16,
  }))

  const minGap = 20
  const margin = 44
  const iterations = 38

  for (let iter = 0; iter < iterations; iter += 1) {
    for (let i = 0; i < working.length; i += 1) {
      for (let j = i + 1; j < working.length; j += 1) {
        const a = working[i]
        const b = working[j]
        const dx = a.x - b.x
        const dy = a.y - b.y
        const distance = Math.sqrt(dx * dx + dy * dy) || 0.001
        const desiredGap = minGap + (a.type === 'PLACE' || b.type === 'PLACE' ? 2.2 : 0) + (a.type === b.type ? 0.6 : 0)

        if (distance >= desiredGap) continue

        const overlap = (desiredGap - distance) / desiredGap
        const ux = dx / distance
        const uy = dy / distance
        const force = overlap * 1.14

        a.x += ux * force * a.mobility
        a.y += uy * force * a.mobility
        b.x -= ux * force * b.mobility
        b.y -= uy * force * b.mobility
      }
    }

    working.forEach(node => {
      node.x += (node.anchorX - node.x) * node.anchorPull
      node.y += (node.anchorY - node.y) * node.anchorPull
      node.x = clamp(node.x, margin, GRAPH_WIDTH - margin)
      node.y = clamp(node.y, margin, GRAPH_HEIGHT - margin)
    })
  }

  return working.map(({ anchorX, anchorY, mobility, anchorPull, ...node }) => node)
}

function buildDemoKnowledgeGraph() {
  const nodes = CORE_NODES.map((node, index) => ({
    ...node,
    ...coreNodePosition(index),
  }))

  const links = []
  const nodeIndex = new Map(nodes.map(node => [node.id, node]))

  const addNode = (node) => {
    if (nodeIndex.has(node.id)) return
    nodeIndex.set(node.id, node)
    nodes.push(node)
  }

  const linkKeys = new Set()
  const addLink = (source, target, relation, inferred = false) => {
    if (!nodeIndex.has(source) || !nodeIndex.has(target)) return
    const key = `${source}|${target}|${relation}|${inferred ? '1' : '0'}`
    if (linkKeys.has(key)) return
    linkKeys.add(key)
    links.push({
      source,
      target,
      relation,
      inferred,
      weight: inferred ? 0.58 : 0.92,
    })
  }

  CLUSTERS.forEach((cluster, clusterIndex) => {
    const created = []
    for (let i = 0; i < 34; i += 1) {
      const type = ['PERSON', 'ORGANIZATION', 'EVENT', 'CONCEPT', 'PLACE'][i % 5]
      const label = makeLabel(cluster, type, i)
      const { x, y } = clusterNodePosition(cluster, clusterIndex, i)

      const node = {
        id: label,
        type,
        description: makeDescription(cluster, type, label),
        x,
        y,
      }
      addNode(node)
      created.push(label)
    }

    created.forEach((label, index) => {
      const primaryHub = cluster.hubs[index % cluster.hubs.length]
      const secondaryHub = cluster.hubs[(index + 2) % cluster.hubs.length]
      addLink(primaryHub, label, RELATIONS[index % RELATIONS.length], false)
      if (index % 2 === 0) {
        addLink(label, created[(index + 7) % created.length], RELATIONS[(index + 3) % RELATIONS.length], true)
      }
      if (index % 3 === 0) {
        addLink(label, secondaryHub, RELATIONS[(index + 5) % RELATIONS.length], false)
      }
      if (index % 5 === 0) {
        const neighborCluster = CLUSTERS[(clusterIndex + 1) % CLUSTERS.length]
        addLink(label, neighborCluster.hubs[index % neighborCluster.hubs.length], RELATIONS[(index + 1) % RELATIONS.length], true)
      }
    })
  })

  const coreNetwork = [
    ['Reserve Bank of India', 'Policy Transmission'],
    ['Reserve Bank of India', 'Liquidity Conditions'],
    ['Reserve Bank of India', 'Bond Yields'],
    ['Government of India', 'Fiscal Deficit'],
    ['Government of India', 'Ministry of Finance'],
    ['Government of India', 'Corporate India'],
    ['Ministry of Finance', 'Policy Transmission'],
    ['Nifty 50', 'Bank Nifty'],
    ['Nifty 50', 'Retail Traders'],
    ['Bank Nifty', 'PSU Banks'],
    ['Corporate India', 'Auto Sector'],
    ['Domestic Mutual Funds', 'Nifty 50'],
    ['Domestic Mutual Funds', 'Corporate India'],
    ['Foreign Portfolio Flows', 'Rupee'],
    ['Foreign Portfolio Flows', 'Global Risk Desk'],
    ['Rupee', 'Energy Import Bill'],
    ['Bond Yields', 'Fiscal Deficit'],
    ['Liquidity Conditions', 'Credit Growth'],
    ['Inflation Path', 'Bond Yields'],
    ['Inflation Path', 'Rupee'],
    ['Credit Growth', 'PSU Banks'],
    ['NBFC Basket', 'Private Credit Desk'],
    ['Risk Narrative', 'Sentiment Loop'],
    ['Financial Media', 'Risk Narrative'],
    ['Retail Traders', 'Sentiment Loop'],
    ['Consumer Demand', 'Auto Sector'],
    ['Mumbai', 'PSU Banks'],
    ['Delhi', 'Government of India'],
    ['Bengaluru', 'Corporate India'],
    ['Singapore Desk', 'Foreign Portfolio Flows'],
  ]

  coreNetwork.forEach(([source, target], index) => {
    addLink(source, target, RELATIONS[index % RELATIONS.length], false)
    if (index % 4 === 0) addLink(target, source, RELATIONS[(index + 2) % RELATIONS.length], true)
  })

  const redistributedNodes = rebalanceDemoGraphNodes(nodes)

  return {
    cacheKey: 'demo-dense-market-graph',
    node_count: redistributedNodes.length,
    link_count: links.length,
    nodes: redistributedNodes,
    links,
    causal_links: [],
  }
}

export const DEMO_GRAPH_DATA = buildDemoKnowledgeGraph()
export const DEMO_GRAPH_NAME = 'demo_dense_market_graph'
export const DEMO_POPULATION = DEMO_POPULATION_MODEL
export const DEMO_CONFIG_PRESET = DEMO_CONFIG

DEMO_SCENARIO.graphStats.entities = DEMO_GRAPH_DATA.node_count
DEMO_SCENARIO.graphStats.relationships = DEMO_GRAPH_DATA.link_count
