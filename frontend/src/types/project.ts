import { type User } from "./auth";

export interface Project {
  id: number;
  title: string;
  description: string | null;
  owner_id: number;
  owner: User;
  created_at: string;
  updated_at: string;
}
