// app.js - UI logic and backend integration
// (Updated: initializes from GET /status)

const API_BASE = ""; // same origin

// UI elements
const btnBlockchain = document.getElementById("btnBlockchain");
const btnNewBlock = document.getElementById("btnNewBlock");
const btnLastBlock = document.getElementById("btnLastBlock");
const output = document.getElementById("output");
const lastAction = document.getElementById("lastAction");

const ddmToggle = document.getElementById("ddmToggle");
const ddmControls = document.getElementById("ddmControls");
// const ddmSubstatus = document.getElementById("ddmSubstatus");
// const globalMode = document.getElementById("globalMode");

const timeoutDisplay = document.getElementById("timeoutDisplay");
const timeoutInput = document.getElementById("timeoutInput");
const btnSetTimeout = document.getElementById("btnSetTimeout");

const btnAuto = document.getElementById("btnAuto");
const btnSetManual = document.getElementById("btnSetManual");
const manualDifficulty = document.getElementById("manualDifficulty");

// Local UI state (will be initialized from server /status)
let state = {
  ddmEnabled: false,
  ddmMode: "auto",
  timeout: 60,
  difficulty: 1,
};

// Helpers
function setOutput(text, append = false) {
  if (!append) output.textContent = text;
  else output.textContent += "\n" + text;
}
function setLastAction(text) {
  if (lastAction) lastAction.textContent = text;
}
function errToOutput(e) {
  setOutput("Error: " + (e.message || e));
  setLastAction("Error");
}

// Fetch helpers
async function apiGet(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${res.statusText} - ${txt}`);
  }
  // some endpoints return plain text on error; try json
  try {
    return await res.json();
  } catch {
    return {};
  }
}

async function apiPost(path) {
  const res = await fetch(API_BASE + path, { method: "POST" });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${res.statusText} - ${txt}`);
  }
  try {
    return await res.json();
  } catch {
    return {};
  }
}

// UI update functions
function showDDMControls(show) {
  if (ddmControls) ddmControls.style.display = show ? "block" : "none";
}

function updateModeLabels() {
  // if (globalMode) globalMode.textContent = state.ddmEnabled ? "DDM" : "Standard";
  // if (ddmSubstatus) ddmSubstatus.textContent = state.ddmEnabled ? `DDM: Enabled (${state.ddmMode})` : "DDM: Disabled";
  if (ddmToggle) ddmToggle.checked = !!state.ddmEnabled;
  showDDMControls(!!state.ddmEnabled);

  // update timeout UI
  if (timeoutDisplay) timeoutDisplay.textContent = state.timeout;
  if (timeoutInput) timeoutInput.value = state.timeout;
}

// Initialize from server /status
async function init() {
  setOutput("Initializing from server...");
  setLastAction("Initializing");
  try {
    const s = await apiGet("/status");
    // Expecting { ddm_enabled, ddm_mode, timeout, difficulty, failed_difficulty }
    state.ddmEnabled = !!s.ddm_enabled;
    state.ddmMode = s.ddm_mode || "auto";
    state.timeout = s.timeout || state.timeout;
    state.difficulty = s.difficulty || state.difficulty;
    updateModeLabels();

    setOutput(`Status loaded from server.\nDDM: ${state.ddmEnabled} (${state.ddmMode})\nTimeout: ${state.timeout}s\nDifficulty: ${state.difficulty}`);
    setLastAction("Ready");
  } catch (err) {
    // If /status not available, fallback to defaults
    setOutput("Could not fetch /status from server. Falling back to defaults.\n" + (err.message || err));
    setLastAction("Init failed (fallback)");
    updateModeLabels();
  }
}

init();

