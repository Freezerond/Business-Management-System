import { authStore } from "../auth/store";
import { Link as RouterLink } from "react-router-dom";

import {Box, Button, Typography, Stack, Paper, Grid} from "@mui/material";

export default function Dashboard() {
  const user = authStore((s) => s.user);

  if (!user) return null;

  const hasTeam = Boolean(user?.team_id);
  const isEmployeeOrManager = user.role === "employee" || user.role === "manager";
  const isManagerOrAdmin = user.role === "manager" || user.role === "admin";

   return (
    <Box sx={{ maxWidth: 1000, mx: "auto", p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Панель управления
      </Typography>
      <Typography variant="body1" gutterBottom>
        Добро пожаловать, <strong>{user?.full_name ?? user?.email}</strong>
      </Typography>

      <Grid container spacing={3}>
        {/* ===== Профиль и команда ===== */}
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper sx={{ p: 2 }} elevation={3}>
            <Typography variant="h6" gutterBottom>
              Профиль и команда
            </Typography>
            <Stack spacing={2}>
              <Button component={RouterLink} to="/profile" variant="contained" color="primary">
                Профиль
              </Button>

              {user?.team_id ? (
                <Button component={RouterLink} to={`/team/${user.team_id}`} variant="contained" color="primary">
                  Моя команда
                </Button>
              ) : (
                <Button component={RouterLink} to="/create-team" variant="contained" color="primary">
                  Создать команду
                </Button>
              )}
            </Stack>
          </Paper>
        </Grid>

        {/* ===== Задачи и оценки ===== */}
        {hasTeam && (
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2 }} elevation={3}>
              <Typography variant="h6" gutterBottom>
                Задачи и оценки
              </Typography>
              <Stack spacing={2}>
                {isEmployeeOrManager && (
                  <Button component={RouterLink} to="/tasks/my" variant="contained" color="secondary">
                    Мои задачи
                  </Button>
                )}
                {isManagerOrAdmin && (
                  <>
                    <Button component={RouterLink} to="/tasks/create" variant="contained" color="secondary">
                      Создать задачу
                    </Button>
                    <Button component={RouterLink} to="/tasks/created" variant="contained" color="secondary">
                      Созданные задачи
                    </Button>
                  </>
                )}
                {isEmployeeOrManager && (
                  <Button component={RouterLink} to="/evaluations/my-received" variant="contained" color="success">
                    Мои оценки
                  </Button>
                )}
                {isManagerOrAdmin && (
                  <Button component={RouterLink} to="/evaluations/my-given" variant="contained" color="success">
                    Выставленные оценки
                  </Button>
                )}
                <Button component={RouterLink} to="/evaluations/average" variant="contained" color="success">
                  Средняя оценка
                </Button>
              </Stack>
            </Paper>
          </Grid>
        )}

        {/* ===== Встречи и календарь ===== */}
        {hasTeam && (
          <Grid size={{ xs: 12, md: 4 }}>
            <Paper sx={{ p: 2 }} elevation={3}>
              <Typography variant="h6" gutterBottom>
                Встречи и календарь
              </Typography>
              <Stack spacing={2}>
                <Button component={RouterLink} to="/meetings" variant="contained" color="warning">
                  Мои встречи
                </Button>
                {isManagerOrAdmin && (
                  <Button component={RouterLink} to="/meetings/create" variant="contained" color="warning">
                    Создать встречу
                  </Button>
                )}
                <Button component={RouterLink} to="/calendar" variant="contained" color="info">
                  Календарь событий
                </Button>
              </Stack>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}

