import numpy as np
import cv2
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN

mtcnn = MTCNN(
    keep_all=True,
    thresholds=[0.4, 0.5, 0.5],
    min_face_size=60
)

resnet = InceptionResnetV1(pretrained='casia-webface').eval()

def extract_embedding(image_path: str) -> np.ndarray | None:
    """
    Load image, detect face, return embedding
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = mtcnn(img)
    
    # Untuk memastikan bahwa hanya ada 1 wajah di foto
    if faces is None or faces.shape[0] != 1:    
        return None
    
    # Menambah batch karena pytorch butuh [BATCH, CHANNEL, HEIGHT, WIDTH]
    # Sedangkan kalau 1 wajah cuman ada [CHANNEL, HEIGHT, WIDTH]
    face = faces[0].unsqueeze(0)

    with torch.no_grad():
        emb = resnet(face)
        
    return emb.squeeze(0).cpu().numpy()