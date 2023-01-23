import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.io
import numpy as np
from voice_recognition.library.Extract_Part_Of_Wav_File import Extract_Part_Of_Wav_File


class Read_Wav_And_Find_Peaks:
    def __init__(self):
        self.Returned_Time_After_Round_And_Removing_Duplicates = []

    def Read_Data_From_Wave_File(self,File):
        global duration, rate
        rate, data = scipy.io.wavfile.read(File)
        duration = (len(data) / rate)
        print(duration)
        self.find_sound_peaks(data, File)


    def find_sound_peaks(self,data, File):
        Extract = Extract_Part_Of_Wav_File()
        Time = np.arange(0, duration, duration/len(data))
        f = plt.figure()
        f.set_figwidth(10)
        f.set_figheight(8)
        plt.xlabel("Time")
        plt.ylabel("Voice Level")
        plt.plot(Time.tolist(),data)
        plt.plot(Time[data>15000],data[data>15000], "x", color="red")
        plt.savefig("static/audioRecordingPeaks.png")
        plt.show()
        Returned_Time = Time[data>15000].tolist()
        Round_Returned_Time = [round(x) for x in Returned_Time]
        self.Returned_Time_After_Round_And_Removing_Duplicates = [*set(Round_Returned_Time)]
        for i in self.Returned_Time_After_Round_And_Removing_Duplicates:
            Extract.pay_specific_part_of_wav_file("static/output.wav", i, 1)
            Extract.Make_new_Wav_File_With_Exctracted_Sounds(File, i)

    def visualize_recording(self,data):
        plt.plot(data,color='green')
        plt.title("Recording")
        plt.xlabel("Time")
        plt.ylabel("Level")
        ax = plt.gca()
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        plt.savefig("audioRecording.png")
        plt.show()
