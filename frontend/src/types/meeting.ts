import type { UserPublic } from "./auth";

export interface MeetingCreateSchema {
  title: string;
  description?: string;
  start_time: string; // ISO string
  end_time: string;   // ISO string
  participant_ids: number[];
}

export interface MeetingListPublicSchema {
  id: number;
  title: string;
  description?: string;
  start_time: string;
  end_time: string;
  creator_id: number;
}

export interface MeetingPublicSchema extends MeetingListPublicSchema {
  participants: UserPublic[];
  // creator: UserPublic;
}