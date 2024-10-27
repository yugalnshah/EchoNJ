import React from "react";
import { AppBar, Toolbar, Typography, Container, Button, CssBaseline, Box } from "@mui/material";
import{BrowserRouter as Router, Routes, Route, useNavigate} from "react-router-dom";
import AssistantPage from "./components/AssistantPage"
import { ThemeProvider, createTheme } from "@mui/material/styles";


const theme = createTheme({
  palette: {
    primary: {
      main: "#1D2951", 
    },
    secondary: {
      main: "#FF6319", 
    },
    background: {
      default: "#0A1F33", 
    },
    text: {
      primary: "#FFFFFF", 
    },
  },
  typography: {
    fontFamily: "Helvetica, Arial, sans-serif",
    h4: {
      fontWeight: "bold",
    },
  },
});
function Home() {
  const navigate = useNavigate(); // useNavigate hook to programmatically navigate

  return (
    <>
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
            EchoNJ
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
      <Box sx={{ backgroundColor: "#0A1F33", color: "#FFFFFF", minHeight: "100vh", paddingTop: "20px" }}>
        <Container maxWidth="lg" style={{ padding: "20px" }}>
          <Typography variant="h4" color="textPrimary" style={{ fontWeight: "bold" }} gutterBottom>
            Plan Your Trip
          </Typography>
          <Typography variant="body1" color="textPrimary">
            Find your way with real-time transit updates, schedules, and alerts.
          </Typography>
          <Typography variant="body1" color="textPrimary">
            Find more about schedules, prices, and routes by just talking!
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: "20px" }}>
            <Button
              variant="contained"
              color="secondary"
              style={{
                fontSize: "1.5rem",
                padding: "16px 32px",
                minWidth: "220px",
              }}
              onClick={() => navigate("/assistant")} // Navigate to the assistant page
            >
              Get Started
            </Button>
          </Box>
        </Container>
      </Box>
    </>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/assistant" element={<AssistantPage />} /> {/* Define route for AssistantPage */}
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;