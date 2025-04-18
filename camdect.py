import cv2
import torch
import pathlib
from datetime import datetime
from notification_k import sendAlert  # Import sendAlert function
import requests
import os

# Fix PosixPath issue on Windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load YOLOv8 Model
day_model = torch.hub.load('yolov5', 'custom', path='weights/day-final.pt', source='local', device="cpu")
thermal_model = torch.hub.load('yolov5', 'custom', path='weights/night-final-aug.pt', source='local', device="cpu")

day_class_to_animal = {
    0: 'Person', 1: 'Elephant', 2: 'Zebra', 3: 'Giraffe', 4: 'Deer',
    5: 'Bison', 6: 'Rhino', 7: 'Boar', 8: 'Leopard', 9: 'Vehicle', 10: 'Fire'
}
thermal_class_to_animal = {
    0: "Person", 1: "Elephant", 2: "Deer", 3: "Rhino", 4: "Boar", 
    5: "Leopard", 6: "Vehicle", 7: "Fire"
}


# Function to get GPS location from the phone
def get_phone_location(phone_ip):
    try:
        url = f"http://{phone_ip}:8080/sensors.json"
        response = requests.get(url, timeout=3)
        data = response.json()

        latitude = data['gps']['latitude']
        longitude = data['gps']['longitude']

        return latitude, longitude
    except Exception as e:
        print("⚠️ Error fetching location:", e)
        return "Unknown", "Unknown"


# Function to draw bounding boxes
def plotBbox(results, frame, class_dict, phone_ip):
    detected_objects = []

    latitude, longitude = get_phone_location(phone_ip)  # Fetch GPS location once per frame

    for box in results.xyxy[0]:
        xA, yA, xB, yB, confidence, class_id = box
        class_id = int(class_id)
        class_name = class_dict.get(class_id, 'Unknown')

        # Draw bounding box
        color = (0, 255, 0)  # Green color for bounding boxes
        cv2.rectangle(frame, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)
        label = f"{class_name}: {confidence:.2f}"
        cv2.putText(frame, label, (int(xA), int(yA) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Store detected objects if relevant
        if class_name in ['Person', 'Vehicle', 'Fire', 'Elephant']:
            detected_objects.append({
                "class_name": class_name,
                "latitude": latitude,
                "longitude": longitude
            })

    return frame, detected_objects


# Function for live video prediction
def predict_live(camera_source, phone_ip, video_class="Daylight"):
    cap = cv2.VideoCapture(camera_source)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer lag

    if not cap.isOpened():
        print("❌ Error: Could not open camera source")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"📷 Live Stream Resolution: {width}x{height} at {fps} FPS")

    frame_count = 0
    result_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Warning: Could not read frame")
            break

        # Convert BGR to RGB (YOLOv5 expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Select appropriate model
        model = day_model if video_class == "Daylight" else thermal_model
        class_dict = day_class_to_animal if video_class == "Daylight" else thermal_class_to_animal

        # Run YOLO detection
        results = model(rgb_frame)

        # Draw bounding boxes and extract detected objects
        frame, detected_objects = plotBbox(results, frame, class_dict, phone_ip)

        # Save frame and send alerts
        if detected_objects:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_path = f"output/detected_{timestamp}.jpg"
            cv2.imwrite(save_path, frame)
            print(f"✅ Frame saved: {save_path}")

            result_list.append({
                "frame_number": frame_count,
                "detections": detected_objects
            })

            sendAlert(result_list)

        frame_count += 1

        # Display live feed with detections
        cv2.imshow("Wildlife Detection - Live Stream", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Set IP Webcam URL
# heli
phone_ip = "192.168.29.224"
predict_live(f"http://{phone_ip}:8080/video", phone_ip)
