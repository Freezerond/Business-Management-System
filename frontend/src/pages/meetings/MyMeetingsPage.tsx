import { useEffect, useState } from "react";
import { getMyMeetings } from "../../api/meetingsApi.ts";
import type { MeetingListPublicSchema } from "../../types/meeting.ts";
import { Link as RouterLink } from "react-router-dom";
import { formatMeetingTime } from "./format_meeting_time.tsx"

import { Box, Typography, Card, CardContent, Stack } from "@mui/material";

export default function MyMeetingsPage() {
    const [meetings, setMeetings] = useState<MeetingListPublicSchema[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getMyMeetings()
            .then(setMeetings)
            .catch(() => alert("Ошибка загрузки встреч"))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <Typography sx={{textAlign: "center", mt: 3}}>Загрузка встреч...</Typography>;

    if (!meetings.length) return <Typography sx={{textAlign: "center", mt: 3}}>Вы пока не участвуете ни в одной
        встрече</Typography>;

    return (
        <Box sx={{maxWidth: 700, mx: "auto", mt: 3}}>
            <Typography variant="h4" gutterBottom>
                Мои встречи
            </Typography>

            <Stack spacing={2}>
                {meetings.map((m) => (
                    <Card
                        key={m.id}
                        variant="outlined"
                        component={RouterLink}
                        to={`/meetings/${m.id}`}
                        sx={{
                            textDecoration: "none",
                            color: "inherit",
                            borderRadius: 2,
                            transition: "transform 0.2s, box-shadow 0.2s",
                            "&:hover": {
                                transform: "translateY(-2px)",
                                boxShadow: 3,
                                backgroundColor: "#f5faff",
                            },
                        }}
                    >
                        <CardContent>
                            <Typography variant="subtitle1" fontWeight={600}>
                                {m.title}
                            </Typography>

                            <Typography variant="body2" color="text.secondary">
                                {formatMeetingTime(m.start_time, m.end_time)}
                            </Typography>

                            {m.description && (
                                <Typography
                                    variant="body2"
                                    color="text.secondary"
                                    sx={{mt: 1}}
                                >
                                    {m.description}
                                </Typography>
                            )}
                        </CardContent>
                    </Card>
                ))}
            </Stack>
        </Box>
    );
}
