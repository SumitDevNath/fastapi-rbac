const TOKEN_KEY = "auth_token";

export const storage = {
  getToken: (): string | null => {
    try {
      return localStorage.getItem(TOKEN_KEY);
    } catch (e) {
      console.error("Failed to read token from localStorage", e);
      return null;
    }
  },

  setToken: (token: string): void => {
    try {
      localStorage.setItem(TOKEN_KEY, token);
    } catch (e) {
      console.error("Failed to write token to localStorage", e);
    }
  },

  clearToken: (): void => {
    try {
      localStorage.removeItem(TOKEN_KEY);
    } catch (e) {
      console.error("Failed to clear token from localStorage", e);
    }
  },
};
