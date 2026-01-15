import cv2
import torch
import os
import json

from sqlmodel import Session, select
from app.models.profile_model import Profile
from app.models.profile_image_model import ProfileImage
from app.models.face_embedding_model import FaceEmbedding

from app.core.face_detector import FaceDetector
from app.core.face_encoder import FaceEncoder
from app.core.face_tracking import FaceTracker

class FaceRecognitionService:
    def __init__(self, session: Session, model_name: str):
        self.detector= FaceDetector()
        self.encoder = FaceEncoder(model_pretrained=model_name)
        self.tracker = FaceTracker()
        self.model_name = model_name
        
        self.identity_map = {}
        self.known_faces = {}
        self.frame_count = 0
        
        self._load_known_faces_from_db(session)

    # DEBUG
    def _load_known_faces_from_folder(self, root_dir):
        for file in os.listdir(root_dir):
            if not file.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            name = file.split("_")[0]  # ikram_1.jpg → ikram

            img_path = os.path.join(root_dir, file)
            img = cv2.imread(img_path)
            if img is None:
                continue

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes, faces = self.detector.detect_box(img)

            if faces is None:
                continue

            emb = self.encoder.encode(faces[0])
            self.known_faces.setdefault(name, []).append(emb)

        print("Loaded known faces:", len(self.known_faces))
        
    def _load_known_faces_from_db(self, session: Session):
        """
        Load face embeddings from database and store them in memory
        as { user_name: embedding_tensor }
        """
        if self.model_name == "casia-webface":
            vector_column = FaceEmbedding.vector_casia
        else:
            vector_column = FaceEmbedding.vector_vgg
            
        statement = (
            select(Profile.id, Profile.name, vector_column)
            .join(ProfileImage, Profile.id == ProfileImage.profile_id)
            .join(FaceEmbedding, ProfileImage.id == FaceEmbedding.profile_image_id)
        )
        
        results = session.exec(statement=statement).all()
        
        for profile_id, name, vector in results:
            emb = torch.tensor(vector, dtype=torch.float32)
            if profile_id not in self.known_faces:
                self.known_faces[profile_id] = {
                    "name": name,
                    "embeddings": []
                }
            
            self.known_faces[profile_id]["embeddings"].append(emb)
        
        print(f"Loaded {sum(len(v['embeddings']) for v in self.known_faces.values())} known face embeddings {vector_column}")
        
    def process_frame(self, frame):
        self.frame_count += 1
        
        if self.model_name == "casia-webface":
            threshold = 0.9
        else:
            threshold = 0.9
        
        scale = 0.5
        small = cv2.resize(frame, None, fx=scale, fy=scale)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        boxes, faces = self.detector.detect_box(rgb)
        
        if boxes is None or faces is None:
            return []
        
        boxes = boxes / scale
        faces = faces / scale
        
        tracked = self.tracker.update(boxes)
        results = []
        
        for i, track_id in enumerate(tracked.tracker_id):
            if track_id in self.identity_map:
                identity = self.identity_map[track_id]
                identity["last_seen"] = self.frame_count
            else:
                face_emb = self.encoder.encode(faces[i])
                
                distances = {}
                
                for profile_id, data in self.known_faces.items():
                    dists = [
                        torch.dist(face_emb, emb).item()
                        for emb in data["embeddings"]
                    ]
                    distances[profile_id] = min(dists)
                
                if distances:
                    best_id = min(distances, key=distances.get)
                    if distances[best_id] < threshold:
                        identity = {
                            "profile_id": best_id,
                            "name": self.known_faces[best_id]["name"]
                        }
                        self.identity_map[track_id] = {
                            **identity,
                            "last_seen" : self.frame_count
                        }
                    else:
                        identity = {"profile_id": None, "name": "Unknown"}   
                else:
                    identity = {"profile_id": None, "name": "Unknown"}
                    
            x1, y1, x2, y2 = tracked.xyxy[i]
            results.append({
                "track_id": int(track_id),
                "profile_id": identity["profile_id"],
                "name": identity["name"],
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
    