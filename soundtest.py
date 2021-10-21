
# import required module
import os
  
# play sound
file = "test.wav"
print('playing sound using native player')
os.system("mpg123 " + file+ "&")

