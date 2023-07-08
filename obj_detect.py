import requests
import cv2
import argparse

api_url = "http://localhost:9900/obj_detect"
image_path = "../../sample_inputs/car.jpg"

def main():

    image = cv2.imread(image_path)
    retval,image_file = cv2.imencode('.jpg', image)
    if retval:
       encoded_image = image_file.tobytes()
    else:
       print("Image encoding failed.")

    response = requests.post(api_url, encoded_image)

    if response.status_code == 200:
       response_data = response.json()

       objects = response_data['objects']

       for obj in objects:
          label = obj['label']
          confidence = obj['confidence']
          x, y, w, h = obj['bounding_box']
          print(f"Object: {label}, Confidence: {confidence}, Bounding Box: ({x}, {y}, {w}, {h})")

       cv2.imshow("detected object", image)
       print("Press any key to continue...")
       cv2.waitKey(0)

    else:
       print("Error occurred during object detection.")
