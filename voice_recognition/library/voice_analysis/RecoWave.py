import numpy as np
import pyaudio
import wave
from pocketsphinx import LiveSpeech


def recording_a_wav_file(first_name: str, last_name: str) -> None:
    """
    This method will record a wav file.
    Make sure that you are in the user work directory.
    :param first_name:  The first name of the user
    :param last_name:   The last name of the user
    :return:        None
    """
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100
    seconds = 1800
    filename = f"{first_name}_{last_name}.wav"

    p = pyaudio.PyAudio()
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
        for x in LiveSpeech():
            print(x)
            data = stream.read(chunk)
            frames.append(data)
            if "stop recording" in i:
                break


    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Finished recording')
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()