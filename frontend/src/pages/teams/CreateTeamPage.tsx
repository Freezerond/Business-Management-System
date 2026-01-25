import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import { createTeam } from "../../api/teamsApi.ts";

import { Box, TextField, Button, Typography, Container } from "@mui/material";

export default function CreateTeamPage() {
  const user = authStore((s) => s.user);
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);

  if (!user) return null; // защита, если не авторизован

  const handleCreate = async () => {
    if (!name) return alert("Введите название команды");
    setLoading(true);
    try {
      const team = await createTeam( name );
      authStore.setState({
        user: { ...user!, team_id: team.id, role: "admin" }
      });
      alert(`Команда "${team.name}" создана!`);
      navigate(`/team/${team.id}`); // переходим в новую команду
    } catch (err: any) {
      alert("Ошибка при создании команды: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h2" gutterBottom>
        Создать команду
      </Typography>

      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField
          label="Название команды"
          value={name}
          onChange={(e) => setName(e.target.value)}
          fullWidth
        />

        <Button
          variant="contained"
          color="success"
          onClick={handleCreate}
          disabled={loading}
        >
          {loading ? "Создаём..." : "Создать"}
        </Button>
      </Box>
    </Container>
  );
}
