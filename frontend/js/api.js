// frontend/js/api.js - Fetch helpers
const API_BASE = "http://localhost:8000";

export async function apiGet(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(await res.text());
  try { return await res.json(); } catch (e) { return {}; }
}

export async function apiPost(path) {
  const res = await fetch(API_BASE + path, { method: "POST" });
  if (!res.ok) throw new Error(await res.text());
  try { return await res.json(); } catch (e) { return {}; }
}
