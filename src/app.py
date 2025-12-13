from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import setting
    


app = FastAPI(
    root_path=setting.ROUTES_PREFIX, 
    swagger_ui_parameters={"filter": True}
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
