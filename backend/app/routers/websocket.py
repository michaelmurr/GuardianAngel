from fastapi import APIRouter, Depends, WebSocket

from app.websocket.connection_manager import ConnectionManager, get_connection_manager

router = APIRouter()


@router.websocket("/live")
async def handle_live_connection(
    ws: WebSocket,
    connection_manager: ConnectionManager = Depends(get_connection_manager),
):
    token = ws.query_params.get("token")
    # TODO check against clerk if token is valid and get user_id
    print(f"Token: {token}")
    user_id = "bla"
    await connection_manager.handle_connection(ws, user_id)
