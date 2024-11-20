import os
import cv2 as cv
from google.cloud import vision_v1p3beta1 as vision
from threading import Thread, Lock
from queue import Queue
import time
from rec import food_scan

def hack():
    #initiate the camera and sizes
    cam = cv.VideoCapture(0) 
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'
    #client = vision.ImageAnnotatorClient()

    showable_label = "Loading..." # initiate the showing label with "Loading..."
    #sum threadding for efficiency
    lock = Lock() 
    frame_queue = Queue(maxsize=5)
    #initializing the google vision client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'
    client=vision.ImageAnnotatorClient()
    #a function for transforming byte data into the detected object and confidence for each frame
    def process_frames():
        nonlocal showable_label
        while True:
            content = frame_queue.get() #getting the byte data from the queue
            if content is None:
                break
            food_item,scan_confidence=food_scan(content,client) # transfering the data and getting the info
            showable_label=f"{food_item},{scan_confidence}" #making it a string

    # more threadding 
    worker = Thread(target=process_frames, daemon=True)
    worker.start()

    #ofc we had to do an fps counter
    fps=0
    prev_time = time.time()
    while True:
        # sleeping for efficiency (too fast != good)
        time.sleep(0.02)
        ret, frame = cam.read()
        #getting the frames and then flipping them
        frame = cv.flip(frame,1)
        if not ret:
            break
        
        #encodding the frames
        success, encoded_frame = cv.imencode(".jpg", frame, [cv.IMWRITE_JPEG_QUALITY, 50])
        if success and not frame_queue.full():
            content = encoded_frame.tobytes()
            frame_queue.put(content)

        #the magic formula for fps
        current_time = time.time()
        elapsed_time = current_time-prev_time
        fps = 1/elapsed_time if elapsed_time>0 else 0
        prev_time = current_time

        text_size_label, _ = cv.getTextSize(showable_label, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_width_label, text_height_label = text_size_label
        cv.rectangle(frame, (40, 20), (50 + text_width_label, 120 + text_height_label), (0, 0, 0), -1)

        #putting the text when sure we have info
        with lock:
            cv.putText(frame, showable_label, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 155), 2, cv.LINE_AA)
            cv.putText(frame, f"FPS: {int(fps)}", (50, 110), cv.FONT_HERSHEY_SIMPLEX, 1, (155, 255, 155), 2, cv.LINE_AA)

        #showing the frames lol
        cv.imshow("CAMERA", frame)

        #quitting the app
        if cv.waitKey(1) & 0xFF == 27:
            break
        
        #taking a photo if we really want to tho
        if cv.waitKey(1) & 0xFF == 32:
            cv.imwrite("food.jpg", frame)

    #exitting all other api, libraries etc
    frame_queue.put(None)
    worker.join()
    cam.release()
    cv.destroyAllWindows()