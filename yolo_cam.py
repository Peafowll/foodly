import ultralytics
import cv2
from ultralytics import YOLO
model=YOLO("yolov8m.pt")
capture= cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        break
    results = model(frame, show=True)
    print(f'results={results}')
    image_results = results[0].plot()
    cv2.imshow("AI Webcam",image_results)

capture.release()
cv2.destroyAllWindows()
