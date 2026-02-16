// frontend/js/blockchain.js - Concurrency-safe Blockchain event handlers
import { apiGet, apiPost } from "./api.js";
import { setOutput, setLastAction, errToOutput } from "./ui.js";
import { state } from "./state.js";

let requestVersion = 0; // protects against stale async overwrites
let miningInProgress = false;

export function bindBlockchainEvents({ btnBlockchain, btnNewBlock, btnLastBlock }) {

  // ---------- GET BLOCKCHAIN ----------
  if (btnBlockchain) {
    btnBlockchain.addEventListener("click", async () => {
      const currentRequest = ++requestVersion;

      setLastAction("Fetching blockchain...");
      try {
        const data = await apiGet("/blockchain/display");

        // Ignore stale response
        if (currentRequest !== requestVersion) return;

        setOutput(JSON.stringify(data.blockchain || data, null, 2));
        setLastAction("Fetched blockchain");
      } catch (e) {
        if (currentRequest !== requestVersion) return;
        errToOutput(e);
      }
    });
  }

  // ---------- GET LAST BLOCK ----------
  if (btnLastBlock) {
    btnLastBlock.addEventListener("click", async () => {
      const currentRequest = ++requestVersion;

      setLastAction("Fetching last block...");
      try {
        const block = await apiGet("/blockchain/last-block");

        if (currentRequest !== requestVersion) return;

        setOutput(JSON.stringify(block || {}, null, 2));
        setLastAction("Fetched last block");
      } catch (e) {
        if (currentRequest !== requestVersion) return;
        errToOutput(e);
      }
    });
  }

  // ---------- ADD NEW BLOCK ----------
  if (btnNewBlock) {
    btnNewBlock.addEventListener("click", async () => {

      // Prevent overlapping mining clicks
      if (miningInProgress) return;

      miningInProgress = true;
      const currentRequest = ++requestVersion;

      // Disable all blockchain buttons during mining
      btnNewBlock.disabled = true;
      if (btnBlockchain) btnBlockchain.disabled = true;
      if (btnLastBlock) btnLastBlock.disabled = true;

      setLastAction("Mining new block...");
      setOutput("Mining in progress... Please wait.");

      try {
        const res = await apiPost("/blockchain/add");

        if (currentRequest !== requestVersion) return;

        if (res.error) {
          setOutput("Mining failed:\n" + JSON.stringify(res, null, 2));
          setLastAction("Mining failed");
          return;
        }

        // Directly fetch last block once mining succeeds
        setLastAction("Fetching mined block...");
        const last = await apiGet("/blockchain/last-block");

        if (currentRequest !== requestVersion) return;

        setOutput(JSON.stringify(last || {}, null, 2));
        setLastAction("Block mined and displayed");

      } catch (e) {
        if (currentRequest !== requestVersion) return;
        errToOutput(e);
      } finally {
        miningInProgress = false;

        // Re-enable buttons
        btnNewBlock.disabled = false;
        if (btnBlockchain) btnBlockchain.disabled = false;
        if (btnLastBlock) btnLastBlock.disabled = false;
      }
    });
  }
}
