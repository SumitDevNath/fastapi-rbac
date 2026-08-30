import React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  isRetrying?: boolean;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "Failed to load resource",
  message,
  onRetry,
  isRetrying = false,
}) => {
  return (
    <div className="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-center space-y-4 shadow-xs">
      <div className="w-12 h-12 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto">
        <AlertCircle size={24} />
      </div>
      <div className="space-y-1">
        <h3 className="text-base font-bold text-rose-950">{title}</h3>
        <p className="text-xs text-rose-700 max-w-md mx-auto leading-relaxed font-mono">
          {message}
        </p>
      </div>
      {onRetry && (
        <div className="pt-1">
          <button
            onClick={onRetry}
            disabled={isRetrying}
            className="inline-flex items-center gap-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold py-2 px-4 rounded-lg transition-colors shadow-xs disabled:bg-rose-400"
          >
            <RefreshCw size={14} className={isRetrying ? "animate-spin" : ""} />
            <span>{isRetrying ? "Retrying..." : "Retry Request"}</span>
          </button>
        </div>
      )}
    </div>
  );
};
