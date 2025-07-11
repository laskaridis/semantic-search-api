from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import index, search, collections
import app.logging  as logging

logging.init()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(search.router)
app.include_router(index.router)
app.include_router(collections.router)


