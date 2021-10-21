import speech_recognition as sr
import os
recognizer = sr.Recognizer()

from googletrans import Translator
import arabic_reshaper
from bidi.algorithm import get_display
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

translator = Translator()

def recognize_speech_from_mic():
    global recognizer
    print('espeak "please say something.."')
    os.system('''arecord -f S16_LE -d 5 -r 44100   test.wav''')
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = recognizer.record(source) 
    print('espeak "decodeing"')
    
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None,
    }

    try:
        word = recognizer.recognize_google(audio, language="ar-EG")
        print(word)
        response["transcription"] = word
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response


