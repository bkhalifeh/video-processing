from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from aiofiles import os as async_os

from .core.settings import settings
from .routes import router


@asynccontextmanager
async def lifespan_impl(app: FastAPI):
    for dir_path in [settings.videos_path, settings.frames_path]:
        if not (await async_os.path.isdir(dir_path)):
            await async_os.makedirs(dir_path)
    yield


app = FastAPI(
    lifespan=lifespan_impl,
    debug=settings.app.debug,
    default_response_class=ORJSONResponse,
)
app.include_router(router)
