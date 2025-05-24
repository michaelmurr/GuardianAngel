from app.routers import router
from database import Base, engine
from fastapi import FastAPI

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(router)
