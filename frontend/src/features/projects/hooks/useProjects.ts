import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { projectService } from "../api/projectService";
import type { ProjectFormData } from "../../../schemas/projectSchemas";

// Centralized Query Keys
export const projectKeys = {
  all: ["projects"] as const,
  lists: () => [...projectKeys.all, "list"] as const,
  mine: () => [...projectKeys.all, "mine"] as const,
  detail: (id: number) => [...projectKeys.all, "detail", id] as const,
};

// 1. Fetch Queries
export const useProjects = () => {
  return useQuery({
    queryKey: projectKeys.lists(),
    queryFn: projectService.getAll,
  });
};

export const useMyProjects = () => {
  return useQuery({
    queryKey: projectKeys.mine(),
    queryFn: projectService.getMyProjects,
  });
};

// 2. Create Project Mutation
export const useCreateProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newProject: ProjectFormData) =>
      projectService.create(newProject),
    onSuccess: () => {
      // Invalidate all project queries so the lists automatically refresh
      queryClient.invalidateQueries({ queryKey: projectKeys.all });
    },
  });
};

// 3. Update Project Mutation
export const useUpdateProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProjectFormData }) =>
      projectService.update({ id, data }),
    onSuccess: (_, variables) => {
      // Invalidate the specific detail query and all lists
      queryClient.invalidateQueries({
        queryKey: projectKeys.detail(variables.id),
      });
      queryClient.invalidateQueries({ queryKey: projectKeys.all });
    },
  });
};

// 4. Delete Project Mutation
export const useDeleteProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => projectService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: projectKeys.all });
    },
  });
};
