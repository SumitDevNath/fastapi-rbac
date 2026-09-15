import { useQuery } from "@tanstack/react-query";
import { resourceService } from "../api/resourceService";
import { useAuth } from "../../../contexts/AuthContext";

export const useResourceData = <T = unknown>(endpoint: string) => {
  const { isAuthenticated } = useAuth();

  return useQuery({
    queryKey: ["external-resource", endpoint],
    queryFn: () => resourceService.fetchResourceData<T>(endpoint),
    // Only execute if user is authenticated and an endpoint is provided
    enabled: isAuthenticated && Boolean(endpoint.trim()),
    retry: 1,
  });
};
