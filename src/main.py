from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.config.database import mongodb_database
from src.app.routes.auth_route import auth_router
from src.app.routes.products_route import products_router
import uvicorn

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    mongodb_database.connect()

    yield
    
    mongodb_database.disconnect()
    

app = FastAPI(lifespan= db_lifespan)
app.include_router(auth_router)
app.include_router(products_router)

