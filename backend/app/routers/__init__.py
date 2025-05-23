
from fastapi import APIRouter


from . import (
  websocket,
  users,
  friends,
  people
)

router = APIRouter()

router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(friends.router, prefix="/friends", tags=["friends"])
router.include_router(people.router, prefix="/people", tags=["people"])