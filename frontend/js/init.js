// frontend/js/init.js - Initialize from /status

import { API_ROUTES, apiGet } from "./api.js";
import { setOutput, setLastAction, updateModeLabels } from "./ui.js";
import { updateDifficultyUI, updateDifficultyUsageIndicator, updateModeUI } from "./mode.js";

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

    const configured =
      current.configured_difficulty ??
      s.configured_difficulty ??
      s.difficulty ??
      state.configuredDifficulty;

    const effective =
      current.effective_difficulty ??
      s.effective_difficulty ??
      s.difficulty ??
      state.effectiveDifficulty;

    state.configuredDifficulty = configured;
    state.effectiveDifficulty = effective;
    state.manualConfigured = state.ddmMode === "manual";
    state.difficulty = state.ddmMode === "manual" ? configured : effective;

    updateModeLabels(state);
    updateModeUI();
    updateDifficultyUI(state.configuredDifficulty, state.effectiveDifficulty);
    updateDifficultyUsageIndicator();
    const manualDifficulty = document.getElementById("manualDifficulty");
    if (manualDifficulty) manualDifficulty.value = String(state.difficulty);
    setOutput(
      `Status loaded.\n` +
      `DDM: ${state.ddmEnabled} (${state.ddmMode})\n` +
      `Timeout: ${state.timeout}s\n` +
      `Configured Difficulty: ${state.configuredDifficulty}\n` +
      `Effective Difficulty: ${state.effectiveDifficulty}`
    );
    setLastAction("Ready");
  } catch (err) {
    setOutput("Could not fetch API status. Using defaults.\n" + err.message);
    setLastAction("Init failed (fallback)");
    updateModeLabels(state);
    updateModeUI();
    updateDifficultyUI(state.configuredDifficulty, state.effectiveDifficulty);
    updateDifficultyUsageIndicator();
  }
}
