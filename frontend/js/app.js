// frontend/js/app.js - Entry point: UI logic wiring + init


import { state } from "./state.js";
import { init } from "./init.js";
import { initLogs } from "./logs.js";
import { bindBlockchainEvents } from "./blockchain.js";
import { bindTimeoutEvents } from "./timeout.js";
import { bindDDMEvents } from "./ddm.js";
import { initMiningSocket } from "./mining_ws.js";

// UI Elements
const btnBlockchain = document.getElementById("btnBlockchain");
const btnNewBlock = document.getElementById("btnNewBlock");
const btnLastBlock = document.getElementById("btnLastBlock");

const timeoutInput = document.getElementById("timeoutInput");
const btnSetTimeout = document.getElementById("btnSetTimeout");

const ddmToggle = document.getElementById("ddmToggle");
const btnAuto = document.getElementById("btnAuto");
const btnSetManual = document.getElementById("btnSetManual");
const manualDifficulty = document.getElementById("manualDifficulty");

// Bind events from modules
bindBlockchainEvents({ btnBlockchain, btnNewBlock, btnLastBlock });
bindTimeoutEvents({ btnSetTimeout, timeoutInput });
bindDDMEvents({ ddmToggle, btnAuto, btnSetManual, manualDifficulty });

// Initialize app from backend
init(state);

// Initialize logs
initLogs();

// Initialize mining WebSocket
initMiningSocket();