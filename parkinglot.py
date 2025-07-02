import cv2
import json
from ultralytics import solutions
import requests

# Stream url from https://oceancitylive.com/ocean-city-webcams/ocean-city-inlet-parking-lot-cam/ acquired with F12 and Network tab
stream_url = "https://t1.ipcamlive.com/timelapses/5aec8d9905b9a/2025-04-06/video.mp4" 

parkingSpots = 59 # Total number of parking spots

# Open the stream using OpenCV
cap = cv2.VideoCapture(stream_url)

#  Initialize parking management with tracking
parkingmanager = solutions.ParkingManagement(
    model="models/yolo11n.pt",  # path to model file
    json_file="resources/bounding_boxes.json",  # path to parking annotations file
    tracker="botsort.yaml" # botsort for better accuracy but slower detection
) 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Live Feed", frame)
    results = parkingmanager(frame)
    
    #  Get occupied and available spots directly from SolutionResults
    occupied = results.filled_slots  # Occupied parking spots
    available = results.available_slots  # Available parking spots

    # Send updated parking status to Flask
    parking_status = {
        "occupied": occupied,
        "available": available
    }

        # Send POST request & handle errors
    try:
        response = requests.post("http://127.0.0.1:5000/api/update-parking", json=parking_status)
        if response.status_code == 200:
            print("API Response:", response.json())  # Print response from server
        else:
            print("API Error:", response.status_code, response.text)  # Print raw error
    except requests.exceptions.RequestException as e:
        print("Request Failed:", e)

    # print(results)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()