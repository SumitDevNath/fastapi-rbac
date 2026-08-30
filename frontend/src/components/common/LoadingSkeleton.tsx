import React from "react";

interface LoadingSkeletonProps {
  variant?: "card" | "table" | "text";
  count?: number;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  variant = "card",
  count = 3,
}) => {
  const items = Array.from({ length: count }, (_, i) => i);

  if (variant === "table") {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs animate-pulse space-y-4">
        <div className="h-6 bg-slate-200 rounded-md w-1/4"></div>
        <div className="space-y-3 pt-2">
          {items.map((i) => (
            <div key={i} className="h-10 bg-slate-100 rounded-lg w-full"></div>
          ))}
        </div>
      </div>
    );
  }

  if (variant === "text") {
    return (
      <div className="animate-pulse space-y-2.5">
        <div className="h-4 bg-slate-200 rounded-md w-3/4"></div>
        <div className="h-4 bg-slate-100 rounded-md w-full"></div>
        <div className="h-4 bg-slate-100 rounded-md w-5/6"></div>
      </div>
    );
  }

  // Default: Card Grid Skeleton
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map((i) => (
        <div
          key={i}
          className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs animate-pulse space-y-4"
        >
          <div className="flex items-center justify-between">
            <div className="h-5 bg-slate-200 rounded w-1/3"></div>
            <div className="h-4 bg-slate-100 rounded w-1/6"></div>
          </div>
          <div className="h-4 bg-slate-100 rounded w-full"></div>
          <div className="h-4 bg-slate-100 rounded w-4/5"></div>
          <div className="pt-4 border-t border-slate-100 flex justify-between">
            <div className="h-3 bg-slate-200 rounded w-1/3"></div>
            <div className="h-3 bg-slate-200 rounded w-1/4"></div>
          </div>
        </div>
      ))}
    </div>
  );
};
