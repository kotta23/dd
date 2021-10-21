import speech_recognition as sr
import os
recognizer = sr.Recognizer()


def recognize_speech_from_mic():
    global recognizer
    print('espeak "please say something.."')
    os.system('''arecord -f S16_LE --device="hw:2,0" -d 5 -r 44100   test.wav''')
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = recognizer.record(source) 
    print('espeak "decodeing"')
    
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        print("try")
        response["transcription"] = recognizer.recognize_google(audio)
        print(response["transcription"])
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response
#words_to_say = recognize_speech_from_mic().get('transcription')

