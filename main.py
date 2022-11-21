from queue import Queue
import threading
import time
import speech_recognition as sr
import sounddevice as sd
from pydub import AudioSegment
import scipy
from whisper import audio
import numpy as np


class RecordingService(threading.Thread):
    def __init__(self, audio_segments: Queue, sample_rate=44100):
        threading.Thread.__init__(self)
        self.r = sr.Recognizer()
        self.m = sr.Microphone(sample_rate=sample_rate)
        self.audio_segments = audio_segments
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    def run(self):
        with self.m as source:
            print("Started recording!")
            while True:
                audio = self.r.listen(source, phrase_time_limit=10)
                self.audio_segments.put(audio)


class TranscriptionService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

    def run(self):
        while True:
            audio_result = self.audio_segments.get()
            transcription = self.r.recognize_whisper(audio_result, language="english")
            print(f'Person: "{transcription}"')
            self.audio_segments.task_done()


if __name__ == "__main__":
    audio_segments = Queue()
    recorder = RecordingService(audio_segments)
    transcriber = TranscriptionService(audio_segments)

    recorder.start()
    transcriber.start()
