import cv2
import torch
import pathlib
from datetime import datetime
from notification import sendAlert  # Import sendAlert function

# Fix PosixPath issue on Windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Load YOLOv8 Model
day_model = torch.hub.load('yolov5', 'custom', path='weights/day-final.pt', source='local', device="cpu")
thermal_model = torch.hub.load('yolov5', 'custom', path='weigh ts/night-final-aug.pt', source='local', device="cpu")

day_class_to_animal = {
    0: 'Person', 1: 'Elephant', 2: 'Zebra', 3: 'Giraffe', 4: 'Deer',
    5: 'Bison', 6: 'Rhino', 7: 'Boar', 8: 'Leopard', 9: 'Vehicle', 10: 'Fire'
}
thermal_class_to_animal = {
    0: "Person", 1: "Elephant", 2: "Deer", 3: "Rhino", 4: "Boar", 
    5: "Leopard", 6: "Vehicle", 7: "Fire"
}

# Function to draw bounding boxes
def plotBbox(results, frame, class_dict):
    detected_objects = []  # Store detected objects for alerting

    for box in results.xyxy[0]:
        xA, yA, xB, yB, confidence, class_id = box
        class_id = int(class_id)
        class_name = class_dict.get(class_id, 'Unknown')

        # Define a unique color for each class
        color = (0, 255, 0)  # Green color for bounding boxes
        cv2.rectangle(frame, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)
        label = f"{class_name}: {confidence:.2f}"
        cv2.putText(frame, label, (int(xA), int(yA) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # If detected object needs an alert, store it
        if class_name in ['Person', 'Vehicle', 'Fire']:
            detected_objects.append({
                "class_name": class_name,
                "latitude": "Unknown",  # Replace with actual GPS if available
                "longitude": "Unknown"
            })

    return frame, detected_objects


def predict_live(camera_source, video_class="Daylight"):
    cap = cv2.VideoCapture(camera_source)
    # cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Reduce buffer lag


    if not cap.isOpened():
        print("Error: Could not open camera source")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Live Stream Resolution: {width}x{height} at {fps} FPS")

    frame_count = 0  # Frame counter
    result_list = []  # Store results for notification

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Could not read frame")
            break

        # Do NOT resize the frame—keep original resolution
        # Convert BGR to RGB (YOLOv5 expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Select appropriate model
        model = day_model if video_class == "Daylight" else thermal_model
        class_dict = day_class_to_animal if video_class == "Daylight" else thermal_class_to_animal

        # Run YOLO detection
        results = model(rgb_frame)

        # Draw bounding boxes and extract detected objects
        frame, detected_objects = plotBbox(results, frame, class_dict)

        # Send alert if relevant objects are detected
        if detected_objects:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Format: YYYY-MM-DD_HH-MM-SS
            save_path = f"output/detected_{timestamp}.jpg"
            cv2.imwrite(save_path, frame)  # Save frame with detections
            print(f"✅ Frame saved: {save_path}")
            
            result_list.append({
                "frame_number": frame_count,
                "detections": detected_objects
            })
            sendAlert(result_list)  # Send notifications

        frame_count += 1  # Increment frame count

        # Show live feed with detections
        cv2.imshow("Wildlife Detection - Live Stream", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Replace with your IP Webcam URL
# khushi
predict_live("http://10.158.72.75:8080/video")

# heli
# predict_live("http://192.168.29.224:8080/video")