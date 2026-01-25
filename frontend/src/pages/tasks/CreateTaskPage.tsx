import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import { createTask } from "../../api/tasksApi.ts";
import { getTeamMembers } from "../../api/teamsApi.ts";
import type { TaskCreateSchema } from "../../types/task.ts";
import type { UserPublic } from "../../types/auth.ts";

import {Box, TextField, Button, Typography, Stack, FormGroup, FormControlLabel, Checkbox} from "@mui/material";

export default function CreateTaskPage() {
  const navigate = useNavigate();
  const user = authStore((s) => s.user);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [deadline, setDeadline] = useState("");
  const [executorIds, setExecutorIds] = useState<number[]>([]);
  const [teamMembers, setTeamMembers] = useState<UserPublic[]>([]);
  const [loading, setLoading] = useState(false);

  const isAdmin = user?.role === "admin";
  const isManager = user?.role === "manager";

  // защита
  if (!user || !user.team_id || (!isAdmin && !isManager)) {
    return <p>У вас нет прав на создание задач</p>;
  }

  // загружаем участников команды
  useEffect(() => {
    const loadMembers = async () => {
      try {
        const members = await getTeamMembers(user.team_id!);

        const allowed = members.filter((m) => {
          if (m.id === user.id) return false; // не назначаем себя
          if (isAdmin) return true;
          if (isManager) return m.role === "employee";
          return false;
        });

        setTeamMembers(allowed);
      } catch (err) {
        console.error("Ошибка загрузки участников команды", err);
      }
    };

    loadMembers();
  }, [user.team_id]);

  const toggleExecutor = (id: number) => {
    setExecutorIds((prev) =>
      prev.includes(id) ? prev.filter((e) => e !== id) : [...prev, id]
    );
  };

  const handleSubmit = async () => {
    if (!title.trim()) {
      alert("Введите название задачи");
      return;
    }

    const payload: TaskCreateSchema = {
      title,
      description: description || undefined,
      deadline: deadline || undefined,
      executor_ids: executorIds,
    };

    try {
      setLoading(true);
      const task = await createTask(payload);
      navigate(`/tasks/${task.id}`);
    } catch (err: any) {
      console.error(err);
      alert("Ошибка создания задачи");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        Создать задачу
      </Typography>

      <Stack spacing={2}>
        <TextField
          label="Название задачи"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          fullWidth
        />

        <TextField
          label="Описание"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          fullWidth
          multiline
          minRows={3}
        />

        <TextField
          label="Дедлайн"
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
          InputLabelProps={{ shrink: true }}
        />

        <Box>
          <Typography variant="h6" gutterBottom>
            Назначить исполнителей
          </Typography>

          {teamMembers.length === 0 ? (
            <Typography>Нет доступных пользователей</Typography>
          ) : (
            <FormGroup>
              {teamMembers.map((m) => (
                <FormControlLabel
                  key={m.id}
                  control={
                    <Checkbox
                      checked={executorIds.includes(m.id)}
                      onChange={() => toggleExecutor(m.id)}
                    />
                  }
                  label={`${m.full_name ?? m.email} (${m.role})`}
                />
              ))}
            </FormGroup>
          )}
        </Box>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Создание..." : "Создать задачу"}
        </Button>
      </Stack>
    </Box>
  );
}
