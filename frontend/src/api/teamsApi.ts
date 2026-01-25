import api from "./axios";
import type { Team, TeamMember } from "../types/team";

export const createTeam = async (name: string): Promise<Team> => {
  const { data } = await api.post("/teams/", { name });
  return data;
};

export const getTeam = async (teamId: string): Promise<Team> => {
  const { data } = await api.get(`/teams/${teamId}`);
  return data;
};

export const getTeamMembers = async (teamId: string): Promise<TeamMember[]> => {
  const { data } = await api.get(`/teams/${teamId}/members`);
  return data;
};

export const addUserToTeam = async (teamId: string, userId: number) => {
  await api.post(`/teams/${teamId}/members/${userId}`);
};

export const promoteUser = async (teamId: string, userId: number) => {
  await api.post(`/teams/${teamId}/promote/${userId}`);
};

export const demoteUser = async (teamId: string, userId: number) => {
  await api.post(`/teams/${teamId}/demote/${userId}`);
};

export const removeUserFromTeam = async (teamId: string, userId: number) => {
  await api.delete(`/teams/${teamId}/members/${userId}`);
};

export const deleteTeam = async (teamId: string) => {
  await api.delete(`/teams/${teamId}`);
};
