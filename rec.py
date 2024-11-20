import io
import os
from datetime import datetime

import cv2   
from google.cloud import vision_v1p3beta1 as vision

allowed_foods=[line.rstrip('\n ').lower() for line in open('food_detection_lists/list.txt')]
def food_scan(continut,client):
    firsttime=datetime.now()
    global allowed_foods
    def find_food(continut,food_list):
        image=vision.types.Image(content=continut)
        response = client.label_detection(image=image)
        labels = response.label_annotations #memorizes each prediction and its lieklyhood
        for label in labels:
            desc = label.description.lower()
            score = round (label.score,2)
            if desc in food_list:
                showable_label=desc.split(" ")[0]# ORIBIL
                return showable_label, score
            if score <=0.65:
                break
        return "food not found",0
    item,confidence=find_food(continut,allowed_foods)
    print(datetime.now()-firsttime)
    return item,confidence
