import ultralytics
import cv2
from ultralytics import YOLO
model=YOLO("yolov8m.pt")
capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        break
    #cv2.imshow("frame",frame)
    results = model(frame)
    #print(f'results={results}')
    image_results = results[0].plot()
    cv2.imshow("AI Webcam",image_results)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

capture.release()
cv2.destroyAllWindows()
