import { apiClient } from "../../../api/apiClient";
import type { ProjectFormData } from "../../../schemas/projectSchemas";
import type { Project } from "../../../types/project";

export const projectService = {
  getAll: async (): Promise<Project[]> => {
    return await apiClient.get<unknown, Project[]>("/projects");
  },

  getMyProjects: async (): Promise<Project[]> => {
    return await apiClient.get<unknown, Project[]>("/projects/my");
  },

  getById: async (id: number): Promise<Project> => {
    return await apiClient.get<unknown, Project>(`/projects/${id}`);
  },

  create: async (data: ProjectFormData): Promise<Project> => {
    return await apiClient.post<unknown, Project>("/projects", data);
  },

  update: async ({
    id,
    data,
  }: {
    id: number;
    data: ProjectFormData;
  }): Promise<Project> => {
    return await apiClient.patch<unknown, Project>(`/projects/${id}`, data);
  },

  delete: async (id: number): Promise<void> => {
    return await apiClient.delete<unknown, void>(`/projects/${id}`);
  },
};
