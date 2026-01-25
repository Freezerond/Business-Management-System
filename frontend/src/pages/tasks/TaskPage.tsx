import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import {
    getTask,
    getComments,
    updateTaskStatus,
    deleteTask,
    createComment,
    deleteComment,
} from "../../api/tasksApi.ts";
import type { TaskPublicSchema, TaskCommentPublicSchema, TaskStatusUpdateSchema, TaskCommentCreateSchema } from "../../types/task.ts";
import type {EvaluationCreateSchema, EvaluationPublicSchema, EvaluationUpdateSchema} from "../../types/evaluation.ts";
import {createEvaluation, deleteEvaluation, getEvaluation, updateEvaluation} from "../../api/evaluationsApi.ts";
import {EvaluationForm} from "../../components/EvaluationForm.tsx";

import { Box, Typography, Button, Paper, List, ListItem, TextField, Stack } from "@mui/material";

export default function TaskPage() {
  const {taskId} = useParams<{ taskId: string }>();
  const user = authStore((s) => s.user);
  const navigate = useNavigate();

  const [task, setTask] = useState<TaskPublicSchema | null>(null);
  const [comments, setComments] = useState<TaskCommentPublicSchema[]>([]);
  const [newComment, setNewComment] = useState("");
  const [loading, setLoading] = useState(true);
  const [statusLoading, setStatusLoading] = useState(false);
  const [commentLoading, setCommentLoading] = useState(false);

  const [evaluations, setEvaluations] = useState<Record<number, EvaluationPublicSchema>>({});
  const [, setEvalLoading] = useState(false);
  const [editingExecutorId, setEditingExecutorId] = useState<number | null>(null);

  const roleMap: Record<string, string> = {
  open: "Открыта",
  in_progress: "В работе",
  done: "Выполнена",
};


  if (!user) return <div>Загрузка пользователя...</div>;
  if (!taskId) return <div>Некорректный ID задачи</div>;

  // проверки ролей и прав
  const isCreator = task?.creator_id === user.id;
  const isExecutor = task?.executors?.some((e) => e.id === user.id);
  const canChangeStatus = !!isExecutor;
  const canEditOrDelete = isCreator || user.role === "admin";
  const canComment = isCreator || isExecutor;

  useEffect(() => {
    const fetchTaskData = async () => {
      setLoading(true);
      try {
        const t = await getTask(Number(taskId));
        setTask(t);

        let evals: Record<number, EvaluationPublicSchema> = {};
        if (t.status === "done" && t.executors?.length) {
          setEvalLoading(true);
          try {
            const evalsArray = await Promise.all(
                t.executors.map(async (ex: {id: number}) => {
                  try {
                    const e = await getEvaluation(t.id, ex.id);
                    return [ex.id, e] as const;
                  } catch {
                    return null; // если оценки нет — нормально
                  }
                })
            );

            for (const item of evalsArray) {
              if (item) evals[item[0]] = item[1];
            }
            setEvaluations(evals);
          } finally {
            setEvalLoading(false);
          }
        }

        const c = await getComments(Number(taskId));
        setComments(c);
      } catch (err) {
        alert("У вас нет доступа к этой задаче");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTaskData();
  }, [taskId]);

  // изменить статус задачи
  const handleStatusChange = async (status: "todo" | "in_progress" | "done") => {
    if (!task) return;
    setStatusLoading(true);
    try {
      const updated = await updateTaskStatus(Number(taskId), {status} as TaskStatusUpdateSchema);
      setTask(updated);
    } catch (err) {
      alert("Нельзя изменить статус оценённой задачи");
    } finally {
      setStatusLoading(false);
    }
  };

  // удалить задачу
  const handleDeleteTask = async () => {
    if (!task) return;
    if (!confirm("Вы точно хотите удалить эту задачу?")) return;

    try {
      await deleteTask(Number(taskId));
      navigate("/", {replace: true}); // вернуться на Dashboard
    } catch (err) {
      alert("Ошибка удаления задачи");
    }
  };

  // добавить комментарий
  const handleAddComment = async () => {
    if (!newComment.trim()) return;
    setCommentLoading(true);
    try {
      const comment = await createComment(Number(taskId), {message: newComment.trim()} as TaskCommentCreateSchema);
      setComments((prev) => [...prev, comment]);
      setNewComment("");
    } catch (err) {
      alert("Ошибка добавления комментария");
    } finally {
      setCommentLoading(false);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm("Удалить комментарий?")) return;

    try {
      await deleteComment(Number(taskId), commentId);
      setComments((prev) => prev.filter((c) => c.id !== commentId));
    } catch (err) {
      alert("Ошибка удаления комментария");
    }
  };

  const handleSaveEvaluation = async (
      executorId: number,
      data: EvaluationCreateSchema | EvaluationUpdateSchema
  ) => {
    setEvalLoading(true);
    try {
      let savedEval: EvaluationPublicSchema;
      if (evaluations[executorId]) {
        // обновление
        savedEval = await updateEvaluation(task!.id, executorId, data as EvaluationUpdateSchema);
      } else {
        // создание
        savedEval = await createEvaluation(task!.id, data as EvaluationCreateSchema);
      }
      setEvaluations((prev) => ({...prev, [executorId]: savedEval}));
      setEditingExecutorId(null); // если редактировали — закрываем форму
    } catch (err) {
      alert("Ошибка при сохранении оценки");
      console.error(err);
    } finally {
      setEvalLoading(false);
    }
  };

  const handleDeleteEvaluation = async (executorId: number) => {
    if (!confirm("Удалить оценку?")) return;

    setEvalLoading(true);
    try {
      await deleteEvaluation(task!.id, executorId);
      setEvaluations((prev) => {
        const copy = {...prev};
        delete copy[executorId];
        return copy;
      });
      if (editingExecutorId === executorId) setEditingExecutorId(null);
    } catch (err) {
      alert("Ошибка удаления оценки");
      console.error(err);
    } finally {
      setEvalLoading(false);
    }
  };

  const getUserName = (id: number) => {
    if (id === user?.id) return "Вы";

    if (task?.creator && id === task.creator.id) {
      return task.creator.full_name ?? task.creator.email;
    }

    const executor = task?.executors.find(e => e.id === id);
    if (executor) return executor.full_name ?? executor.email;

    return `Пользователь ${id}`;
  };

  if (loading || !task) return <div>Загрузка задачи...</div>;

  return (
      <Box sx={{maxWidth: 700, mx: "auto", mt: 3}}>
        <Typography variant="h4" gutterBottom>{task.title}</Typography>

        <Typography sx={{mb: 1}}>{task.description || "-"}</Typography>

        <Typography><strong>Дедлайн:</strong> {task.deadline ? new Date(task.deadline).toLocaleDateString() : "-"}
        </Typography>
        <Typography><strong>Статус:</strong> {roleMap[task.status] ?? task.status}</Typography>
        <Typography><strong>Создал:</strong> {getUserName(task.creator_id)}</Typography>

        {canChangeStatus && (
            <Stack direction="row" spacing={1} sx={{mt: 2}}>
              <Button
                  variant="contained"
                  color="info"
                  onClick={() => handleStatusChange("in_progress")}
                  disabled={statusLoading || task.status === "in_progress"}
              >
                В работе
              </Button>
              <Button
                  variant="contained"
                  color="success"
                  onClick={() => handleStatusChange("done")}
                  disabled={statusLoading || task.status === "done"}
              >
                Выполнено
              </Button>
            </Stack>
        )}

        {canEditOrDelete && (
            <Stack direction="row" spacing={1} sx={{mt: 2}}>
              <Button variant="outlined" onClick={() => navigate(`/tasks/${task.id}/edit`)}>Редактировать</Button>
              <Button variant="outlined" color="error" onClick={handleDeleteTask}>Удалить</Button>
            </Stack>
        )}

        {/* ===== Оценки ===== */}
        {task.status === "done" && isExecutor && (
            <Paper sx={{mt: 4, p: 2}}>
              <Typography variant="h6">Ваша оценка по задаче</Typography>
              {evaluations[user.id] ? (
                  <Box sx={{mt: 1}}>
                    <Typography>⭐ {evaluations[user.id].score}</Typography>
                    <Typography>{evaluations[user.id].comment || "-"}</Typography>
                    <Typography variant="caption">Оценка
                      от {getUserName(evaluations[user.id].evaluator_id)}</Typography>
                  </Box>
              ) : (
                  <Typography>Задача ещё не оценена</Typography>
              )}
            </Paper>
        )}

        {task.status === "done" && isCreator && task.executors?.length > 0 && (
            <Paper sx={{mt: 4, p: 2}}>
              <Typography variant="h6">Оценка исполнителей</Typography>
              <Stack spacing={2} sx={{mt: 1}}>
                {task.executors.map((executor) => {
                  const evalData = evaluations[executor.id];
                  const isEditing = editingExecutorId === executor.id || !evalData;
                  return (
                      <Paper key={executor.id} sx={{p: 1}}>
                        <Typography fontWeight={600}>{executor.full_name ?? executor.email}</Typography>
                        {isEditing ? (
                            <EvaluationForm
                                executors={[{id: executor.id, name: executor.full_name ?? executor.email}]}
                                initial={evalData}
                                taskId={task.id}
                                singleExecutor
                                onSave={async (data) => await handleSaveEvaluation(executor.id, data)}
                                onCancel={() => setEditingExecutorId(null)}
                            />
                        ) : (
                            <Stack direction="row" spacing={1} sx={{mt: 1, alignItems: "center"}}>
                              <Typography>⭐ {evalData.score}</Typography>
                              <Typography>{evalData.comment || "-"}</Typography>
                              <Button size="small"
                                      onClick={() => setEditingExecutorId(executor.id)}>Редактировать</Button>
                              <Button size="small" color="error"
                                      onClick={() => handleDeleteEvaluation(executor.id)}>Удалить</Button>
                            </Stack>
                        )}
                      </Paper>
                  );
                })}
              </Stack>
            </Paper>
        )}

        {/* ===== Комментарии ===== */}
        <Paper sx={{mt: 4, p: 2}}>
          <Typography variant="h6">Комментарии</Typography>
          {comments.length === 0 ? (
              <Typography>Комментариев нет</Typography>
          ) : (
              <List>
                {comments.map((c) => (
                    <ListItem key={c.id}
                              sx={{display: "flex", justifyContent: "space-between", alignItems: "center", p: 1}}>
                      <Typography>
                        <strong>{getUserName(c.author_id)}:</strong> {c.message}
                      </Typography>
                      {c.author_id === user.id && (
                          <Button variant="text" color="error" size="small"
                                  onClick={() => handleDeleteComment(c.id)}>Удалить</Button>
                      )}
                    </ListItem>
                ))}
              </List>
          )}

          {canComment && (
              <Stack direction="row" spacing={1} sx={{mt: 2}}>
                <TextField
                    fullWidth
                    size="small"
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Написать комментарий..."
                />
                <Button variant="contained" onClick={handleAddComment} disabled={commentLoading}>Добавить</Button>
              </Stack>
          )}
        </Paper>
      </Box>
  );
}
