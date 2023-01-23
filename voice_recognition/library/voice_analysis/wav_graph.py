# imports
import matplotlib.pyplot as plt
import numpy as np
import wave
import speech_recognition as sr

def convert_to_text(path):
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        print(text, end="")
    except:
        print("Error")


# shows the sound waves
def visualize(first_name: str, last_name: str):
    # reading the audio file
    raw = wave.open(f"{first_name}_{last_name}.wav")

    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int32")
    f_rate = raw.getframerate()

    time = np.linspace(
        0,  # start
        len(signal) / f_rate,
        num=len(signal)
    )
    plt.figure(1)
    plt.title("Sound Wave")
    plt.xlabel("Time")
    plt.plot(time, signal)
    plt.savefig(f"{first_name}_{last_name}_wav_graph.png")
    plt.show()