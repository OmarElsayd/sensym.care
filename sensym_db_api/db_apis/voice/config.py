import pyaudio


class VoiceGraphConfig():
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 4