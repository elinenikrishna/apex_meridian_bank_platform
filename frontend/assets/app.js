const platform = {
  kpis: {
    transaction_volume_7d: 128450982,
    transaction_amount_7d: 18742550913.42,
    fraud_loss_avoided_7d: 24840150.25,
    confirmed_fraud_rate_bps: 18.7,
    chargeback_rate_bps: 31.4,
    active_customers: 8420000,
    high_risk_merchants: 183,
    pipeline_sla_percent: 99.63,
    gold_quality_score: 98.4,
    ai_reports_validated: 42
  },
  fraudTrend: [
    { day: "Mon", alerts: 18124, confirmed: 1921, loss: 3.52 },
    { day: "Tue", alerts: 20418, confirmed: 2142, loss: 3.94 },
    { day: "Wed", alerts: 22672, confirmed: 2433, loss: 4.31 },
    { day: "Thu", alerts: 21809, confirmed: 2351, loss: 4.02 },
    { day: "Fri", alerts: 26791, confirmed: 3128, loss: 5.83 },
    { day: "Sat", alerts: 23964, confirmed: 2710, loss: 4.78 },
    { day: "Sun", alerts: 18731, confirmed: 1904, loss: 3.21 }
  ],
  merchantRisk: [
    { category: "Cross-border luxury resale", risk_score: 94, volume_delta_pct: 18.6 },
    { category: "Digital gaming marketplaces", risk_score: 91, volume_delta_pct: 22.1 },
    { category: "Expedited travel brokers", risk_score: 88, volume_delta_pct: 14.4 },
    { category: "Electronics repair aggregators", risk_score: 83, volume_delta_pct: 9.9 }
  ],
  regions: [
    { region: "Northeast", risk_score: 72, chargeback_delta_pct: 4.8 },
    { region: "Southeast", risk_score: 79, chargeback_delta_pct: 8.2 },
    { region: "Midwest", risk_score: 61, chargeback_delta_pct: -1.7 },
    { region: "West", risk_score: 84, chargeback_delta_pct: 11.5 }
  ],
  segments: [
    { segment: "Meridian Prime", customers: 920000, avg_balance: 84300, risk: 21 },
    { segment: "Apex Everyday", customers: 4800000, avg_balance: 7950, risk: 44 },
    { segment: "Summit Credit Builder", customers: 1970000, avg_balance: 2140, risk: 63 },
    { segment: "Horizon Small Business", customers: 730000, avg_balance: 31600, risk: 38 }
  ],
  behavior: [
    { metric: "mobile wallet spend", change_pct: 12.8 },
    { metric: "cash advance frequency", change_pct: 3.4 },
    { metric: "loan autopay adoption", change_pct: 5.9 },
    { metric: "reward redemption value", change_pct: 8.1 }
  ],
  jobs: [
    { name: "daily_batch_ingestion", status: "healthy", sla: "met", duration_min: 18 },
    { name: "stream_checkpoint_validation", status: "healthy", sla: "met", duration_min: 4 },
    { name: "bronze_to_silver_transform", status: "healthy", sla: "met", duration_min: 31 },
    { name: "silver_to_gold_kpi_publish", status: "healthy", sla: "met", duration_min: 12 },
    { name: "fraud_model_scoring", status: "watch", sla: "met", duration_min: 16 },
    { name: "ai_report_validation", status: "healthy", sla: "met", duration_min: 6 }
  ],
  layers: [
    { layer: "Bronze", records_7d: 142900441, partitions: 168, retention_days: 730, copy: "Immutable raw events, CDC snapshots, and replayable Kafka payloads." },
    { layer: "Silver", records_7d: 139730205, partitions: 168, retention_days: 365, copy: "Validated, deduplicated, masked, enriched, and conformed records." },
    { layer: "Gold", records_7d: 18420991, partitions: 84, retention_days: 2555, copy: "Governed KPIs, dimensional marts, regulatory aggregates, and AI-approved context." }
  ],
  policies: [
    { id: "PII-001", name: "Customer direct identifier masking", status: "active", owner: "Data Governance Office" },
    { id: "RBAC-004", name: "Gold-layer executive metrics access", status: "active", owner: "Platform Security" },
    { id: "AI-007", name: "Cited-answer enforcement", status: "active", owner: "AI Risk Council" },
    { id: "RET-009", name: "Seven-year regulatory KPI retention", status: "active", owner: "Compliance Engineering" }
  ],
  lineage: [
    "mysql.core_customers",
    "postgres.card_authorizations",
    "kafka.card.transactions.raw",
    "bronze.transactions_raw",
    "silver.card_transactions",
    "gold.fraud_daily_kpis",
    "warehouse.executive_risk_mart",
    "vector.governed_metric_context",
    "ai.weekly_risk_report"
  ],
  quality: [
    { dataset: "gold.fraud_daily_kpis", score: 99.1, failed_rules: 0, freshness_minutes: 11 },
    { dataset: "gold.customer_360", score: 98.8, failed_rules: 1, freshness_minutes: 22 },
    { dataset: "silver.card_transactions", score: 97.4, failed_rules: 3, freshness_minutes: 7 },
    { dataset: "silver.loan_payments", score: 98.2, failed_rules: 1, freshness_minutes: 18 },
    { dataset: "bronze.fraud_alerts_raw", score: 96.7, failed_rules: 2, freshness_minutes: 3 }
  ],
  audit: [
    { event_id: "audit-20260616-0001", actor: "airflow:fraud_model_scoring", action: "score_transactions", dataset: "silver.card_transactions", status: "success", timestamp: "2026-06-16T08:41:18Z" },
    { event_id: "audit-20260616-0002", actor: "ai-agent:weekly_report", action: "validate_report_metrics", dataset: "gold.fraud_daily_kpis", status: "success", timestamp: "2026-06-16T08:55:04Z" },
    { event_id: "audit-20260616-0003", actor: "api:risk_executive", action: "ask_governed_chatbot", dataset: "vector.governed_metric_context", status: "success", timestamp: "2026-06-16T09:02:31Z" }
  ]
};

