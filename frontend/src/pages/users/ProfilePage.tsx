import { useEffect, useState } from "react";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import { deleteProfile } from "../../api/usersApi.ts";
import { getTeam } from "../../api/teamsApi.ts";

import { Box, Typography, Button, Paper, Stack } from "@mui/material";

export default function ProfilePage() {
  const user = authStore((s) => s.user);
  const logout = authStore((s) => s.logout);
  const navigate = useNavigate();
  const roleMap: Record<string, string> = {
  admin: "Админ",
  manager: "Менеджер",
  employee: "Сотрудник",
};

  const [teamName, setTeamName] = useState<string | null>(null);

  useEffect(() => {
    if (!user?.team_id) return;

    const fetchTeam = async () => {
      try {
        const team = await getTeam(user.team_id!);
        setTeamName(team.name);
      } catch {
        setTeamName("Не удалось загрузить команду");
      }
    };

    fetchTeam();
  }, [user?.team_id]);

  if (!user) return null;

  const handleDelete = async () => {
    if (!confirm("Вы точно хотите удалить свой аккаунт?")) return;

    try {
      await deleteProfile();
      logout();
      navigate("/register", { replace: true });
    } catch (err: any) {
      alert("Ошибка при удалении аккаунта: " + err.message);
    }
  };

  return (
    <Box sx={{ maxWidth: 500, mx: "auto", mt: 4 }}>
      <Paper sx={{ p: 4, borderRadius: 2, boxShadow: 3 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Профиль
        </Typography>

        <Stack spacing={1} sx={{ mb: 3 }}>
          <Typography><strong>Email:</strong> {user.email}</Typography>
          <Typography><strong>ФИО:</strong> {user.full_name ?? "-"}</Typography>
          <Typography><strong>Роль:</strong> {roleMap[user.role] ?? user.role}</Typography>
          <Typography><strong>Команда:</strong> {teamName ?? "Не состоит в команде"}</Typography>
          <Typography>
            <strong>Зарегистрирован:</strong>{" "}
            {new Date(user.created_at).toLocaleString()}
          </Typography>
        </Stack>

        <Stack direction="row" spacing={2}>
          <Button
            component={RouterLink}
            to="/profile/edit"
            variant="contained"
            color="secondary"
          >
            Редактировать профиль
          </Button>

          <Button
            variant="contained"
            color="error"
            onClick={handleDelete}
            sx={{
              "&:hover": {
                backgroundColor: "#b71c1c",
              },
            }}
          >
            Удалить аккаунт
          </Button>
        </Stack>
      </Paper>
    </Box>
  );
}
