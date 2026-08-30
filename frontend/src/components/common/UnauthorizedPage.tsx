import React from "react";
import { Link } from "react-router-dom";
import { ShieldAlert, ArrowLeft } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

export const UnauthorizedPage: React.FC = () => {
  const { role } = useAuth();

  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-100 p-8 text-center space-y-4">
        <div className="w-16 h-16 bg-rose-100 text-rose-600 rounded-2xl flex items-center justify-center mx-auto">
          <ShieldAlert size={36} />
        </div>
        <h1 className="text-2xl font-bold text-slate-900">
          403 — Access Denied
        </h1>
        <p className="text-sm text-slate-500">
          Your current role (
          <span className="font-semibold text-slate-700">{role}</span>) does not
          have permission to view this resource.
        </p>
        <div className="pt-2">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-2.5 px-5 rounded-lg transition-colors"
          >
            <ArrowLeft size={16} /> Return to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};
