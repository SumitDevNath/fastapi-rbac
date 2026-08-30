import React, { createContext, useContext, useEffect, useState } from "react";
import { storage } from "../utils/storage";
import type { User, UserRole } from "../types/auth";
import type { LoginFormData, RegisterFormData } from "../schemas/authSchemas";
import { authService } from "../api/authService";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  role: UserRole | null;
  loading: boolean;
  login: (credentials: LoginFormData) => Promise<void>;
  register: (data: RegisterFormData) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(storage.getToken());
  const [loading, setLoading] = useState<boolean>(true);

  // Rehydrate user session on initial page load / refresh
  useEffect(() => {
    const initializeAuth = async () => {
      const savedToken = storage.getToken();
      if (!savedToken) {
        setLoading(false);
        return;
      }

      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
        setToken(savedToken);
      } catch (error) {
        console.error("Session expired or invalid token:", error);
        storage.clearToken();
        setUser(null);
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (credentials: LoginFormData) => {
    const response = await authService.login(credentials);
    storage.setToken(response.access_token);
    setToken(response.access_token);
    setUser(response.user);
  };

  const register = async (data: RegisterFormData) => {
    await authService.register(data);
  };

  const logout = () => {
    storage.clearToken();
    setToken(null);
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    role: user?.role || null,
    loading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
