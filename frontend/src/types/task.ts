import type { UserPublic } from "./auth";

export type TaskStatus = "open" | "in_progress" | "done";

export interface TaskBase {
  title: string;
  description?: string;
  deadline?: string; // ISO date
}

export interface TaskCreateSchema extends TaskBase {
  executor_ids: number[];
}

export interface TaskUpdateSchema extends Partial<TaskBase> {
  executor_ids?: number[] | null;
}

export type TaskListPublicSchema = {
  id: number;
  title: string;
  description: string | null;
  deadline: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
  creator_id: number;
  team_id: string;
  executors?: UserPublic[];
  creator?: UserPublic;
};

export interface TaskPublicSchema extends TaskListPublicSchema {
  executors: UserPublic[];
  creator: UserPublic;
}

export interface TaskStatusUpdateSchema {
  status: TaskStatus;
}

export interface TaskCommentCreateSchema {
  message: string;
}

export interface TaskCommentPublicSchema extends TaskCommentCreateSchema {
  id: number;
  task_id: number;
  author_id: number;
  created_at: string;
}
