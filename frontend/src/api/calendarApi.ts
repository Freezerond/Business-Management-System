import api from "./axios.ts";
import type {CalendarEvent, CalendarMonth} from "../types/calendar.ts";

export const getDayCalendar = (date: string) =>
  api.get<CalendarEvent[]>(`/calendar/day`, { params: { date } });

export const getMonthCalendar = (year: number, month: number) =>
  api.get<CalendarMonth[]>(`/calendar/month`, { params: { year, month } });