export type Team = {
  id: string;
  name: string;
  created_at: string;
};

export type TeamMember = {
  id: number;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
  team_id: string | null;
};
