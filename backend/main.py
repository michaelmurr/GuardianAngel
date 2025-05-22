from fastapi import FastAPI
from database import Base, engine
from app.routers import router


app = FastAPI()

## binding the database and models from alchemy/ submodule
Base.metadata.create_all(bind=engine)


app.include_router(router)