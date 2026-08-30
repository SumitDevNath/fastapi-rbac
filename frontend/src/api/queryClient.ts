import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // 1. Stale Time: How long data remains "fresh" before triggering background refetch
      staleTime: 1000 * 60 * 3, // 3 Minutes: Navigating between tabs uses cached data with zero network delay

      // 2. Garbage Collection Time: How long inactive data stays in browser memory
      gcTime: 1000 * 60 * 15, // 15 Minutes

      // 3. Retry Strategy: Prevents hammering the backend on legitimate errors (e.g. 404/403)
      retry: (failureCount, error) => {
        // Do not retry 401 or 403 errors (they won't succeed on retry)
        const msg = error instanceof Error ? error.message : "";
        if (
          msg.includes("401") ||
          msg.includes("403") ||
          msg.includes("Forbidden")
        ) {
          return false;
        }
        return failureCount < 2;
      },

      // 4. Background Sync on Tab Switch
      refetchOnWindowFocus: true,
    },
  },
});
