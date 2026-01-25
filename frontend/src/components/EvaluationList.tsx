import type { EvaluationPublicSchema } from "../types/evaluation";

import { Card, CardContent, Typography, Button, Stack, Box } from "@mui/material";

type Props = {
  evaluations: EvaluationPublicSchema[];
  canEdit: (e: EvaluationPublicSchema) => boolean;
  onEdit: (e: EvaluationPublicSchema) => void;
  onDelete: (e: EvaluationPublicSchema) => void;
};

export function EvaluationList({
  evaluations,
  canEdit,
  onEdit,
  onDelete,
}: Props) {
  if (evaluations.length === 0) {
    return <Typography>Оценок пока нет</Typography>;
  }

  return (
    <Stack spacing={2}>
      {evaluations.map((e) => (
        <Card
          key={e.executor_id}
          variant="outlined"
          sx={{
            transition: "transform 0.2s, box-shadow 0.2s",
            "&:hover": {
              transform: "translateY(-2px)",
              boxShadow: 3,
            },
          }}
        >
          <CardContent sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Box>
              <Typography variant="subtitle1">
                ⭐ {e.score} — {e.comment || "-"}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Исполнитель #{e.executor_id}, оценил #{e.evaluator_id}
              </Typography>
            </Box>

            {canEdit(e) && (
              <Stack direction="row" spacing={1}>
                <Button size="small" variant="contained" onClick={() => onEdit(e)}>
                  Редактировать
                </Button>
                <Button size="small" variant="outlined" color="error" onClick={() => onDelete(e)}>
                  Удалить
                </Button>
              </Stack>
            )}
          </CardContent>
        </Card>
      ))}
    </Stack>
  );
}