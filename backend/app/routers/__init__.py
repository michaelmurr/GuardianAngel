from fastapi import APIRouter


from . import (
  websocket
)

router = APIRouter()

router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
