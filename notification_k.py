from twilio.rest import Client
from datetime import datetime

# Twilio credentials
# heli
# account_sid = 'AC6896e5fdc1041de79c0303ca53240e06'
# auth_token = '6c163a4ab77536c72c733706bed57121'

# # khushi
# account_sid = 'AC1661a4f35b87fa2c6c10889a43ca6e3a'
# auth_token = '36755f29a1b399be4f3dda08444a5037'

# dhara
account_sid = 'ACf280d26ce5f654d60b383b993e03a13d'
auth_token = '01dcaa14529aef41ddda6ba45c071d21'
client = Client(account_sid, auth_token)


# Function to send SMS alerts
def alert(object, latitude, longitude):
    """
    Sends an SMS alert with the detected object and GPS location.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = client.messages.create(
        body=f"🚨 ALERT: {object} detected!\n🕒 Date & Time: {timestamp}\n📍 Location: {latitude}, {longitude}",
        # from_='+17345085114', # heli
        # from_='+18457233219', # khushi
        from_='+12185020634', # dhara
        to='+917043022473'
    )
    print("✅ Alert sent successfully!")


# Function to handle multiple alerts
def sendAlert(result_list):
    """
    Iterates through the detection results and triggers alerts.
    """
    alert_classes = ['Person', 'Vehicle', 'Fire', 'Elephant']

    last_seen_locations = {class_name: None for class_name in alert_classes}

    for frame in result_list:
        detections = frame['detections']

        for detection in detections:
            class_name = detection['class_name']
            latitude = detection['latitude']
            longitude = detection['longitude']

            if class_name in alert_classes:
                last_seen_locations[class_name] = (latitude, longitude)

    # Send alerts for the latest detections
    for class_name, location in last_seen_locations.items():
        if location:
            latitude, longitude = location
            alert(class_name, latitude, longitude)
