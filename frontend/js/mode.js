import { API_ROUTES, apiPut } from "./api.js";
import { setOutput, setLastAction } from "./ui.js";
import { state } from "./state.js";

const modeBadge = document.getElementById("modeBadge");
const manualControls = document.getElementById("manualControls");
const difficultyUsageIndicator = document.getElementById("difficultyUsageIndicator");

export function updateModeUI() {
  const modeToggle = document.getElementById("modeToggle");
  if (modeToggle) modeToggle.checked = state.ddmMode === "manual";

  if (state.ddmMode === "manual") {
    modeBadge.textContent = "MANUAL";
    modeBadge.classList.remove("auto");
    modeBadge.classList.add("manual");
    manualControls.classList.add("show");
  } else {
    modeBadge.textContent = "AUTO";
    modeBadge.classList.remove("manual");
    modeBadge.classList.add("auto");
    manualControls.classList.remove("show");
  }
}

export function updateDifficultyUI(configuredDifficulty, effectiveDifficulty) {
  const configuredBadge = document.getElementById("configuredDifficultyBadge");
  const effectiveBadge = document.getElementById("effectiveDifficultyBadge");

  if (configuredBadge) {
    configuredBadge.textContent = `Cfg: ${configuredDifficulty}`;
    configuredBadge.classList.add("bump");
    setTimeout(() => configuredBadge.classList.remove("bump"), 200);
  }

  if (effectiveBadge) {
    effectiveBadge.textContent = `Eff: ${effectiveDifficulty}`;

    // Smooth color scaling (blue -> red) on the effective badge only.
    const intensity = effectiveDifficulty / 10;
    const hue = 220 - (intensity * 220);  // 220=blue -> 0=red
    effectiveBadge.style.background = `hsl(${hue}, 70%, 35%)`;

    effectiveBadge.classList.add("bump");
    setTimeout(() => effectiveBadge.classList.remove("bump"), 200);
  }
}

export function updateDifficultyUsageIndicator() {
  if (!difficultyUsageIndicator) return;

  const useConfigured =
    state.ddmMode === "manual" &&
    state.manualConfigured &&
    state.effectiveDifficulty === state.configuredDifficulty;

  if (useConfigured) {
    difficultyUsageIndicator.textContent = "Mining uses: Configured difficulty";
    difficultyUsageIndicator.classList.add("configured");
  } else {
    const fallbackActive =
      state.ddmMode === "manual" &&
      state.manualConfigured &&
      state.effectiveDifficulty !== state.configuredDifficulty;

    difficultyUsageIndicator.textContent = fallbackActive
      ? "Mining uses: Effective difficulty (fallback active)"
      : "Mining uses: Effective difficulty";
    difficultyUsageIndicator.classList.remove("configured");
  }
}


export function bindModeEvents({ modeToggle, btnSetManual, manualDifficulty }) {

  if (modeToggle) {
    modeToggle.addEventListener("change", async (e) => {
      const isManual = e.target.checked;

      if (!isManual) {
        const current = await apiPut(API_ROUTES.difficultySwitchToAuto);
        state.ddmMode = current.mode || "automatic";
        state.manualConfigured = false;

        state.configuredDifficulty = current.configured_difficulty ?? state.configuredDifficulty;
        state.effectiveDifficulty = current.effective_difficulty ?? current.current_difficulty ?? state.effectiveDifficulty;
        state.difficulty = state.effectiveDifficulty;

        updateModeUI();
        updateDifficultyUI(state.configuredDifficulty, state.effectiveDifficulty);
        updateDifficultyUsageIndicator();
        if (manualDifficulty) manualDifficulty.value = String(state.difficulty);
        setOutput("Switched to Automatic Mode.");
        setLastAction("Automatic Mode");
      } else {
        state.ddmMode = "manual";
        state.manualConfigured = false;
        // Manual toggled without apply should still use effective difficulty.
        state.difficulty = state.effectiveDifficulty;
        updateModeUI();
        updateDifficultyUI(state.configuredDifficulty, state.effectiveDifficulty);
        updateDifficultyUsageIndicator();
      }
    });
  }

  if (btnSetManual) {
    btnSetManual.addEventListener("click", async () => {
      const d = Number(manualDifficulty.value);
      if (!d || d < 1 || d > 10) {
        alert("Difficulty must be 1-10.");
        return;
      }

      const current = await apiPut(API_ROUTES.difficultySetManual(d));
      state.ddmMode = current.mode || "manual";
      state.manualConfigured = true;

      state.configuredDifficulty = current.configured_difficulty ?? d;
      state.effectiveDifficulty = current.effective_difficulty ?? current.current_difficulty ?? d;
      state.difficulty = state.configuredDifficulty;

      updateModeUI();
      updateDifficultyUI(state.configuredDifficulty, state.effectiveDifficulty);
      updateDifficultyUsageIndicator();
      if (manualDifficulty) manualDifficulty.value = String(state.difficulty);

      setOutput(`Manual Mode enabled. Difficulty: ${state.difficulty}`);
      setLastAction("Manual Mode");
    });
  }
}
