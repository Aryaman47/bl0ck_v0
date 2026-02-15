// init.js - Initialize from /status
import { apiGet } from "./api.js";
import { setOutput, setLastAction, updateModeLabels } from "./ui.js";

export async function init(state) {
  setOutput("Initializing from server...");
  setLastAction("Initializing");
  try {
    const s = await apiGet("/blockchain/status");
    state.ddmEnabled = !!s.ddm_enabled;
    state.ddmMode = s.ddm_mode || "auto";
    state.timeout = s.timeout || state.timeout;
    state.difficulty = s.difficulty || state.difficulty;

    updateModeLabels(state);
    setOutput(`Status loaded.\nDDM: ${state.ddmEnabled} (${state.ddmMode})\nTimeout: ${state.timeout}s\nDifficulty: ${state.difficulty}`);
    setLastAction("Ready");
  } catch (err) {
    setOutput("Could not fetch /status. Using defaults.\n" + err.message);
    setLastAction("Init failed (fallback)");
    updateModeLabels(state);
  }
}
