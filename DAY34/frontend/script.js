let ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onopen = () => console.log("WebSocket connected!");
ws.onmessage = (event) => console.log("Message from server:", event.data);

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false; // 

function startListening() {
    recognition.start();
    console.log("🎤 Listening...");
}

recognition.onresult = (event) => {
    let transcript = event.results[0][0].transcript;
    console.log("You said: ", transcript);
    ws.send(transcript);
};


recognition.onerror = (event) => console.error("Speech recognition error:", event.error);
document.getElementById("speakButton").addEventListener("click", startListening);
