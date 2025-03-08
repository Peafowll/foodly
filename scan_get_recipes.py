import json
from yolo_cam import food_identify
import ultralytics
from ultralytics import YOLO
import cv2


def food_identify():
    food_list = []  # Global list to store detected food items

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
                    cv2.putText(frame, label, (center_x-15,center_y), font, 0.5, (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("AI Webcam", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return food_list
            break

    # Release resources
    capture.release()
    cv2.destroyAllWindows()

def load_recipes(file_path):
    """Load recipes from an external file."""
    with open(file_path, 'r', encoding='windows-1252') as file:
        return json.load(file)



def check_recipes(recipes, available_ingredients):
    """Check which recipes can be made and list missing ingredients."""
    listlol=[]
    cnt = 0
    for recipe_name, recipe_details in recipes.items():
        if cnt>=9:
            break
        cnt=cnt+1
        instructions = recipe_details.get("instructions", "Unknown Instructions")
        recipe_ingredients = set(recipe_details.get("ingredients", []))
        missing_ingredients = recipe_ingredients - set(available_ingredients)
        
        print(f"Recipe: {recipe_name}")
        print(f"Instructions: {instructions}")
        if missing_ingredients:
            print(f"Missing ingredients: {', '.join(missing_ingredients)}")
        else:
            print("You have all the ingredients!")
        print("-" * 40)

        real_available_ingredients = []


        real_available_ingredients = [ingredient for ingredient in available_ingredients if ingredient in recipe_ingredients]
        
        missing_ingredients = list(missing_ingredients)
        for i in range(len(missing_ingredients)):
            if missing_ingredients[i] in available_ingredients:
                missing_ingredients.pop(i)      

        list2 = [recipe_name,real_available_ingredients,missing_ingredients]
        if real_available_ingredients != []:
            listlol.append(list2)
    return listlol


def scan_n_load():
    recipes_file = "recipes.json"
    available_ingredients = food_identify()
    print("\n\n----------------------------------\n\n")
    print(available_ingredients)
    print("\n\n----------------------------------\n\n")
    try:
        recipes = load_recipes(recipes_file)
        return check_recipes(recipes, available_ingredients)
    except Exception as e:
        print(f"Error loading recipes: {e}")

