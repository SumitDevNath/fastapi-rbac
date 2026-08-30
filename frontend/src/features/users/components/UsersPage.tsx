import React, { useState } from "react";
import { useAuth } from "../../../contexts/AuthContext";
import { useUsers, useUpdateUserRole } from "../hooks/useUsers";
import { UserRoleModal } from "./UserRoleModal";
import type { User } from "../../../types/auth";
import type { UserRoleUpdateFormData } from "../../../schemas/userSchemas";
import {
  Users,
  RefreshCw,
  AlertCircle,
  Shield,
  CheckCircle2,
  XCircle,
  SlidersHorizontal,
} from "lucide-react";

export const UsersPage: React.FC = () => {
  const { role: currentRole } = useAuth();
  const {
    data: users,
    isLoading,
    isError,
    error,
    refetch,
    isFetching,
  } = useUsers();
  const updateRoleMutation = useUpdateUserRole();

  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const isAdmin = currentRole === "ADMIN";

  const handleOpenEdit = (user: User) => {
    setSelectedUser(user);
    setModalError(null);
    setModalOpen(true);
  };

  const handleFormSubmit = async (data: UserRoleUpdateFormData) => {
    if (!selectedUser) return;
    setModalError(null);
    try {
      await updateRoleMutation.mutateAsync({ userId: selectedUser.id, data });
      setModalOpen(false);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setModalError(err.message);
      } else {
        setModalError("Failed to update user role.");
      }
    }
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case "ADMIN":
        return "bg-purple-50 text-purple-700 border-purple-200";
      case "MANAGER":
        return "bg-blue-50 text-blue-700 border-blue-200";
      case "EDITOR":
        return "bg-emerald-50 text-emerald-700 border-emerald-200";
      default:
        return "bg-slate-100 text-slate-700 border-slate-200";
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            User Identity & Access Management
          </h1>
          <p className="text-sm text-slate-500">
            Governed users in SQLite with RBAC privilege assignments.
          </p>
        </div>

        <button
          onClick={() => refetch()}
          disabled={isFetching}
          className="inline-flex items-center gap-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-medium py-2 px-3.5 rounded-lg transition-colors shadow-xs self-start"
        >
          <RefreshCw
            size={16}
            className={isFetching ? "animate-spin text-indigo-600" : ""}
          />
          <span>{isFetching ? "Syncing..." : "Sync Users"}</span>
        </button>
      </div>

      {isLoading && (
        <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-xs animate-pulse space-y-4">
          <div className="h-6 bg-slate-200 rounded w-1/4"></div>
          <div className="h-10 bg-slate-100 rounded w-full"></div>
          <div className="h-10 bg-slate-100 rounded w-full"></div>
          <div className="h-10 bg-slate-100 rounded w-full"></div>
        </div>
      )}

      {isError && (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-center space-y-3">
          <div className="w-12 h-12 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto">
            <AlertCircle size={24} />
          </div>
          <h3 className="text-base font-bold text-rose-900">
            Access Restricted
          </h3>
          <p className="text-sm text-rose-700 max-w-md mx-auto">
            {error instanceof Error
              ? error.message
              : "Unable to fetch user registry."}
          </p>
        </div>
      )}

      {!isLoading && !isError && users && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-50 text-xs font-semibold uppercase tracking-wider text-slate-500 border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-6">User ID</th>
                  <th className="py-3.5 px-6">Email Address</th>
                  <th className="py-3.5 px-6">Assigned Role</th>
                  <th className="py-3.5 px-6">Status</th>
                  <th className="py-3.5 px-6">Joined Date</th>
                  {isAdmin && (
                    <th className="py-3.5 px-6 text-right">Actions</th>
                  )}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-normal">
                {users.map((u) => (
                  <tr
                    key={u.id}
                    className="hover:bg-slate-50/80 transition-colors"
                  >
                    <td className="py-4 px-6 font-mono text-xs text-slate-400">
                      #{u.id}
                    </td>
                    <td className="py-4 px-6 font-medium text-slate-900">
                      {u.email}
                    </td>
                    <td className="py-4 px-6">
                      <span
                        className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getRoleBadge(
                          u.role,
                        )}`}
                      >
                        <Shield size={12} />
                        {u.role}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      {u.is_active ? (
                        <span className="inline-flex items-center gap-1 text-emerald-600 text-xs font-medium">
                          <CheckCircle2 size={14} /> Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-slate-400 text-xs font-medium">
                          <XCircle size={14} /> Suspended
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-6 text-xs text-slate-400">
                      {new Date(u.created_at).toLocaleDateString()}
                    </td>
                    {isAdmin && (
                      <td className="py-4 px-6 text-right">
                        <button
                          onClick={() => handleOpenEdit(u)}
                          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 text-slate-600 text-xs font-medium rounded-lg transition-colors"
                        >
                          <SlidersHorizontal size={13} />
                          <span>Edit Role</span>
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <UserRoleModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        user={selectedUser}
        onSubmit={handleFormSubmit}
        isLoading={updateRoleMutation.isPending}
        serverError={modalError}
      />
    </div>
  );
};
