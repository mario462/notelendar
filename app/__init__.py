from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine

from app.models.note import Note  # noqa

# initialize APP
APP = FastAPI()
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize DB ENGINE
SQLITE_FILENAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILENAME}"
ENGINE = create_engine(SQLITE_URL, echo=True)
SQLModel.metadata.create_all(ENGINE)
