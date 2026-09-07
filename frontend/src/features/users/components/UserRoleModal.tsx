import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { X, Loader2, ShieldCheck, AlertCircle } from "lucide-react";
import {
  userAdminUpdateSchema,
  type UserAdminUpdateFormData,
} from "../../../schemas/userSchemas";
import type { User } from "../../../types/auth";

interface UserRoleModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: User | null;
  onSubmit: (data: UserAdminUpdateFormData) => Promise<void>;
  isLoading: boolean;
  serverError?: string | null;
}

export const UserRoleModal: React.FC<UserRoleModalProps> = ({
  isOpen,
  onClose,
  user,
  onSubmit,
  isLoading,
  serverError,
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<UserAdminUpdateFormData>({
    resolver: zodResolver(userAdminUpdateSchema),
    defaultValues: {
      role: "user",
      is_active: true,
      status: "pending",
    },
  });

  useEffect(() => {
    if (user) {
      reset({
        role: user.role,
        is_active: user.is_active,
        status: user.status || "pending",
      });
    }
  }, [user, reset, isOpen]);

  if (!isOpen || !user) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl border border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
              <ShieldCheck size={18} />
            </div>
            <div>
              <h3 className="font-bold text-slate-800 text-sm">
                Administrative Profile Edit
              </h3>
              <p className="text-xs text-slate-400 truncate max-w-[240px]">
                {user.email}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg"
          >
            <X size={18} />
          </button>
        </div>

        {serverError && (
          <div className="mx-6 mt-4 p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-xs flex items-center gap-2">
            <AlertCircle size={16} className="shrink-0" />
            <span>{serverError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Assigned Role
            </label>
            <select
              {...register("role")}
              className="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-200 font-medium"
            >
              <option value="user">User (Standard Access)</option>
              <option value="EDITOR">Editor (Project Create & Update)</option>
              <option value="MANAGER">
                Manager (Project Full & User Read)
              </option>
              <option value="ADMIN">Admin (Full System Governance)</option>
            </select>
            {errors.role && (
              <p className="text-xs text-rose-500 mt-1">
                {errors.role.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Account Status
            </label>
            <select
              {...register("status")}
              className="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-200"
            >
              <option value="pending">Pending Approval</option>
              <option value="approved">Approved</option>
              <option value="suspended">Suspended</option>
            </select>
          </div>

          <div className="pt-2 flex items-center gap-3">
            <input
              type="checkbox"
              id="modal_is_active"
              {...register("is_active")}
              className="w-4 h-4 rounded text-indigo-600 border-slate-300"
            />
            <label
              htmlFor="modal_is_active"
              className="text-xs font-medium text-slate-700 cursor-pointer"
            >
              Account Active
            </label>
          </div>

          <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white text-sm font-medium rounded-lg flex items-center gap-2"
            >
              {isLoading && <Loader2 size={16} className="animate-spin" />}
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
