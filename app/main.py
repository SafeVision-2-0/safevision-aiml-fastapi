from fastapi import FastAPI
# from app.routes.face_embedding_routes import router as face_embedding_router
from app.routes.face_recognition_routes import router as face_recognition_router

app = FastAPI()

# app.include_router(face_embedding_router)
app.include_router(face_recognition_router)