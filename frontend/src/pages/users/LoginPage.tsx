import { useState } from "react";
import { authStore } from "../../auth/store.ts";
import { useNavigate, Link } from "react-router-dom";

import { Box, TextField, Button, Typography, Container, CircularProgress } from "@mui/material";

export default function LoginPage() {
  const login = authStore((s) => s.login);
  const isLoading = authStore((s) => s.isLoading);
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    try {
      await login(email, password);
      navigate("/");
    } catch (err: any) {
      alert("Ошибка входа: " + err.message);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          mt: 8,
          p: 4,
          boxShadow: 3,
          borderRadius: 2,
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        <Typography variant="h4" component="h1" align="center">
          Вход
        </Typography>

        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
        />
        <TextField
          label="Пароль"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
        />

        <Button
          variant="contained"
          color="primary"
          onClick={submit}
          disabled={isLoading}
          fullWidth
          sx={{ mt: 2 }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : "Войти"}
        </Button>

        <Typography variant="body2" align="center" sx={{ mt: 2 }}>
          Если нет аккаунта, <Link to="/register">зарегистрируйтесь</Link>
        </Typography>
      </Box>
    </Container>
  );
}
