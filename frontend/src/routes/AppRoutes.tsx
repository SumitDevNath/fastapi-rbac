// import React, { Suspense, lazy } from "react";
// import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
// import { useAuth } from "../contexts/AuthContext";
// import { ProtectedRoute } from "./ProtectedRoute";
// import { RoleGuard } from "./RoleGuard";
// import { AppLayout } from "../components/layout/AppLayout";
// import { Loader2 } from "lucide-react";

// // Lazy-loaded Feature Chunks
// const LoginPage = lazy(() =>
//   import("../features/auth/components/LoginPage").then((m) => ({
//     default: m.LoginPage,
//   })),
// );
// const RegisterPage = lazy(() =>
//   import("../features/auth/components/RegisterPage").then((m) => ({
//     default: m.RegisterPage,
//   })),
// );
// const DashboardPage = lazy(() =>
//   import("../features/dashboard/DashboardPage").then((m) => ({
//     default: m.DashboardPage,
//   })),
// );
// const ProjectsPage = lazy(() =>
//   import("../features/projects/components/ProjectsPage").then((m) => ({
//     default: m.ProjectsPage,
//   })),
// );
// const UsersPage = lazy(() =>
//   import("../features/users/components/UsersPage").then((m) => ({
//     default: m.UsersPage,
//   })),
// );
// const UnauthorizedPage = lazy(() =>
//   import("../components/common/UnauthorizedPage").then((m) => ({
//     default: m.UnauthorizedPage,
//   })),
// );

// // Fallback Loader for Suspense
// const RouteLoadingFallback: React.FC = () => (
//   <div className="min-h-[50vh] flex flex-col items-center justify-center p-8">
//     <div className="flex flex-col items-center gap-3">
//       <Loader2 size={32} className="animate-spin text-indigo-600" />
//       <p className="text-xs font-medium text-slate-400">Loading module...</p>
//     </div>
//   </div>
// );

// const PublicAuthWrapper: React.FC<{ children: React.ReactNode }> = ({
//   children,
// }) => {
//   const { isAuthenticated } = useAuth();
//   if (isAuthenticated) {
//     return <Navigate to="/dashboard" replace />;
//   }
//   return (
//     <div className="min-h-screen flex items-center justify-center bg-slate-900 p-4">
//       {children}
//     </div>
//   );
// };

// export const AppRoutes: React.FC = () => {
//   const navigate = useNavigate();

//   return (
//     <Suspense fallback={<RouteLoadingFallback />}>
//       <Routes>
//         {/* Public Routes */}
//         <Route
//           path="/login"
//           element={
//             <PublicAuthWrapper>
//               <LoginPage onNavigateToRegister={() => navigate("/register")} />
//             </PublicAuthWrapper>
//           }
//         />
//         <Route
//           path="/register"
//           element={
//             <PublicAuthWrapper>
//               <RegisterPage onNavigateToLogin={() => navigate("/login")} />
//             </PublicAuthWrapper>
//           }
//         />

//         {/* Protected Routes */}
//         <Route element={<ProtectedRoute />}>
//           <Route element={<AppLayout />}>
//             <Route path="/dashboard" element={<DashboardPage />} />
//             <Route path="/projects" element={<ProjectsPage />} />
//             <Route path="/unauthorized" element={<UnauthorizedPage />} />

//             {/* Admin & Manager Restricted */}
//             <Route element={<RoleGuard allowedRoles={["ADMIN", "MANAGER"]} />}>
//               <Route path="/admin/users" element={<UsersPage />} />
//             </Route>
//           </Route>
//         </Route>

//         <Route path="*" element={<Navigate to="/dashboard" replace />} />
//       </Routes>
//     </Suspense>
//   );
// };

import React from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { ProtectedRoute } from "./ProtectedRoute";
import { RoleGuard } from "./RoleGuard";
import { AppLayout } from "../components/layout/AppLayout";

// Direct Static Imports (No React.lazy)
import { LoginPage } from "../features/auth/components/LoginPage";
import { RegisterPage } from "../features/auth/components/RegisterPage";
import { DashboardPage } from "../features/dashboard/DashboardPage";
import { ProjectsPage } from "../features/projects/components/ProjectsPage";
import { UsersPage } from "../features/users/components/UsersPage";
import { UnauthorizedPage } from "../components/common/UnauthorizedPage";

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

      {/* Protected Routes */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/unauthorized" element={<UnauthorizedPage />} />

          {/* Admin & Manager Restricted */}
          <Route element={<RoleGuard allowedRoles={["ADMIN", "MANAGER"]} />}>
            <Route path="/admin/users" element={<UsersPage />} />
          </Route>
        </Route>
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};
