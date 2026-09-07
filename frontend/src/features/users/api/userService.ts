import { apiClient } from "../../../api/apiClient";
import type {
  UserAdminUpdateFormData,
  UserSelfUpdateFormData,
} from "../../../schemas/userSchemas";
import type { User } from "../../../types/auth";

export interface UserFilterParams {
  status?: string;
  role?: string;
  facility_id?: string;
}

export const userService = {
  getAll: async (filters?: UserFilterParams): Promise<User[]> => {
    return await apiClient.get<unknown, User[]>("/users", { params: filters });
  },

  getById: async (userId: number): Promise<User> => {
    return await apiClient.get<unknown, User>(`/users/${userId}`);
  },

  updateSelf: async (data: UserSelfUpdateFormData): Promise<User> => {
    return await apiClient.put<unknown, User>("/users/me", data);
  },

  updateUser: async ({
    userId,
    data,
  }: {
    userId: number;
    data: UserAdminUpdateFormData;
  }): Promise<User> => {
    return await apiClient.put<unknown, User>(`/users/${userId}`, data);
  },
};
