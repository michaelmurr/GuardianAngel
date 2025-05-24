import threading
from contextlib import asynccontextmanager

from app.routers import router
from app.services.websocket_manager import get_websocket_manager
from database import Base, engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    wm = get_websocket_manager()
    thread = threading.Thread(target=wm.start, daemon=True)
    thread.start()
    yield
    thread.join(timeout=1)


app = FastAPI(lifespan=lifespan)


Base.metadata.create_all(bind=engine)


app.include_router(router)
