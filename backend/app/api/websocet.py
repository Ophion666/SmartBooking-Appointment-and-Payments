from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.connection_manager import manager
router = APIRouter()

@router.websocket("/ws/slots/{master_id}/{date}")
async def slots_websocket(websocket: WebSocket, master_id: int, date: str):
    room = f"{master_id}_{date}"
    await manager.connect(websocket, room)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)




