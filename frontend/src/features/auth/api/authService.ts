import { apiClient } from "../../../api/apiClient";
import type {
  LoginFormData,
  RegisterFormData,
} from "../../../schemas/authSchemas";
import type {
  LoginResponse,
  LogoutResponse,
  Tokens,
  User,
} from "../../../types/auth";

export const authService = {
  login: async (credentials: LoginFormData): Promise<LoginResponse> => {
    return await apiClient.post<unknown, LoginResponse>(
      "/auth/login",
      credentials,
    );
  },

  register: async (data: RegisterFormData): Promise<User> => {
    const nameParts = data.full_name.trim().split(" ");
    const first_name = nameParts[0];
    const last_name = nameParts.slice(1).join(" ") || undefined;

    const payload = {
      email: data.email,
      password: data.password,
      first_name,
      last_name,
    };

    return await apiClient.post<unknown, User>("/users", payload);
  },

  refreshToken: async (refreshToken: string): Promise<Tokens> => {
    return await apiClient.post<unknown, Tokens>("/auth/refresh", {
      refresh_token: refreshToken,
    });
  },

  validateToken: async (): Promise<User> => {
    return await apiClient.get<unknown, User>("/auth/validate");
  },

  logout: async (refreshToken: string): Promise<LogoutResponse> => {
    return await apiClient.post<unknown, LogoutResponse>("/auth/logout", {
      refresh_token: refreshToken,
    });
  },
};
