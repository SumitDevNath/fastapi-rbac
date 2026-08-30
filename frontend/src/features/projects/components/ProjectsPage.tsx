import React, { useState } from "react";
import { useAuth } from "../../../contexts/AuthContext";
import { useToast } from "../../../contexts/ToastContext";
import {
  useProjects,
  useCreateProject,
  useUpdateProject,
  useDeleteProject,
} from "../hooks/useProjects";
import { ProjectModal } from "./ProjectModal";
import type { Project } from "../../../types/project";
import type { ProjectFormData } from "../../../schemas/projectSchemas";
import {
  FolderKanban,
  Plus,
  RefreshCw,
  AlertCircle,
  Calendar,
  User as UserIcon,
  Layers,
  Edit2,
  Trash2,
} from "lucide-react";

export const ProjectsPage: React.FC = () => {
  const { role } = useAuth();
  const toast = useToast();
  const {
    data: projects,
    isLoading,
    isError,
    error,
    refetch,
    isFetching,
  } = useProjects();

  const createMutation = useCreateProject();
  const updateMutation = useUpdateProject();
  const deleteMutation = useDeleteProject();

  const [modalOpen, setModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [modalError, setModalError] = useState<string | null>(null);

  const canCreateOrEdit =
    role === "ADMIN" || role === "MANAGER" || role === "EDITOR";
  const canDelete = role === "ADMIN" || role === "MANAGER";

  const handleOpenCreate = () => {
    setEditingProject(null);
    setModalError(null);
    setModalOpen(true);
  };

  const handleOpenEdit = (project: Project) => {
    setEditingProject(project);
    setModalError(null);
    setModalOpen(true);
  };

  const handleFormSubmit = async (formData: ProjectFormData) => {
    setModalError(null);
    try {
      if (editingProject) {
        await updateMutation.mutateAsync({
          id: editingProject.id,
          data: formData,
        });
        toast.success(`Project "${formData.title}" updated successfully!`);
      } else {
        await createMutation.mutateAsync(formData);
        toast.success(`Project "${formData.title}" created successfully!`);
      }
      setModalOpen(false);
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Failed to save project.";
      setModalError(msg);
      toast.error(msg, "Action Failed");
    }
  };

  const handleDelete = async (projectId: number, projectTitle: string) => {
    if (window.confirm(`Are you sure you want to delete "${projectTitle}"?`)) {
      try {
        await deleteMutation.mutateAsync(projectId);
        toast.success(`Project "${projectTitle}" was deleted.`);
      } catch (err: unknown) {
        const msg =
          err instanceof Error ? err.message : "Failed to delete project.";
        toast.error(msg, "Deletion Denied");
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Project Management
          </h1>
          <p className="text-sm text-slate-500">
            Real-time CRUD resource center with integrated toast notifications.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              refetch();
              toast.info("Synchronizing with SQLite database...");
            }}
            disabled={isFetching}
            className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-medium py-2 px-3.5 rounded-lg transition-colors shadow-xs"
          >
            <RefreshCw
              size={16}
              className={isFetching ? "animate-spin text-indigo-600" : ""}
            />
            <span>{isFetching ? "Syncing..." : "Sync Cache"}</span>
          </button>

          {canCreateOrEdit && (
            <button
              onClick={handleOpenCreate}
              className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition-colors shadow-xs"
            >
              <Plus size={16} />
              <span>Create Project</span>
            </button>
          )}
        </div>
      </div>

      {/* Loading Skeleton */}
      {isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((n) => (
            <div
              key={n}
              className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs animate-pulse space-y-4"
            >
              <div className="h-5 bg-slate-200 rounded w-2/3"></div>
              <div className="h-4 bg-slate-100 rounded w-full"></div>
              <div className="h-4 bg-slate-100 rounded w-4/5"></div>
            </div>
          ))}
        </div>
      )}

      {/* Error State */}
      {isError && (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-center space-y-3">
          <div className="w-12 h-12 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto">
            <AlertCircle size={24} />
          </div>
          <h3 className="text-base font-bold text-rose-900">
            Failed to load projects
          </h3>
          <p className="text-sm text-rose-700 max-w-md mx-auto">
            {error instanceof Error ? error.message : "An error occurred."}
          </p>
          <button
            onClick={() => refetch()}
            className="bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold py-2 px-4 rounded-lg"
          >
            Retry Request
          </button>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !isError && projects && projects.length === 0 && (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center space-y-3">
          <div className="w-14 h-14 bg-indigo-50 text-indigo-500 rounded-2xl flex items-center justify-center mx-auto">
            <Layers size={28} />
          </div>
          <h3 className="text-base font-bold text-slate-800">
            No Projects Found
          </h3>
          <p className="text-sm text-slate-500 max-w-sm mx-auto">
            Get started by creating your first project using the button above.
          </p>
        </div>
      )}

      {/* Project Cards Grid */}
      {!isLoading && !isError && projects && projects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs hover:shadow-md transition-shadow flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-indigo-600">
                    <FolderKanban size={18} />
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 font-mono">
                      PROJ-#{project.id}
                    </span>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center gap-1">
                    {canCreateOrEdit && (
                      <button
                        onClick={() => handleOpenEdit(project)}
                        className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                        title="Edit Project"
                      >
                        <Edit2 size={15} />
                      </button>
                    )}
                    {canDelete && (
                      <button
                        onClick={() => handleDelete(project.id, project.title)}
                        className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                        title="Delete Project"
                      >
                        <Trash2 size={15} />
                      </button>
                    )}
                  </div>
                </div>

                <h3 className="text-lg font-bold text-slate-900 leading-snug">
                  {project.title}
                </h3>
                <p className="text-sm text-slate-600 line-clamp-3">
                  {project.description || (
                    <span className="italic text-slate-400">
                      No description provided.
                    </span>
                  )}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <div className="flex items-center gap-1.5 font-medium text-slate-700">
                  <UserIcon size={14} className="text-indigo-500" />
                  <span>
                    {project.owner?.email || `User #${project.owner_id}`}
                  </span>
                </div>
                <div className="flex items-center gap-1 text-slate-400">
                  <Calendar size={13} />
                  <span>
                    {new Date(project.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Project Create / Edit Modal */}
      <ProjectModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleFormSubmit}
        initialData={editingProject}
        isLoading={createMutation.isPending || updateMutation.isPending}
        serverError={modalError}
      />
    </div>
  );
};
