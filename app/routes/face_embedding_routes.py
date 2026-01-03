from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.services.face_embedding_service import run_face_embedding_pipeline

router = APIRouter(
    prefix="/face-embedding",
    tags=["Face Embedding"]
)

@router.post("/run")
def run_embedding_pipeline(
    session: Session = Depends(get_session)
):
    """
    Trigger face embedding pipeline:
    - Ambil image yang belum punya embedding
    - Generate embedding
    - Simpan ke database
    """
    result = run_face_embedding_pipeline(session)
    return result