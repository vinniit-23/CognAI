// src/api/backend.js
import axios from "axios";
import { getSessionToken } from "@descope/react-sdk";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
if (!BACKEND_URL) {
  console.error(
    "VITE_BACKEND_URL is required in environment variables (e.g. http://localhost:8000)"
  );
}

const api = axios.create({
  baseURL: BACKEND_URL,
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    throw error;
  }
);

/**
 * Helper: POST with optional sessionToken. If sessionToken is not passed,
 * getSessionToken() will be used as fallback (client-side SDK).
 */
export async function apiPost(
  path,
  body = {},
  options = { sessionToken: null }
) {
  const token = options.sessionToken ?? getSessionToken();
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  const resp = await api.post(path, body, { headers });
  return resp.data;
}

export async function apiGet(
  path,
  params = {},
  options = { sessionToken: null }
) {
  const token = options.sessionToken ?? getSessionToken();
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  const resp = await api.get(path, { params, headers });
  return resp.data;
}

/* Convenience wrappers */
export const notifyConnection = async (userId, sessionToken = null) => {
  return apiPost(
    "/auth/notify-connection",
    { user_id: userId },
    { sessionToken }
  );
};

export const getEmails = async (
  userId,
  maxResults = 10,
  sessionToken = null
) => {
  return apiGet(
    "/emails",
    { user_id: userId, max_results: maxResults },
    { sessionToken }
  );
};

export const postChat = async (prompt, userId, sessionToken = null) => {
  return apiPost(
    "/chat",
    { user_prompt: prompt, user_id: userId },
    { sessionToken }
  );
};

export default api;
