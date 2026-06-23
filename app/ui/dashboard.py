from __future__ import annotations


def dashboard_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Hardline OpsAgent Core</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 0; background: #0b1020; color: #eef2ff; }
    header { padding: 28px 32px; background: linear-gradient(135deg, #111827, #1f2937); border-bottom: 1px solid #334155; }
    main { padding: 28px 32px; max-width: 1180px; margin: 0 auto; }
    h1 { margin: 0 0 8px; font-size: 32px; }
    p { color: #cbd5e1; line-height: 1.5; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 20px; }
    .card { background: #111827; border: 1px solid #334155; border-radius: 14px; padding: 18px; box-shadow: 0 8px 28px rgba(0,0,0,.22); }
    .big { font-size: 38px; font-weight: 800; margin: 6px 0; }
    .ok { color: #22c55e; }
    .warn { color: #f59e0b; }
    .bad { color: #ef4444; }
    button { background: #2563eb; border: 0; color: white; font-weight: 700; padding: 12px 16px; border-radius: 10px; cursor: pointer; margin: 4px 6px 4px 0; }
    button:hover { background: #1d4ed8; }
    button.secondary { background: #334155; }
    button.secondary:hover { background: #475569; }
    button.danger { background: #7f1d1d; }
    button.danger:hover { background: #991b1b; }
    code { color: #bfdbfe; }
    pre { white-space: pre-wrap; background: #020617; color: #dbeafe; padding: 16px; border-radius: 12px; border: 1px solid #1e293b; overflow-x: auto; }
    a { color: #93c5fd; }
    .muted { color: #94a3b8; font-size: 13px; }
  </style>
</head>
<body>
<header>
  <h1>Hardline OpsAgent Core</h1>
  <p>Docker-deployable AI operations assistant. Mock/offline by default. Turn system and container state into health reports, runbooks, tickets, and proof.</p>
</header>
<main>
  <div class="grid">
    <section class="card">
      <h2>Status</h2>
      <div id="status" class="big warn">checking</div>
      <p id="provider" class="muted">provider unknown</p>
    </section>
    <section class="card">
      <h2>Run Analysis</h2>
      <p>Collect live state, score health, and generate a Markdown ops report.</p>
      <button onclick="runAnalyze()">Run analysis</button>
    </section>
    <section class="card">
      <h2>Reports</h2>
      <p>Generated reports are stored in <code>data/reports</code> and can be opened below.</p>
      <button onclick="loadReports()">Refresh reports</button>
      <div id="reports"></div>
    </section>
    <section class="card">
      <h2>GitHub Issues</h2>
      <p>Create a GitHub issue from the latest report. Safe dry-run mode is the default.</p>
      <p id="issueStatus" class="muted">issue connector unknown</p>
      <button class="secondary" onclick="issueDryRun()">Preview issue</button>
      <button class="danger" onclick="issueCreate()">Create issue</button>
    </section>
  </div>

  <section class="card" style="margin-top:16px;">
    <h2>Latest Result</h2>
    <pre id="output">No analysis run yet.</pre>
  </section>
</main>
<script>
async function checkHealth() {
  try {
    const res = await fetch('/health');
    const data = await res.json();
    document.getElementById('status').textContent = data.status || 'unknown';
    document.getElementById('status').className = 'big ok';
    document.getElementById('provider').textContent = 'LLM provider: ' + data.llm_provider;
  } catch (e) {
    document.getElementById('status').textContent = 'offline';
    document.getElementById('status').className = 'big bad';
  }
}

async function checkIssueStatus() {
  try {
    const res = await fetch('/issues/status');
    const data = await res.json();
    document.getElementById('issueStatus').textContent =
      'enabled=' + data.enabled + ' dry_run=' + data.dry_run + ' repo_configured=' + data.repo_configured;
  } catch (e) {
    document.getElementById('issueStatus').textContent = 'issue connector offline';
  }
}

async function runAnalyze() {
  document.getElementById('output').textContent = 'Running analysis...';
  const res = await fetch('/analyze');
  const data = await res.json();
  document.getElementById('output').textContent = JSON.stringify(data, null, 2);
  await loadReports();
}

async function loadReports() {
  const res = await fetch('/reports');
  const data = await res.json();
  const box = document.getElementById('reports');
  if (!data.reports || data.reports.length === 0) {
    box.innerHTML = '<p class="muted">No reports yet.</p>';
    return;
  }
  box.innerHTML = '<ul>' + data.reports.map(r => `<li><a href="/reports/${r.name}" target="_blank">${r.name}</a></li>`).join('') + '</ul>';
}

async function issueDryRun() {
  document.getElementById('output').textContent = 'Building issue preview...';
  const res = await fetch('/issues/dry-run', {method: 'POST'});
  const data = await res.json();
  document.getElementById('output').textContent = JSON.stringify(data, null, 2);
}

async function issueCreate() {
  document.getElementById('output').textContent = 'Requesting issue creation...';
  const res = await fetch('/issues/create', {method: 'POST'});
  const data = await res.json();
  document.getElementById('output').textContent = JSON.stringify(data, null, 2);
  await checkIssueStatus();
}

checkHealth();
checkIssueStatus();
loadReports();
</script>
</body>
</html>"""
