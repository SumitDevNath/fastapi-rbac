import { Component, type ErrorInfo, type ReactNode } from "react";
import { AlertOctagon, RotateCcw } from "lucide-react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught component error:", error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white p-4">
          <div className="max-w-md w-full bg-slate-800 border border-slate-700 rounded-2xl p-8 text-center space-y-4 shadow-2xl">
            <div className="w-16 h-16 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-2xl flex items-center justify-center mx-auto">
              <AlertOctagon size={36} />
            </div>
            <h1 className="text-xl font-bold">Something went wrong</h1>
            <p className="text-xs text-slate-400 leading-relaxed">
              An unexpected UI error occurred. You can safely reload the view.
            </p>
            {this.state.error && (
              <div className="p-3 bg-slate-950 rounded-lg text-left text-[11px] font-mono text-rose-300 overflow-x-auto border border-slate-800">
                {this.state.error.message}
              </div>
            )}
            <button
              onClick={this.handleReload}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-xs flex items-center justify-center gap-2"
            >
              <RotateCcw size={14} /> Reload Interface
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
