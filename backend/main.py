import logging

import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.db_helper import db_helper

from api import router as api_router
from core.logging import setup_logging

setup_logging(log_file="logs/logger.logs", level=logging.DEBUG)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router, prefix=settings.api.prefix)


@main_app.get("/")
def hello_index():
    return {"message": "Hello!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
