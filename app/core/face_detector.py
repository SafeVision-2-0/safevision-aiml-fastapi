from facenet_pytorch import MTCNN
import torch

class FaceDetector:
    def __init__(self, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60):
        self.mtcnn = MTCNN(
            keep_all=keep_all,
            thresholds=thresholds,
            min_face_size=min_face_size
        )
        
    def detect_box(self, rgb_img):
        # boxes, _ = self.mtcnn.detect(rgb_img)
        # faces = self.mtcnn(rgb_img)
        # return boxes, faces
        try:
            boxes, _ = self.mtcnn.detect(rgb_img)
            if boxes is None or len(boxes) == 0:
                return None, None

            faces = self.mtcnn(rgb_img)
            if faces is None or (isinstance(faces, torch.Tensor) and faces.numel() == 0):
                return None, None

            return boxes, faces

        except Exception as e:
            print(f"Face detection error: {e}")
            return None, None