// api.js - Fetch helpers
const API_BASE = "";

export async function apiGet(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(await res.text());
  try { return await res.json(); } catch { return {}; }
}

export async function apiPost(path) {
  const res = await fetch(API_BASE + path, { method: "POST" });
  if (!res.ok) throw new Error(await res.text());
  try { return await res.json(); } catch { return {}; }
}
