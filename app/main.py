from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session

from app.routes.face_embedding_routes import router as face_embedding_router
from app.routes.face_recognition_routes import router as face_recognition_router

from app.db.session import get_session, create_db_and_tables

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(face_embedding_router)
app.include_router(face_recognition_router)