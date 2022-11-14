import time
import sounddevice as sd
import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print(
            "Google Speech Recognition thinks you said "
            + recognizer.recognize_google(audio)
        )
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )


r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(
        source
    )  # we only need to calibrate once, before we start listening

stop_listening = r.listen_in_background(m, callback)

print("Hello world")

while True:
    time.sleep(1)

stop_listening(wait_for_stop=False)
