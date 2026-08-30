import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Loader2 } from "lucide-react";

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        <div className="flex flex-col items-center gap-3">
          <Loader2 size={36} className="animate-spin text-indigo-400" />
          <p className="text-sm text-slate-400">Authenticating session...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Preserve the current path so the user can be redirected back after logging in
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
};
