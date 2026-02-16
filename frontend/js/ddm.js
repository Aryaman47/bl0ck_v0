// frontend/js/ddm.js - Dynamic Difficulty Mode
import { apiPost } from "./api.js";
import { setOutput, setLastAction, errToOutput, updateModeLabels } from "./ui.js";
import { state } from "./state.js";

export function bindDDMEvents({ ddmToggle, btnAuto, btnSetManual, manualDifficulty }) {
  if (ddmToggle) ddmToggle.addEventListener("change", async (e) => {
    try {
      if (e.target.checked) {
        await apiPost("/difficulty/enable");
        state.ddmEnabled = true; state.ddmMode = "auto";
        setOutput("DDM enabled."); setLastAction("Enabled DDM");
      } else {
        await apiPost("/difficulty/disable");
        state.ddmEnabled = false; state.ddmMode = "auto";
        setOutput("DDM disabled."); setLastAction("Disabled DDM");
      }
      updateModeLabels(state);
    } catch (err) { errToOutput(err); e.target.checked = !e.target.checked; }
  });

  if (btnAuto) btnAuto.addEventListener("click", async () => {
    if (!state.ddmEnabled) return alert("Enable DDM first.");
    try {
      await apiPost("/difficulty/switch-to-auto");
      state.ddmMode = "auto"; updateModeLabels(state);
      setOutput("Switched to Auto mode."); setLastAction("DDM Auto");
    } catch (e) { errToOutput(e); }
  });

  if (btnSetManual) btnSetManual.addEventListener("click", async () => {
    if (!state.ddmEnabled) return alert("Enable DDM first.");
    const d = Number(manualDifficulty.value);
    if (!d || d < 1 || d > 10) return alert("Manual difficulty must be 1-10.");
    try {
      await apiPost(`/difficulty/set-manual/${d}`);
      state.ddmMode = "manual"; state.difficulty = d;
      updateModeLabels(state);
      setOutput(`Manual difficulty set to ${d}.`);
      setLastAction(`Manual difficulty ${d}`);
    } catch (e) { errToOutput(e); }
  });
}