import { z } from "zod";

export const userAdminUpdateSchema = z.object({
  role: z.enum(["ADMIN", "MANAGER", "EDITOR", "user"]).optional(),
  status: z.string().optional(),
  is_active: z.boolean().optional(),
  facility_id: z.string().nullable().optional(),
  lab_id: z.string().nullable().optional(),
  mobile: z.string().nullable().optional(),
  first_name: z.string().nullable().optional(),
  last_name: z.string().nullable().optional(),
});

export type UserAdminUpdateFormData = z.infer<typeof userAdminUpdateSchema>;

export const userSelfUpdateSchema = z.object({
  first_name: z.string().nullable().optional(),
  last_name: z.string().nullable().optional(),
  mobile: z.string().nullable().optional(),
});

export type UserSelfUpdateFormData = z.infer<typeof userSelfUpdateSchema>;
