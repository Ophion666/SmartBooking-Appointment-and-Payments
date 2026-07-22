from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as aioredis
import json
import os

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room]= []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        self.active_connections[room].remove(websocket)
        if not self.active_connections[room]:
            del self.active_connections[room]

    async def broadcast(self, room: str, message: str):
        connections = self.active_connections.get(room, [])
        for connection in connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def redis_listener():
    redis_url = os.getenv("REDIS_URL")
    redis = aioredis.from_url(redis_url)
    pubsub = redis.pubsub()
    await pubsub.subscribe("slots_updates")

    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            await manager.broadcast(data["room"], data["message"])