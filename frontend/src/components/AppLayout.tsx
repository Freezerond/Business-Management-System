import type { ReactNode } from "react";
import Header from "./Header";

import { Box, Container } from "@mui/material";

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Header />
      <Container sx={{ flex: 1, mt: 2 }}>{children}</Container>
    </Box>
  );
}
