import { ShieldCheck } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white p-4">
      <div className="max-w-md w-full bg-slate-800 rounded-xl p-8 shadow-2xl border border-slate-700 text-center">
        <div className="flex justify-center mb-4 text-emerald-400">
          <ShieldCheck size={48} />
        </div>
        <h1 className="text-2xl font-bold mb-2">FastAPI + React RBAC Client</h1>
        <p className="text-slate-400 text-sm mb-6">
          Vite, TypeScript, Tailwind CSS, TanStack Query & Context API
          initialized.
        </p>
        <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-700 text-xs font-mono text-emerald-300">
          Target API: {import.meta.env.VITE_API_BASE_URL || "Not configured"}
        </div>
      </div>
    </div>
  );
}
