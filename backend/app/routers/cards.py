

from datetime import datetime, timezone
from typing import Annotated, List
from fastapi import APIRouter, Depends

from dependencies import get_current_user
import models.pyd.game_card as py_model
import models.alchemy.game_card as db_model
from models.pyd.user import UserInDB
from dependencies import db_dependency

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add", response_model=py_model.HostedGame)
async def addGame(current_user: Annotated[UserInDB, Depends(get_current_user)], db: db_dependency, game: py_model.HostedGame):
       db_hosted_game = db_model.HostedGame(title=game.title, startDate=datetime.now(timezone.utc), isActive=game.isActive, host=current_user.id)
       db.add(db_hosted_game)
       db.commit()
       db.refresh(db_hosted_game)
       return  db_hosted_game


@router.get("/get_all", response_model=List[py_model.HostedGame])
async def getHostedGames(current_user: Annotated[UserInDB, Depends(get_current_user)], db: db_dependency):
       return db.query(db_model.HostedGame).filter(db_model.HostedGame.host == current_user.id).all()