import { useEffect, useState } from "react";
import { getMyReceivedEvaluations } from "../../api/evaluationsApi.ts";
import { getTask } from "../../api/tasksApi.ts";
import type { EvaluationPublicSchema } from "../../types/evaluation.ts";
import { Link } from "react-router-dom";

import { Box, Typography, Card, CardContent, Stack, Chip, Link as MuiLink } from "@mui/material";

interface EvaluationWithTaskTitle extends EvaluationPublicSchema {
  task_title: string;
}

export default function MyReceivedEvaluationsPage() {
  const [evaluations, setEvaluations] = useState<EvaluationWithTaskTitle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvaluations = async () => {
      setLoading(true);
      try {
        const data: EvaluationPublicSchema[] = await getMyReceivedEvaluations();

        // Подгружаем названия задач для каждой оценки
        const evaluationsWithTitle = await Promise.all(
          data.map(async (e) => {
            try {
              const task = await getTask(e.task_id);
              return { ...e, task_title: task.title };
            } catch {
              // Если задача не найдена — fallback
              return { ...e, task_title: `Задача #${e.task_id}` };
            }
          })
        );

        setEvaluations(evaluationsWithTitle);
      } catch (err) {
        console.error(err);
        alert("Ошибка при загрузке оценок");
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
        Полученные оценки
      </Typography>

      {evaluations.length === 0 ? (
        <Typography>Вы ещё не получили ни одной оценки</Typography>
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

                    <Typography variant="body2" sx={{ mt: 0.5 }}>
                      Оценка: <strong>{e.score}</strong>
                    </Typography>

                    {e.comment && (
                      <Typography variant="body2" sx={{ mt: 0.5, color: "text.secondary" }}>
                        Комментарий: {e.comment}
                      </Typography>
                    )}
                  </Box>

                  <Chip
                    label={`⭐ ${e.score}`}
                    color={e.score >= 4 ? "success" : e.score === 3 ? "warning" : "error"}
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