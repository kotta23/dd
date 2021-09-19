import speech_recognition as sr
import os
from googletrans import Translator
import arabic_reshaper
from bidi.algorithm import get_display

recognizer = sr.Recognizer()
translator = Translator()


def recognize_speech_from_mic():
    global recognizer
    print('espeak "please say something.."')
    # os.system('''arecord -f S16_LE -d 5 -r 44100 --device="hw:1,0"  test.wav''')
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = recognizer.record(source) 
    print('espeak "decodeing"')
    
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None,
        "transcription_ar":None
    }
    try:

        aud_to_txt = recognizer.recognize_google(audio)
        txt_en_ar = translator.translate(aud_to_txt, dest='ar')
        print(aud_to_txt,'yahoooo',txt_en_ar)
        reshaped_text = arabic_reshaper.reshape(str(txt_en_ar.text))    # correct its shape
        bidi_text = get_display(reshaped_text)   
        print('yaaaaay')
        print(reshaped_text,'yahoooo',bidi_text)
        print(type(aud_to_txt))
        print(type(bidi_text))
        # response["transcription"] = aud_to_txt
        response["transcription_ar"] = bidi_text
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response


recognize_speech_from_mic()