import api from "./axios";
import type { Token, UserPublic } from "../types/auth";

export const login = async (email: string, password: string): Promise<Token> => {
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  const { data } = await api.post("/auth/login", formData);
  return data;
};

export const register = async (email: string, full_name: string, password: string): Promise<UserPublic> => {
  const { data } = await api.post("/auth/register", { email, full_name, password });
  return data;
};

export const refreshToken = async (refreshToken: string): Promise<Token> => {
  const { data } = await api.post("/auth/refresh", { refresh_token: refreshToken });
  return data;
};
