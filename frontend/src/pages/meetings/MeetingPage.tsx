import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { authStore } from "../../auth/store";
import { getMeeting, deleteMeeting } from "../../api/meetingsApi";
import type { MeetingPublicSchema } from "../../types/meeting";
import { formatMeetingTime } from "./format_meeting_time";

import { Box, Typography, Paper, Stack, List, ListItem, ListItemText, Button, Divider } from "@mui/material";

export default function MeetingPage() {
  const {id} = useParams();
  const navigate = useNavigate();
  const user = authStore((s) => s.user);

  const [meeting, setMeeting] = useState<MeetingPublicSchema | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting] = useState(false);

  useEffect(() => {
    if (!id) return;

    getMeeting(Number(id))
        .then(setMeeting)
        .catch(() => alert("Ошибка загрузки встречи"))
        .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Typography sx={{textAlign: "center", mt: 4}}>Загрузка встречи...</Typography>;
  if (!meeting) return <Typography sx={{textAlign: "center", mt: 4}}>Встреча не найдена</Typography>;
  if (!user) return null;

  const canDelete =
      user.role === "admin" || user.id === meeting.creator_id;

  const handleDelete = async () => {
    if (!confirm("Вы уверены, что хотите удалить встречу?")) return;

    try {
      await deleteMeeting(meeting.id);

      navigate("/", {replace: true});
    } catch {
      alert("Ошибка при удалении встречи");
    }
  };

  return (
      <Paper sx={{maxWidth: 700, mx: "auto", mt: 3, p: 3}}>
        <Stack spacing={2}>
          <Box>
            <Typography variant="h4">{meeting.title}</Typography>
            <Typography variant="body2" color="text.secondary">
              {formatMeetingTime(meeting.start_time, meeting.end_time)}
            </Typography>
          </Box>

          {meeting.description && (
              <Typography>{meeting.description}</Typography>
          )}

          <Divider/>

          <Box>
            <Typography variant="h6" gutterBottom>
              Участники
            </Typography>

            <List dense>
              {meeting.participants.map((p) => (
                  <ListItem key={p.id} disablePadding>
                    <ListItemText
                        primary={p.full_name ?? p.email}
                    />
                  </ListItem>
              ))}
            </List>
          </Box>

          {canDelete && (
              <>
                <Divider/>
                <Box>
                  <Button
                      variant="contained"
                      color="error"
                      onClick={handleDelete}
                      disabled={deleting}
                  >
                    {deleting ? "Удаление..." : "Удалить встречу"}
                  </Button>
                </Box>
              </>
          )}
        </Stack>
      </Paper>
  );
}
