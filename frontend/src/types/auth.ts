export type UserRole = "ADMIN" | "MANAGER" | "EDITOR" | "user";

export interface User {
  id: number;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  username?: string | null;
  status?: string | null;
  auth_provider?: string | null;
  must_change_password?: boolean | null;
  hris_id?: string | null;
  facility_id?: string | null;
  lab_id?: string | null;
  mobile?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  division_id?: string | null;
  district_id?: string | null;
  upazila_id?: string | null;
  union_id?: string | null;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginResponse {
  user: User;
  tokens: Tokens;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface LogoutRequest {
  refresh_token: string;
}

export interface LogoutResponse {
  message: string;
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
