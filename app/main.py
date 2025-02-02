from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from rich.console import Console

from app.auth.router import router as router_auth
from app.config import settings
from app.excel_to_db.router import router as router_excel
from app.organizations.router import router as router_filter
from app.vk.router import router as vk_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    console.rule("[bold white on blue] STARTUP ")
    pattern = "*"
    cursor = "0"
    while cursor != "0":
        cursor, keys = await redis_.scan(cursor, match=pattern)
        for key in keys:
            print(key)

    FastAPICache.init(RedisBackend(redis_), prefix="fastapi-cache")

    yield


app = FastAPI(
    lifespan=lifespan,
    root_path="/api"
)

console = Console(color_system="truecolor", width=140)
redis_ = redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=5,
    socket_keepalive=True,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS.split(",")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_auth)
app.include_router(router_filter)
app.include_router(router_excel)
app.include_router(vk_router)
