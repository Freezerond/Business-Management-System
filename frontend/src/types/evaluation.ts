export interface EvaluationBaseSchema {
  score: number; // 1..5
  comment: string;
}

export interface EvaluationCreateSchema extends EvaluationBaseSchema {
  executor_id: number;
}

export interface EvaluationUpdateSchema {
  score?: number;
  comment?: string;
}

export interface EvaluationPublicSchema extends EvaluationBaseSchema {
  task_id: number;
  executor_id: number;
  evaluator_id: number;
  created_at: string;
}

export interface AvgEvaluationSchema {
  user_id: number;
  average_score: number;
  count: number;
  start_date?: string | null;
  end_date?: string | null;
}
