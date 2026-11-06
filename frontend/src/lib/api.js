import axios from "axios";

const DEFAULT_BACKEND_URL = "https://finlingo-api.onrender.com";
const BASE = (process.env.REACT_APP_BACKEND_URL || DEFAULT_BACKEND_URL).replace(/\/+$/, "");
export const API = `${BASE}/api`;
export const PRIVACY_URL = `${BASE}/privacy`;

export const api = axios.create({
  baseURL: API,
  withCredentials: false,
  headers: { "Content-Type": "application/json" },
  timeout: 90000, // a sleeping free-tier server can take about a minute to wake
});

// Tell the UI when a request has been pending a while, so it can show a "waking up" message.
let pending = 0;
let slowTimer = null;
const emitSlow = (slow) => window.dispatchEvent(new CustomEvent("fl:slow", { detail: slow }));
const requestStarted = () => {
  pending += 1;
  if (!slowTimer) slowTimer = setTimeout(() => emitSlow(true), 4000);
};
const requestEnded = () => {
  pending = Math.max(0, pending - 1);
  if (pending === 0) {
    clearTimeout(slowTimer);
    slowTimer = null;
    emitSlow(false);
  }
};

// Attach bearer token if available (fallback to cookies if blocked)
api.interceptors.request.use((config) => {
  requestStarted();
  const token = localStorage.getItem("fl_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  // Lets the server count days (streak, daily goal) on the learner's own clock.
  config.headers["X-TZ-Offset"] = String(new Date().getTimezoneOffset());
  return config;
}, (error) => { requestEnded(); return Promise.reject(error); });

api.interceptors.response.use(
  (res) => { requestEnded(); return res; },
  (error) => { requestEnded(); return Promise.reject(error); },
);

export function formatApiError(err) {
  const d = err?.response?.data?.detail;
  if (d == null) return err?.message || "Something went wrong.";
  if (typeof d === "string") return d;
  if (Array.isArray(d))
    return d.map((e) => (e?.msg ? e.msg : JSON.stringify(e))).join(" ");
  return String(d);
}
