import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { storage } from "../utils/storage";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Request Interceptor: Attach Access Token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = storage.getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error),
);

// Concurrency mutex state for Refresh Token rotation
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (token) {
      prom.resolve(token);
    } else {
      prom.reject(error);
    }
  });
  failedQueue = [];
};

// Response Interceptor: Seamless Refresh Rotation
apiClient.interceptors.response.use(
  (response) => response.data,
  async (
    error: AxiosError<{
      error?: { code: string; message: string; details?: unknown };
      detail?: unknown;
    }>,
  ) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (!error.response) {
      return Promise.reject(
        new Error("Network error: Unable to connect to backend server."),
      );
    }

    const { status, data } = error.response;
    const requestUrl = originalRequest.url || "";

    // Bypass refresh logic for auth lifecycle endpoints to avoid infinite loops
    const isAuthEndpoint =
      requestUrl.includes("/auth/login") ||
      requestUrl.includes("/auth/register") ||
      requestUrl.includes("/auth/refresh") ||
      requestUrl.includes("/auth/logout");

    if (status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      const currentRefreshToken = storage.getRefreshToken();

      if (!currentRefreshToken) {
        storage.clearTokens();
        if (!window.location.pathname.includes("/login")) {
          window.location.href = "/login?expired=true";
        }
        return Promise.reject(
          new Error("Session expired. Please log in again."),
        );
      }

      if (isRefreshing) {
        // Queue parallel requests until refresh completes
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((newToken) => {
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${newToken}`;
            }
            return apiClient(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Direct call to refresh endpoint bypassing standard interceptor
        const response = await axios.post(
          `${apiClient.defaults.baseURL}/auth/refresh`,
          { refresh_token: currentRefreshToken },
          { headers: { "Content-Type": "application/json" } },
        );

        const { access_token, refresh_token } = response.data;
        // Atomically rotate tokens in storage
        storage.setTokens(access_token, refresh_token);

        processQueue(null, access_token);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }
        return apiClient(originalRequest);
      } catch (refreshErr) {
        processQueue(refreshErr, null);
        storage.clearTokens();
        if (!window.location.pathname.includes("/login")) {
          window.location.href = "/login?expired=true";
        }
        return Promise.reject(
          new Error("Session terminated. Please log in again."),
        );
      } finally {
        isRefreshing = false;
      }
    }

    // Standardize error message extraction
    let serverMessage = data?.error?.message;
    if (!serverMessage && Array.isArray(data?.detail)) {
      serverMessage = data.detail
        .map((d: { msg?: string }) => d.msg)
        .join(", ");
    } else if (typeof data?.detail === "string") {
      serverMessage = data.detail;
    }

    return Promise.reject(
      new Error(
        serverMessage || error.message || "An unexpected error occurred.",
      ),
    );
  },
);
