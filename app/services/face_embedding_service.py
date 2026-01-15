from sqlmodel import Session, select
from app.models.profile_image_model import ProfileImage
from app.models.face_embedding_model import FaceEmbedding
from app.core.face_model import extract_embedding
from app.core.config import settings
import numpy as np
import requests
import tempfile
import os

def run_face_embedding_pipeline(session: Session):
    """
    Pipeline:
    1. ambil semua image
    2. generate embedding
    3. simpan ke database
    """
    images = session.exec(
        select(ProfileImage)
        .where(
            ProfileImage.id.not_in(
                select(FaceEmbedding.profile_image_id)
            )
        )
    ).all()
    
    if not images:
        return {"message": "Images not found"}
    
    for img in images:
        # print("DEBUG: image_id => ", img.id)
        BASE_URL = settings.EXPRESS_API_URL 
        img_url = f"{BASE_URL}/{img.image}"
        embedding_casia = extract_embedding_from_url("casia-webface", img_url)
        if embedding_casia is None:
            continue
        
        embedding_vgg = extract_embedding_from_url("vggface2", img_url)
        if embedding_vgg is None:
            continue
        
        face_embedding = FaceEmbedding(
            profile_image_id=img.id,
            vector_casia=embedding_casia.tolist(),
            vector_vgg=embedding_vgg.tolist()
        )
        
        session.add(face_embedding)
        
    session.commit()
    
    return {"message": "Embedding pipeline finished"}

def extract_embedding_from_url(resnet: str, image_url: str) -> np.ndarray | None:
    resp = requests.get(image_url, timeout=10)
    if resp.status_code != 200:
        return None
    
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        f.write(resp.content)
        temp_path = f.name
        
    try:
        return extract_embedding(resnet, temp_path)
    finally:
        os.remove(temp_path)