<<<<<<< HEAD
// api.js - Fetch helpers
const API_BASE = "http://127.0.0.1:8000";
=======
// frontend/js/api.js - Fetch helpers
const API_BASE = `${window.location.origin}`;

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
