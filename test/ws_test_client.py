import cv2
import base64
import json
import asyncio
import websockets

async def test_ws():
    cap = cv2.VideoCapture(0)
    uri="ws://localhost:8000/ws/face-recognition/vggface2"
    # uri="ws://localhost:8000/ws/face-recognition/casia-webface"
    async with websockets.connect(uri,  max_size=10 * 1024 * 1024) as ws:
        print("Connected to ws")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                cv2.imshow("Client camera", frame)
                
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bs64 = base64.b64encode(buffer).decode()
                
                await ws.send(json.dumps({
                    "frame": frame_bs64
                }))
                
                response = await ws.recv()
                print(response)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Exit by user")
                    break
                
                await asyncio.sleep(0.03)
        except websockets.ConnectionClosed:
            print("WebSocket closed by server")
    
    cap.release()
    cv2.destroyAllWindows()
    
asyncio.run(test_ws())
