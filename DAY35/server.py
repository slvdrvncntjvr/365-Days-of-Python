import asyncio
import websockets
from cryptography.fernet import Fernet

# 🔑 Use the SAME key for both server and client
SECRET_KEY = b'_PF_42Uu7dKlQnfphgaVCKp9Fd_b32JZJ2ti337E5PY='
cipher = Fernet(SECRET_KEY)

connected_clients = set()

async def handle_client(websocket, path):
    """ Handles WebSocket connections """
    connected_clients.add(websocket)
    try:
        async for encrypted_message in websocket:
            print(f"Received Encrypted: {encrypted_message}")  # Debugging
            
            try:
                decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
                print(f"Decrypted Message: {decrypted_message}")

                # Encrypt response before sending
                encrypted_response = cipher.encrypt(f"Server received: {decrypted_message}".encode()).decode()
                await websocket.send(encrypted_response)

            except Exception as e:
                print(f"Decryption failed: {e}")
                await websocket.send("Invalid encryption!")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    finally:
        connected_clients.remove(websocket)

async def main():
    """ Starts the WebSocket server """
    server = await websockets.serve(handle_client, "127.0.0.1", 8000)
    print("WebSocket server started at ws://127.0.0.1:8000")
    await server.wait_closed()

asyncio.run(main())
