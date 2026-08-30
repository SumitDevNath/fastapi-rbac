import React from "react";
import { useAuth } from "../../contexts/AuthContext";

export const DashboardPage: React.FC = () => {
  const { user, role } = useAuth();
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
      <p className="text-slate-600 text-sm">
        Welcome back,{" "}
        <span className="font-semibold text-indigo-600">{user?.email}</span>.
        You are logged in with the{" "}
        <span className="font-semibold text-slate-800">{role}</span> role.
      </p>
    </div>
  );
};
