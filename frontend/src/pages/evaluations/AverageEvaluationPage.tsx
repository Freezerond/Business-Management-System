import { useEffect, useState } from "react";
import { authStore } from "../../auth/store.ts";
import { getAverageEvaluation } from "../../api/evaluationsApi.ts";
import { getTeamMembers } from "../../api/teamsApi.ts";
import type { AvgEvaluationSchema } from "../../types/evaluation.ts";
import type { TeamMember } from "../../types/team.ts";

import { Box,  Typography,  Card,  CardContent,  Button,  TextField,  MenuItem,  Stack,  Chip } from "@mui/material";

export default function AverageEvaluationPage() {
  const user = authStore((s) => s.user);

  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [result, setResult] = useState<AvgEvaluationSchema | null>(null);
  const [loading, setLoading] = useState(false);

  const employeeMembers = teamMembers.filter((m) => m.role === "employee");

  if (!user) return [];
  const nonAdminMembers = teamMembers.filter((m) => m.id !== user.id);

  if (!user) return null;

  const isEmployee = user.role === "employee";
  const isManager = user.role === "manager";
  const isAdmin = user.role === "admin";

  const canSelectUser = isManager || isAdmin;

  // ===== загрузка участников команды для менеджера =====
  useEffect(() => {
    if ((isManager || isAdmin) && user.team_id) {
      getTeamMembers(user.team_id)
          .then(setTeamMembers)
          .catch(() => alert("Ошибка загрузки команды"));
    }
  }, [isManager, user.team_id]);

  const handleFetchAverage = async () => {
    let targetUserId: number | null = null;

    if (isEmployee) {
      targetUserId = user.id;
    } else {
      targetUserId = selectedUserId;
    }

    if (!targetUserId) {
      alert("Выберите пользователя");
      return;
    }

    setLoading(true);
    try {
      const res = await getAverageEvaluation(
          targetUserId,
          startDate || undefined,
          endDate || undefined
      );
      setResult(res);
    } catch (err) {
      alert("Ошибка при получении средней оценки");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
      <Box sx={{maxWidth: 700, mx: "auto", mt: 3}}>
        <Typography variant="h4" gutterBottom>
          Средняя оценка
        </Typography>

        {/* ===== Фильтры ===== */}
        <Card variant="outlined" sx={{borderRadius: 2, mb: 3}}>
          <CardContent>
            <Stack spacing={2}>
              {/* Пользователь */}
              {canSelectUser && (
                  <TextField
                      select
                      label="Пользователь"
                      value={selectedUserId ?? ""}
                      onChange={(e) =>
                          setSelectedUserId(e.target.value ? Number(e.target.value) : null)
                      }
                      fullWidth
                  >
                    <MenuItem value="">— выбрать —</MenuItem>

                    {isManager && (
                        <>
                          <MenuItem value={user.id}>Я</MenuItem>
                          {employeeMembers.map((m) => (
                              <MenuItem key={m.id} value={m.id}>
                                {m.full_name ?? m.email}
                              </MenuItem>
                          ))}
                        </>
                    )}

                    {isAdmin &&
                        nonAdminMembers.map((m) => (
                            <MenuItem key={m.id} value={m.id}>
                              {m.full_name ?? m.email}
                            </MenuItem>
                        ))}
                  </TextField>
              )}

              {/* Период */}
              <Stack direction={{xs: "column", sm: "row"}} spacing={2}>
                <TextField
                    type="date"
                    label="С"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    InputLabelProps={{shrink: true}}
                    fullWidth
                />

                <TextField
                    type="date"
                    label="По"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    InputLabelProps={{shrink: true}}
                    fullWidth
                />
              </Stack>

              <Button
                  variant="contained"
                  onClick={handleFetchAverage}
                  disabled={loading}
                  sx={{alignSelf: "flex-start"}}
              >
                {loading ? "Формирование..." : "Сформировать"}
              </Button>
            </Stack>
          </CardContent>
        </Card>

        {/* ===== Результат ===== */}
        {result && (
            <Card
                sx={{
                  borderRadius: 2,
                  backgroundColor: "#f5f5f5",
                  transition: "box-shadow 0.2s",
                  "&:hover": {boxShadow: 3},
                }}
            >
              <CardContent>
                <Stack spacing={1}>
                  <Typography variant="h6">
                    Результат
                  </Typography>

                  <Stack direction="row" spacing={2} alignItems="center">
                    <Typography>
                      Средняя оценка:
                    </Typography>
                    <Chip
                        label={result.average_score.toFixed(2)}
                        color={
                          result.average_score >= 4
                              ? "success"
                              : result.average_score >= 3
                                  ? "warning"
                                  : "error"
                        }
                        sx={{fontWeight: "bold"}}
                    />
                  </Stack>

                  <Typography>
                    Количество оценок: <strong>{result.count}</strong>
                  </Typography>

                  {(result.start_date || result.end_date) && (
                      <Typography color="text.secondary">
                        Период: {result.start_date ?? "∞"} — {result.end_date ?? "∞"}
                      </Typography>
                  )}
                </Stack>
              </CardContent>
            </Card>
        )}
      </Box>
  );
}
