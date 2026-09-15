import React, { useState } from "react";
import { useResourceData } from "../hooks/useResourceData";
import {
  Database,
  Search,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
} from "lucide-react";

export const ResourceExplorerPage: React.FC = () => {
  const [pathInput, setPathInput] = useState<string>("/data");
  const [activeEndpoint, setActiveEndpoint] = useState<string>("/data");

  const { data, isLoading, isError, error, refetch, isFetching } =
    useResourceData(activeEndpoint);

  const handleFetch = (e: React.FormEvent) => {
    e.preventDefault();
    if (pathInput.trim()) {
      setActiveEndpoint(pathInput.trim());
    }
  };

  const isArrayData = Array.isArray(data);
  const isObjectData =
    data !== null && typeof data === "object" && !isArrayData;

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Database className="text-indigo-400" size={24} />
            External Resource Service
          </h1>
          <p className="text-sm text-slate-400">
            Authorized requests verified via Bearer JWT from the Auth Service.
          </p>
        </div>

        {/* Dynamic Endpoint Query Bar */}
        <form onSubmit={handleFetch} className="flex items-center gap-2">
          <div className="relative">
            <input
              type="text"
              value={pathInput}
              onChange={(e) => setPathInput(e.target.value)}
              placeholder="e.g. /items or /records"
              className="px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500 w-64"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading || isFetching}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-medium transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <RefreshCw size={14} className={isFetching ? "animate-spin" : ""} />
            Fetch
          </button>
        </form>
      </div>

      {/* State Displays */}
      {isLoading && (
        <div className="p-8 text-center bg-slate-800/50 rounded-xl border border-slate-700">
          <RefreshCw
            className="animate-spin text-indigo-400 mx-auto mb-2"
            size={28}
          />
          <p className="text-slate-300 text-sm">
            Querying resource backend with your session token...
          </p>
        </div>
      )}

      {isError && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-start gap-3">
          <AlertCircle className="text-rose-400 shrink-0 mt-0.5" size={20} />
          <div>
            <h3 className="text-sm font-semibold text-rose-300">
              Request Failed
            </h3>
            <p className="text-xs text-rose-200 mt-1">
              {error instanceof Error
                ? error.message
                : "Unable to retrieve data from resource service."}
            </p>
          </div>
        </div>
      )}

      {/* Structured Presentation of Results */}
      {!isLoading && !isError && data !== undefined && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1 text-emerald-400 font-medium">
              <CheckCircle2 size={14} /> 200 OK — Data received
            </span>
            <span>
              Target: {import.meta.env.VITE_RESOURCE_API_URL}
              {activeEndpoint}
            </span>
          </div>

          {/* If the response is a list/table */}
          {isArrayData && (
            <div className="overflow-x-auto rounded-xl border border-slate-700 bg-slate-800">
              <table className="w-full text-left text-sm text-slate-300">
                <thead className="bg-slate-900/60 text-xs uppercase text-slate-400 border-b border-slate-700">
                  <tr>
                    {data.length > 0 &&
                      Object.keys(data[0] as object).map((col) => (
                        <th key={col} className="px-4 py-3 font-semibold">
                          {col}
                        </th>
                      ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {data.map((row: Record<string, unknown>, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-700/40 transition">
                      {Object.values(row).map((val, cellIdx) => (
                        <td
                          key={cellIdx}
                          className="px-4 py-3 font-mono text-xs"
                        >
                          {typeof val === "object"
                            ? JSON.stringify(val)
                            : String(val)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Raw / Object JSON Viewer */}
          {(!isArrayData || data.length === 0) && (
            <div className="p-4 bg-slate-900 rounded-xl border border-slate-700 overflow-x-auto">
              <pre className="text-xs text-emerald-400 font-mono">
                {JSON.stringify(data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
