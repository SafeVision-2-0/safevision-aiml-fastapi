from facenet_pytorch import InceptionResnetV1
import torch

class FaceEncoder:
    def __init__(self, model_pretrained="casia-webface"):
        self.model = InceptionResnetV1(pretrained=model_pretrained).eval()

    @torch.no_grad()
    def encode(self, face_tensor):
        if face_tensor.ndim == 3:
            face_tensor = face_tensor.unsqueeze(0)
        return self.model(face_tensor)[0]