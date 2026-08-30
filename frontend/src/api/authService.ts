import type { LoginFormData, RegisterFormData } from "../schemas/authSchemas";
import type { TokenResponse, User } from "../types/auth";
import { apiClient } from "./apiClient";

export const authService = {
  login: async (credentials: LoginFormData): Promise<TokenResponse> => {
    return await apiClient.post<unknown, TokenResponse>(
      "/auth/login",
      credentials,
    );
  },

  register: async (data: RegisterFormData): Promise<User> => {
    return await apiClient.post<unknown, User>("/auth/register", data);
  },

  getCurrentUser: async (): Promise<User> => {
    return await apiClient.get<unknown, User>("/users/me");
  },
};
