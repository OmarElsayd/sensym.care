from flask import Flask, render_template, url_for
import os
import json
from weasyprint import CSS, HTML

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/','', self.index)

    def get_Peaks_Json(self):
        os.chdir("/voice_recognition")
        file = open("Sounddata.json", "r")
        data = json.load(file)
        file.close()
        return data

    def gen_word_cloud(self):
        os.chdir("/voice_recognition/static")
        for file in os.listdir():
            if file.__contains__("wordCloud"):
                print(file)
                return str(url_for('static', filename=file))

    def get_Peaks_Image(self):
        os.chdir("/voice_recognition/static")
        for file in os.listdir():
            if file.__contains__("audioRecordingPeaks"):
                print(file)
                return str(url_for('static', filename=file))


    def Generate_PDF_Report(self):
        os.chdir("/voice_recognition/Templates")
        css_Style = CSS(string='''@page { size: A4 landscape; } body {  }''')
        HTML_File = HTML(filename="Base.html")
        os.chdir("/voice_recognition/PDF_Reports")
        HTML_File.write_pdf("report.pdf", stylesheets=[css_Style])


    def read_text_file(self):
        os.chdir("/voice_recognition")
        ReadFile = open("Voice_To_Text_File.txt", "r")
        ReadFile = ReadFile.read()
        return ReadFile

    def read_wav_file(self):
        os.chdir("/voice_recognition/static")
        for file in os.listdir():
            if file.__contains__("output"):
                print(file)
                return str(url_for('static', filename=file))

    def get_exctracted_sound_Files(self):
        os.chdir("/voice_recognition/static")
        Extracted_Sounds = ''
        for file in os.listdir():
            if file.__contains__("Exctracted_Sound"):
                Extracted_Sounds += f'''<audio controls>
                <source src='static/{file}' type='audio/wav'>
                </audio><br>'''
        return Extracted_Sounds

    def index(self):
        return render_template('Base.html', Text = self.read_text_file(), Audio = self.read_wav_file(),
                               Peaks = self.get_Peaks_Image(), JSONFILE = self.get_Peaks_Json(),
                               WordCloud = self.gen_word_cloud())