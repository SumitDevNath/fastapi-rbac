import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Loader2 } from "lucide-react";

export const ProtectedRoute: React.FC = () => {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        <div className="flex flex-col items-center gap-3">
          <Loader2 size={36} className="animate-spin text-indigo-400" />
          <p className="text-sm text-slate-400">
            Validating session with backend...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Preserve the current path so the user can be redirected back after logging in
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Block users whose status is not "approved"
  if (user?.status !== "approved") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white p-4">
        <div className="max-w-md w-full bg-slate-800 border border-slate-700 rounded-2xl p-8 text-center space-y-4">
          <h2 className="text-xl font-bold text-amber-400">
            Account Pending Approval
          </h2>
          <p className="text-sm text-slate-300">
            Your account ({user?.email}) has been registered, but an
            Administrator must approve your account before you can perform
            tasks.
          </p>
          <button
            onClick={() => (window.location.href = "/login")}
            className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm"
          >
            Back to Sign In
          </button>
        </div>
      </div>
    );
  }

  return <Outlet />;
};
