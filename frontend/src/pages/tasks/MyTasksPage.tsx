import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import { getMyTasks  } from "../../api/tasksApi.ts";
import type { TaskListPublicSchema } from "../../types/task.ts";

import { Box, Typography, Stack, Chip, Card, CardContent, CardActionArea } from "@mui/material";

export default function MyTasksPage() {
  const user = authStore((s) => s.user);
  const [tasks, setTasks] = useState<TaskListPublicSchema[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const data = await getMyTasks();
        setTasks(data);
      } catch (err) {
        alert("Ошибка загрузки задач");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  if (loading) return <div>Загрузка моих задач...</div>;
  if (!user) return <div>Загрузка пользователя...</div>;

  return (
    <Box sx={{ maxWidth: 700, mx: "auto", mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        Мои задачи
      </Typography>

      {tasks.length === 0 ? (
        <Typography>Нет задач</Typography>
      ) : (
        <Stack spacing={2}>
          {tasks.map((task) => {
            let statusText = "";
            let statusColor: "default" | "success" | "warning" | "info" | "error" | "secondary" = "default";
            let bgColor = "#f5f5f5"; // светлый фон по умолчанию

            switch (task.status) {
              case "open":
                statusText = "Открыта";
                statusColor = "warning";
                bgColor = "#fff8e1"; // мягкий желтый
                break;
              case "in_progress":
                statusText = "В работе";
                statusColor = "info";
                bgColor = "#e3f2fd"; // светло-синий
                break;
              case "done":
                statusText = "Выполнена";
                statusColor = "success";
                bgColor = "#e8f5e9"; // светло-зеленый
                break;
              default:
                statusText = task.status;
                bgColor = "#f5f5f5";
            }

            return (
              <Card
                key={task.id}
                variant="outlined"
                sx={{
                  backgroundColor: bgColor,
                  borderRadius: 2,
                  transition: "transform 0.2s, box-shadow 0.2s",
                  "&:hover": {
                    transform: "translateY(-2px)",
                    boxShadow: 3,
                  },
                }}
              >
                <CardActionArea component={RouterLink} to={`/tasks/${task.id}`}>
                  <CardContent sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        {task.title}
                      </Typography>
                      {task.deadline && (
                        <Typography variant="body2" color="text.secondary">
                          Дедлайн: {new Date(task.deadline).toLocaleDateString()}
                        </Typography>
                      )}
                    </Box>

                    <Chip label={statusText} color={statusColor} sx={{ fontWeight: "bold" }} />
                  </CardContent>
                </CardActionArea>
              </Card>
            );
          })}
        </Stack>
      )}
    </Box>
  );
}
