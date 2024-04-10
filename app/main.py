from fastapi import FastAPI
from app.auth.router import router as router_auth
from app.organizations.router import router as router_filter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5468",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_filter)


            # location / {
            #     proxy_set_header Host $http_host;
            #     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            #     proxy_set_header X-Forwarded-Proto $scheme;
            #     proxy_set_header Upgrade $http_upgrade;
            #     proxy_redirect off;
            #     proxy_buffering off;
            #     proxy_pass http://api:4444/;
            # },