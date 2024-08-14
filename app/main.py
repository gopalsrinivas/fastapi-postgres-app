import logging
from fastapi import FastAPI, Request
from app import models
from app.database import engine
from app.routers import items
from fastapi.responses import JSONResponse
import asyncio

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(items.router, prefix="/items", tags=["items"])


@app.on_event("startup")
async def on_startup():
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database tables created.")


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "details": str(exc)},
    )
