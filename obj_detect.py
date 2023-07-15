import requests
import cv2
import argparse
import os

api_url = "http://localhost:9900/v1/detectobjects"
image_path = os.path.join("obj_detect_example", "car.jpg")

image = cv2.imread(image_path)
retval,image_file = cv2.imencode('.jpg', image)
if retval:
    encoded_image = image_file.tobytes()
    print("encoded")
else:
    print("Image encoding failed.")

response = requests.post(api_url, encoded_image)

if response.status_code == 200:
    response_data = response.json()

    print(response_data)
    objects = response_data["result"]["objects"]
    for obj in objects:
      if obj["boundingBox"]["width"] > 0 and obj["boundingBox"]["height"] > 0:
        left = int(obj["boundingBox"]["top"])
        top = int(obj["boundingBox"]["left"])
        width = int(obj["boundingBox"]["width"])
        height = int(obj["boundingBox"]["height"])
        cv2.rectangle(image, (left, top), (left + width, top + height), (0, 255, 0), 2)


    cv2.imshow("detected object", image)
    print("Press any key to continue...")
    cv2.waitKey(0)

else:
    print("Error: Response received from the server {}".format(response.status_code))
print("Code execution completed.")
