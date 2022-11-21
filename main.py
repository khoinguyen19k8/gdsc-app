from queue import Queue
import threading
import time
import speech_recognition as sr
import sounddevice as sd


class RecordingService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.audio_segments = audio_segments
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    def run(self):
        with self.m as source:
            while True:
                audio = self.r.listen(source)
                self.audio_segments.put(
                    self.r.recognize_whisper(audio, language="english")
                )
                time.sleep(0.5)


class TranscriptionService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments

    def run(self):
        with open("transcript.txt", "a+") as f:
            while True:
                result = self.audio_segments.get()
                print(f'Person: "{result}"')
                f.write(f"{result}\n")
                self.audio_segments.task_done()


audio_segments = Queue()
recorder = RecordingService(audio_segments)
transcriber = TranscriptionService(audio_segments)

recorder.start()
transcriber.start()
transcriber.join()
