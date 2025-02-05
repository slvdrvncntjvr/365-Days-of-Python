import asyncio
import websockets
from flask import Flask
from cryptography.fernet import Fernet
import threading


SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebSocket Chat</title>
        <script>
            let ws = new WebSocket("ws://127.0.0.1:8000/ws");

            ws.onmessage = (event) => {
                let messageBox = document.getElementById("messages");
                messageBox.innerHTML += "<p><b>Server:</b> " + event.data + "</p>";
            };

            function sendMessage() {
                let input = document.getElementById("messageInput").value;
                ws.send(input);
                document.getElementById("messages").innerHTML += "<p><b>You:</b> " + input + "</p>";
                document.getElementById("messageInput").value = "";
            }
        </script>
    </head>
    <body>
        <h2>WebSocket Chat</h2>
        <div id="messages"></div>
        <input type="text" id="messageInput" placeholder="Type a message">
        <button onclick="sendMessage()">Send</button>
    </body>
    </html>
    """

async def handle_client(websocket, path):
    try:
        async for message in websocket:
            encrypted_message = cipher.encrypt(message.encode())
            decrypted_message = cipher.decrypt(encrypted_message).decode()
            print(f"Received: {decrypted_message}")

            await websocket.send(f"Encrypted: {encrypted_message.decode()} | Decrypted: {decrypted_message}")
    except Exception as e:
        print("Connection error:", e)

async def websocket_server():
    async with websockets.serve(handle_client, "127.0.0.1", 8000):
        await asyncio.Future() 

def run_flask():
    app.run("127.0.0.1", 5000, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(websocket_server())
