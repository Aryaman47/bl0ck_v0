// frontend/js/api.js - Fetch helpers
const API_BASE = `${window.location.origin}/api/v1`;

export const API_ROUTES = {
  status: "/status",
  blockchainDisplay: "/blockchain/display",
  blockchainAdd: "/blockchain/add",
  blockchainLastBlock: "/blockchain/last-block",
  difficultyCurrent: "/difficulty/current",
  difficultySetManual: (difficulty) => `/difficulty/manual/${difficulty}`,
  difficultySwitchToAuto: "/difficulty/auto",
  miningSetTimeout: (timeout) => `/mining/timeout/${timeout}`,
  logs: "/logs",
};

export const WS_ROUTES = {
  mining: "/ws/mining",
};

function normalizePath(path) {
  if (!path) return "/";
  return path.startsWith("/") ? path : `/${path}`;
}

async function parseResponse(res) {
  try {
    return await res.json();
  } catch (e) {
    return {};
  }
}

function buildError(res, payload) {
  const fallback = `HTTP ${res.status} ${res.statusText}`.trim();
  const message = payload?.error?.message || payload?.detail?.message || payload?.detail || fallback;

  const err = new Error(String(message));
  err.status = res.status;
  err.code = payload?.error?.code || `HTTP_${res.status}`;
  err.details = payload?.error?.details;
  err.payload = payload;
  return err;
}

async function request(method, path) {
  const fetchOptions = { method };
  if (method === "GET") {
    fetchOptions.cache = "no-store";
  }

  const res = await fetch(API_BASE + normalizePath(path), fetchOptions);
  const payload = await parseResponse(res);

  if (!res.ok) {
    throw buildError(res, payload);
  }

  // New contract format: { success, message, data }
  if (payload && Object.prototype.hasOwnProperty.call(payload, "data")) {
    return payload.data;
  }

  return payload || {};
}

export async function apiGet(path) {
  return request("GET", path);
}

export async function apiPost(path) {
  return request("POST", path);
}

export async function apiPut(path) {
  return request("PUT", path);
}

export function wsUrl(path) {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://${window.location.host}${normalizePath(path)}`;
}
