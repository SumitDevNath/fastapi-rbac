import { useEffect, useState } from "react";
import { ShieldCheck, CheckCircle2, XCircle, RefreshCw } from "lucide-react";
import { apiClient } from "./api/apiClient";

interface HealthStatus {
  status: string;
  database: string;
  version: string;
}

export default function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.get<unknown, HealthStatus>("/health");
      setHealth(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white p-4">
      <div className="max-w-md w-full bg-slate-800 rounded-xl p-8 shadow-2xl border border-slate-700">
        <div className="flex justify-center mb-4 text-emerald-400">
          <ShieldCheck size={48} />
        </div>
        <h1 className="text-2xl font-bold text-center mb-2">
          FastAPI + React API Bridge
        </h1>
        <p className="text-slate-400 text-sm text-center mb-6">
          Centralized Axios client with Request & Response interceptors.
        </p>

        <div className="bg-slate-900/80 p-4 rounded-lg border border-slate-700 space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-400">Backend Connection:</span>
            {loading ? (
              <span className="flex items-center text-amber-400 text-xs">
                <RefreshCw size={14} className="animate-spin mr-1" />{" "}
                Connecting...
              </span>
            ) : health ? (
              <span className="flex items-center text-emerald-400 text-xs font-semibold">
                <CheckCircle2 size={14} className="mr-1" /> ONLINE
              </span>
            ) : (
              <span className="flex items-center text-rose-400 text-xs font-semibold">
                <XCircle size={14} className="mr-1" /> OFFLINE
              </span>
            )}
          </div>

          {health && (
            <div className="text-xs font-mono bg-slate-950 p-2.5 rounded border border-slate-800 space-y-1 text-slate-300">
              <div>
                API Status:{" "}
                <span className="text-emerald-400">{health.status}</span>
              </div>
              <div>
                Database:{" "}
                <span className="text-emerald-400">{health.database}</span>
              </div>
              <div>
                Version:{" "}
                <span className="text-slate-400">{health.version}</span>
              </div>
            </div>
          )}

          {error && (
            <div className="text-xs bg-rose-950/50 border border-rose-800 text-rose-300 p-2.5 rounded">
              {error}
            </div>
          )}
        </div>

        <button
          onClick={checkHealth}
          disabled={loading}
          className="mt-5 w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm flex items-center justify-center gap-2"
        >
          <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
          Recheck Backend Status
        </button>
      </div>
    </div>
  );
}
