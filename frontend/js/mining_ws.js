import { state } from "./state.js";
import { updateDifficultyUI, updateDifficultyUsageIndicator } from "./mode.js";
import { WS_ROUTES, wsUrl } from "./api.js";

let ws;

export function initMiningSocket() {
  ws = new WebSocket(wsUrl(WS_ROUTES.mining));

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateMiningUI(data);
  };

  ws.onclose = () => {
    console.log("Mining WebSocket closed.");
  };
}

/* 🔹 LIVE DASHBOARD UPDATE FUNCTION */
function updateMiningUI(data) {
  const dashboard = document.getElementById("miningDashboard");
  const elapsedEl = document.getElementById("liveElapsed");
  const nonceEl = document.getElementById("liveNonce");
  const hashRateEl = document.getElementById("liveHashRate");
  const progressFill = document.getElementById("progressFill");

  if (!dashboard) return;

  // If mining stopped → hide dashboard
  if (!data.active) {
    dashboard.classList.add("hidden");
    progressFill.style.width = "0%";
    return;
  }

  // Sync live effective difficulty while mining in every mode.
  // In manual mode this makes fallback difficulty visible immediately.
  if (data.difficulty && state.effectiveDifficulty !== data.difficulty) {
    state.effectiveDifficulty = data.difficulty;
    if (state.ddmMode !== "manual" || !state.manualConfigured) {
      state.difficulty = state.effectiveDifficulty;
    }
    updateDifficultyUI(state.configuredDifficulty, state.effectiveDifficulty);
    updateDifficultyUsageIndicator();
  }

  // Show dashboard
  dashboard.classList.remove("hidden");

  elapsedEl.textContent = data.elapsed.toFixed(2);
  nonceEl.textContent = data.nonce.toLocaleString();
  hashRateEl.textContent = data.hash_rate.toLocaleString();

  const expectedHashes = Math.pow(16, data.difficulty);

  let estimatedTime = 0;
  if (data.hash_rate > 0) {
    estimatedTime = expectedHashes / data.hash_rate;
  }

  let progress = 0;
  if (estimatedTime > 0) {
    progress = Math.min((data.elapsed / estimatedTime) * 100, 100);
  }

  progressFill.style.width = progress + "%";
}
