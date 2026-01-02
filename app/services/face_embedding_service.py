from sqlmodel import Session, select
from app.models.user_image_model import UserImage
from app.models.face_embedding_model import FaceEmbedding
from app.core.face_model import extract_embedding

def run_face_embedding_pipeline(session: Session):
    """
    Pipeline:
    1. ambil semua image
    2. generate embedding
    3. simpan ke database
    """
    images = session.exec(
        select(UserImage)
        .where(
            UserImage.id.not_in(
                select(FaceEmbedding.user_image_id)
            )
        )
    ).all()
    
    if not images:
        return {"message": "Images not found"}
    
    for img in images:
        embedding = extract_embedding(img.image_path)
        
        if embedding is None:
            continue
        
        face_embedding = FaceEmbedding(
            user_image_id=img.id,
            vector=embedding.tolist()
        )
        
        session.add(face_embedding)
        
    session.commit()
    
    return {"message": "Embedding pipeline finished"}