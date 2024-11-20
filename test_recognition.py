import os
import cv2 as cv
from google.cloud import vision_v1p3beta1 as vision
from threading import Thread, Lock
from queue import Queue
import time
from rec import food_scan
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'
#client = vision.ImageAnnotatorClient()

showable_label = "Loading..."
lock = Lock()
frame_queue = Queue(maxsize=1)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'
client=vision.ImageAnnotatorClient()
def process_frames():
    global showable_label
    while True:
        content = frame_queue.get()
        if content is None:
            break
        food_item,scan_confidence=food_scan(content,client)
        showable_label=f"{food_item},{scan_confidence}"

worker = Thread(target=process_frames, daemon=True)
worker.start()


while True:
    time.sleep(0.02)
    ret, frame = cam.read()
    if not ret:
        break

    success, encoded_frame = cv.imencode(".jpg", frame, [cv.IMWRITE_JPEG_QUALITY, 50])
    if success and not frame_queue.full():
        content = encoded_frame.tobytes()
        frame_queue.put(content)

    with lock:
        cv.putText(frame, showable_label, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

    cv.imshow("CAMERA", frame)

    if cv.waitKey(1) & 0xFF == 27:
        break

    if cv.waitKey(1) & 0xFF == 32:
        cv.imwrite("food.jpg", frame)

frame_queue.put(None)
worker.join()
cam.release()
cv.destroyAllWindows()
