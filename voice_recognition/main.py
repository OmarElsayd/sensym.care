from voice_recognition.library.realtime_stuff import Real_Time_Sound_Graph
import multiprocessing as mp
from voice_recognition.library import preparation_phase
from voice_recognition.library.voice_analysis import RecoWave

if __name__ == "__main__":
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    client_dir = preparation_phase.check_client_dir(first_name, last_name)
    if client_dir:
        preparation_phase.cd_client_dir(first_name, last_name)

    else:
        preparation_phase.create_client_dir(first_name, last_name)
        preparation_phase.cd_client_dir(first_name, last_name)

    preparation_phase.create_session_dir()
    preparation_phase.cd_session_dir(first_name, last_name)

    # Real_Time_Sound_Graph()

    Real_Time_Sound_Graph = Real_Time_Sound_Graph()

    first = mp.Process(target=Real_Time_Sound_Graph.record_audio)

    first.start()
    Real_Time_Sound_Graph.VoiceToText()
    RecoWave.recording_a_wav_file(first_name, last_name)













