import React, { useState } from "react";
import { AuthProvider, useAuth } from "./contexts/AuthContext";

import {
  ShieldCheck,
  LogOut,
  UserCheck,
  KeyRound,
  Loader2,
} from "lucide-react";
import { LoginPage } from "./components/LoginPage";
import { RegisterPage } from "./components/RegisterPage";

const AppContent: React.FC = () => {
  const { user, isAuthenticated, loading, logout } = useAuth();
  const [authView, setAuthView] = useState<"login" | "register">("login");

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        <div className="flex flex-col items-center gap-3">
          <Loader2 size={36} className="animate-spin text-indigo-400" />
          <p className="text-sm text-slate-400">Verifying session...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 p-4">
        {authView === "login" ? (
          <LoginPage onNavigateToRegister={() => setAuthView("register")} />
        ) : (
          <RegisterPage onNavigateToLogin={() => setAuthView("login")} />
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6 flex flex-col items-center justify-center">
      <div className="max-w-md w-full bg-slate-800 border border-slate-700 rounded-2xl p-8 shadow-2xl space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20">
              <ShieldCheck size={28} />
            </div>
            <div>
              <h1 className="text-lg font-bold">Authenticated Session</h1>
              <p className="text-xs text-slate-400">AuthContext state active</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
            title="Sign Out"
          >
            <LogOut size={20} />
          </button>
        </div>

        <div className="space-y-3 text-sm">
          <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-700/60">
            <span className="text-slate-400 flex items-center gap-2">
              <UserCheck size={16} className="text-indigo-400" /> Email:
            </span>
            <span className="font-mono text-slate-200">{user?.email}</span>
          </div>

          <div className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-700/60">
            <span className="text-slate-400 flex items-center gap-2">
              <KeyRound size={16} className="text-amber-400" /> Role:
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              {user?.role}
            </span>
          </div>
        </div>

        <button
          onClick={logout}
          className="w-full bg-rose-600 hover:bg-rose-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm flex items-center justify-center gap-2"
        >
          <LogOut size={16} /> Sign Out
        </button>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
