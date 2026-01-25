import api from "./axios";
import type { UserPublic } from "../types/auth";

export const getFreeUsers = async (): Promise<UserPublic[]> => {
  const { data } = await api.get("/users/free");
  return data;
};

export const updateProfile = async (data: Partial<{ email: string; full_name: string; password: string }>): Promise<UserPublic> => {
  const { data: updated } = await api.patch("/users/my_profile", data);
  return updated;
};

export const deleteProfile = async (): Promise<void> => {
  await api.delete("/users/my_profile");
};

export const getUser = async (userId: number): Promise<UserPublic> => {
  const { data } = await api.get(`/users/${userId}`);
  return data;
};
