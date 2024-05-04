from fastapi import FastAPI
from app.auth.router import router as router_auth
from app.organizations.router import router as router_filter
from app.excel_to_db.router import router as router_excel
from fastapi.middleware.cors import CORSMiddleware
from rich.console import Console
import redis.asyncio as redis
from app.config import settings
from app.vk.router import router as vk_router 


app = FastAPI()
console = Console(color_system="truecolor", width=140)
redis_ = redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf-8", decode_responses=True, socket_timeout=5, socket_keepalive=True)
async def startup(_: FastAPI = app) -> None:
    console.rule("[bold white on blue] STARTUP ")
    pattern = f"*"
    cursor = '0'
    records = []
    while cursor != 0:
        cursor, keys = await redis_.scan(cursor, match=pattern)
        for key in keys:
            print(key)


origins = ["http://localhost:5468", "http://localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_filter)
app.include_router(router_excel)
app.include_router(vk_router)
app.add_event_handler("startup", startup)