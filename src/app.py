import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import setting
from src.core.redis import get_redis, close_redis
from src.core.log import AppServerLog

logging.config.dictConfig(AppServerLog)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_redis()
    yield
    await close_redis()
    

app = FastAPI(
    root_path=setting.ROUTES_PREFIX, 
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

# v1 routers
from src.auth.routes.v1.api import router as v1_auth_router
from src.user.routes.v1.api import router as v1_user_router

v1_prefix = "/v1"
v1_routers = (
    v1_auth_router,
    v1_user_router
)
for router in v1_routers:
    app.include_router(router, prefix=v1_prefix)

