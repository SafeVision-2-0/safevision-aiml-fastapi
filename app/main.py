from fastapi import FastAPI
from app.routes.face_embedding_routes import router as face_embedding_router

app = FastAPI()

app.include_router(face_embedding_router)