import { API_ROUTES, apiPost } from "./api.js";
import { setOutput, setLastAction } from "./ui.js";
import { state } from "./state.js";

const modeBadge = document.getElementById("modeBadge");
const difficultyBadge = document.getElementById("difficultyBadge");
const manualControls = document.getElementById("manualControls");

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

export function updateDifficultyUI(state_difficulty) {
  const badge = document.getElementById("difficultyBadge");
  if (!badge) return;

  badge.textContent = `D: ${state_difficulty}`;

  // Smooth color scaling (blue → red)
  const intensity = state_difficulty / 10;
  const hue = 220 - (intensity * 220);  // 220=blue → 0=red
  badge.style.background = `hsl(${hue}, 70%, 35%)`;
  badge.classList.add("bump");
  setTimeout(() => badge.classList.remove("bump"), 200);

}


export function bindModeEvents({ modeToggle, btnSetManual, manualDifficulty }) {

  if (modeToggle) {
    modeToggle.addEventListener("change", async (e) => {
      const isManual = e.target.checked;

      if (!isManual) {
        const current = await apiPost(API_ROUTES.difficultySwitchToAuto);
        state.ddmMode = current.mode || "automatic";
        state.difficulty = current.current_difficulty || state.difficulty;
        updateModeUI();
        updateDifficultyUI(state.difficulty);
        if (manualDifficulty) manualDifficulty.value = String(state.difficulty);
        setOutput("Switched to Automatic Mode.");
        setLastAction("Automatic Mode");
      } else {
        state.ddmMode = "manual";
        updateModeUI();
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

      const current = await apiPost(API_ROUTES.difficultySetManual(d));
      state.ddmMode = current.mode || "manual";
      state.difficulty = current.current_difficulty || d;

      updateModeUI();
      updateDifficultyUI(state.difficulty);
      if (manualDifficulty) manualDifficulty.value = String(state.difficulty);

      setOutput(`Manual Mode enabled. Difficulty: ${state.difficulty}`);
      setLastAction("Manual Mode");
    });
  }
}
