import { apiGet } from "./api.js";

const logPanel = document.getElementById("logPanel");
const logOutput = document.getElementById("logOutput");
const toggleBtn = document.getElementById("toggleLogsBtn");

let logsVisible = false;

export function initLogs() {
  if (!logPanel || !logOutput || !toggleBtn) return;

  toggleBtn.addEventListener("click", () => {
    logsVisible = !logsVisible;

    if (logsVisible) {
      logPanel.classList.add("show");
      toggleBtn.textContent = "Hide Logs";
    } else {
      logPanel.classList.remove("show");
      toggleBtn.textContent = "Show Logs";
    }
  });

  setInterval(async () => {
    if (!logsVisible) return;

    try {
      const data = await apiGet("/logs");
      logOutput.textContent = (data.logs || []).join("\n");
      logOutput.scrollTop = logOutput.scrollHeight;
    } catch {}
  }, 10000);
}
