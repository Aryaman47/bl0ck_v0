import { state } from "./state.js";
import { updateDifficultyUI } from "./mode.js";

let ws;

export function initMiningSocket() {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${protocol}://${window.location.host}/ws/mining`;

  ws = new WebSocket(wsUrl);

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
  
  if (data.difficulty && state.difficulty !== data.difficulty) {
      state.difficulty = data.difficulty;
      updateDifficultyUI(state.difficulty);
  }

  // If mining stopped → hide dashboard
  if (!data.active) {
    dashboard.classList.add("hidden");
    progressFill.style.width = "0%";
    return;
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
