export type CalendarEventType = "task" | "meeting";

export interface CalendarEvent {
  type: CalendarEventType;
  id: number;
  title: string;
  date: string;
  start_time?: string;
  end_time?: string;
  status?: string;
}

export interface CalendarMonth {
  date: string;
  events: CalendarEvent[];
}
