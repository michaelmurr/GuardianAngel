from fastapi import FastAPI
from database import Base, engine
from routers import auth, cards, users

app = FastAPI()

## binding the database and models from alchemy/ submodule
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(cards.router)
app.include_router(auth.router)


