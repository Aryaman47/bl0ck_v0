// frontend/js/blockchain.js - Concurrency-safe Blockchain event handlers
import { apiGet, apiPost } from "./api.js";
import { setOutput, setLastAction, errToOutput } from "./ui.js";
import { state } from "./state.js";

let requestVersion = 0; // protects against stale async overwrites
let miningInProgress = false;

export function bindBlockchainEvents({ btnBlockchain, btnNewBlock, btnLastBlock }) {
<<<<<<< HEAD
  if (btnBlockchain) btnBlockchain.addEventListener("click", async () => {
    setLastAction("Fetching blockchain...");
    try {
      const data = await apiGet("/blockchain/display");
      setOutput(JSON.stringify(data.blockchain || data, null, 2));
      setLastAction("Fetched blockchain");
    } catch (e) { errToOutput(e); }
  });
=======
>>>>>>> exp-GPU

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

<<<<<<< HEAD
      // const s = await apiGet("/status");
      // state.timeout = s.timeout || state.timeout;
      // state.difficulty = s.difficulty || state.difficulty;
      updateModeLabels(state);
    } catch (e) { errToOutput(e); }
  });
=======
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

      if (miningInProgress) return;

      miningInProgress = true;
      btnNewBlock.disabled = true;

      let elapsed = 0;
      let miningInterval = null;

      setLastAction("Mining started...");
      setOutput("Mining in progress...\nElapsed: 0s");

      // Start live elapsed timer
      miningInterval = setInterval(() => {
        elapsed++;
        setOutput(`Mining in progress...\nElapsed: ${elapsed}s`);
      }, 1000);

      try {
        const res = await apiPost("/blockchain/add");

        clearInterval(miningInterval);

        if (res.error) {
          setOutput("Mining failed:\n" + JSON.stringify(res, null, 2));
          setLastAction("Mining failed");
          miningInProgress = false;
          btnNewBlock.disabled = false;
          return;
        }

        setLastAction("Block mined successfully");

        const last = await apiGet("/blockchain/last-block");

        setOutput(
          `Block mined successfully!\n` +
          `Elapsed (frontend): ${elapsed}s\n` +
          `Actual mining time: ${last.mining_time}s\n\n` +
          JSON.stringify(last, null, 2)
        );

      } catch (e) {
        clearInterval(miningInterval);
        errToOutput(e);
      } finally {
        miningInProgress = false;
        btnNewBlock.disabled = false;
      }
    });
  }

}
