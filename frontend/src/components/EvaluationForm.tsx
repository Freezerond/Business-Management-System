import { useState } from "react";
import type {
  EvaluationCreateSchema,
  EvaluationUpdateSchema,
  EvaluationPublicSchema,
} from "../types/evaluation";

import { Box, TextField, Button, MenuItem, Stack } from "@mui/material";

type Props = {
  executors: { id: number; name: string }[];
  taskId: number;
  initial?: EvaluationPublicSchema;
  onSave: (data: EvaluationCreateSchema | EvaluationUpdateSchema) => Promise<void>;
  onCancel?: () => void;
  singleExecutor?: boolean;
};

export function EvaluationForm({
  executors,
  initial,
  onSave,
  onCancel,
  singleExecutor = false,
}: Props) {
  const [executorId, setExecutorId] = useState<number>(
    initial?.executor_id ?? executors[0]?.id
  );
  const [score, setScore] = useState(initial?.score ?? 5);
  const [comment, setComment] = useState(initial?.comment ?? "");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    await onSave(
      initial
        ? { score, comment }
        : { executor_id: executorId!, score, comment }
    );
    setLoading(false);
  };

  return (
    <Box sx={{ border: "1px solid #ddd", p: 2, mt: 2, borderRadius: 1 }}>
      {!singleExecutor && (
        <TextField
          select
          label="Исполнитель"
          value={executorId}
          onChange={(e) => setExecutorId(Number(e.target.value))}
          size="small"
          fullWidth
          sx={{ mb: 2 }}
        >
          {executors.map((e) => (
            <MenuItem key={e.id} value={e.id}>
              {e.name}
            </MenuItem>
          ))}
        </TextField>
      )}

      <TextField
        label="Оценка"
        type="number"
        inputProps={{ min: 1, max: 5 }}
        value={score}
        onChange={(e) => setScore(Number(e.target.value))}
        size="small"
        sx={{ mb: 2 }}
        fullWidth
      />

      <TextField
        label="Комментарий"
        multiline
        minRows={2}
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        size="small"
        fullWidth
        sx={{ mb: 2 }}
      />

      <Stack direction="row" spacing={1}>
        <Button variant="contained" onClick={handleSubmit} disabled={loading}>
          {loading ? "Сохранение..." : "Сохранить"}
        </Button>
        {onCancel && (
          <Button variant="outlined" onClick={onCancel}>
            Отмена
          </Button>
        )}
      </Stack>
    </Box>
  );
}
