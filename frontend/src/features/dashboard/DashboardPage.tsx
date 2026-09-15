import React from "react";
import { useAuth } from "../../contexts/AuthContext";
import { storage } from "../../utils/storage";
import {
  ShieldCheck,
  Building2,
  Calendar,
  Key,
  CheckCircle2,
  Mail,
  User as UserIcon,
  Activity,
  Code,
} from "lucide-react";

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const accessToken = storage.getAccessToken();
  const refreshToken = storage.getRefreshToken();

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-sm">
        <div>
          <div className="flex items-center gap-2 text-emerald-400 font-semibold text-xs tracking-wider uppercase mb-1">
            <CheckCircle2 size={16} />
            <span>Identity Validated • Status: {user?.status}</span>
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Welcome, {user?.first_name} {user?.last_name}
          </h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Username: @{user?.username} (ID: #{user?.id})
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className="px-3 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-mono rounded-full font-medium uppercase">
            Role: {user?.role}
          </span>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono rounded-full font-medium uppercase">
            Provider: {user?.auth_provider}
          </span>
          <span className="px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs font-mono rounded-full font-medium">
            Facility ID: {user?.facility_id || "None"}
          </span>
        </div>
      </div>

      {/* Grid: Profile Details and Session Tokens */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Claims Detail Card */}
        <div className="lg:col-span-2 bg-slate-800 border border-slate-700 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-700 pb-3">
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              <UserIcon className="text-indigo-400" size={18} />
              Validated User Claims
            </h2>
            <span className="text-xs text-slate-400 font-mono">
              DB Record ID: {user?.id}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl space-y-1">
              <span className="text-slate-500 block text-[11px] font-medium items-center gap-1.5">
                <Mail size={13} className="text-slate-400" /> Email Address
              </span>
              <span className="text-slate-200 font-mono font-medium block">
                {user?.email}
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl space-y-1">
              <span className="text-slate-500 block text-[11px] font-medium items-center gap-1.5">
                <Building2 size={13} className="text-slate-400" /> Assigned
                Facility ID
              </span>
              <span className="text-cyan-300 font-mono font-medium block">
                {user?.facility_id ?? "Unassigned"}
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl space-y-1">
              <span className="text-slate-500 block text-[11px] font-medium items-center gap-1.5">
                <ShieldCheck size={13} className="text-slate-400" /> System Role
              </span>
              <span className="text-indigo-300 font-medium block uppercase">
                {user?.role}
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl space-y-1">
              <span className="text-slate-500 block text-[11px] font-medium items-center gap-1.5">
                <Activity size={13} className="text-slate-400" /> Account Flags
              </span>
              <span className="text-slate-300 font-mono block">
                Active:{" "}
                <span className="text-emerald-400 font-semibold">
                  {String(user?.is_active)}
                </span>{" "}
                | Must Change Pass:{" "}
                <span className="text-slate-400">
                  {String(user?.must_change_password)}
                </span>
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl space-y-1">
              <span className="text-slate-500 block text-[11px] font-medium items-center gap-1.5">
                <Calendar size={13} className="text-slate-400" /> Account
                Created
              </span>
              <span className="text-slate-300 font-mono block">
                {user?.created_at
                  ? new Date(user.created_at).toLocaleString()
                  : "N/A"}
              </span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-3.5 rounded-xl space-y-1">
              <span className="text-slate-500 block text-[11px] font-medium items-center gap-1.5">
                <Calendar size={13} className="text-slate-400" /> Last Updated
              </span>
              <span className="text-slate-300 font-mono block">
                {user?.updated_at
                  ? new Date(user.updated_at).toLocaleString()
                  : "N/A"}
              </span>
            </div>
          </div>
        </div>

        {/* Live Token Status Card */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-700 pb-3 mb-4">
              <h2 className="text-base font-semibold text-white flex items-center gap-2">
                <Key className="text-amber-400" size={18} />
                Active JWT Bearers
              </h2>
              <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                Bearer
              </span>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <span className="text-slate-400 block mb-1 text-[11px] font-medium">
                  Access Token
                </span>
                <div className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 font-mono text-[11px] text-slate-400 break-all select-all max-h-24 overflow-y-auto">
                  {accessToken || "None"}
                </div>
              </div>

              <div>
                <span className="text-slate-400 block mb-1 text-[11px] font-medium">
                  Refresh Token
                </span>
                <div className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 font-mono text-[11px] text-slate-400 break-all select-all max-h-24 overflow-y-auto">
                  {refreshToken || "None"}
                </div>
              </div>
            </div>
          </div>

          <p className="text-[11px] text-slate-500 mt-4 border-t border-slate-700/50 pt-3">
            These credentials are automatically injected into outgoing HTTP
            calls to downstream services via the shared Axios interceptor.
          </p>
        </div>
      </div>

      {/* Raw JSON Payload Accordion / Viewer */}
      <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6">
        <div className="flex items-center gap-2 text-white font-semibold text-sm mb-3">
          <Code className="text-cyan-400" size={18} />
          <span>Raw Server Response Payload</span>
        </div>
        <div className="bg-slate-950 border border-slate-900 rounded-xl p-4 overflow-x-auto">
          <pre className="text-xs font-mono text-emerald-400">
            {JSON.stringify(
              {
                user,
                tokens: {
                  access_token: accessToken,
                  refresh_token: refreshToken,
                  token_type: "bearer",
                },
              },
              null,
              2,
            )}
          </pre>
        </div>
      </div>
    </div>
  );
};
