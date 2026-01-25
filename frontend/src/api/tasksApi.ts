import api from "./axios";
import type {
  TaskCreateSchema,
  TaskUpdateSchema,
  TaskStatusUpdateSchema,
  TaskCommentCreateSchema,
} from "../types/task";

export const getMyTasks = async () => {
  const { data } = await api.get("/tasks/");
  return data;
};

export const getCreatedTasks = async () => {
  const { data } = await api.get("/tasks/created");
  return data;
};

export const getTask = async (taskId: number) => {
  const { data } = await api.get(`/tasks/${taskId}`);
  return data;
};

export const createTask = async (task: TaskCreateSchema) => {
  const { data } = await api.post("/tasks/", task);
  return data;
};

export const updateTask = async (taskId: number, task: TaskUpdateSchema) => {
  const { data } = await api.patch(`/tasks/${taskId}`, task);
  return data;
};

export const updateTaskStatus = async (
  taskId: number,
  status: TaskStatusUpdateSchema
) => {
  const { data } = await api.patch(`/tasks/${taskId}/status`, status);
  return data;
};

export const deleteTask = async (taskId: number) => {
  await api.delete(`/tasks/${taskId}`);
};

export const getComments = async (taskId: number) => {
  const { data } = await api.get(`/tasks/${taskId}/comments`);
  return data;
};

export const createComment = async (
  taskId: number,
  comment: TaskCommentCreateSchema
) => {
  const { data } = await api.post(`/tasks/${taskId}/comments`, comment);
  return data;
};

export const deleteComment = async (taskId: number, commentId: number) => {
  await api.delete(`/tasks/${taskId}/comments/${commentId}`);
};