const fmt = new Intl.NumberFormat("en-US");
const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

function showView(id) {
  document.querySelectorAll(".view").forEach(view => view.classList.toggle("active", view.id === id));
  document.querySelectorAll(".nav button").forEach(button => button.classList.toggle("active", button.dataset.view === id));
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.querySelectorAll("[data-view]").forEach(button => {
  button.addEventListener("click", () => showView(button.dataset.view));
});

document.querySelectorAll("[data-jump]").forEach(button => {
  button.addEventListener("click", () => showView(button.dataset.jump));
});

function renderMetrics() {
  const metrics = [
    ["Transaction volume", fmt.format(platform.kpis.transaction_volume_7d), "Seven-day authorized activity"],
    ["Transaction amount", money.format(platform.kpis.transaction_amount_7d), "Portfolio card movement"],
    ["Loss avoided", money.format(platform.kpis.fraud_loss_avoided_7d), "Fraud controls impact"],
    ["Confirmed fraud", `${platform.kpis.confirmed_fraud_rate_bps} bps`, "Validated against Gold KPIs"],
    ["Chargebacks", `${platform.kpis.chargeback_rate_bps} bps`, "Network dispute rate"],
    ["Active customers", fmt.format(platform.kpis.active_customers), "Customer 360 population"],
    ["High-risk merchants", fmt.format(platform.kpis.high_risk_merchants), "Enhanced monitoring"],
    ["AI reports", fmt.format(platform.kpis.ai_reports_validated), "Cited and validated"]
  ];
  document.getElementById("executiveMetrics").innerHTML = metrics.map(([label, value, note]) => `
    <article class="metric"><span>${label}</span><strong>${value}</strong><em>${note}</em></article>
  `).join("");
}

function renderFraudTrend() {
  const maxAlerts = Math.max(...platform.fraudTrend.map(item => item.alerts));
  document.getElementById("fraudTrendChart").innerHTML = platform.fraudTrend.map(item => `
    <div class="bar">
      <i style="height:${Math.round((item.alerts / maxAlerts) * 260)}px"></i>
      <span>${item.day}<br>${fmt.format(item.alerts)}</span>
    </div>
  `).join("");
}

function drawDonut() {
  const canvas = document.getElementById("riskDonut");
  if (!canvas) return;
  const context = canvas.getContext("2d");
  const parts = [
    { value: 58, color: "#00796b" },
    { value: 28, color: "#c89120" },
    { value: 14, color: "#a63d54" }
  ];
  let start = -Math.PI / 2;
  context.clearRect(0, 0, canvas.width, canvas.height);
  parts.forEach(part => {
    const angle = (part.value / 100) * Math.PI * 2;
    context.beginPath();
    context.moveTo(130, 130);
    context.arc(130, 130, 108, start, start + angle);
    context.closePath();
    context.fillStyle = part.color;
    context.fill();
    start += angle;
  });
  context.beginPath();
  context.arc(130, 130, 68, 0, Math.PI * 2);
  context.fillStyle = "#ffffff";
  context.fill();
  context.fillStyle = "#16201f";
  context.font = "700 30px Inter, sans-serif";
  context.textAlign = "center";
  context.fillText("18.7", 130, 126);
  context.font = "600 13px Inter, sans-serif";
  context.fillStyle = "#64716f";
  context.fillText("fraud bps", 130, 150);
}

function renderTables() {
  document.getElementById("merchantRiskTable").innerHTML = table(
    ["Category", "Risk score", "Volume delta"],
    platform.merchantRisk.map(item => [item.category, item.risk_score, `${item.volume_delta_pct}%`])
  );
  document.getElementById("qualityTable").innerHTML = table(
    ["Dataset", "Score", "Failed rules", "Freshness"],
    platform.quality.map(item => [item.dataset, `${item.score}%`, item.failed_rules, `${item.freshness_minutes} min`])
  );
}

function table(headers, rows) {
  return `
    <table>
      <thead><tr>${headers.map(header => `<th>${header}</th>`).join("")}</tr></thead>
      <tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody>
    </table>
  `;
}

function renderFraudDetails() {
  document.getElementById("regionalRisk").innerHTML = platform.regions.map(item => `
    <div>
      <strong>${item.region}</strong>
      <span>${item.risk_score} risk score, ${item.chargeback_delta_pct}% chargeback delta</span>
      <div class="progress"><i style="width:${item.risk_score}%"></i></div>
    </div>
  `).join("");
}

function renderCustomer() {
  document.getElementById("customerSegments").innerHTML = platform.segments.map(segment => `
    <article class="segment-card">
      <strong>${segment.segment}</strong>
      <span>${fmt.format(segment.customers)} customers</span>
      <div class="progress"><i style="width:${Math.max(12, 100 - segment.risk)}%"></i></div>
      <span>${money.format(segment.avg_balance)} average balance</span>
    </article>
  `).join("");
  document.getElementById("behaviorChanges").innerHTML = platform.behavior.map(item => `
    <div>
      <strong>${item.metric}</strong>
      <span>${item.change_pct}%</span>
      <div class="progress"><i style="width:${Math.min(100, item.change_pct * 5)}%"></i></div>
    </div>
  `).join("");
  updateRiskProfile("CUST-0000421052");
}

function updateRiskProfile(customerId) {
  const seed = customerId.split("").reduce((sum, char) => sum + char.charCodeAt(0), 0) % 100;
  const segment = platform.segments[seed % platform.segments.length];
  document.getElementById("riskProfile").innerHTML = `
    <span>${customerId}</span>
    <strong>${seed}</strong>
    <span>${segment.segment}</span>
    <div class="progress"><i style="width:${seed}%"></i></div>
    <span>Signals: transaction velocity, merchant shift, device consistency</span>
  `;
}

document.getElementById("customerSearch").addEventListener("change", event => {
  updateRiskProfile(event.target.value || "CUST-0000421052");
});

function renderPipelines() {
  document.getElementById("pipelineBoard").innerHTML = platform.jobs.map(job => {
    const width = job.status === "healthy" ? 96 : 78;
    return `
      <article class="pipeline-card">
        <strong>${job.name.replaceAll("_", " ")}</strong>
        <span>${job.status} · SLA ${job.sla} · ${job.duration_min} min</span>
        <div class="progress"><i style="width:${width}%"></i></div>
      </article>
    `;
  }).join("");
}

function renderLakehouse() {
  document.getElementById("lakehouseLayers").innerHTML = platform.layers.map(layer => `
    <article class="layer-card">
      <strong>${layer.layer}</strong>
      <span>${fmt.format(layer.records_7d)} records in 7 days</span>
      <p>${layer.copy}</p>
      <span>${layer.partitions} partitions · ${fmt.format(layer.retention_days)} days retention</span>
    </article>
  `).join("");
}

function renderGovernance() {
  document.getElementById("policyGrid").innerHTML = platform.policies.map(policy => `
    <article class="policy-card">
      <strong>${policy.id}</strong>
      <span>${policy.name}</span>
      <p>${policy.owner}</p>
      <div class="status-pill good">${policy.status}</div>
    </article>
  `).join("");
}

function answerLocally(question) {
  const q = question.toLowerCase();
  const topics = ["fraud", "merchant", "transaction", "customer", "chargeback", "regional", "quality", "pipeline", "kpi"];
  if (!topics.some(topic => q.includes(topic))) {
    return {
      refused: true,
      answer: "I can only answer from governed Gold Layer metrics and approved metadata. This question requires an approved dataset that is not indexed yet.",
      citations: []
    };
  }
  if (q.includes("merchant")) {
    const top = platform.merchantRisk[0];
    return {
      refused: false,
      answer: `${top.category} is the highest-risk merchant category with risk score ${top.risk_score} and volume delta ${top.volume_delta_pct}%.`,
      citations: ["gold.merchant_risk_kpis"]
    };
  }
  if (q.includes("quality") || q.includes("pipeline")) {
    return {
      refused: false,
      answer: `Gold quality is ${platform.kpis.gold_quality_score}% and the pipeline SLA is ${platform.kpis.pipeline_sla_percent}%.`,
      citations: ["gold.data_quality_scorecards", "gold.pipeline_observability"]
    };
  }
  return {
    refused: false,
    answer: `Confirmed fraud is ${platform.kpis.confirmed_fraud_rate_bps} bps, seven-day transaction volume is ${fmt.format(platform.kpis.transaction_volume_7d)}, and loss avoided is ${money.format(platform.kpis.fraud_loss_avoided_7d)}.`,
    citations: ["gold.fraud_daily_kpis", "warehouse.executive_risk_mart"]
  };
}

function addMessage(text, type = "assistant", citations = []) {
  const node = document.createElement("div");
  node.className = `message ${type}`;
  node.innerHTML = `${text}${citations.length ? `<small>Citations: ${citations.join(", ")}</small>` : ""}`;
  document.getElementById("chatWindow").appendChild(node);
}

document.getElementById("chatForm").addEventListener("submit", async event => {
  event.preventDefault();
  const input = document.getElementById("chatInput");
  const question = input.value.trim();
  if (!question) return;
  addMessage(question, "user");
  const response = answerLocally(question);
  addMessage(response.answer, response.refused ? "assistant refused" : "assistant", response.citations);
});

function renderReport() {
  document.getElementById("reportPreview").innerHTML = `
    <p class="eyebrow">Generated Preview</p>
    <h3>Apex Meridian Weekly Executive Risk Report</h3>
    <p>Transaction volume reached ${fmt.format(platform.kpis.transaction_volume_7d)} with ${money.format(platform.kpis.fraud_loss_avoided_7d)} in fraud loss avoided. All narrative claims are checked against governed Gold metrics before release.</p>
    <table>
      <tbody>
        <tr><th>Validation</th><td>validated_against_gold_layer</td></tr>
        <tr><th>Prompt version</th><td>amip-reporting-v1.3</td></tr>
        <tr><th>Citations</th><td>gold.fraud_daily_kpis, warehouse.executive_risk_mart, gold.data_quality_scorecards</td></tr>
      </tbody>
    </table>
  `;
}

document.getElementById("generateReport").addEventListener("click", renderReport);

function renderLineage() {
  document.getElementById("lineageGraph").innerHTML = platform.lineage.map((node, index) => `
    <article class="lineage-node">
      <strong>${node}</strong>
      <span>${index === 0 ? "source" : index === platform.lineage.length - 1 ? "AI output" : `step ${index}`}</span>
    </article>
  `).join("");
}

function renderAudit() {
  document.getElementById("auditLog").innerHTML = platform.audit.map(event => `
    <div class="audit-item">
      <strong>${event.action}</strong>
      <span>${event.actor} · ${event.dataset} · ${event.status}</span>
      <span>${event.timestamp}</span>
    </div>
  `).join("");
}

function animateHero() {
  const canvas = document.getElementById("heroCanvas");
  const context = canvas.getContext("2d");
  const resize = () => {
    canvas.width = canvas.offsetWidth * window.devicePixelRatio;
    canvas.height = canvas.offsetHeight * window.devicePixelRatio;
    context.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);
  };
  resize();
  window.addEventListener("resize", resize);
  let tick = 0;
  const draw = () => {
    const width = canvas.offsetWidth;
    const height = canvas.offsetHeight;
    context.clearRect(0, 0, width, height);
    context.fillStyle = "#26302f";
    context.fillRect(0, 0, width, height);
    context.strokeStyle = "rgba(244, 209, 154, 0.2)";
    context.lineWidth = 1;
    for (let x = -120; x < width + 120; x += 64) {
      context.beginPath();
      context.moveTo(x + (tick % 64), 0);
      context.lineTo(x - 180 + (tick % 64), height);
      context.stroke();
    }
    const lanes = 8;
    for (let lane = 0; lane < lanes; lane += 1) {
      const y = 48 + lane * (height - 96) / lanes;
      context.strokeStyle = lane % 3 === 0 ? "rgba(0, 121, 107, 0.7)" : "rgba(255,255,255,0.15)";
      context.beginPath();
      context.moveTo(0, y);
      for (let x = 0; x <= width; x += 28) {
        context.lineTo(x, y + Math.sin((x + tick * (lane + 1)) / 48) * 16);
      }
      context.stroke();
    }
    for (let i = 0; i < 46; i += 1) {
      const x = (i * 83 + tick * (1 + (i % 5) * 0.18)) % width;
      const y = 38 + ((i * 47) % Math.max(120, height - 76));
      context.fillStyle = i % 4 === 0 ? "#f4d19a" : i % 3 === 0 ? "#b66b2b" : "#5bb7a8";
      context.fillRect(x, y, 5, 5);
    }
    tick += 0.8;
    requestAnimationFrame(draw);
  };
  draw();
}

function boot() {
  renderMetrics();
  renderFraudTrend();
  drawDonut();
  renderTables();
  renderFraudDetails();
  renderCustomer();
  renderPipelines();
  renderLakehouse();
  renderGovernance();
  renderReport();
  renderLineage();
  renderAudit();
  addMessage("Gold context is ready. Fraud trends, merchant risk, Customer 360, pipeline health, and data quality scorecards are indexed for this session.", "assistant");
  animateHero();
}

document.getElementById("refreshKpis").addEventListener("click", renderMetrics);
boot();
