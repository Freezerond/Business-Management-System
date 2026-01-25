export type UserPublic = {
  id: number;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
  team_id: string | null;
};

export type Token = {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
};