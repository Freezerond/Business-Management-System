import { useEffect, useState } from "react";
import { getMyGivenEvaluations } from "../../api/evaluationsApi.ts";
import { getTask } from "../../api/tasksApi.ts";
import type { EvaluationPublicSchema } from "../../types/evaluation.ts";
import { Link } from "react-router-dom";

import { Box, Typography, Card, CardContent, Stack, Chip, Link as MuiLink } from "@mui/material";

interface EvaluationWithDetails extends EvaluationPublicSchema {
  task_title: string;
  executor_name: string;
}

export default function MyGivenEvaluationsPage() {
  const [evaluations, setEvaluations] = useState<EvaluationWithDetails[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvaluations = async () => {
      setLoading(true);
      try {
        const data: EvaluationPublicSchema[] = await getMyGivenEvaluations();

        const evaluationsWithDetails = await Promise.all(
          data.map(async (e) => {
            // ===== Название задачи =====
            let task_title = `Задача #${e.task_id}`;
            let executor_name = `Пользователь #${e.executor_id}`;

            try {
              const task = await getTask(e.task_id);
              if (task?.title) task_title = task.title;

              // Предположим, что у задачи есть поле исполнителя:
              if (task?.executor) {
                executor_name = task.executor.full_name ?? task.executor.email ?? executor_name;
              }
            } catch {
              // fallback уже установлен
            }

            return { ...e, task_title, executor_name };
          })
        );

        setEvaluations(evaluationsWithDetails);
      } catch (err) {
        console.error(err);
        alert("Ошибка загрузки оценок");
      } finally {
        setLoading(false);
      }
    };

    fetchEvaluations();
  }, []);

  if (loading) return <Typography>Загрузка оценок...</Typography>;

  return (
    <Box sx={{ maxWidth: 700, mx: "auto", mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        Мои выставленные оценки
      </Typography>

      {evaluations.length === 0 ? (
        <Typography>Вы ещё не поставили ни одной оценки</Typography>
      ) : (
        <Stack spacing={2}>
          {evaluations.map((e: any) => (
            <Card
              key={`${e.task_id}-${e.executor_id}-${e.created_at}`}
              variant="outlined"
              sx={{
                backgroundColor: "#f5f5f5",
                borderRadius: 2,
                transition: "transform 0.2s, box-shadow 0.2s",
                "&:hover": { transform: "translateY(-2px)", boxShadow: 3 },
              }}
            >
              <CardContent>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <Box>
                    <Typography variant="subtitle1">
                      <MuiLink component={Link} to={`/tasks/${e.task_id}`} underline="hover">
                        {e.task_title}
                      </MuiLink>
                    </Typography>

                    <Typography variant="body2" color="text.secondary">
                      Исполнитель: {e.executor_name}
                    </Typography>

                    {e.comment && (
                      <Typography variant="body2" sx={{ mt: 1, color: "text.secondary" }}>
                        Комментарий: {e.comment}
                      </Typography>
                    )}
                  </Box>

                  <Chip
                    label={`⭐ ${e.score}`}
                    color="primary"
                    sx={{ fontWeight: "bold", ml: 2 }}
                  />
                </Box>
              </CardContent>
            </Card>
          ))}
        </Stack>
      )}
    </Box>
  );
}
