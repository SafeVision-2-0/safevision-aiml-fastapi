# import numpy as np
# import 

# class FaceTracking:
#     def __init__(self):
        
        
#     def update(self, detections, img_shape):
#         """
#         detections: list of [x1, y1, x2, y2, score]
#         """
#         if len(detections) == 0:
#             dets = np.empty((0,6))
#         else:
#             dets = np.array([det + [0] for det in detections], dtype=np.float32)
        
#         h, w = img_shape[:2]
#         tracks = self.tracker.update(dets, img=(h,w))
#         return tracks