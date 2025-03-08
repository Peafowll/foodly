import ultralytics
from ultralytics import YOLO
import cv2
from threading import Thread, Lock
from queue import Queue
import time

def hack():
    food_classes = [i for i in range(46,56)]
    lock = Lock() 
    frame_queue = Queue(maxsize=5)
    model = YOLO("yolov8n.pt")
    capture = cv2.VideoCapture(0)

    processing = True  # Shared state flag
    lock = Lock()

    def process_image():
        while True:
            frame = frame_queue.get()
            if frame is None:
                break
            with lock:  # Ensure thread safety
                results = model(frame, classes = food_classes)
            x1,y1,x2,y2 = results.boxes.xyxy[0]
            
            print(results)
            cv2.imshow("AI Webcam", image_results)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    worker = Thread(target=process_image, daemon=True)
    worker.start()

    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break
        
        if not frame_queue.full():
            frame_queue.put(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    with lock:
        processing = False
    frame_queue.put(None)  # Signal worker thread to exit
    worker.join()
    capture.release()
    cv2.destroyAllWindows()

hack()
