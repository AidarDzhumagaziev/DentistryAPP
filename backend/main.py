import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
