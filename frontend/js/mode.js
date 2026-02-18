import { apiPost } from "./api.js";
import { setOutput, setLastAction } from "./ui.js";
import { state } from "./state.js";

const modeBadge = document.getElementById("modeBadge");
const difficultyBadge = document.getElementById("difficultyBadge");
const manualControls = document.getElementById("manualControls");

export function updateModeUI() {
  if (state.mode === "manual") {
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

export function updateDifficultyUI() {
  if (difficultyBadge) {
    difficultyBadge.textContent = `D: ${state.difficulty}`;
  }
}

export function bindModeEvents({ modeToggle, btnSetManual, manualDifficulty }) {

  if (modeToggle) {
    modeToggle.addEventListener("change", async (e) => {
      const isManual = e.target.checked;

      if (!isManual) {
        await apiPost("/difficulty/switch-to-auto");
        state.mode = "automatic";
        updateModeUI();
        setOutput("Switched to Automatic Mode.");
        setLastAction("Automatic Mode");
      } else {
        state.mode = "manual";
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

      await apiPost(`/difficulty/set-manual/${d}`);
      state.mode = "manual";
      state.difficulty = d;

      updateModeUI();
      updateDifficultyUI();

      setOutput(`Manual Mode enabled. Difficulty: ${d}`);
      setLastAction("Manual Mode");
    });
  }

  updateModeUI();
  updateDifficultyUI();
}
