import sys
import matplotlib
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
matplotlib.use('TkAgg')



class Real_Time_Sound_Graph:
    # This class will include all the methods all the methods for real time ploting and
    # voice to text conversion in real time and also the word cloud generation
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 4

    def record_audio(self):

        p = pyaudio.PyAudio()

        # start Recording
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=False,
            frames_per_buffer=self.CHUNK,
        )

        fig, ax = plt.subplots()  # create a figure and a subplot
        x = np.arange(0, 2 * self.CHUNK, 2)  # create an array containing the time
        line, = ax.plot(x, np.random.rand(self.CHUNK))  # create a line object with random data

        ax.set_ylim(-16000, 16000)
        ax.set_xlim(0, self.CHUNK)  # set the x axis limits
        plt.show(block=False)  # show the plot, but block until closed

        while True:
            data = stream.read(self.CHUNK, exception_on_overflow = False)  # read a chunk of data
            data_int = struct.unpack(str(self.CHUNK) + 'H', data)  # convert from bytes to int
            data_int = np.array(data_int, dtype='h')  # convert to numpy array
            wf_data = [i + 100 for i in data_int]  # add 100 to waveform data
            line.set_ydata(wf_data)  # update the data
            fig.canvas.draw()  # draw the plot
            fig.canvas.flush_events()  # update the plot

    def VoiceToText(self) -> None:

        import os
        from pathlib import Path
        directory_path = Path(os.getcwd()).parent
        folder_name = os.path.basename(directory_path)
        r = sr.Recognizer()  # create a recognizer object
        with sr.Microphone() as source:  # use the default microphone as the audio source
            while True:
                print('Listening.....')  # listen for the first phrase and extract it into audio data
                r.pause_threshold = 1  # wait for the user to pause the recognizer
                r.energy_threshold = 4000  # consider recognize when audio energy is above the threshold
                audio = r.listen(source)  # listen for the first phrase and extract it into audio data
                print('Recognizing...')  # recognize the speech in the audio data
                try:
                    query = r.recognize_google(audio, language='en-in')  # recognize the speech in the audio data
                    print('User Said : ', query)
                    if 'Stop Recording'.lower() in query:

                        print("Voice Recording has been stopped! Please proceed to the analysis report")
                except:
                    print('Sorry, could not understand what you have said\nPlease Try Again')
                    continue
                with open(f"{folder_name}.txt", "a") as f:
                    f.write(str(query) + "\n")
                    f.close()
                # sys.exit()



