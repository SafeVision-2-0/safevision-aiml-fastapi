import supervision as sv
import numpy as np

class FaceTracker:
    def __init__(self):
        self.tracker = sv.ByteTrack()