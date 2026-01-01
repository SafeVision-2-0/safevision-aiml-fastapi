import os
import cv2
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from tqdm import tqdm
from types import MethodType
# from face_tracking import FaceTracking


class FaceRecognize:
    def __init__(self, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60):
        self.mtcnn = MTCNN(
            keep_all=keep_all,
            thresholds=thresholds,
            min_face_size=min_face_size
        )
        self.resnet = InceptionResnetV1(pretrained='casia-webface').eval()
        self.keep_all = keep_all
        self.tracker = FaceTracking()
        self.saved_picture = "./picture/"
        self.all_people_faces = {}

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

            emb = self.resnet(face)
            self.all_people_faces[person_name] = emb[0]

        print("Selesai load gambar.")
        print("Jumlah orang tersimpan:", len(self.all_people_faces))

    def detect(self, cam=0, thres=0.9):
        video = cv2.VideoCapture(cam)

        while True:
            ret, img0 = video.read()
            if not ret:
                break

            rgb = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
            boxes, faces = self.detect_box_faces(rgb) 
            
            if faces is not None and boxes is not None:
                for box, face_tensor in zip(boxes, faces):
                    x, y, x2, y2 = map(int, box)

                    img_embedding = self.encode(face_tensor)
                    distances = {
                        name: torch.dist(img_embedding, saved_emb).item()
                        for name, saved_emb in self.all_people_faces.items()
                    }

                    min_name = min(distances, key=distances.get)
                    min_dist = distances[min_name]

                    if min_dist > thres:
                        min_name = "Unknown"

                    cv2.rectangle(img0, (x, y), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(
                        img0,
                        f"{min_name} ({min_dist})",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.6,
                        (255, 255, 255)
                    )

            cv2.imshow("Face Recognition: ", img0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    face = FaceRecognize()
    face.read_images()
    face.detect(0)
