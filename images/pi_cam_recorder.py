from picamera import PiCamera
from time import sleep
import datetime
from gpiozero import Button
import os 
base_base = '/home/pi/videos'
if not os.path.isdir(base_base):
    os.makedirs(base_base)

b1 = Button(21, pull_up=True, bounce_time=0.1)
camera = PiCamera()
camera.start_preview()
while True:
    if b1.is_pressed:
        video_file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".h264"
        camera.start_recording(os.path.join(base_base, video_file_name))
        sleep(5)
        camera.stop_recording()

camera.stop_preview()