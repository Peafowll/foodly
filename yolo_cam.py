import ultralytics
import cv2
from ultralytics import YOLO
model=YOLO("yolov8m.pt")
capture = cv2.VideoCapture(0)
allowed_foods=[line.rstrip('\n ').lower() for line in open('food.list')]#opens a list of allowed food items
while True:
    ret, frame = capture.read()
    if not ret:
        break
    #cv2.imshow("frame",frame)
    results = model(frame)
    print(f'results={results}')
    foundfood="nothing"
    for i in range(3):
        #print(f'Found object [{i}]={results[0].names[i]}\n')
        if results[0].names[i] in allowed_foods:
            foundfood=results.names[i]
    if foundfood != "nothing":
        image_results = results[0].plot()
    else:
        image_results=frame
    image_results=results[0].plot()
    cv2.imshow("AI Webcam",image_results)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

capture.release()
cv2.destroyAllWindows()
