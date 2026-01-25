import { useEffect, useState } from "react";
import { getDayCalendar, getMonthCalendar } from "../../api/calendarApi";
import type { CalendarEvent, CalendarMonth } from "../../types/calendar";
import { Link as RouterLink} from "react-router-dom";

import { Box, Typography, Paper, Stack, Button, IconButton, Divider, Chip, List, ListItem } from "@mui/material";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

function formatDate(date: Date) {
  return date.toISOString().slice(0, 10); // YYYY-MM-DD
}

function formatTimeRange(e: CalendarEvent) {
  if (!e.start_time || !e.end_time) return null;
  return `${e.start_time.slice(0, 5)} – ${e.end_time.slice(0, 5)}`;
}

export default function CalendarPage() {
  const today = new Date();

  const [currentDate, setCurrentDate] = useState(today);
  const [monthEvents, setMonthEvents] = useState<CalendarMonth[]>([]);
  const [dayEvents, setDayEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth() + 1;

  // ===== Загружаем месяц =====
 useEffect(() => {
  setLoading(true);
  getMonthCalendar(year, month)
    .then((res) => setMonthEvents(res.data))
    .catch(() => alert("Ошибка загрузки календаря"))
    .finally(() => setLoading(false));
}, [year, month]);

useEffect(() => {
  getDayCalendar(formatDate(currentDate))
    .then((res) => setDayEvents(res.data))
    .catch(() => alert("Ошибка загрузки дня"));
}, [currentDate]);

  const changeMonth = (delta: number) => {
    setCurrentDate(new Date(year, month - 1 + delta, 1));
  };

  return (
  <Box sx={{ maxWidth: 900, mx: "auto", mt: 3 }}>
    <Typography variant="h4" gutterBottom>
      Календарь
    </Typography>

    {/* ===== Навигация ===== */}
    <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 3 }}>
      <IconButton onClick={() => changeMonth(-1)}>
        <ArrowBackIosNewIcon />
      </IconButton>

      <Typography variant="h6">
        {currentDate.toLocaleString("ru-RU", {
          month: "long",
          year: "numeric",
        })}
      </Typography>

      <IconButton onClick={() => changeMonth(1)}>
        <ArrowForwardIosIcon />
      </IconButton>
    </Stack>

    {loading ? (
      <Typography>Загрузка...</Typography>
    ) : (
      <Stack direction={{ xs: "column", md: "row" }} spacing={3}>
        {/* ===== Месяц ===== */}
        <Paper sx={{ flex: 1, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            События месяца
          </Typography>

          {monthEvents.length === 0 ? (
            <Typography color="text.secondary">Нет событий</Typography>
          ) : (
            <List dense>
              {monthEvents.map((day) => {
                const date = new Date(day.date);
                const isActive =
                  date.toDateString() === currentDate.toDateString();

                return (
                  <ListItem
                    key={day.date}
                    disablePadding
                    sx={{ mb: 0.5 }}
                  >
                    <Button
                      fullWidth
                      variant={isActive ? "contained" : "text"}
                      onClick={() => setCurrentDate(date)}
                      sx={{ justifyContent: "space-between" }}
                    >
                      {date.toLocaleDateString("ru-RU")}
                      <Chip size="small" label={day.events.length} />
                    </Button>
                  </ListItem>
                );
              })}
            </List>
          )}
        </Paper>

        {/* ===== День ===== */}
        <Paper sx={{ flex: 2, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            {currentDate.toLocaleDateString("ru-RU", {
              day: "2-digit",
              month: "long",
              year: "numeric",
            })}
          </Typography>

          <Divider sx={{ mb: 2 }} />

          {dayEvents.length === 0 ? (
            <Typography color="text.secondary">
              Событий нет
            </Typography>
          ) : (
            <Stack spacing={2}>
  {dayEvents.map((e) => (
    <Paper
      key={`${e.type}-${e.id}`}
      component={RouterLink}
      to={
        e.type === "task"
          ? `/tasks/${e.id}`
          : `/meetings/${e.id}`
      }
      variant="outlined"
      sx={{
        p: 2,
        borderRadius: 2,
        textDecoration: "none",
        color: "inherit",
        cursor: "pointer",
        transition: "transform 0.2s, box-shadow 0.2s",
        "&:hover": {
          transform: "translateY(-2px)",
          boxShadow: 3,
        },
      }}
    >
      <Typography variant="subtitle1" fontWeight={600}>
        {e.title}
      </Typography>

      {formatTimeRange(e) && (
        <Typography variant="body2" color="text.secondary">
          {formatTimeRange(e)}
        </Typography>
      )}

      <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
        <Chip
          size="small"
          label={e.type === "task" ? "Задача" : "Встреча"}
          color={e.type === "task" ? "primary" : "secondary"}
        />

        {e.type === "task" && e.status && (
          <Chip
            size="small"
            label={e.status}
            variant="outlined"
          />
        )}
      </Stack>
    </Paper>
  ))}
</Stack>
          )}
        </Paper>
      </Stack>
    )}
  </Box>
);
  }
