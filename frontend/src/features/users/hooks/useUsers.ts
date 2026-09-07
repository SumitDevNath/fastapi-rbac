import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { userService, type UserFilterParams } from "../api/userService";
import type {
  UserAdminUpdateFormData,
  UserSelfUpdateFormData,
} from "../../../schemas/userSchemas";
// import { useAuth } from "../../../contexts/AuthContext";

export const userKeys = {
  all: ["users"] as const,
  lists: () => [...userKeys.all, "list"] as const,
  list: (filters?: UserFilterParams) =>
    [...userKeys.lists(), filters ?? {}] as const,
  detail: (id: number) => [...userKeys.all, "detail", id] as const,
  me: ["current-user"] as const,
};

export const useUsers = (filters?: UserFilterParams) => {
  // const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => userService.getAll(filters),
    // Do not run this query if the user is logged out:
    // enabled: isAuthenticated,
  });
};

export const useUser = (userId: number) => {
  return useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => userService.getById(userId),
    enabled: !!userId,
  });
};

export const useUpdateSelf = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UserSelfUpdateFormData) => userService.updateSelf(data),
    onSuccess: (updatedUser) => {
      queryClient.setQueryData(userKeys.me, updatedUser);
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      userId,
      data,
    }: {
      userId: number;
      data: UserAdminUpdateFormData;
    }) => userService.updateUser({ userId, data }),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: userKeys.detail(variables.userId),
      });
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
};
