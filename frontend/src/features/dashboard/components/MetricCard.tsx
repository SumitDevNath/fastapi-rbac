import React from "react";
import type { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  colorClass: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  colorClass,
}) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex items-center justify-between">
      <div className="space-y-1">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {title}
        </p>
        <h3 className="text-2xl font-black text-slate-900">{value}</h3>
        {subtitle && (
          <p className="text-xs text-slate-500 font-medium">{subtitle}</p>
        )}
      </div>
      <div className={`p-3.5 rounded-2xl ${colorClass}`}>
        <Icon size={24} />
      </div>
    </div>
  );
};
