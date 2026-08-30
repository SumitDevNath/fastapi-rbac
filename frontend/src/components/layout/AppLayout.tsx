import React from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import {
  LayoutDashboard,
  FolderKanban,
  Users,
  LogOut,
  ShieldCheck,
  Shield,
} from "lucide-react";

export const AppLayout: React.FC = () => {
  const { user, role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
      isActive
        ? "bg-indigo-600 text-white shadow-sm shadow-indigo-200"
        : "text-slate-600 hover:text-indigo-600 hover:bg-slate-100"
    }`;

  return (
    <div className="min-h-screen flex bg-slate-50 text-slate-800">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col shrink-0">
        <div className="h-16 flex items-center gap-2.5 px-6 border-b border-slate-200">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
            <ShieldCheck size={22} />
          </div>
          <span className="font-bold text-slate-900 text-base">
            RBAC Portal
          </span>
        </div>

        <nav className="p-4 space-y-1.5 flex-1">
          <NavLink to="/dashboard" className={navLinkClass}>
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </NavLink>

          <NavLink to="/projects" className={navLinkClass}>
            <FolderKanban size={18} />
            <span>Projects</span>
          </NavLink>

          {/* Role-Gated UI Navigation: Only visible to ADMIN and MANAGER */}
          {(role === "ADMIN" || role === "MANAGER") && (
            <NavLink to="/admin/users" className={navLinkClass}>
              <Users size={18} />
              <span>User Management</span>
            </NavLink>
          )}
        </nav>

        {/* User Identity Card & Logout */}
        <div className="p-4 border-t border-slate-200 bg-slate-50/50">
          <div className="flex items-center justify-between mb-3">
            <div className="truncate pr-2">
              <p className="text-xs font-semibold text-slate-900 truncate">
                {user?.email}
              </p>
              <div className="flex items-center gap-1 text-[11px] font-medium text-indigo-600">
                <Shield size={12} />
                <span>{role}</span>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
              title="Sign Out"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-y-auto">
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8">
          <h2 className="text-sm font-semibold text-slate-700">
            Enterprise Control Plane
          </h2>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              ● API Online
            </span>
          </div>
        </header>

        <div className="p-8 flex-1">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
