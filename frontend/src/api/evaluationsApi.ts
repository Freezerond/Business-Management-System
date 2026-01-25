import api from "./axios";
import type {
  EvaluationCreateSchema,
  EvaluationUpdateSchema,
  EvaluationPublicSchema,
  AvgEvaluationSchema,
} from "../types/evaluation";

export const createEvaluation = async (
  taskId: number,
  data: EvaluationCreateSchema
): Promise<EvaluationPublicSchema> => {
  const res = await api.post(`/evaluations/${taskId}`, data);
  return res.data;
};

export const getEvaluation = async (
  taskId: number,
  executorId: number
): Promise<EvaluationPublicSchema> => {
  const res = await api.get(`/evaluations/${taskId}/${executorId}`);
  return res.data;
};

export const updateEvaluation = async (
  taskId: number,
  executorId: number,
  data: EvaluationUpdateSchema
): Promise<EvaluationPublicSchema> => {
  const res = await api.patch(`/evaluations/${taskId}/${executorId}`, data);
  return res.data;
};

export const deleteEvaluation = async (
  taskId: number,
  executorId: number
) => {
  await api.delete(`/evaluations/${taskId}/${executorId}`);
};

export const getMyGivenEvaluations = async () => {
  const res = await api.get(`/evaluations/my_given`);
  return res.data;
};

export const getMyReceivedEvaluations = async () => {
  const res = await api.get(`/evaluations/my_received`);
  return res.data;
};

export const getAverageEvaluation = async (
  userId: number,
  start?: string,
  end?: string
): Promise<AvgEvaluationSchema> => {
  const res = await api.get(`/evaluations/average`, {
    params: { user_id: userId, start, end },
  });
  return res.data;
};
