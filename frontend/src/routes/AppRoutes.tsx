import React from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { ProtectedRoute } from "./ProtectedRoute";
import { RoleGuard } from "./RoleGuard";
import { AppLayout } from "../components/layout/AppLayout";
import { UsersPage } from "../features/users/components/UsersPage";
import { UnauthorizedPage } from "../components/common/UnauthorizedPage";
import { LoginPage } from "../features/auth/components/LoginPage";
import { RegisterPage } from "../features/auth/components/RegisterPage";
import { DashboardPage } from "../features/dashboard/DashboardPage";
import { ProjectsPage } from "../features/projects/components/ProjectsPage";

const PublicAuthWrapper: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { isAuthenticated } = useAuth();
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 p-4">
      {children}
    </div>
  );
};

export const AppRoutes: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/login"
        element={
          <PublicAuthWrapper>
            <LoginPage onNavigateToRegister={() => navigate("/register")} />
          </PublicAuthWrapper>
        }
      />
      <Route
        path="/register"
        element={
          <PublicAuthWrapper>
            <RegisterPage onNavigateToLogin={() => navigate("/login")} />
          </PublicAuthWrapper>
        }
      />

      {/* Protected Routes (All Authenticated Roles) */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/unauthorized" element={<UnauthorizedPage />} />

          {/* Admin & Manager Only Routes */}
          <Route element={<RoleGuard allowedRoles={["ADMIN", "MANAGER"]} />}>
            <Route path="/admin/users" element={<UsersPage />} />
          </Route>
        </Route>
      </Route>

      {/* Fallback Redirect */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};
