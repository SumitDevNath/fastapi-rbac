import React from "react";

import {
  Users,
  FolderKanban,
  ShieldCheck,
  Activity,
  // Layers,
  // Sparkles,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { useAuth } from "../../contexts/AuthContext";
import { useProjects } from "../projects/hooks/useProjects";
import { useUsers } from "../users/hooks/useUsers";
import { MetricCard } from "./components/MetricCard";

const ROLE_COLORS: Record<string, string> = {
  ADMIN: "#9333ea", // Purple
  MANAGER: "#2563eb", // Blue
  EDITOR: "#059669", // Emerald
  VIEWER: "#64748b", // Slate
};

const STATUS_COLORS = ["#10b981", "#f43f5e"]; // Emerald (Active), Rose (Inactive)

export const DashboardPage: React.FC = () => {
  const { user, role } = useAuth();
  const { data: projects, isLoading: projectsLoading } = useProjects();
  const { data: users, isLoading: usersLoading } = useUsers();

  const totalProjects = projects?.length || 0;
  const totalUsers = users?.length || 0;

  // 1. Compute Role Distribution Data for BarChart & PieChart
  const roleCounts: Record<string, number> = {
    ADMIN: 0,
    MANAGER: 0,
    EDITOR: 0,
    VIEWER: 0,
  };

  let activeUsersCount = 0;
  let inactiveUsersCount = 0;

  if (users) {
    users.forEach((u) => {
      if (roleCounts[u.role] !== undefined) {
        roleCounts[u.role]++;
      }
      if (u.is_active) {
        activeUsersCount++;
      } else {
        inactiveUsersCount++;
      }
    });
  }

  const roleChartData = Object.entries(roleCounts).map(([roleName, count]) => ({
    name: roleName,
    count,
    color: ROLE_COLORS[roleName] || "#64748b",
  }));

  const userStatusData = [
    {
      name: "Active Accounts",
      value: activeUsersCount || (user?.is_active ? 1 : 0),
    },
    { name: "Suspended Accounts", value: inactiveUsersCount },
  ];

  const isLoading = projectsLoading || usersLoading;

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-linear-to-r from-indigo-900 to-slate-900 rounded-3xl p-8 text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2">
          {/* <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-semibold">
            <Sparkles size={14} /> Enterprise Observability Center
          </div> */}
          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
            System Overview
          </h1>
        </div>

        <div className="flex items-center gap-3 self-start md:self-auto bg-white/10 backdrop-blur-md px-4 py-3 rounded-2xl border border-white/10">
          <Activity size={20} className="text-emerald-400 animate-pulse" />
          <div className="text-xs">
            <p className="text-slate-300 font-medium">Server Status</p>
            <p className="text-emerald-400 font-bold">Optimal & Active</p>
          </div>
        </div>
      </div>

      {/* KPI Metric Cards - Dynamically adjusts columns from 3 to 4 based on role */}
      <div
        className={`grid grid-cols-1 sm:grid-cols-2 ${
          role === "ADMIN" || role === "MANAGER"
            ? "lg:grid-cols-4"
            : "lg:grid-cols-3"
        } gap-6`}
      >
        <MetricCard
          title="Total Projects"
          value={isLoading ? "..." : totalProjects}
          subtitle="Managed in SQLite database"
          icon={FolderKanban}
          colorClass="bg-indigo-50 text-indigo-600"
        />

        {(role === "ADMIN" || role === "MANAGER") && (
          <MetricCard
            title="Registered Users"
            value={isLoading ? "..." : totalUsers}
            subtitle="Active identities in registry"
            icon={Users}
            colorClass="bg-blue-50 text-blue-600"
          />
        )}

        <MetricCard
          title="Assigned Role"
          value={role || "VIEWER"}
          subtitle="Current session privilege"
          icon={ShieldCheck}
          colorClass="bg-purple-50 text-purple-600"
        />

        <MetricCard
          title={
            role === "ADMIN" || role === "MANAGER"
              ? "Active Accounts"
              : "Account Status"
          }
          value={
            role === "ADMIN" || role === "MANAGER"
              ? isLoading
                ? "..."
                : `${activeUsersCount} / ${totalUsers}`
              : user?.is_active
                ? "Active"
                : "Suspended"
          }
          subtitle={
            role === "ADMIN" || role === "MANAGER"
              ? "Non-suspended user profiles"
              : "Authentication status"
          }
          icon={Activity}
          colorClass={
            user?.is_active
              ? "bg-emerald-50 text-emerald-600"
              : "bg-rose-50 text-rose-600"
          }
        />
      </div>

      {/* Charts Section */}
      {
        (role === "ADMIN" || role === "MANAGER") && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Bar Chart: Users by Role */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  User Distribution by Role
                </h3>
                <p className="text-xs text-slate-500">
                  Breakdown of system role assignments
                </p>
              </div>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={roleChartData}
                    margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                  >
                    <XAxis
                      dataKey="name"
                      tick={{ fontSize: 12, fill: "#64748b" }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      allowDecimals={false}
                      tick={{ fontSize: 12, fill: "#64748b" }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0f172a",
                        borderRadius: "12px",
                        color: "#fff",
                        border: "none",
                        fontSize: "12px",
                      }}
                    />
                    <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                      {roleChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Pie Chart: Account Status Ratio */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Account Health Ratio
                </h3>
                <p className="text-xs text-slate-500">
                  Active vs. Suspended accounts
                </p>
              </div>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={userStatusData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={85}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {userStatusData.map((_, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={STATUS_COLORS[index % STATUS_COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0f172a",
                        borderRadius: "12px",
                        color: "#fff",
                        border: "none",
                        fontSize: "12px",
                      }}
                    />
                    <Legend
                      verticalAlign="bottom"
                      wrapperStyle={{ fontSize: "12px", paddingTop: "10px" }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )
        //  : (
        //   /* Non-Admin Informational Banner */
        //   <div className="bg-slate-100 border border-slate-200 rounded-3xl p-8 text-center space-y-2">
        //     <h3 className="text-base font-bold text-slate-800">
        //       Advanced Analytics Restricted
        //     </h3>
        //     <p className="text-xs text-slate-500 max-w-md mx-auto">
        //       User distribution breakdowns require{" "}
        //       <span className="font-semibold text-slate-700">user:read</span>{" "}
        //       permissions (Manager or Admin role). You have full access to create
        //       and manage Projects.
        //     </p>
        //   </div>
        // )
      }
    </div>
  );
};
