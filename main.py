from rec import food_scan
from camera import get_camera
import io
import os
from datetime import datetime

import cv2   
#get_camera()

loc="C:\\Hackathon\\HackathonFoodRec\\food.jpg"
food_item,scan_confidence=food_scan(loc)
print(f'{food_item}, {scan_confidence}')
