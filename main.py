from queue import Queue
import threading
import time


class RecordingService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments

    def run(self):
        while True:
            self.audio_segments.put(time.time())
            time.sleep(1)


class TranscriptionService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments

    def run(self):
        while True:
            result = self.audio_segments.get()
            print(result)
            self.audio_segments.task_done()


audio_segments = Queue()
recorder = RecordingService(audio_segments)
transcriber = TranscriptionService(audio_segments)

recorder.start()
transcriber.start()
