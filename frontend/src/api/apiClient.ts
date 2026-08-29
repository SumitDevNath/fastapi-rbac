import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { storage } from "../utils/storage";

// 1. Create configured Axios instance
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
  timeout: 15000, // 15-second timeout protection
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// 2. Request Interceptor: Attach JWT Bearer Token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = storage.getToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  },
);

// 3. Response Interceptor: Normalize Errors and Handle Session Expiration
apiClient.interceptors.response.use(
  (response) => {
    // Return data directly so callers don't have to write response.data
    return response.data;
  },
  (
    error: AxiosError<{
      error?: { code: string; message: string; details?: unknown };
    }>,
  ) => {
    if (error.response) {
      const { status, data } = error.response;

      // Handle session expiration or invalid credentials globally
      if (status === 401) {
        // Clear stale local token
        storage.clearToken();

        // If the 401 occurred on a protected page (not during initial login), redirect
        const isAuthRoute =
          window.location.pathname.includes("/login") ||
          window.location.pathname.includes("/register");
        if (!isAuthRoute) {
          window.location.href = "/login?expired=true";
        }
      }

      // Extract backend standardized error message
      const serverMessage =
        data?.error?.message ||
        error.message ||
        "An unexpected error occurred.";
      return Promise.reject(new Error(serverMessage));
    } else if (error.request) {
      // Network failure / Server unreachable
      return Promise.reject(
        new Error("Network error: Unable to connect to the backend server."),
      );
    }

    return Promise.reject(new Error(error.message));
  },
);
