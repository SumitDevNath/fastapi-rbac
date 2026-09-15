import { resourceClient } from "../../../api/apiClient";

export const resourceService = {
  fetchResourceData: async <T = unknown>(endpoint: string): Promise<T> => {
    const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    // Pass T as the second generic so Axios knows the unpacked return type is T:
    const data = await resourceClient.get<unknown, T>(cleanEndpoint);
    return data as T;
  },
};
