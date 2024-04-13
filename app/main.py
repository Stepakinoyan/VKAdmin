from fastapi import FastAPI
from app.auth.router import router as router_auth
from app.organizations.router import router as router_filter
from app.excel_to_db.router import router as router_excel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

<<<<<<< HEAD
origins = ["http://localhost:5468"]
=======
origins = ["http://localhost:5173"]
>>>>>>> 2f21a14af65e5a7730bdb4566ffe116e3753c460

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
