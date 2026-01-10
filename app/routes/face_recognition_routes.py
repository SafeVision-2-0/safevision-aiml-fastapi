import cv2
import base64
import numpy as np
from fastapi import WebSocket, APIRouter

# from app.db.session import get_session
from app.services.face_recognition_service import FaceRecognitionService

router = APIRouter()
service = FaceRecognitionService()

@router.websocket("/ws/face-recognition")
async def face_ws(ws: WebSocket):
    await ws.accept()
    
    try:
        while True:
            # Receive frame from Front-End
            data = await ws.receive_json()
            frame_bs64 = data["frame"]
            
            # Decode base64 -> OpenCV Image
            img_bytes = base64.b64decode(frame_bs64)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if frame is None:
                continue
            
            # Run Face Recognition
            results = service.process_frame(frame)
            
            # Send Metadata back
            await ws.send_json({
                "detections": results
            })
    except Exception as e:
        print("websocket error: ", e) 
    # finally:
        # await ws.close()