import pyaudio
import numpy as np
import wave
import struct
import speech_recognition as sr
from pydub import AudioSegment
import json

class Extract_Part_Of_Wav_File:
    def pay_specific_part_of_wav_file(self, File, start, length):
        """
        This function plays a specific part of a wave file
        :param File:
        :param start:
        :param length:
        :return:
        """
        chunk = 1024
        spf = wave.open(File, 'rb')
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, 'int16')
        p = pyaudio.PyAudio()
        stream = p.open(format=
                        p.get_format_from_width(spf.getsampwidth()),
                        channels=spf.getnchannels(),
                        rate=spf.getframerate(),
                        output=True)
        pos = spf.getframerate() * length
        signal = signal[start * spf.getframerate():(start * spf.getframerate()) + pos]
        sig = signal[1:chunk]
        inc = 0
        data = 0
        while data != '':
            data = struct.pack("%dh" % (len(sig)), *list(sig))
            stream.write(data)
            inc = inc + chunk
            sig = signal[inc:inc + chunk]
            if len(data) < chunk:
                break

    def Make_new_Wav_File_With_Exctracted_Sounds(self, File, Start):
        Lenght = 1000
        End = Start * 1000 + Lenght
        Old_Wave_File = AudioSegment.from_wav(File)
        Exctracted_Sound = Old_Wave_File[Start * 1000:End]
        Exctracted_Sound.export(f"static/Exctracted_Sound{Start}.wav", format="wav")
        self.Extract_Text_From_Wav_File(f"static/Exctracted_Sound{Start}.wav",Start)

    def Extract_Text_From_Wav_File(self, File, Time):
        r = sr.Recognizer()
        with sr.AudioFile(File) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            self.StoreDataInJsonFile(Time, text)
        except:
            print("Error! Couldn't understand What you said")


    def StoreDataInJsonFile(self, Time, Text):
        DataFile = open("Sounddata.json", "r")
        Data = json.load(DataFile)
        DataFile.close()
        Data.update({str(Time):str(Text)})
        print(Data)
        DataFile = open("Sounddata.json", "w")
        json.dump(Data, DataFile, indent=4)
        DataFile.close()


