import { apiClient } from "../../../api/apiClient";
import type { UserRoleUpdateFormData } from "../../../schemas/userSchemas";
import type { User } from "../../../types/auth";

export const userService = {
  getAll: async (): Promise<User[]> => {
    return await apiClient.get<unknown, User[]>("/users");
  },

  updateRole: async ({
    userId,
    data,
  }: {
    userId: number;
    data: UserRoleUpdateFormData;
  }): Promise<User> => {
    return await apiClient.patch<unknown, User>(`/users/${userId}/role`, data);
  },
};
