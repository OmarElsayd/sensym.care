import pyaudio
import struct
import numpy as np
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import speech_recognition as sr


def voice_visualization() -> None:
    """
    This method will visualize the voice data
    """
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024 * 4
    p = pyaudio.PyAudio()
    # start Recording
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=False,
        frames_per_buffer=CHUNK,
    )

    fig, ax = plt.subplots()  # create a figure and a subplot
    x = np.arange(0, 2 * CHUNK, 2)  # create an array containing the time
    line, = ax.plot(x, np.random.rand(CHUNK))  # create a line object with random data

    ax.set_ylim(-16000, 16000)
    ax.set_xlim(0, CHUNK)  # set the x axis limits
    plt.show(block=False)  # show the plot, but block until closed

    while True:
        data = stream.read(CHUNK)  # read a chunk of data
        data_int = struct.unpack(str(CHUNK) + 'H', data)  # convert from bytes to int
        data_int = np.array(data_int, dtype='h')  # convert to numpy array
        wf_data = [i + 100 for i in data_int]  # add 100 to waveform data
        line.set_ydata(wf_data)  # update the data
        fig.canvas.draw()  # draw the plot
        fig.canvas.flush_events()  # update the plot



def get_users_path(path:str)->str:
    """
    This method will return the path to the user directory
    :param path:
    :return: string path to user directory
    """
    os.chdir(path)
    return os.getcwd()


def go_to_main_workspace() -> str:
    """
    This method will go to the main workspace
    :return: string path to main workspace
    """
    os.chdir("/voice_recognition")
    return os.getcwd()


def real_time_voice_to_text(user_name:str, path_to_user_dir:str, session_name = None) -> str:
    """
    This method will convert the voice to text in real time
    :param user_name:
    :param path_to_user_dir:
    :param session_name:
    :return:
    """
    get_users_path(path_to_user_dir)
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
                    break
            except:
                print('Sorry, could not understand what you have said\nPlease Try Again')
                continue
            file_name = get_file_name(user_name, "txt", "voice_to_text", session_name)
            with open(file_name, "a") as f:
                f.write(str(query) + "\n")
                f.close()

    go_to_main_workspace()



def get_file_name(user_name:str,type:str,action:str, session_name = None) -> str:
    """
    This method will return the file name
    :param user_name: username
    :param type:    type of file
    :param action:  action to be performed
    :param session_name:    name of the session
    :return:    string file name
    """
    return f"{user_name}_{action}_{session_name}.{type}"


def journalWordCloud(path_to_user_dir: str,user_name:str, session_name = None) -> None:
    """
    This method will create a word cloud from the journal
    :param path_to_user_dir:    path to user directory
    :param user_name:   username
    :param session_name:    name of the session
    :return:    None
    """
    get_users_path(path_to_user_dir)
    file_name = get_file_name(user_name, "txt", "voice_to_text", session_name)
    with open(file_name, "r") as f:
        data = f.read()
        f.close()
    wordcloud = WordCloud().generate(data)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.savefig(f"{user_name}_wordCloud_{session_name}.png")
    go_to_main_workspace()
