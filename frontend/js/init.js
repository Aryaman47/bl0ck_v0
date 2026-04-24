// frontend/js/init.js - Initialize from /status

import { API_ROUTES, apiGet } from "./api.js";
import { setOutput, setLastAction, updateModeLabels } from "./ui.js";
import { updateDifficultyUI, updateModeUI } from "./mode.js";

export async function init(state) {
  setOutput("Initializing from server...");
  setLastAction("Initializing");
  try {
    const [s, current] = await Promise.all([
      apiGet(API_ROUTES.status),
      apiGet(API_ROUTES.difficultyCurrent),
    ]);

    state.ddmEnabled = !!s.ddm_enabled;
    state.ddmMode = current.mode === "manual" ? "manual" : "auto";
    state.timeout = s.timeout || state.timeout;
    state.difficulty = current.current_difficulty || s.difficulty || state.difficulty;

    updateModeLabels(state);
    updateModeUI();
    updateDifficultyUI(state.difficulty);
    const manualDifficulty = document.getElementById("manualDifficulty");
    if (manualDifficulty) manualDifficulty.value = String(state.difficulty);
    setOutput(`Status loaded.\nDDM: ${state.ddmEnabled} (${state.ddmMode})\nTimeout: ${state.timeout}s\nDifficulty: ${state.difficulty}`);
    setLastAction("Ready");
  } catch (err) {
    setOutput("Could not fetch API status. Using defaults.\n" + err.message);
    setLastAction("Init failed (fallback)");
    updateModeLabels(state);
    updateModeUI();
    updateDifficultyUI(state.difficulty);
  }
}
