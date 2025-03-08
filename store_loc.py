import requests
import geocoder
from math import radians, sin, cos, sqrt, atan2


partners=[line.rstrip('\n ') for line in open('partners.list')]
#print(f'partners={partners}')


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c 


def stores_near_me():
    my_location=geocoder.ip('me')
    my_coords=my_location.latlng

    my_lat=my_coords[0]
    my_long=my_coords[1]

    print( f"https://www.google.com/maps?q={my_lat},{my_long}")

    query_supermarkets = f"""
    [out:json];
    node
        ["shop"~"supermarket|convenience|hypermarket|grocery"]   
        (around:2000, {my_lat}, {my_long});
    out;
    """


    url = "http://overpass-api.de/api/interpreter"

    response = requests.get(url, params={"data": query_supermarkets})

    data=response.json()

    stores = {} 


    #print(f'DATA ESTE {data}\n-----------------------------------')

    # Extract store names & locations
    for element in data["elements"]:
        #print(f'{element}\n')
        name = element.get("tags", {}).get("name", "Unnamed Store")
        street = element.get("tags",{}).get("addr:street","Strada Necunoscuta")
        store_lat = element["lat"]
        store_long = element["lon"]
        distance=haversine(my_lat,my_long,store_lat,store_long)
        if name in partners:
            stores[name]=[street,distance,store_lat,store_long]
            #print(f"{name}, {street} , distanta : {distance:.2f} km: https://www.google.com/maps?q={store_lat},{store_long}")
    return(stores)

