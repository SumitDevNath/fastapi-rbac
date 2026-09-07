import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { UserPlus, AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { useAuth } from "../../../contexts/AuthContext";
import {
  registerSchema,
  type RegisterFormData,
} from "../../../schemas/authSchemas";

interface RegisterPageProps {
  onNavigateToLogin: () => void;
}

export const RegisterPage: React.FC<RegisterPageProps> = ({
  onNavigateToLogin,
}) => {
  const { register: registerUser } = useAuth();
  const [serverError, setServerError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      full_name: "",
      email: "",
      password: "",
      confirm_password: "",
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    setServerError(null);
    try {
      await registerUser(data);
      setSuccess(true);
    } catch (err: unknown) {
      setServerError(
        err instanceof Error ? err.message : "Registration failed.",
      );
    }
  };

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
          <UserPlus size={24} />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-900">Create Account</h2>
          <p className="text-xs text-slate-500">Sign up to join the portal</p>
        </div>
      </div>

      {serverError && (
        <div className="mb-5 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
          <AlertCircle size={16} className="shrink-0" />
          <span>{serverError}</span>
        </div>
      )}

      {success ? (
        <div className="text-center py-6 space-y-4">
          <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
            <CheckCircle2 size={24} />
          </div>
          <h3 className="text-base font-bold text-slate-800">
            Registration Successful!
          </h3>
          <p className="text-xs text-slate-500">
            Your account has been created. Please sign in to continue.
          </p>
          <button
            onClick={onNavigateToLogin}
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition-colors"
          >
            Go to Sign In
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Full Name
            </label>
            <input
              type="text"
              {...register("full_name")}
              placeholder="Alice Johnson"
              className={`w-full px-3.5 py-2 text-sm bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 transition-all ${
                errors.full_name
                  ? "border-rose-400 focus:ring-rose-200"
                  : "border-slate-200 focus:ring-emerald-200 focus:border-emerald-500"
              }`}
            />
            {errors.full_name && (
              <p className="text-xs text-rose-500 mt-1">
                {errors.full_name.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              {...register("email")}
              placeholder="user@example.com"
              className={`w-full px-3.5 py-2 text-sm bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 transition-all ${
                errors.email
                  ? "border-rose-400 focus:ring-rose-200"
                  : "border-slate-200 focus:ring-emerald-200 focus:border-emerald-500"
              }`}
            />
            {errors.email && (
              <p className="text-xs text-rose-500 mt-1">
                {errors.email.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Password
            </label>
            <input
              type="password"
              {...register("password")}
              placeholder="••••••••"
              className={`w-full px-3.5 py-2 text-sm bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 transition-all ${
                errors.password
                  ? "border-rose-400 focus:ring-rose-200"
                  : "border-slate-200 focus:ring-emerald-200 focus:border-emerald-500"
              }`}
            />
            {errors.password && (
              <p className="text-xs text-rose-500 mt-1">
                {errors.password.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Confirm Password
            </label>
            <input
              type="password"
              {...register("confirm_password")}
              placeholder="••••••••"
              className={`w-full px-3.5 py-2 text-sm bg-slate-50 border rounded-lg focus:outline-none focus:ring-2 transition-all ${
                errors.confirm_password
                  ? "border-rose-400 focus:ring-rose-200"
                  : "border-slate-200 focus:ring-emerald-200 focus:border-emerald-500"
              }`}
            />
            {errors.confirm_password && (
              <p className="text-xs text-rose-500 mt-1">
                {errors.confirm_password.message}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors text-sm flex items-center justify-center gap-2 disabled:bg-slate-300 mt-2 shadow-sm"
          >
            {isSubmitting ? (
              <>
                <Loader2 size={16} className="animate-spin" /> Creating
                Account...
              </>
            ) : (
              "Create Account"
            )}
          </button>
        </form>
      )}

      {!success && (
        <div className="mt-6 text-center text-xs text-slate-500">
          Already have an account?{" "}
          <button
            onClick={onNavigateToLogin}
            className="text-emerald-600 font-semibold hover:underline"
          >
            Sign In
          </button>
        </div>
      )}
    </div>
  );
};
