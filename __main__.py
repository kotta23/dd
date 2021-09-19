import os
from ocr_lib import  ocr_space_file, API_KEY
from test_asl_model import ai_cap
print("hey")
from camera import Camera
from sound_recognizer import recognize_speech_from_mic
import sound_recognizer_ar as eg
from image_viewer_thread import ImageViewer
import requests
from multiprocessing import Queue
import cv2
from gpiozero import Button
from time import sleep
from picamera import PiCamera
from t import dict
import requests
from gtts import gTTS
from playsound import playsound

print("before camera")
camera = PiCamera()
camera.resolution = (640, 480)
print("after cam.....")
B1_PIN  = 20
B2_PIN  = 21
# assign physically
B3_PIN  = 12
B4_PIN  = 16

b1 = Button(B1_PIN, pull_up=True, bounce_time=0.1)
b2 = Button(B2_PIN, pull_up=True, bounce_time=0.1)
b3 = Button(B3_PIN, pull_up=True, bounce_time=0.1)
b4 = Button(B4_PIN, pull_up=True, bounce_time=0.1)

images_container = Queue(3)
#cam = Camera(images_container)
#cam.start()
print("after btns")
image_viewer = ImageViewer()
image_viewer.start()
ar = False

words_to_say = eg.recognize_speech_from_mic().get('transcription')
print('encoded',words_to_say)
words_to_say = words_to_say.decode('utf-8')
print('decode ',words_to_say)

while False:
    
    words_to_say = ""
    if b1.is_pressed:
        print("b1 is pressed")
        camera.start_preview()
        sleep(5)
        camera.capture('hello.png')
        camera.stop_preview()
        try:
            words_to_say = ocr_space_file(filename="hello.png", api_key=API_KEY, language='eng')
        except requests.exceptions.ConnectionError:
            print("fail to communicate")
        #os.remove(".tmp.png")
    elif b2.is_pressed:
        print("b2 is pressed")
         
        words_to_say = recognize_speech_from_mic().get('transcription')
        ar = False
    elif b3.is_pressed:
        print("b3 is pressed")
        words_to_say = eg.recognize_speech_from_mic().get('transcription')
        ar = True
        # print("b3 is pressed")
        # camera.start_preview()
        # sleep(5)
        # camera.capture('ai.png')
        # camera.stop_preview()
        # try:
        #     words_to_say = ai_cap()

        # except requests.exceptions.ConnectionError:
        #     print("fail to communicate")
    elif b4.is_pressed:
        try:
            camera.start_preview()
            sleep(5)
            camera.capture('ai.png')
            camera.stop_preview()
            words_to_say = ai_cap()
            if words_to_say in dict:
                words_to_say=arabic_reshaper.reshape(str(dict[words_to_say]))
            print(words_to_say)
            
            myobj = gTTS(text=words_to_say, lang='ar', slow=False)
            myobj.save("welcome.mp3")
            import os

            os.system('mpg321 welcome.mp3 ')
            #playsound("welcome.mp3")
        except requests.exceptions.ConnectionError:
            print("fail to communicate")   
    if not words_to_say is None and len(words_to_say) > 0:
        
        words_to_say = words_to_say.decode('utf-8')
        print("the word is      :",words_to_say)
        
        image_viewer.add_cmd(words_to_say ,ar)
        print("press any key again..")



cam.close()
##