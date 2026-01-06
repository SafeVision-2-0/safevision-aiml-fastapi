import cv2
import torch
import os

from sqlmodel import Session, select
from app.models.user_model import User
from app.models.user_image_model import UserImage
from app.models.face_embedding_model import FaceEmbedding

from app.core.face_detector import FaceDetector
from app.core.face_encoder import FaceEncoder
from app.core.face_tracking import FaceTracker

class FaceRecognitionService:
    def __init__(self, known_faces_dir="./picture/"):
        self.detector= FaceDetector()
        self.encoder = FaceEncoder()
        self.tracker = FaceTracker()
        
        self.identity_map = {}
        self.known_faces = {}
        self.frame_count = 0
        
        self._load_known_faces_from_folder(known_faces_dir)

    def _load_known_faces_from_folder(self, root_dir):
        for person in os.listdir(root_dir):
            person_dir = os.path.join(root_dir, person)
            if not os.path.isdir(person_dir):
                continue

            for file in os.listdir(person_dir):
                if not file.lower().endswith((".jpg", ".png", ".jpeg")):
                    continue

                img = cv2.imread(os.path.join(person_dir, file))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                boxes, faces = self.detector.detect(img)
                if faces is None:
                    continue

                emb = self.encoder.encode(faces[0])
                self.known_faces.setdefault(person, []).append(emb)

        print("Loaded known faces:", len(self.known_faces))
        
    def _load_known_faces_from_db(self, session: Session):
        """
        Load face embeddings from database and store them in memory
        as { user_name: embedding_tensor }
        """
        statement = (
            select(User.name, FaceEmbedding.vector)
            .join(UserImage, User.id == UserImage.user_id)
            .join(FaceEmbedding, UserImage.id == FaceEmbedding.user_image_id)
        )
        
        results = session.exec(statement).all()
        
        for name, vector in results:
            self.known_faces[name] = torch.tensor(
                vector, dtype=torch.float32
            )
        
        print(f"Loaded {len(self.known_faces)} known face embeddings")
        
    def process_frame(self, frame, threshold=0.7):
        self.frame_count += 1
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, faces = self.detector.detect_box(rgb)
        if boxes is None or faces is None:
            return []
        
        tracked = self.tracker.update(boxes)
        results = []
        
        for i, track_id in enumerate(tracked.tracker_id):
            face_emb = self.encoder.encode(faces[i])
            
            if track_id in self.identity_map:
                name = self.identity_map[track_id]["name"]
                self.identity_map[track_id]["last_seen"] = self.frame_count
            else:
                distances = {
                    k: torch.dist(face_emb, v).item()
                    for k, v in self.known_faces.items()
                }
                
                if distances:
                    min_name = min(distances, key=distances.get)
                    if distances[min_name] < threshold:
                        name = min_name
                        self.identity_map[track_id] = {
                            "name" : name,
                            "last_seen" : self.frame_count
                        }
                    else:
                        name = "Unknown"   
                else:
                    name = "Unknown"
                    
            x1, y1, x2, y2 = tracked.xyxy[i]
            results.append({
                "track_id": int(track_id),
                "name": name,
                "bbox": [
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ]
            })
            
        self.identity_map = {
            k: v for k, v in self.identity_map.items()
            if self.frame_count - v["last_seen"] < 30
        }
        
        return results