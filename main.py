from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.controllers.routes import api
from src import constants


app = FastAPI()

# add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=constants.ALLOWED_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api, prefix="/api")
