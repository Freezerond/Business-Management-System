import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authStore } from "../../auth/store.ts";
import { updateProfile } from "../../api/usersApi.ts";
import {Box, Button, Container, TextField, Typography} from "@mui/material";

export default function EditProfilePage() {
  const user = authStore((s) => s.user);
  const navigate = useNavigate();

  const [email, setEmail] = useState(user?.email ?? "");
  const [fullName, setFullName] = useState(user?.full_name ?? "");
  const [isSaving, setIsSaving] = useState(false);

  if (!user) return <div>Загрузка пользователя...</div>;

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await updateProfile({ email, full_name: fullName });
      alert("Профиль обновлён");

      // Обновляем user в store
      await authStore.getState().loadUser();

      navigate("/profile"); // возвращаем на страницу просмотра профиля
    } catch (err: any) {
      alert("Ошибка при обновлении: " + err.message);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h2" gutterBottom>
        Редактировать профиль
      </Typography>

      <Box component="form" sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
        />

        <TextField
          label="ФИО"
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          fullWidth
        />

        <Box sx={{ display: "flex", gap: 2, mt: 2 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSave}
            disabled={isSaving}
          >
            {isSaving ? "Сохраняем..." : "Сохранить"}
          </Button>

          <Button
            variant="outlined"
            color="secondary"
            onClick={() => navigate("/profile")}
          >
            Отмена
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
