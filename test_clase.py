from ultralytics import YOLO

model = YOLO('yolov8m.pt')
class_names = model.names
print(class_names)