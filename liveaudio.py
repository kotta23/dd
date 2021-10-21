import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("*"*40,"A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("*"*40,"Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("*"*40,"Say something!")
        with m as source: audio = r.listen(source)
        print("*"*40,"Got it! Now to recognize it...")
        try:
            value = r.recognize_google(audio)

            if str is bytes:
                print("*"*40,u"You said {}".format(value).encode("utf-8"))
            else:
                print("*"*40,"You said {}".format(value))
        except sr.UnknownValueError:
            print("*"*40,"Oops! Didn't catch that")
        except sr.RequestError as e:
            print("*"*40,"Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass