// app.js - UI logic and backend integration

const API_BASE = ""; // empty => same origin; served from same uvicorn server (/) when backend mounts frontend

// UI elements
const btnBlockchain = document.getElementById("btnBlockchain");
const btnNewBlock = document.getElementById("btnNewBlock");
const btnLastBlock = document.getElementById("btnLastBlock");
const output = document.getElementById("output");
const lastAction = document.getElementById("lastAction");

const ddmToggle = document.getElementById("ddmToggle");
const ddmControls = document.getElementById("ddmControls");
const ddmSubstatus = document.getElementById("ddmSubstatus");
const globalMode = document.getElementById("globalMode");

const timeoutDisplay = document.getElementById("timeoutDisplay");
const timeoutInput = document.getElementById("timeoutInput");
const btnSetTimeout = document.getElementById("btnSetTimeout");

const btnAuto = document.getElementById("btnAuto");
const btnSetManual = document.getElementById("btnSetManual");
const manualDifficulty = document.getElementById("manualDifficulty");

// Local UI state mirrors server state where useful
let state = {
  ddmEnabled: false,
  ddmMode: "auto", // "auto" or "manual"
  timeout: 60,
};

// Helpers
function setOutput(text, append = false) {
  if (!append) output.textContent = text;
  else output.textContent += "\n" + text;
}
function setLastAction(text) {
  lastAction.textContent = text;
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
  return res.json();
}

async function apiPost(path) {
  const res = await fetch(API_BASE + path, { method: "POST" });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${res.statusText} - ${txt}`);
  }
  return res.json();
}

// UI update functions
function showDDMControls(show) {
  ddmControls.style.display = show ? "block" : "none";
}

function updateModeLabels() {
  globalMode.textContent = state.ddmEnabled ? "DDM" : "Standard";
  ddmSubstatus.textContent = state.ddmEnabled ? `DDM: Enabled (${state.ddmMode})` : "DDM: Disabled";
  ddmToggle.checked = state.ddmEnabled;
  showDDMControls(state.ddmEnabled);
}

// Initialize: fetch current timeout from mining module by reading client-side fallback
// Your backend doesn't expose a GET timeout endpoint, so we use the client-side default in mining.py.
// We'll try to show the current value known client-side by asking the server via a cheap add-and-cancel? 
// To keep it simple: read default at load (60) and let user set.
function init() {
  updateModeLabels();
  timeoutDisplay.textContent = state.timeout;
  timeoutInput.value = state.timeout;
  setOutput("Ready. Click 'Get Blockchain' or 'Last Block' or 'New Block'.");
  setLastAction("Idle");
}

init();

// Events
ddmToggle.addEventListener("change", async (e) => {
  try {
    if (e.target.checked) {
      await apiPost("/difficulty/enable");
      state.ddmEnabled = true;
      // default to auto when enabled
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
    ddmToggle.checked = !e.target.checked; // revert UI on failure
  }
});

btnBlockchain.addEventListener("click", async () => {
  setLastAction("Fetching blockchain...");
  try {
    const data = await apiGet("/blockchain/");
    setOutput(JSON.stringify(data.blockchain, null, 2));
    setLastAction("Fetched blockchain");
  } catch (err) {
    errToOutput(err);
  }
});

btnLastBlock.addEventListener("click", async () => {
  setLastAction("Fetching last block...");
  try {
    const block = await apiGet("/blockchain/last-block");
    setOutput(JSON.stringify(block, null, 2));
    setLastAction("Fetched last block");
  } catch (err) {
    errToOutput(err);
  }
});

btnNewBlock.addEventListener("click", async () => {
  setLastAction("Adding new block...");
  try {
    // POST to add block
    const res = await apiPost("/blockchain/add");
    if (res.error) {
      setOutput("Block mining failed: " + JSON.stringify(res, null, 2));
      setLastAction("Block mining failed");
      // Optionally show last failed difficulty
      return;
    }
    setOutput("Block added:\n" + JSON.stringify(res, null, 2));
    setLastAction("Block added, fetching last block...");
    // Fetch last block to refresh dataset
    const last = await apiGet("/blockchain/last-block");
    setOutput(JSON.stringify(last, null, 2));
    setLastAction("Last block displayed");
  } catch (err) {
    errToOutput(err);
  }
});

btnSetTimeout.addEventListener("click", async () => {
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
btnAuto.addEventListener("click", async () => {
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

btnSetManual.addEventListener("click", async () => {
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
    // This endpoint expects DDM to be enabled; it will set manual difficulty and toggle Manual mode on the backend behavior
    await apiPost(`/difficulty/set-manual/${d}`);
    state.ddmMode = "manual";
    updateModeLabels();
    setOutput(`Manual difficulty set to ${d}.`);
    setLastAction(`Manual difficulty ${d}`);
  } catch (err) {
    errToOutput(err);
  }
});
