// frontend/js/timeout.js - Timeout setting logic
import { apiPost } from "./api.js";
import { setOutput, setLastAction, errToOutput } from "./ui.js";
import { state } from "./state.js";

export function bindTimeoutEvents({ btnSetTimeout, timeoutInput }) {
  if (!btnSetTimeout) return;
  btnSetTimeout.addEventListener("click", async () => {
    const v = Number(timeoutInput.value);
    if (!v || v < 10 || v > 300) {
      alert("Timeout must be 10-300 seconds."); return;
    }
    setLastAction("Setting timeout...");
    try {
      await apiPost(`/mining/set-timeout/${v}`);
      state.timeout = v;
      setOutput(`Timeout set to ${v} seconds.`);
      setLastAction("Timeout updated");
    } catch (e) { errToOutput(e); }
  });
}
