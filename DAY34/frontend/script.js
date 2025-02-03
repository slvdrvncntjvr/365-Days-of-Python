let ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onopen = function () {
    console.log("WebSocket connected!");
    ws.send("Hello, Server!");
};

ws.onmessage = function (event) {
    console.log("Message from server: ", event.data);
};

ws.onclose = function (event) {
    console.log("WebSocket closed: ", event);
};


ws.onmessage = (event) => {
    console.log("Server:", event.data);
    const tasks = document.getElementById("tasks");
    const li = document.createElement("li");
    li.textContent = event.data;
    tasks.appendChild(li);
};

function startListening() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        ws.send(transcript);
    };
}
