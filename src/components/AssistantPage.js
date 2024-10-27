import React, { useEffect, useState } from "react";
import { Typography, Box, IconButton } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useNavigate } from "react-router-dom";
import io from "socket.io-client";
import "./App.css";

const socket = io("http://localhost:5000");

function AssistantPage() {
const navigate = useNavigate();
const [response, setResponse] = useState("");

useEffect(() => {
socket.on("answer", (data) => {
const answer = data.answer;
setResponse(answer);
speakAnswer(answer);
});

return () => {
socket.off("answer");
};
}, []);

const startListening = () => {
const recognition = new window.webkitSpeechRecognition();
recognition.lang = "en-US";
recognition.interimResults = false;
recognition.maxAlternatives = 1;

recognition.onresult = (event) => {
const spokenText = event.results[0][0].transcript;
console.log("Recognized Text:", spokenText);
socket.emit("question", { question: spokenText });
};

recognition.onerror = (event) => {
console.error("Recognition error:", event.error);
};

recognition.start();
};

const speakAnswer = (text) => {
const synth = window.speechSynthesis;
const utterance = new SpeechSynthesisUtterance(text);
utterance.lang = "en-US";
synth.speak(utterance);
};

return (
<Box
sx={{
position: "relative",
display: "flex",
flexDirection: "column",
justifyContent: "center",
alignItems: "center",
minHeight: "100vh",
width: "100vw",
backgroundColor: "#000",
textAlign: "center",
color: "#FFFFFF",
}}
>
<IconButton
onClick={() => navigate("/")}
sx={{
position: "absolute",
top: "20px",
left: "20px",
color: "#FFFFFF",
}}
>
<ArrowBackIcon fontSize="large" />
</IconButton>

<Typography variant="h4" sx={{ fontWeight: "300", marginBottom: "5px" }}>
Welcome to EchoNJ
</Typography>
<Typography variant="h5" sx={{ fontWeight: "400", marginBottom: "40px" }}>
How can I help you?
</Typography>

<div className="circle-container" onClick={startListening}>
<span className="circle-text">PRESS TO SPEAK</span>
<div className="infinity-circle"></div>
</div>

<Typography
variant="body1"
sx={{ fontWeight: "300", color: "#FFFFFF", marginTop: "30px" }}
>
{response}
</Typography>
 </Box>
);
}

export default AssistantPage;