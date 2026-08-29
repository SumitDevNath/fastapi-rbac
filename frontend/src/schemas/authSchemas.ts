import { z } from "zod";

// Login Validation Schema
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Please enter a valid email address"),
  password: z
    .string()
    .min(1, "Password is required")
    .min(8, "Password must be at least 8 characters long")
    .max(128, "Password must not exceed 128 characters"),
});

export type LoginFormData = z.infer<typeof loginSchema>;

// Register Validation Schema
export const registerSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Please enter a valid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters long")
    .max(128, "Password must not exceed 128 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one digit"),
  role: z.enum(["ADMIN", "MANAGER", "EDITOR", "VIEWER"]).default("VIEWER"),
});

export type RegisterFormData = z.infer<typeof registerSchema>;
