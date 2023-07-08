import requests
import cv2
import argparse

# API endpoint URL
api_url = "http://localhost:9900/obj_detect"

# Image file path
image_path = "../../car.jpg"

# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    # Create the HTTP POST request with the image file
    files = {'image': image_file}
    response = requests.post(api_url, files=files)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON data
    response_data = response.json()

    # Extract the detected objects
    objects = response_data['objects']

    # Print the detected objects
    for obj in objects:
        label = obj['label']
        confidence = obj['confidence']
        x, y, w, h = obj['bounding_box']
        print(f"Object: {label}, Confidence: {confidence:.2f}, Bounding Box: ({x}, {y}, {w}, {h})")
else:
    print("Error occurred during object detection.")

print("Code execution completed.")
