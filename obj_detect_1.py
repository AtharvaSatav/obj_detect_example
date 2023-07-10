"""
@file: api_client_example_images.py
@breif: File contains example code for testing the API client
"""
import os
import requests
import cv2
import argparse
import time

INPUT_DIR = "../../sample_inputs/images"
OUTPUT_DIR = "./output"
API_SERVER_URL = "http://localhost:9900/obj_detect"

def draw_bounding_box_on_image(image, object):
    """
    @breif: Draw bounding box on given image
    @param: image Input Image
    @param: object Object dict which contains the 
            bounding box and label info from the API server
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    blue_color = (255, 178, 50) # blue color in BGR format
        
    x = int(object["object_rectangle"]["x"])
    y = int(object["object_rectangle"]["y"])
    w = int(object["object_rectangle"]["width"])
    h = int(object["object_rectangle"]["height"])

    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
    
    label = object["label"]+":"+object["score"]
    
    # Get the size of the text
    (_, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

    # Draw the Text 
    cv2.putText(image,label,(x, y+text_height), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    return image

def display_image(image):
    """
    @breif: Display the image on screen
    @param: image Input Image
    """
    cv2.imshow("image", image)
    print("Press any key to continue...")
    cv2.waitKey(0)

def save_image(image, image_path, output_dir):
    """
    @breif: Save the image to the disk
    @param: image Input Image
    """
    print("Saving output image to dir {}".format(output_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = "result_{}".format(image_path.split('/')[-1])
    filepath = os.path.join(output_dir, filename)
    cv2.imwrite(filepath, image)

def send_requests_to_api_server(url, input_folder, out_dir, save, display):
    '''
    The function iterates over all files in the input_folder and reads each file as an image.
    The image is then sent as a POST request to the url using the requests library. 
    If the response code is 200 (i.e., successful), the function reads the response body as a JSON object
     and draws bounding boxes around detected objects in the input image.
    The processed image is then displayed and saved to the out_dir directory (if save is True).

    url: the URL of a web page that expects to receive images via HTTP POST requests
    input_folder: a directory containing input images in JPEG format
    out_dir: a directory where the output images with object detection bounding boxes will be saved
    save: a boolean flag indicating whether to save the output images or not

    return: void
    '''
    count = 0
    completedRequests =0

    for entry in os.scandir(input_folder):
        if entry.is_file():

            # Get the file path
            image_path = entry.path
            count += 1

            # Read the image using OpenCV
            image = cv2.imread(image_path)

            # Encode the image in jpeg format 
            _, image_data = cv2.imencode('.jpg', image)

            # Send the HTTP request to the API server
            response = requests.post(url, data = image_data.tobytes())

            #print("Response code =",response.status_code,"\nResponse body size =", len(response.content))

            if response.status_code == 200:
                completedRequests += 1
                result = response.json()
                for object in result["objects"]:
                    image = draw_bounding_box_on_image(image, object)

                if(display):
                    display_image(image)
                if(save):
                    save_image(image,image_path, out_dir)
            else:
                print("Error: Response received from the server {}".format(response.status_code))

    return count, completedRequests

def main():
    """
    Main function
    """
    start_time = time.time()
    count, completedRequests = send_requests_to_api_server(API_SERVER_URL, INPUT_DIR, OUTPUT_DIR, True, True)
    end_time = time.time()

    print("Summary of execution")
    print(f"Total number of requests sent     : {count}")
    print(f"Total number of responses received: {completedRequests}")
    print(f"Total number of requests failed   : {count - completedRequests}")
    print(f"Total time of execution           : {int((end_time-start_time)*1000)}ms")


if __name__ == '__main__':
    main()
