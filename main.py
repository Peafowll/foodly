from rec import food_scan
#from camera import get_camera

#get_camera()

loc="C:\\Hackathon\\HackathonFoodRec\\food.jpg"
food_item,scan_confidence=food_scan(loc)
print(f'{food_item}, {scan_confidence}')
