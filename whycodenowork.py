import ultralytics
from ultralytics import YOLO
import cv2

food_list = []  # Global list to store detected food items

def food_identify():
    global food_list

    food_classes = [i for i in range(46, 52)]  # Food class IDs in COCO dataset
    model = YOLO("yolov8n.pt")  # Load the YOLO model
    capture = cv2.VideoCapture(0)  # Open the webcam

    if not capture.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip horizontally for a natural mirror effect

        results = model(frame, stream=True)  # Process the frame with YOLO

        for result in results:
            for box, cls in zip(result.boxes.xyxy, result.boxes.cls): 
                x1, y1, x2, y2 = map(int, box)
                class_id = int(cls)

                if class_id in food_classes:  # Check if it's a food item
                    class_name = model.names[class_id]
                    if class_name not in food_list:
                        food_list.append(class_name)

                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    axis_x = (x2 - x1) // 2
                    axis_y = (y2 - y1) // 3
                    
                    # Draw bounding ellipse
                    cv2.ellipse(frame, (center_x, center_y), (axis_x, axis_y), 
                                angle=0, startAngle=0, endAngle=360, 
                                color=(0, 255, 0), thickness=2)

                    # Display class name
                    label = class_name
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, label, (x1, y1 - 10), font, 0.5, (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("AI Webcam", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(food_list)
            break

    # Release resources
    capture.release()
    cv2.destroyAllWindows()

food_identify()
print("jobsdone")
