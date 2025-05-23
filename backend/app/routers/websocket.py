from dependencies import db_dependency, verify_token_ws
from fastapi import APIRouter, Depends, WebSocket

from app.websocket.connection_manager import ConnectionManager, get_connection_manager
from app.websocket.websocket_connection import WebSocketMetaData

router = APIRouter()


@router.websocket("/live")
async def handle_live_connection(
    ws: WebSocket,
    db: db_dependency,
    connection_manager: ConnectionManager = Depends(get_connection_manager),
):
    token = ws.query_params.get("token")
    device_id = ws.query_params.get("device_id")
    user_id = await verify_token_ws(token, db)
    metadata = WebSocketMetaData(user_id, device_id)

    await connection_manager.handle_connection(ws, metadata)
