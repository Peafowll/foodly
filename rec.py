import io
import os
from datetime import datetime

import cv2   
from google.cloud import vision_v1p3beta1 as vision

allowed_foods=[line.rstrip('\n ').lower() for line in open('food.list')]#opens a list of allowed food items
def food_scan(continut,client):
    '''
        args : 
        continut = the google vision content parsed to function (in bytes)
        client = the google vision API client object
    '''
    firsttime=datetime.now()#starts a timer for efficieny tracking
    global allowed_foods #parses the list
    def find_food(continut,food_list):
        image=vision.types.Image(content=continut) #turns content to an image
        response = client.label_detection(image=image) 
        labels = response.label_annotations #memorizes each prediction and its likelyhood
        for label in labels: #goes thru all the potential predictions seen
            desc = label.description.lower()
            score = round (label.score,2)
            if desc in food_list: #checks if it detected an allowed object
                showable_label=desc.split(" ")[0]# ORIBIL
                return showable_label, score # returns the object and the confidence
            if score <=0.50: #checks if the AI is confient
                break
        return "food not found",0 #if it doesnt find a valid object, returns so
    item,confidence=find_food(continut,allowed_foods)
    #print(datetime.now()-firsttime) # (FOR EFFICICENY TESTING)
    return item,confidence # returns the found item and confidence
