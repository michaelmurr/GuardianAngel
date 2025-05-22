from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]


    async def handle_connection(self, ws: WebSocket, jwt: str):
        await ws.accept()
        
        while True:
            try:
                data = await ws.receive_text()
                print(f"Received data: {data}")
            except Exception as e:
                print(f"Error: {e}")
                break
            
CONNECTION_MANAGER = ConnectionManager()

def get_connection_manager():
    return CONNECTION_MANAGER
