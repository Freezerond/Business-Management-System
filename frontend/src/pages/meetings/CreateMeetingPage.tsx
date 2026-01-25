import { useEffect, useState } from "react";
import { getTeamMembers } from "../../api/teamsApi.ts";
import { createMeeting } from "../../api/meetingsApi.ts";
import type { MeetingCreateSchema } from "../../types/meeting.ts";
import { authStore } from "../../auth/store.ts";

import { Box, Typography, TextField, Button, Stack, FormGroup, FormControlLabel, Checkbox, Paper } from "@mui/material";

interface TeamMember {
  id: number;
  full_name?: string;
  email: string;
}

export default function CreateMeetingPage() {
  const user = authStore((s) => s.user);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [selectedParticipants, setSelectedParticipants] = useState<number[]>([]);
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(false);

 useEffect(() => {
  if (user?.team_id) {
    getTeamMembers(user.team_id)
      .then((members) =>
        setTeamMembers(members.filter((m) => m.id !== user.id))
      )
      .catch(() => alert("Ошибка загрузки команды"));
  }
}, [user?.team_id, user?.id]);

  const handleSubmit = async () => {
    if (!title || !startTime || !endTime) {
      alert("Заполните обязательные поля");
      return;
    }

    const meetingData: MeetingCreateSchema = {
      title,
      description: description || undefined,
      start_time: new Date(startTime).toISOString(),
      end_time: new Date(endTime).toISOString(),
      participant_ids: selectedParticipants,
    };

    setLoading(true);
    try {
      await createMeeting(meetingData);
      alert("Встреча создана");
      window.location.href = "/";
    } catch (err: any) {
      alert(err.response?.data?.detail ?? "Ошибка при создании встречи");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleParticipant = (id: number) => {
    setSelectedParticipants((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  if (!user) return null;

  return (
  <Paper sx={{ maxWidth: 600, mx: "auto", mt: 3, p: 3 }}>
    <Typography variant="h4" gutterBottom>
      Создать встречу
    </Typography>

    <Stack spacing={2}>
      <TextField
        label="Название"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        fullWidth
        required
      />

      <TextField
        label="Описание"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        fullWidth
        multiline
        minRows={3}
      />

      <TextField
        label="Начало"
        type="datetime-local"
        value={startTime}
        onChange={(e) => setStartTime(e.target.value)}
        InputLabelProps={{ shrink: true }}
        fullWidth
      />

      <TextField
        label="Конец"
        type="datetime-local"
        value={endTime}
        onChange={(e) => setEndTime(e.target.value)}
        InputLabelProps={{ shrink: true }}
        fullWidth
      />

      <Box>
        <Typography variant="subtitle1" gutterBottom>
          Участники
        </Typography>

        <FormGroup>
          {teamMembers.map((m) => (
            <FormControlLabel
              key={m.id}
              control={
                <Checkbox
                  checked={selectedParticipants.includes(m.id)}
                  onChange={() => toggleParticipant(m.id)}
                />
              }
              label={m.full_name ?? m.email}
            />
          ))}
        </FormGroup>
      </Box>

      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        disabled={loading}
        size="large"
      >
        {loading ? "Создание..." : "Создать встречу"}
      </Button>
    </Stack>
  </Paper>
);
}
