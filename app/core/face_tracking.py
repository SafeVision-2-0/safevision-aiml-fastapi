import supervision as sv
import numpy as np

class FaceTracker:
    def __init__(self):
        self.tracker = sv.ByteTrack()
        
    def to_detections(self, boxes):
        boxes = np.array(boxes, dtype=np.float32)
        
        return sv.Detections(
            xyxy=boxes,
            confidence=np.ones(len(boxes), dtype=np.float32),
            class_id=np.zeros(len(boxes), dtype=np.int32)
        )
        
    def update(self, boxes):
        detections = self.to_detections(boxes)
        return self.tracker.update_with_detections(detections)