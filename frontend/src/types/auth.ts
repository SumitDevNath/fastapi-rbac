export type UserRole = "ADMIN" | "MANAGER" | "EDITOR" | "VIEWER";

export interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  status: "string";
  auth_provider: "string";
  must_change_password: true;
  hris_id: "string";
  facility_id: "string";
  lab_id: "string";
  mobile: "string";
  first_name: "string";
  last_name: "string";
  division_id: "string";
  district_id: "string";
  upazila_id: "string";
  union_id: "string";
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface ApiErrorDetail {
  field?: string;
  issue?: string;
  type?: string;
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: ApiErrorDetail[] | null;
  };
}
