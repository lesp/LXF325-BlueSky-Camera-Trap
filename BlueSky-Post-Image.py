from atproto import Client
import secret_file
import time
from picamera2 import Picamera2, Preview
from libcamera import controls
import datetime
from gpiozero import MotionSensor

pir = MotionSensor(17)

def capture_and_post():
    filename = datetime.datetime.now().replace(microsecond=0).isoformat()+".jpg"
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start(show_preview=True)
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    time.sleep(2)
    picam2.capture_file(filename)
    picam2.stop_preview()
    picam2.stop()

    with open(filename, 'rb') as f:
        img_data = f.read()
        
    client = Client()
    client.login(secret_file.username, secret_file.app_password)
    message = "ALERT: MOVEMENT DETECTED! This image was taken at "+filename
    client.send_image(text=message, image=img_data, image_alt="This is a photo taken by the Raspberry Pi Camera and catches and object moving in front of a PIR sensor, triggering the camera trap")
    
while True:
    print("Waiting for sensor to be triggered")
    pir.when_motion = capture_and_post
    time.sleep(5)