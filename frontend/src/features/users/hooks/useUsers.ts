import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { userService } from "../api/userService";
import type { UserRoleUpdateFormData } from "../../../schemas/userSchemas";

export const userKeys = {
  all: ["users"] as const,
  lists: () => [...userKeys.all, "list"] as const,
};

export const useUsers = () => {
  return useQuery({
    queryKey: userKeys.lists(),
    queryFn: userService.getAll,
  });
};

export const useUpdateUserRole = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      userId,
      data,
    }: {
      userId: number;
      data: UserRoleUpdateFormData;
    }) => userService.updateRole({ userId, data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.all });
    },
  });
};
