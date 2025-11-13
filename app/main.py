from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import app.routes as routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all domains
    allow_credentials=True,
    allow_methods=["*"],      # GET, POST, OPTIONS, etc.
    allow_headers=["*"],      # allow all headers
)

app.include_router(routes.router)