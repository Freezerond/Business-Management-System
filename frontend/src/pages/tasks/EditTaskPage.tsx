import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getTask, updateTask } from "../../api/tasksApi.ts";
import { getTeamMembers } from "../../api/teamsApi.ts";
import { authStore } from "../../auth/store.ts";
import type { TaskPublicSchema, TaskUpdateSchema } from "../../types/task.ts";
import type { UserPublic } from "../../types/auth.ts";

import { Box, Typography, TextField, Button, Stack, Checkbox, FormControlLabel } from "@mui/material";

export default function EditTaskPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const user = authStore((s) => s.user);

  const [task, setTask] = useState<TaskPublicSchema | null>(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [deadline, setDeadline] = useState("");
  const [executorIds, setExecutorIds] = useState<number[]>([]);
  const [teamMembers, setTeamMembers] = useState<UserPublic[]>([]);
  const [loading, setLoading] = useState(true);

  const isAdmin = user?.role === "admin";
  const isManager = user?.role === "manager";

  // защита
  if (!user || !user.team_id || (!isAdmin && !isManager)) {
    return <p>У вас нет прав на редактирование задач</p>;
  }

  useEffect(() => {
    const loadData = async () => {
      try {
        const t = await getTask(Number(taskId));

        // только создатель может редактировать
        if (t.creator_id !== user.id) {
          alert("Редактировать задачу может только её создатель");
          navigate("/");
          return;
        }

        setTask(t);
        setTitle(t.title);
        setDescription(t.description ?? "");
        setDeadline(t.deadline ?? "");
        setExecutorIds(t.executors?.map((e: UserPublic) => e.id) ?? []);

        const members = await getTeamMembers(user.team_id!);

        const allowed = members.filter((m) => {
          if (m.id === user.id) return false;
          if (isAdmin) return true;
          if (isManager) return m.role === "employee";
          return false;
        });

        setTeamMembers(allowed);
      } catch (err) {
        console.error(err);
        alert("Ошибка загрузки задачи");
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [taskId]);

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

    const payload: TaskUpdateSchema = {
      title,
      description: description || undefined,
      deadline: deadline || undefined,
      executor_ids: executorIds,
    };

    try {
      await updateTask(Number(taskId), payload);
      navigate(`/tasks/${taskId}`);
    } catch (err) {
      console.error(err);
      alert("Ошибка обновления задачи");
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (!task) return null;

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        Редактировать задачу
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
          multiline
          rows={4}
          fullWidth
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
            Исполнители
          </Typography>

          {teamMembers.length === 0 ? (
            <Typography>Нет доступных пользователей</Typography>
          ) : (
            <Stack spacing={1}>
              {teamMembers.map((m: any) => (
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
            </Stack>
          )}
        </Box>

        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Сохранить
        </Button>
      </Stack>
    </Box>
  );
}