// Events
if (ddmToggle) ddmToggle.addEventListener("change", async (e) => {
  try {
    if (e.target.checked) {
      await apiPost("/difficulty/enable");
      state.ddmEnabled = true;
      state.ddmMode = "auto";
      setOutput("Dynamic Difficulty Mode enabled.");
      setLastAction("Enabled DDM");
    } else {
      await apiPost("/difficulty/disable");
      state.ddmEnabled = false;
      state.ddmMode = "auto";
      setOutput("Dynamic Difficulty Mode disabled. Back to Standard Mode.");
      setLastAction("Disabled DDM");
    }
    updateModeLabels();
  } catch (err) {
    errToOutput(err);
    // revert UI toggle
    e.target.checked = !e.target.checked;
  }
});

if (btnBlockchain) btnBlockchain.addEventListener("click", async () => {
  setLastAction("Fetching blockchain...");
  try {
    const data = await apiGet("/blockchain/");
    setOutput(JSON.stringify(data.blockchain || data, null, 2));
    setLastAction("Fetched blockchain");
  } catch (err) {
    errToOutput(err);
  }
});

if (btnLastBlock) btnLastBlock.addEventListener("click", async () => {
  setLastAction("Fetching last block...");
  try {
    const block = await apiGet("/blockchain/last-block");
    setOutput(JSON.stringify(block || {}, null, 2));
    setLastAction("Fetched last block");
  } catch (err) {
    errToOutput(err);
  }
});

if (btnNewBlock) btnNewBlock.addEventListener("click", async () => {
  setLastAction("Adding new block...");
  try {
    const res = await apiPost("/blockchain/add");
    if (res.error) {
      setOutput("Block mining failed: " + JSON.stringify(res, null, 2));
      setLastAction("Block mining failed");
      // optionally update failed_difficulty display if server returns it
      return;
    }
    setOutput("Block add response:\n" + JSON.stringify(res, null, 2));
    setLastAction("Block added, fetching last block...");
    // fetch last block to display actual stored block
    const last = await apiGet("/blockchain/last-block");
    setOutput(JSON.stringify(last || {}, null, 2));
    setLastAction("Last block displayed");
    // refresh server state (timeout/difficulty) after successful add
    try {
      const s = await apiGet("/status");
      state.timeout = s.timeout || state.timeout;
      state.difficulty = s.difficulty || state.difficulty;
      updateModeLabels();
    } catch (_) { /* ignore */ }
  } catch (err) {
    errToOutput(err);
  }
});

if (btnSetTimeout) btnSetTimeout.addEventListener("click", async () => {
  const v = Number(timeoutInput.value);
  if (!v || v < 10 || v > 300) {
    alert("Timeout must be a number between 10 and 300 seconds.");
    return;
  }
  setLastAction("Setting timeout...");
  try {
    await apiPost(`/mining/set-timeout/${v}`);
    state.timeout = v;
    timeoutDisplay.textContent = state.timeout;
    setOutput(`Timeout set to ${v} seconds.`);
    setLastAction("Timeout updated");
  } catch (err) {
    errToOutput(err);
  }
});

// DDM controls
if (btnAuto) btnAuto.addEventListener("click", async () => {
  if (!state.ddmEnabled) {
    alert("Enable DDM first (toggle the switch).");
    return;
  }
  try {
    await apiPost(`/difficulty/switch-to-auto`);
    state.ddmMode = "auto";
    updateModeLabels();
    setOutput("Switched to Auto mode for DDM.");
    setLastAction("Switched to DDM Auto");
  } catch (err) {
    errToOutput(err);
  }
});

if (btnSetManual) btnSetManual.addEventListener("click", async () => {
  if (!state.ddmEnabled) {
    alert("Enable DDM first.");
    return;
  }
  const d = Number(manualDifficulty.value);
  if (!d || d < 1 || d > 10) {
    alert("Manual difficulty must be 1-10.");
    return;
  }
  try {
    await apiPost(`/difficulty/set-manual/${d}`);
    state.ddmMode = "manual";
    state.difficulty = d;
    updateModeLabels();
    setOutput(`Manual difficulty set to ${d}.`);
    setLastAction(`Manual difficulty ${d}`);
  } catch (err) {
    errToOutput(err);
  }
});
