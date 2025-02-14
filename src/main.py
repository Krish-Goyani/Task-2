from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.config.database import mongodb_database
from src.app.routes.auth_route import auth_router
from src.app.routes.products_route import products_router
from src.app.routes.complaints_rote import complaints_router
from src.app.routes.cart_and_orders_route import cart_and_orders_router
import uvicorn
import uvloop
import asyncio

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    mongodb_database.connect()

    yield
    
    mongodb_database.disconnect()
    

app = FastAPI(lifespan= db_lifespan)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_and_orders_router)
app.include_router(complaints_router)

