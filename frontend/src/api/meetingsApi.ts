import api from "./axios";
import type { MeetingCreateSchema, MeetingListPublicSchema, MeetingPublicSchema } from "../types/meeting";

export const getMyMeetings = async (): Promise<MeetingListPublicSchema[]> => {
  const { data } = await api.get("/meetings/");
  return data;
};

export const getMeeting = async (meetingId: number): Promise<MeetingPublicSchema> => {
  const { data } = await api.get(`/meetings/${meetingId}`);
  return data;
};

export const createMeeting = async (meeting: MeetingCreateSchema): Promise<MeetingPublicSchema> => {
  const { data } = await api.post("/meetings/", meeting);
  return data;
};

export const deleteMeeting = async (meetingId: number) => {
  await api.delete(`/meetings/${meetingId}`);
};