from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as router_auth
from app.config import settings
from app.excel_to_db.router import router as router_excel
from app.organizations.router import router as router_filter
from app.vk.router import router as vk_router


app = FastAPI(root_path="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_HOST],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_auth)
app.include_router(router_filter)
app.include_router(router_excel)
app.include_router(vk_router)
