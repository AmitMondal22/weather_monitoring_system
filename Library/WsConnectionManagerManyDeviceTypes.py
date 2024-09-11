import json
from fastapi import WebSocket

class WsConnectionManagerManyDeviceTypes:
    """Class for managing WebSocket connections for multiple device types."""

    def __init__(self):
        # Initialize active connections without loading from a file.
        self.active_connections = {}

    async def connect(self, data_type: str, client_id: str, device_id: str, device: str, websocket: WebSocket):
        """Connect a new client."""
        user_id = f"{data_type}-{client_id}-{device_id}-{device}"
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, data_type: str, client_id: str, device_id: str, device: str):
        """Disconnect an existing client."""
        user_id = f"{data_type}-{client_id}-{device_id}-{device}"

        if user_id in self.active_connections:
            self.active_connections[user_id] = [conn for conn in self.active_connections[user_id] if conn != websocket]
            
            # Remove the user if no connections remain.
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            print(f"User {user_id} disconnected. Remaining connections: {len(self.active_connections.get(user_id, []))}")

    async def send_personal_message(self, data_type: str, client_id: str, device_id: str, device: str, message: str):
        """Send a message to a specific user identified by data_type, client_id, and device_id."""
        user_id = f"{data_type}-{client_id}-{device_id}-{device}"
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message)
            print(f"Message sent to {user_id}")
        else:
            print(f"User {user_id} not in active connections.")
