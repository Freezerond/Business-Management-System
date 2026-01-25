import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../../api/authApi.ts";

import { Box, TextField, Button, Typography, Container } from "@mui/material";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [full_name, setFullName] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
  try {
    await register(email, full_name, password);
    alert("Регистрация успешна");
    navigate("/login");
  } catch (err: any) {
    const message =
    err.response?.data?.detail?.[0]?.msg || "Ошибка регистрации";
  alert(message);
  }
};

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: 4,
          border: "1px solid #ccc",
          borderRadius: 2,
          boxShadow: 2,
          backgroundColor: "#fff",
        }}
      >
        <Typography component="h1" variant="h5" sx={{ mb: 3 }}>
          Регистрация
        </Typography>

        <TextField
          label="Email"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          label="ФИО"
          fullWidth
          margin="normal"
          value={full_name}
          onChange={(e) => setFullName(e.target.value)}
        />
        <TextField
          label="Пароль"
          type="password"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <Button
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 3 }}
          onClick={submit}
        >
          Зарегистрироваться
        </Button>

        <Typography variant="body2" sx={{ mt: 2, textAlign: "center" }}>
          Если есть аккаунт, <Link to="/login">войдите</Link>
        </Typography>
      </Box>
    </Container>
  );
}
