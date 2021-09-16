from threading import Thread
from collections import deque
import os
import time
import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image

# Load image based on OLED display height.  Note that image is converted to 1 bit color.

    
class ImageViewer(Thread):
    def __init__(self , ar=False):
        super(ImageViewer, self).__init__()
        self.__buffer = deque(maxlen=10)
        self.ar = ar

    def run(self) -> None:
        while True:
            if len(self.__buffer ):
                words_to_say = self.__buffer.popleft()
                if len(words_to_say):
                    words = words_to_say.split()
                    print(words)
                    for word in words:
                        #print(word)
                        target_path = os.path.join(os.getcwd(), "images", f"{word}.bmp")
                        print(target_path)
                        if os.path.isfile(target_path):
                            image =  cv2.imread(target_path)
                        else:
                            if not self.ar:
                                image = np.full((64,128,3), 255,np.uint8 )
                                cv2.putText(image,word,(30,30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2 )
                            else:
                                image = np.full((64,128,3), 255,np.uint8 )
                                cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                                pil_im = Image.fromarray(cv2_im_rgb)
                                draw = ImageDraw.Draw(pil_im)
                                # Choose a font
                                font = ImageFont.truetype("arial.ttf", 50)
                                # Draw the text
                                draw.text((0, 0), word,fill="black", font=font)
                                # Save the image
                                image = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
                        cv2.imshow("image viewer", image)
                        cv2.waitKey(2500)
                        print(self.ar)
                    cv2.destroyAllWindows()
    def add_cmd(self, cmd , ar):
        self.__buffer.append(cmd)
        self.ar = ar


