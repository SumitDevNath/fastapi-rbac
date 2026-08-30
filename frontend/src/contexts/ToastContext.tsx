import React, { createContext, useContext, useState, useCallback } from "react";
import {
  CheckCircle2,
  AlertCircle,
  Info,
  AlertTriangle,
  X,
} from "lucide-react";

export type ToastType = "success" | "error" | "warning" | "info";

export interface Toast {
  id: string;
  type: ToastType;
  title?: string;
  message: string;
}

interface ToastContextType {
  showToast: (message: string, type?: ToastType, title?: string) => void;
  success: (message: string, title?: string) => void;
  error: (message: string, title?: string) => void;
  warning: (message: string, title?: string) => void;
  info: (message: string, title?: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const showToast = useCallback(
    (message: string, type: ToastType = "info", title?: string) => {
      const id = `${Date.now()}-${Math.random()}`;
      const newToast: Toast = { id, type, title, message };

      setToasts((prev) => [...prev, newToast]);

      // Automatically dismiss toast after 4.5 seconds
      setTimeout(() => {
        removeToast(id);
      }, 4500);
    },
    [removeToast],
  );

  const success = (message: string, title?: string) =>
    showToast(message, "success", title);
  const error = (message: string, title?: string) =>
    showToast(message, "error", title);
  const warning = (message: string, title?: string) =>
    showToast(message, "warning", title);
  const info = (message: string, title?: string) =>
    showToast(message, "info", title);

  const getToastIcon = (type: ToastType) => {
    switch (type) {
      case "success":
        return <CheckCircle2 size={18} className="text-emerald-500 shrink-0" />;
      case "error":
        return <AlertCircle size={18} className="text-rose-500 shrink-0" />;
      case "warning":
        return <AlertTriangle size={18} className="text-amber-500 shrink-0" />;
      default:
        return <Info size={18} className="text-indigo-500 shrink-0" />;
    }
  };

  const getToastBorder = (type: ToastType) => {
    switch (type) {
      case "success":
        return "border-emerald-200 bg-emerald-50/90 text-emerald-950";
      case "error":
        return "border-rose-200 bg-rose-50/90 text-rose-950";
      case "warning":
        return "border-amber-200 bg-amber-50/90 text-amber-950";
      default:
        return "border-indigo-200 bg-indigo-50/90 text-indigo-950";
    }
  };

  return (
    <ToastContext.Provider value={{ showToast, success, error, warning, info }}>
      {children}

      {/* Floating Toast Notification Container */}
      <div className="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto flex items-start gap-3 p-4 rounded-xl border shadow-lg backdrop-blur-xs transition-all animate-in slide-in-from-bottom-5 duration-200 ${getToastBorder(
              t.type,
            )}`}
          >
            {getToastIcon(t.type)}
            <div className="flex-1 text-xs">
              {t.title && (
                <h4 className="font-bold mb-0.5 text-slate-900">{t.title}</h4>
              )}
              <p className="leading-relaxed">{t.message}</p>
            </div>
            <button
              onClick={() => removeToast(t.id)}
              className="text-slate-400 hover:text-slate-700 p-0.5 rounded transition-colors"
            >
              <X size={14} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextType => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
};
