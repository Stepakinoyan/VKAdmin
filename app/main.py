from fastapi import FastAPI
from app.auth.router import router as router_auth
from app.organizations.router import router as router_filter
from app.excel_to_db.router import router as router_excel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://78.24.216.129:5468", "http://localhost:5173"]

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
