// blockchain.js - Blockchain event handlers
import { apiGet, apiPost } from "./api.js";
import { setOutput, setLastAction, errToOutput, updateModeLabels } from "./ui.js";
import { state } from "./state.js";

export function bindBlockchainEvents({ btnBlockchain, btnNewBlock, btnLastBlock }) {
  if (btnBlockchain) btnBlockchain.addEventListener("click", async () => {
    setLastAction("Fetching blockchain...");
    try {
      const data = await apiGet("/blockchain/");
      setOutput(JSON.stringify(data.blockchain || data, null, 2));
      setLastAction("Fetched blockchain");
    } catch (e) { errToOutput(e); }
  });

  if (btnLastBlock) btnLastBlock.addEventListener("click", async () => {
    setLastAction("Fetching last block...");
    try {
      const block = await apiGet("/blockchain/last-block");
      setOutput(JSON.stringify(block || {}, null, 2));
      setLastAction("Fetched last block");
    } catch (e) { errToOutput(e); }
  });

  if (btnNewBlock) btnNewBlock.addEventListener("click", async () => {
    setLastAction("Adding new block...");
    try {
      const res = await apiPost("/blockchain/add");
      if (res.error) {
        setOutput("Block mining failed: " + JSON.stringify(res, null, 2));
        setLastAction("Block mining failed");
        return;
      }
      setOutput("Block add response:\n" + JSON.stringify(res, null, 2));
      setLastAction("Fetching last block...");
      const last = await apiGet("/blockchain/last-block");
      setOutput(JSON.stringify(last || {}, null, 2));
      setLastAction("Last block displayed");

      const s = await apiGet("/status");
      state.timeout = s.timeout || state.timeout;
      state.difficulty = s.difficulty || state.difficulty;
      updateModeLabels(state);
    } catch (e) { errToOutput(e); }
  });
}
