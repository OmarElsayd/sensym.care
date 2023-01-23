import json
import Read_Wav_And_FindPeaks

ReadWav = Read_Wav_And_FindPeaks.Read_Wav_And_Find_Peaks()

Voicescript = open("Voice_To_Text_File.txt", "r")
Voicescript = Voicescript.read()

Peaks_From_JSOn_File = open("Sounddata.json", "r")
Peaks_From_JSOn_File = json.load(Peaks_From_JSOn_File)


Extarcted_Sounds = ''
print(ReadWav.Returned_Time_After_Round_And_Removing_Duplicates)

for i in ReadWav.Returned_Time_After_Round_And_Removing_Duplicates:
    Extarcted_Sounds += f"<audio controls><source src='Exctracted_Sound{i}.wav' type='audio/wav'></audio><br>"

print(Extarcted_Sounds)

HTML_ = f""" <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1 style="text-align: center;">Voice Recognition Report </h1>
    <hr>
    <h2 style="text-align: center;">Recording Script</h2>
    <audio controls>
    <source src="output.wav" type="audio/wav">
    This document does not support wav files.
    </audio>
    <p style="text-align: center;">{Voicescript}</p>
    <hr>
    <h2 style="text-align: center;">Word Cloud Report</h2>
    <img src="wordCloud.png" style="text-align: center;">
    <hr>
    <h2 style="text-align: center;">Voice Peaks Report</h2>
    <img src="audioRecordingPeaks.png" style="text-align: center;">
    <hr>
    <h2 style="text-align: center;">Detected Peaks time and words</h2>
    <h3 style="text-align: center;"> [ Time : Word ] -> This feature will show you time peak accorded and what did the user say during that peak<br> </h3>
    
    <p style=>{Peaks_From_JSOn_File}</p>

""" + f"{Extarcted_Sounds}" + """</body>
</html>"""

print(HTML_)

with open("report.html", "w") as f:
    f.write(HTML_)
    f.close()








