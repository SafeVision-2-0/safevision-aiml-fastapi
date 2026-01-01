import os
import cv2
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import supervision as sv
import numpy as np

class FaceRecognize:
    def __init__(self, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60):
        self.mtcnn = MTCNN(
            keep_all=keep_all,
            thresholds=thresholds,
            min_face_size=min_face_size
        )
        self.resnet = InceptionResnetV1(pretrained='casia-webface').eval()
        self.keep_all = keep_all
        self.saved_picture = "./picture/"
        self.all_people_faces = {}
        self.tracker = sv.ByteTrack()
        self.identity_map = {}
        self.frame_count = 0      

    def to_detections(self, boxes):
        boxes = np.array(boxes, dtype=np.float32)
        
        return sv.Detections(
            xyxy=boxes,
            confidence=np.ones(len(boxes), dtype=np.float32),
            class_id=np.zeros(len(boxes), dtype=np.int32)
        )

    def encode(self, face_tensor):
        if face_tensor.ndim == 3:
            face_tensor = face_tensor.unsqueeze(0)

        with torch.no_grad():
            emb = self.resnet(face_tensor)

        return emb[0]

    def detect_box_faces(self, img):
        boxes, _ = self.mtcnn.detect(img)
        faces = self.mtcnn(img)
        return boxes, faces

    def read_images(self):
        print("Loading saved face images...")

        for file in os.listdir(self.saved_picture):
            person_name, ext = os.path.splitext(file)

            if ext.lower() not in [".jpg", ".png", ".jpeg"]:
                continue

            path = os.path.join(self.saved_picture, file)
            img = cv2.imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            face = self.mtcnn(img)
            if face is None:
                print(f"Wajah tidak ditemukan di: {file}")
                continue

            with torch.no_grad():
                emb = self.resnet(face)
                
            self.all_people_faces[person_name] = emb[0]

        print("Selesai load gambar.")
        print("Jumlah orang tersimpan:", len(self.all_people_faces))

    def detect(self, cam=0, thres=0.7):
        WINDOW_NAME = "Face Recognition"
        video = cv2.VideoCapture(cam)

        while True:
            self.frame_count += 1
            ret, img0 = video.read()
            if not ret:
                break

            rgb = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
            boxes, faces = self.detect_box_faces(rgb) 
            
            
            if boxes is None or faces is None:
                cv2.imshow(WINDOW_NAME, img0)
                continue
            
            detections = self.to_detections(boxes)
            tracked = self.tracker.update_with_detections(detections)
            
            if tracked.xyxy is None:
                cv2.imshow(WINDOW_NAME, img0)
                continue
            
            for i in range(len(tracked.xyxy)):    
                x, y, x2, y2 = tracked.xyxy[i].astype(int)
                track_id = tracked.tracker_id[i]
                face_tensor = faces[i]
                    
                if track_id in self.identity_map:
                    name = self.identity_map[track_id]["name"]
                    self.identity_map[track_id]["last_seen"] = self.frame_count
                    
                else:
                    img_embedding = self.encode(face_tensor)
                        
                    distances = {
                        name: torch.dist(img_embedding, saved_emb).item()
                        for name, saved_emb in self.all_people_faces.items()
                    }

                    min_name = min(distances, key=distances.get)
                    min_dist = distances[min_name]

                    if min_dist < thres:
                        name = min_name
                        self.identity_map[track_id] = {
                            "name" : name,
                            "last_seen" : self.frame_count
                        }
                    else:
                        name = "Unknown"

                cv2.rectangle(img0, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(
                    img0,
                    f"{name} | {track_id}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.6,
                    (255, 255, 255)
                )

            for tid in list(self.identity_map.keys()):
                if self.frame_count - self.identity_map[tid]["last_seen"] > 60:
                    del self.identity_map[tid]
            
            cv2.imshow(WINDOW_NAME, img0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    face = FaceRecognize()
    face.read_images()
    face.detect(0)
