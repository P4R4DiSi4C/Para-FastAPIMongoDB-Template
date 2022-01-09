import uvicorn
from fastapi import FastAPI
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from routers.restaurant import router as restaurant_router

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.db_url)
    app.mongodb = app.mongodb_client[settings.db_name]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(restaurant_router, tags=[
                   "restaurants"], prefix="/restaurant")

# entry point
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        reload=settings.debug_mode,
        port=settings.port,
    )
