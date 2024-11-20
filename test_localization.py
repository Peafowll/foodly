
from google.cloud import vision
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'

client = vision.ImageAnnotatorClient()

uri = "food.jpeg"

image = vision.Image()
image.source.image_uri = uri

objects = client.object_localization(image=image).localized_object_annotations

print(f"Number of objects found: {len(objects)}")
for object_ in objects:
    print(f"\n{object_.name} (confidence: {object_.score})")
    print("Normalized bounding polygon vertices: ")
    for vertex in object_.bounding_poly.normalized_vertices:
        print(f" - ({vertex.x}, {vertex.y})")
