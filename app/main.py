from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.console import Console

from app.auth.router import router as router_auth
from app.config import settings
from app.excel_to_db.router import router as router_excel
from app.organizations.router import router as router_filter
from app.vk.router import router as vk_router


app = FastAPI(root_path="/api")

console = Console(color_system="truecolor", width=140)


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
