
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import setting
from src.core.postgres_db import init_postdb

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_postdb()
    yield
    
app = FastAPI(root_path=setting.ROUTES_PREFIX, 
    swagger_ui_parameters={"filter": True},
    lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
