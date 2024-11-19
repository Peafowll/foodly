import io
import os
from datetime import datetime

import cv2   
from google.cloud import vision_v1p3beta1 as vision

def food_scan(image_root):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'

    default_path=""
    food_type="popular foods"
    #foods = [line.rstrip('\n').lower() for line in open('food_names/' + food_type + '.dict')]

    def find_food(img_location):
        start_time= datetime.now()

        photo = cv2.imread(img_location)

        h,w = photo.shape[:2]
        photo = cv2.resize(photo,(800,int((h*800)/w)))
        cv2.imwrite(default_path+"temp.jpg",photo)
        img_location=default_path+"temp.jpg"

        client=vision.ImageAnnotatorClient()
        with io.open(img_location,'rb') as image_file:
            content = image_file.read()
        
        image=vision.types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations #memorizes each prediction and its lieklyhood

        for label in labels:
            desc = label.description.lower()
            score = round (label.score,2)
            if desc != "food":
                showable_label=desc.split(" ")[0]# ORIBIL
                return showable_label, score
    #print("START")
    path = default_path+ 'test.jpg'
    item,confidence=find_food(image_root)
    #print(item,confidence)
    return item,confidence
    print("end") 
