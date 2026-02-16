// frontend/js/ui.js - UI helpers
const output = document.getElementById("output");
const lastAction = document.getElementById("lastAction");
const ddmControls = document.getElementById("ddmControls");
const timeoutDisplay = document.getElementById("timeoutDisplay");
const timeoutInput = document.getElementById("timeoutInput");
const ddmToggle = document.getElementById("ddmToggle");

export function setOutput(text, append = false) {
  output.textContent = append ? output.textContent + "\n" + text : text;
}
export function setLastAction(t) {
  if (lastAction) lastAction.textContent = t;
}
export function errToOutput(e) {
  setOutput("Error: " + (e.message || e)); setLastAction("Error");
}

export function showDDMControls(show) {
  if (ddmControls) ddmControls.classList.toggle("show", show);
}
export function updateModeLabels(state) {
  if (ddmToggle) ddmToggle.checked = !!state.ddmEnabled;
  showDDMControls(state.ddmEnabled);
  if (timeoutDisplay) timeoutDisplay.textContent = state.timeout;
  if (timeoutInput) timeoutInput.value = state.timeout;
}

const btnClear = document.getElementById("btnClear");

if (btnClear) {
  btnClear.addEventListener("click", () => {
    if (output) output.textContent = "Welcome to The bl0ck 🔗 API UI. Use controls on left ";
    if (lastAction) lastAction.textContent = "Cleared";
  });
}
