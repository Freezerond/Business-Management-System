import { create } from "zustand";
import api from "../api/axios";

export type User = {
  id: number;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
  team_id: string | null;
};

type AuthState = {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;

  login: (email: string, password: string) => Promise<void>;
  refresh: () => Promise<void>;
  loadUser: () => Promise<void>;
  logout: () => void;
};

export const authStore = create<AuthState>((set, get) => ({
  user: JSON.parse(localStorage.getItem("user") || "null"),
  accessToken: localStorage.getItem("access_token"),
  isLoading: false,

  async login(email, password) {
    set({ isLoading: true });

    const form = new FormData();
    form.append("username", email);
    form.append("password", password);

    const { data } = await api.post("/auth/login", form);

    // сохраняем токены
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem("access_token", data.access_token);

    set({ accessToken: data.access_token });

    await get().loadUser(); // загружаем профиль
    set({ isLoading: false });
  },

  async refresh() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) throw new Error("No refresh token");

    const { data } = await api.post("/auth/refresh", {
      refresh_token: refreshToken,
    });

    localStorage.setItem("access_token", data.access_token);
    set({ accessToken: data.access_token });
  },

  async loadUser() {
    try {
      const { data } = await api.get("/users/my_profile");
      localStorage.setItem("user", JSON.stringify(data)); // сохраняем пользователя
      set({ user: data });
    } catch {
      get().logout(); // если токен невалидный
    }
  },

  logout() {
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    set({ user: null, accessToken: null });
  },
}));
