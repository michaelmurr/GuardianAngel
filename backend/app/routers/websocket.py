from fastapi import APIRouter, Depends, WebSocket

from app.websocket.connection_manager import ConnectionManager, get_connection_manager
from dependencies import verify_token_ws

router = APIRouter()


@router.websocket("/live")
async def handle_live_connection(
    ws: WebSocket,
    connection_manager: ConnectionManager = Depends(get_connection_manager),
):
    token = ws.query_params.get("token")
    # TODO check against clerk if token is valid and get user_id
    print(f"Token: {token}")
    user_id = verify_token_ws(token)
    print(f"UserId: {user_id}")
    await connection_manager.handle_connection(ws, user_id)
