from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlmodel import Session
from pathlib import Path
import os

from app.routes.face_embedding_routes import router as face_embedding_router
from app.routes.face_recognition_routes import router as face_recognition_router

from app.db.session import get_session, create_db_and_tables

SessionDep = Annotated[Session, Depends(get_session)]

# Ini debug
BASE_DIR = Path(__file__).resolve().parent
PICTURE_DIR = BASE_DIR / "picture"

app = FastAPI()

# Ini debug
app.mount(
    "/picture",
    StaticFiles(directory=PICTURE_DIR),
    name="picture"
)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


app.include_router(face_embedding_router)
app.include_router(face_recognition_router)