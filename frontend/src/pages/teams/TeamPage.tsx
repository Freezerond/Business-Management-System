import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import {
  getTeam,
  getTeamMembers,
  promoteUser,
  demoteUser,
  removeUserFromTeam, deleteTeam, addUserToTeam,
} from "../../api/teamsApi.ts";
import type { Team, TeamMember } from "../../types/team.ts";
import type { UserPublic } from "../../types/auth.ts";
import {getFreeUsers} from "../../api/usersApi.ts";

import { Box, Typography, Button, Stack, Container } from "@mui/material";

export default function TeamPage() {
  const { teamId } = useParams<{ teamId: string }>();
  const user = authStore((s) => s.user);
  const isAdmin = user?.role === "admin";
  const navigate = useNavigate();

  const [team, setTeam] = useState<Team | null>(null);
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [ , setLoading] = useState(true);

  const [freeUsers, setFreeUsers] = useState<UserPublic[]>([]);
    const roleMap: Record<string, string> = {
  admin: "Админ",
  manager: "Менеджер",
  employee: "Сотрудник",
};

  useEffect(() => {
    if (!teamId) return;

    const fetchData = async () => {
      try {
        setLoading(true);

        const teamData = await getTeam(teamId);
        setTeam(teamData);

        const membersData = await getTeamMembers(teamId);
        setMembers(membersData);
      } catch (err) {
        console.error("Ошибка загрузки команды", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [teamId]);

  const refreshMembers = async () => {
    if (!teamId) return;
    const membersData = await getTeamMembers(teamId);
    setMembers(membersData);
  };

  useEffect(() => {
  if (!isAdmin) return;

  const loadFreeUsers = async () => {
    const users = await getFreeUsers();
    setFreeUsers(users);
  };

  loadFreeUsers();
}, [isAdmin]);

  const handleAddUser = async (userId: number) => {
  await addUserToTeam(teamId!, userId);

  // обновляем участников команды
  const updatedMembers = await getTeamMembers(teamId!);
  setMembers(updatedMembers);

  // убираем пользователя из списка свободных
  setFreeUsers((prev) => prev.filter((u) => u.id !== userId));
};

  const handlePromote = async (userId: number) => {
    if (!teamId) return;
    await promoteUser(teamId, userId);
    await refreshMembers();
  };

  const handleDemote = async (userId: number) => {
    if (!teamId) return;
    await demoteUser(teamId, userId);
    await refreshMembers();
  };

  const handleRemove = async (userId: number) => {
    if (!teamId) return;
    await removeUserFromTeam(teamId, userId);
    await refreshMembers();

    // обновляем свободных пользователей
  const users = await getFreeUsers();
  setFreeUsers(users);
  };

  if (!team) return <div>Загрузка команды...</div>;
  if (!user) return <div>Загрузка пользователя...</div>;

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Команда: {team.name}
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Создана: {new Date(team.created_at).toLocaleString()}
      </Typography>

      <Box sx={{ mt: 3 }}>
  <Typography variant="h5" gutterBottom>
    Члены команды
  </Typography>

  {members.length === 0 ? (
    <Typography>Нет участников</Typography>
  ) : (
    <Stack spacing={1}>
      {members.map((m: any) => (
        <Box
          key={m.id}
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            p: 1,
            borderBottom: "1px solid #e0e0e0",
          }}
        >
          <Box>
            <Typography variant="subtitle1">{m.full_name}</Typography>
            <Typography variant="body2" color="text.secondary">
              {roleMap[m.role] ?? m.role}
            </Typography>
          </Box>

          {isAdmin && user.id !== m.id && (
            <Stack direction="row" spacing={1}>
              <Button
                size="small"
                variant="contained"
                sx={{ bgcolor: "success.main", "&:hover": { bgcolor: "success.dark" } }}
                onClick={() => handlePromote(m.id)}
              >
                Повысить
              </Button>
              <Button
                size="small"
                variant="contained"
                sx={{ bgcolor: "warning.main", "&:hover": { bgcolor: "warning.dark" } }}
                onClick={() => handleDemote(m.id)}
              >
                Понизить
              </Button>
              <Button
                size="small"
                variant="outlined"
                color="error"
                onClick={() => handleRemove(m.id)}
              >
                Удалить
              </Button>
            </Stack>
          )}
        </Box>
      ))}
    </Stack>
  )}
</Box>

{isAdmin && freeUsers.length > 0 && (
  <Box sx={{ mt: 4 }}>
    <Typography variant="h5" gutterBottom>
      Добавить пользователя
    </Typography>
    <Stack spacing={1}>
      {freeUsers.map((u: any) => (
        <Box
          key={u.id}
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            p: 1,
            borderBottom: "1px solid #e0e0e0",
          }}
        >
          <Box>
            <Typography>{u.full_name}</Typography>
            <Typography variant="body2" color="text.secondary">
              {u.email}
            </Typography>
          </Box>
          <Button variant="contained" onClick={() => handleAddUser(u.id)}>
            Добавить
          </Button>
        </Box>
      ))}
    </Stack>
  </Box>
)}

      {user?.role === "admin" && team && (
        <Box sx={{ mt: 4 }}>
          <Button
            variant="contained"
            color="error"
            onClick={async () => {
              if (!confirm("Вы точно хотите удалить команду?")) return;
              await deleteTeam(team.id);
              authStore.setState({ user: { ...user, team_id: null, role: "user" } });
              navigate("/");
            }}
          >
            Удалить команду
          </Button>
        </Box>
      )}
    </Container>
  );
}
