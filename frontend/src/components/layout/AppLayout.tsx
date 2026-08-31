import React, { useState } from "react";
import { Outlet, NavLink, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import {
  LayoutDashboard,
  FolderKanban,
  Users,
  LogOut,
  ShieldCheck,
  Shield,
  Menu,
  X,
} from "lucide-react";

export const AppLayout: React.FC = () => {
  const { user, role, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Close mobile sidebar whenever the active route changes
  React.useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

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

  const NavigationContent = () => (
    <div className="flex flex-col h-full">
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-6 border-b border-slate-200">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
            <ShieldCheck size={22} />
          </div>
          <span className="font-bold text-slate-900 text-base">
            RBAC Portal
          </span>
        </div>
        {/* Close Button on Mobile Drawer */}
        <button
          onClick={() => setMobileMenuOpen(false)}
          className="md:hidden p-1.5 text-slate-400 hover:text-slate-600 rounded-lg"
        >
          <X size={20} />
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="p-4 space-y-1.5 flex-1">
        <NavLink to="/dashboard" className={navLinkClass}>
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/projects" className={navLinkClass}>
          <FolderKanban size={18} />
          <span>Projects</span>
        </NavLink>

        {(role === "ADMIN" || role === "MANAGER") && (
          <NavLink to="/admin/users" className={navLinkClass}>
            <Users size={18} />
            <span>User Management</span>
          </NavLink>
        )}
      </nav>

      {/* User Session Footer */}
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
    </div>
  );

  return (
    <div className="min-h-screen flex bg-slate-50 text-slate-800">
      {/* 1. Desktop Persistent Sidebar */}
      <aside className="hidden md:flex w-64 bg-white border-r border-slate-200 flex-col shrink-0 sticky top-0 h-screen">
        <NavigationContent />
      </aside>

      {/* 2. Mobile Backdrop Overlay */}
      {mobileMenuOpen && (
        <div
          onClick={() => setMobileMenuOpen(false)}
          className="fixed inset-0 z-40 bg-slate-900/60 backdrop-blur-xs md:hidden transition-opacity"
        />
      )}

      {/* 3. Mobile Slide-out Drawer */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-2xl transform transition-transform duration-200 ease-in-out md:hidden ${
          mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <NavigationContent />
      </div>

      {/* 4. Main Viewport */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Mobile-Only Top Bar for Hamburger Toggle */}
        <header className="md:hidden h-14 bg-white border-b border-slate-200 flex items-center px-4 sticky top-0 z-10">
          <button
            onClick={() => setMobileMenuOpen(true)}
            className="p-2 text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
            aria-label="Open Navigation Menu"
          >
            <Menu size={22} />
          </button>
        </header>

        {/* Page Content Container */}
        <div className="p-4 sm:p-6 md:p-8 flex-1 max-w-7xl w-full mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
