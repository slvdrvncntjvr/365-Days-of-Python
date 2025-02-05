import asyncio
import websockets
import json
import threading
import speech_recognition as sr
from flask import Flask, render_template_string
from cryptography.fernet import Fernet

SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)
tasks = []

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Task Manager</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
</head>
<body>
    <h1>Voice-Controlled Encrypted Task Manager</h1>
    <button onclick="startListening()">🎤 Speak</button>
    <input type="text" id="taskInput" placeholder="Type a task">
    <button onclick="sendTask()">Add Task</button>
    <ul id="taskList"></ul>
    <script>
        const SECRET_KEY = "{{ secret_key.decode() }}";
        let ws = new WebSocket("ws://127.0.0.1:8000");

        function encryptMessage(message) {
            return CryptoJS.AES.encrypt(message, SECRET_KEY).toString();
        }

        function decryptMessage(encryptedMessage) {
            let bytes = CryptoJS.AES.decrypt(encryptedMessage, SECRET_KEY);
            return bytes.toString(CryptoJS.enc.Utf8);
        }

        ws.onmessage = (event) => {
            let decryptedData = decryptMessage(event.data);
            let taskList = document.getElementById("taskList");
            taskList.innerHTML = "";
            JSON.parse(decryptedData).forEach(task => {
                let li = document.createElement("li");
                li.textContent = task;
                taskList.appendChild(li);
            });
        };

        function sendTask() {
            let task = document.getElementById("taskInput").value;
            let encryptedTask = encryptMessage(task);
            ws.send(encryptedTask);
            document.getElementById("taskInput").value = "";
        }

        function startListening() {
            let recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.start();
            recognition.onresult = (event) => {
                let task = event.results[0][0].transcript;
                let encryptedTask = encryptMessage(task);
                ws.send(encryptedTask);
            };
        }
    </script>
</body>
</html>
"""

async def handle_client(websocket, path):
    global tasks
    async for encrypted_message in websocket:
        try:
            decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
            if decrypted_message.lower() == "list tasks":
                encrypted_response = cipher.encrypt(json.dumps(tasks).encode()).decode()
                await websocket.send(encrypted_response)
            elif decrypted_message.startswith("complete "):
                task_to_remove = decrypted_message.replace("complete ", "").strip()
                tasks = [task for task in tasks if task != task_to_remove]
                encrypted_response = cipher.encrypt(json.dumps(tasks).encode()).decode()
                await websocket.send(encrypted_response)
            else:
                tasks.append(decrypted_message)
                encrypted_response = cipher.encrypt(json.dumps(tasks).encode()).decode()
                await websocket.send(encrypted_response)
        except Exception:
            await websocket.send(cipher.encrypt(json.dumps(["Invalid encryption!"]).encode()).decode())

async def websocket_server():
    server = await websockets.serve(handle_client, "127.0.0.1", 8000)
    await server.wait_closed()

def start_flask():
    app.run(host="127.0.0.1", port=5000)

@app.route("/")
def index():
    return render_template_string(HTML_PAGE, secret_key=SECRET_KEY)

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    asyncio.run(websocket_server())
