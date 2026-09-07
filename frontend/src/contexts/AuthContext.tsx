import React, { createContext, useContext, useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { authService } from "../features/auth/api/authService";
import type { LoginFormData, RegisterFormData } from "../schemas/authSchemas";
import type { User, UserRole } from "../types/auth";
import { storage } from "../utils/storage";

interface AuthContextType {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  role: UserRole | null;
  loading: boolean;
  login: (credentials: LoginFormData) => Promise<void>;
  register: (data: RegisterFormData) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(
    storage.getAccessToken(),
  );
  const [loading, setLoading] = useState<boolean>(true);
  const queryClient = useQueryClient();

  useEffect(() => {
    const initializeAuth = async () => {
      const token = storage.getAccessToken();
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const validatedUser = await authService.validateToken();
        setUser(validatedUser);
        setAccessToken(token);
      } catch (error) {
        console.error("Session validation error:", error);
        storage.clearTokens();
        setUser(null);
        setAccessToken(null);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (credentials: LoginFormData) => {
    const response = await authService.login(credentials);
    storage.setTokens(
      response.tokens.access_token,
      response.tokens.refresh_token,
    );
    setAccessToken(response.tokens.access_token);
    setUser(response.user);
  };

  const register = async (data: RegisterFormData) => {
    await authService.register(data);
  };

  const logout = async () => {
    const currentRefreshToken = storage.getRefreshToken();

    // 1. Cancel any active outgoing background queries immediately
    // await queryClient.cancelQueries();

    // 2. Clear all cached server state
    // queryClient.clear();

    try {
      if (currentRefreshToken) {
        await authService.logout(currentRefreshToken);
      }
    } catch (e) {
      console.warn(
        "Backend logout encountered error; proceeding with local cleanup",
        e,
      );
    } finally {
      storage.clearTokens();
      setAccessToken(null);
      setUser(null);
      queryClient.clear();
    }
  };

  const value: AuthContextType = {
    user,
    accessToken,
    isAuthenticated: !!accessToken && !!user,
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
