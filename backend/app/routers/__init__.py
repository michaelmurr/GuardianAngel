
from fastapi import APIRouter


from . import (
  websocket,
  users
)

router = APIRouter()

router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
router.include_router(users.router, prefix="/users", tags=["users"])
