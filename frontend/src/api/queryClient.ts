import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2, // 2 minutes: Data is considered fresh for 2 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes: Inactive cache garbage collected after 10 minutes
      retry: 1, // Retry failed network requests once before showing error
      refetchOnWindowFocus: true, // Re-sync server state when user returns to the tab
    },
  },
});
