import { z } from "zod";

export const userRoleUpdateSchema = z.object({
  role: z.enum(["ADMIN", "MANAGER", "EDITOR", "VIEWER"]),
  is_active: z.boolean().optional(),
});

export type UserRoleUpdateFormData = z.infer<typeof userRoleUpdateSchema>;
