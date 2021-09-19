from threading import Thread
from collections import deque
import os
import time
import numpy as np
import cv2
os.system("i2cdetect -y 1")
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

# Load image based on OLED display height.  Note that image is converted to 1 bit color.

    
class ImageViewer(Thread):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.__buffer = deque(maxlen=10)
        

    def run(self) -> None:
        while True:
            if len(self.__buffer ):
                words_to_say = self.__buffer.popleft()
                if len(words_to_say):
                    words = words_to_say.split()
                    for word in words:
                        target_path = os.path.join(os.getcwd(), "images", f"{word}.bmp")
                        print(target_path)
                        disp.clear()
                        disp.display()
                        if os.path.isfile(target_path):
                            image = Image.open(target_path).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
                        else:
                            image = np.full((64,128,3), 255,np.uint8 )
                            cv2.putText(image,word,(30,30),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2)
                            cv2.imwrite("tmp.png" , image)
                            image = Image.open("tmp.png").resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
                        disp.image(image)
                        disp.display()
                        time.sleep(3)
    def add_cmd(self, cmd):
        self.__buffer.append(cmd)

