import pyaudio
import wave


def Play_Whole_Wave_File(filename: str) -> None:
    """
    Plays a wave file.
    :param filename:
    :return: None
    """
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
        if len(data) < chunk:
            break
    stream.close()
    p.terminate()
