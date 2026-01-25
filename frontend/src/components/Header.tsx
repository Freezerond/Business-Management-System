import { Link as RouterLink, useNavigate } from "react-router-dom";
import { authStore } from "../auth/store";

import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";

export default function Header() {
  const user = authStore((s) => s.user);
  const logout = authStore((s) => s.logout);
  const navigate = useNavigate();

  if (!user) return null; // скрываем header для неавторизованных

   return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div">
          <RouterLink to="/" style={{ textDecoration: "none", color: "inherit" }}>
            Панель управления
          </RouterLink>
        </Typography>

        <Box sx={{ flexGrow: 1 }} />

        <Typography sx={{ mr: 2 }}>
          {user.full_name ?? user.email}
        </Typography>

        <Button
          variant="contained"
          color="error"  // красная заливка
          onClick={() => {
            logout();
            navigate("/login");
          }}
          sx={{
            textTransform: "none", // чтобы текст не был капсом
            "&:hover": {
              backgroundColor: "#b71c1c", // темнее при наведении
            },
          }}
        >
          Выйти
        </Button>
      </Toolbar>
    </AppBar>
  );
}
